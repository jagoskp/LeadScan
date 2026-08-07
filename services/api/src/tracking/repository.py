import uuid
from datetime import datetime, timezone, timedelta
from sqlalchemy import select, func, update
from sqlalchemy.ext.asyncio import AsyncSession

from services.api.src.auth.models import User
from services.api.src.users.models import UserProfile
from services.api.src.tracking.models import (
    UserDevice,
    UserSubscription,
    UserSessionLog,
    UserUsageStats,
)


class TrackingRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_device_by_installation_id(self, installation_id: str) -> UserDevice | None:
        result = await self.db.execute(
            select(UserDevice).where(UserDevice.installation_id == installation_id)
        )
        return result.scalar_one_or_none()

    async def count_active_devices_for_user(self, user_id: uuid.UUID) -> int:
        result = await self.db.execute(
            select(func.count(UserDevice.id)).where(
                UserDevice.user_id == user_id,
                UserDevice.is_active == True,
            )
        )
        return result.scalar_one() or 0

    async def get_user_subscription(self, user_id: uuid.UUID) -> UserSubscription | None:
        result = await self.db.execute(
            select(UserSubscription).where(UserSubscription.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def ensure_default_subscription(self, user_id: uuid.UUID) -> UserSubscription:
        sub = await self.get_user_subscription(user_id)
        if not sub:
            sub = UserSubscription(
                user_id=user_id,
                tier="FREE",
                status="ACTIVE",
                max_devices=1,
            )
            self.db.add(sub)
            await self.db.commit()
            await self.db.refresh(sub)
        return sub

    async def register_device(
        self,
        user_id: uuid.UUID,
        installation_id: str,
        device_model: str,
        manufacturer: str,
        os_version: str,
        app_version: str,
    ) -> UserDevice:
        existing = await self.get_device_by_installation_id(installation_id)
        now = datetime.now(timezone.utc)
        if existing:
            existing.user_id = user_id
            existing.device_model = device_model
            existing.manufacturer = manufacturer
            existing.os_version = os_version
            existing.app_version = app_version
            existing.is_active = True
            existing.last_active_at = now
            await self.db.commit()
            await self.db.refresh(existing)
            return existing

        device = UserDevice(
            user_id=user_id,
            installation_id=installation_id,
            device_model=device_model,
            manufacturer=manufacturer,
            os_version=os_version,
            app_version=app_version,
            is_active=True,
            last_active_at=now,
        )
        self.db.add(device)
        await self.db.commit()
        await self.db.refresh(device)
        return device

    async def update_device_last_active(self, device_id: uuid.UUID) -> None:
        now = datetime.now(timezone.utc)
        await self.db.execute(
            update(UserDevice).where(UserDevice.id == device_id).values(last_active_at=now)
        )
        await self.db.commit()

    async def start_session(self, user_id: uuid.UUID, device_id: uuid.UUID) -> UserSessionLog:
        now = datetime.now(timezone.utc)
        session_log = UserSessionLog(
            user_id=user_id,
            device_id=device_id,
            session_start=now,
        )
        self.db.add(session_log)
        await self.db.commit()
        await self.db.refresh(session_log)
        return session_log

    async def end_session(
        self, session_id: uuid.UUID, session_end: datetime | None = None
    ) -> UserSessionLog | None:
        result = await self.db.execute(
            select(UserSessionLog).where(UserSessionLog.id == session_id)
        )
        session_log = result.scalar_one_or_none()
        if not session_log:
            return None

        end_time = session_end or datetime.now(timezone.utc)
        session_log.session_end = end_time

        # Calculate duration
        start_time = session_log.session_start
        if start_time.tzinfo is None:
            start_time = start_time.replace(tzinfo=timezone.utc)
        if end_time.tzinfo is None:
            end_time = end_time.replace(tzinfo=timezone.utc)

        duration = int((end_time - start_time).total_seconds())
        session_log.duration_seconds = max(0, duration)

        await self.db.commit()
        await self.db.refresh(session_log)
        return session_log

    async def get_or_create_usage_stats(self, user_id: uuid.UUID) -> UserUsageStats:
        result = await self.db.execute(
            select(UserUsageStats).where(UserUsageStats.user_id == user_id)
        )
        stats = result.scalar_one_or_none()
        if not stats:
            stats = UserUsageStats(user_id=user_id)
            self.db.add(stats)
            await self.db.commit()
            await self.db.refresh(stats)
        return stats

    async def record_event(self, user_id: uuid.UUID, event_type: str) -> UserUsageStats:
        stats = await self.get_or_create_usage_stats(user_id)
        stats.last_active_at = datetime.now(timezone.utc)

        event_upper = event_type.upper()
        if event_upper == "APP_OPEN":
            stats.total_app_opens += 1
        elif event_upper == "LOGIN":
            stats.total_login_count += 1
        elif event_upper == "SCAN":
            stats.total_scan_count += 1
        elif event_upper == "LEAD_CREATED":
            stats.total_leads_created += 1
        elif event_upper == "BACKUP":
            stats.total_backup_count += 1
        elif event_upper == "SHEETS_SYNC":
            stats.total_sheets_sync_count += 1

        await self.db.commit()
        await self.db.refresh(stats)
        return stats

    async def get_admin_dashboard_metrics(self) -> dict:
        now = datetime.now(timezone.utc)
        five_minutes_ago = now - timedelta(minutes=5)

        # Online users count (active within 5 min)
        online_stmt = select(func.count(func.distinct(UserDevice.user_id))).where(
            UserDevice.last_active_at >= five_minutes_ago,
            UserDevice.is_active == True,
        )
        online_res = await self.db.execute(online_stmt)
        online_users_count = online_res.scalar() or 0

        # Total registered users
        users_stmt = select(func.count(User.id))
        users_res = await self.db.execute(users_stmt)
        total_registered_users = users_res.scalar() or 0

        # Total registered devices
        devices_stmt = select(func.count(UserDevice.id))
        devices_res = await self.db.execute(devices_stmt)
        total_registered_devices = devices_res.scalar() or 0

        # Subscriptions breakdown
        sub_stmt = select(UserSubscription.tier, func.count(UserSubscription.id)).group_by(
            UserSubscription.tier
        )
        sub_res = await self.db.execute(sub_stmt)
        sub_breakdown = {row[0]: row[1] for row in sub_res.all()}

        # Usage totals
        usage_stmt = select(
            func.sum(UserUsageStats.total_app_opens),
            func.sum(UserUsageStats.total_login_count),
            func.sum(UserUsageStats.total_scan_count),
            func.sum(UserUsageStats.total_leads_created),
            func.sum(UserUsageStats.total_backup_count),
            func.sum(UserUsageStats.total_sheets_sync_count),
        )
        usage_res = await self.db.execute(usage_stmt)
        u_row = usage_res.one_or_none()
        usage_totals = {
            "total_app_opens": u_row[0] or 0 if u_row else 0,
            "total_login_count": u_row[1] or 0 if u_row else 0,
            "total_scan_count": u_row[2] or 0 if u_row else 0,
            "total_leads_created": u_row[3] or 0 if u_row else 0,
            "total_backup_count": u_row[4] or 0 if u_row else 0,
            "total_sheets_sync_count": u_row[5] or 0 if u_row else 0,
        }

        # Last active users list
        active_users_stmt = (
            select(
                User.id,
                User.email,
                UserProfile.full_name,
                UserUsageStats.last_active_at,
                UserSubscription.tier,
            )
            .join(UserProfile, User.id == UserProfile.user_id, isouter=True)
            .join(UserUsageStats, User.id == UserUsageStats.user_id, isouter=True)
            .join(UserSubscription, User.id == UserSubscription.user_id, isouter=True)
            .order_by(UserUsageStats.last_active_at.desc().nullslast())
            .limit(10)
        )
        active_res = await self.db.execute(active_users_stmt)

        last_active_users = []
        for row in active_res.all():
            device_cnt_stmt = select(func.count(UserDevice.id)).where(UserDevice.user_id == row[0])
            dev_res = await self.db.execute(device_cnt_stmt)
            dev_cnt = dev_res.scalar() or 0

            last_active_users.append(
                {
                    "user_id": row[0],
                    "email": row[1],
                    "display_name": row[2] or row[1].split("@")[0],
                    "last_active_at": row[3] or now,
                    "registered_devices_count": dev_cnt,
                    "subscription_tier": row[4] or "FREE",
                }
            )

        return {
            "online_users_count": online_users_count,
            "total_registered_users": total_registered_users,
            "total_registered_devices": total_registered_devices,
            "subscriptions_breakdown": sub_breakdown,
            "usage_totals": usage_totals,
            "last_active_users": last_active_users,
        }
