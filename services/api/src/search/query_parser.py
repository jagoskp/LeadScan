import re
from typing import Any
from services.api.src.search.interfaces import IQueryParser


class SearchQueryParser(IQueryParser):
    """Query Parser supporting Boolean operators (AND/OR/NOT), field specifiers, exact phrases, and prefixes."""

    def parse(self, raw_query: str) -> dict[str, Any]:
        cleaned = raw_query.strip()

        # 1. Extract exact phrases inside double quotes
        exact_phrases = re.findall(r'"([^"]+)"', cleaned)
        query_no_phrases = re.sub(r'"[^"]+"', "", cleaned).strip()

        # 2. Extract field specifiers e.g. gst:27AAAAA, company:Acme, tag:HighValue
        field_specs: dict[str, str] = {}
        field_matches = re.findall(r'(\b[a-zA-Z_]+):([^\s]+)', query_no_phrases)
        for key, val in field_matches:
            field_specs[key.lower()] = val

        query_no_fields = re.sub(r'\b[a-zA-Z_]+:[^\s]+', "", query_no_phrases).strip()
        normalized_str = " " + re.sub(r'\s+', " ", query_no_fields) + " "

        # 3. Detect Boolean operators
        has_and = " AND " in normalized_str
        has_or = " OR " in normalized_str
        has_not = " NOT " in normalized_str

        terms = [t for t in re.split(r'\s+', query_no_fields) if t and t not in ("AND", "OR", "NOT")]

        return {
            "raw_query": raw_query,
            "terms": terms,
            "exact_phrases": exact_phrases,
            "field_specs": field_specs,
            "boolean_operators": {
                "AND": has_and,
                "OR": has_or,
                "NOT": has_not,
            },
        }
