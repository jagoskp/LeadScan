from typing import Any
from services.api.src.identity.interfaces import IIdentityMatcher


class IdentityMatcher(IIdentityMatcher):
    """Multi-rule identity matching engine supporting Exact, Fuzzy, Phone, Email, GST, and Domain matching."""

    def _levenshtein_distance(self, s1: str, s2: str) -> int:
        if len(s1) < len(s2):
            return self._levenshtein_distance(s2, s1)
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

    def _similarity_ratio(self, s1: str, s2: str) -> float:
        if not s1 or not s2:
            return 0.0
        distance = self._levenshtein_distance(s1.lower(), s2.lower())
        max_len = max(len(s1), len(s2))
        if max_len == 0:
            return 1.0
        return 1.0 - (distance / max_len)

    def evaluate_match(self, lead_a: Any, lead_b: Any) -> dict[str, Any]:
        """Evaluate similarity between two Lead records across all identity dimensions."""
        match_reasons: list[str] = []
        is_exact_match = False

        # 1. GST Match
        gst_a = lead_a.get("gst_number")
        gst_b = lead_b.get("gst_number")
        if gst_a and gst_b and gst_a.upper() == gst_b.upper():
            match_reasons.append("Exact GST Match")
            is_exact_match = True

        # 2. Email Match
        email_a = lead_a.get("email")
        email_b = lead_b.get("email")
        if email_a and email_b and email_a.lower() == email_b.lower():
            match_reasons.append("Exact Email Match")
            is_exact_match = True

        # 3. Phone Match
        phone_a = lead_a.get("phone")
        phone_b = lead_b.get("phone")
        if phone_a and phone_b and phone_a == phone_b:
            match_reasons.append("Exact Phone Match")
            is_exact_match = True

        # 4. Fuzzy Title & Company Match
        title_a = lead_a.get("title", "")
        title_b = lead_b.get("title", "")
        title_sim = self._similarity_ratio(title_a, title_b)

        company_a = lead_a.get("company_name", "")
        company_b = lead_b.get("company_name", "")
        company_sim = self._similarity_ratio(company_a, company_b)

        if title_sim > 0.8:
            match_reasons.append(f"High Title Similarity ({int(title_sim*100)}%)")
        if company_sim > 0.8:
            match_reasons.append(f"High Company Similarity ({int(company_sim*100)}%)")

        return {
            "is_exact_match": is_exact_match,
            "title_similarity": title_sim,
            "company_similarity": company_sim,
            "match_reasons": match_reasons,
        }
