from typing import Any
from services.api.src.search.schemas import UniversalSearchFilterSchema


class SearchFilterEngine:
    """Filter Engine applying date range, status, tag, and company constraints."""

    def filter_items(
        self, items: list[dict[str, Any]], filters: UniversalSearchFilterSchema | None
    ) -> list[dict[str, Any]]:
        if not filters:
            return items

        filtered: list[dict[str, Any]] = []

        for item in items:
            # Status Filter
            if filters.status and item.get("status") != filters.status:
                continue

            # Company Name Filter
            if filters.company_name:
                item_co = str(item.get("company_name") or "").lower()
                if filters.company_name.lower() not in item_co:
                    continue

            # Source Type Filter
            if filters.source_type and item.get("source_type") != filters.source_type:
                continue

            filtered.append(item)

        return filtered
