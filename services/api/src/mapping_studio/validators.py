from typing import Any

from fastapi import HTTPException, status


def validate_logical_rule(condition_json: dict[str, Any]) -> None:
    """Ensure logical operators in condition definitions match allowed standards."""
    allowed_operators = {
        "AND",
        "OR",
        "NOT",
        "IF",
        "ELSE",
        "Contains",
        "Starts With",
        "Ends With",
        "Regex",
    }
    operator = condition_json.get("logical_operator")
    if not operator or operator not in allowed_operators:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported logical rule operator: '{operator}'",
        )
