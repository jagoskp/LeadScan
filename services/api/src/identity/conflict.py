from typing import Any


class ConflictResolver:
    """Conflict Resolver applying policy rules to resolve field-level merge differences."""

    def resolve_field_conflict(
        self,
        field_name: str,
        primary_val: Any,
        secondary_val: Any,
        policy: str = "keep_original",
        manual_val: str | None = None,
    ) -> tuple[str | None, str]:
        if policy == "manual" and manual_val is not None:
            return str(manual_val), "manual"

        if policy == "keep_latest" and secondary_val:
            return str(secondary_val), "keep_latest"

        # Default fallback: keep_original
        return str(primary_val) if primary_val else (str(secondary_val) if secondary_val else None), "keep_original"
