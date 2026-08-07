import logging
import uuid
from typing import Sequence

from services.api.src.google_connector.interfaces import IRemappingAssistant
from services.api.src.google_connector.schemas import RemappingSuggestionSchema

logger = logging.getLogger(__name__)

# Enterprise Synonym & Field Aliases Dictionary
SYNONYM_MAP = {
    "company name": ["business name", "organization", "company", "firm", "client name"],
    "email id": ["email", "email address", "e-mail", "contact email"],
    "phone": ["mobile number", "phone number", "mobile", "telephone", "contact number"],
    "full name": ["contact person", "name", "customer name", "lead name"],
    "address": ["location", "street address", "city", "billing address"],
    "zip code": ["postal code", "pincode", "zip"],
}


def _levenshtein_distance(s1: str, s2: str) -> int:
    """Compute Levenshtein edit distance between two strings."""
    if len(s1) < len(s2):
        return _levenshtein_distance(s2, s1)
    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    return previous_row[-1]


def calculate_similarity(str1: str, str2: str) -> float:
    """Calculate normalized similarity ratio between 0.0 and 1.0."""
    s1, s2 = str1.lower().strip(), str2.lower().strip()
    if s1 == s2:
        return 1.0

    # Direct synonym match boost
    for key, synonyms in SYNONYM_MAP.items():
        if (s1 == key and s2 in synonyms) or (s2 == key and s1 in synonyms):
            return 0.95
        if s1 in synonyms and s2 in synonyms:
            return 0.90

    dist = _levenshtein_distance(s1, s2)
    max_len = max(len(s1), len(s2))
    if max_len == 0:
        return 1.0
    return round(1.0 - (dist / max_len), 2)


class AutoRemappingAssistant(IRemappingAssistant):
    """Intelligent Auto Remapping Assistant providing smart column mapping suggestions."""

    def generate_suggestions(
        self, missing_columns: list[str], discovered_headers: list[str]
    ) -> list[RemappingSuggestionSchema]:
        suggestions: list[RemappingSuggestionSchema] = []

        for missing in missing_columns:
            best_match: str | None = None
            highest_score: float = 0.0
            reason: str = "Low similarity score"

            for header in discovered_headers:
                score = calculate_similarity(missing, header)
                if score > highest_score:
                    highest_score = score
                    best_match = header

            if best_match and highest_score >= 0.5:
                if highest_score >= 0.9:
                    reason = f"High synonym/exact match score ({int(highest_score * 100)}%)"
                else:
                    reason = f"Fuzzy string similarity score ({int(highest_score * 100)}%)"

                suggestions.append(
                    RemappingSuggestionSchema(
                        id=uuid.uuid4(),
                        source_column=best_match,
                        target_entity_field=missing,
                        similarity_score=highest_score,
                        suggestion_reason=reason,
                        status="Pending",
                    )
                )

        return suggestions
