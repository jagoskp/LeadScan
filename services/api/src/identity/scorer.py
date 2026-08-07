from typing import Any
from services.api.src.identity.interfaces import IIdentityScorer


class IdentityScorer(IIdentityScorer):
    """Scorer Engine generating multi-dimensional duplicate scores & confidence level classifications."""

    def compute_scores(self, match_eval: dict[str, Any]) -> dict[str, Any]:
        if match_eval.get("is_exact_match"):
            duplicate_score = 100.0
            confidence_score = 100.0
            confidence_level = "100%"
            match_type = "exact"
        else:
            title_sim = match_eval.get("title_similarity", 0.0)
            company_sim = match_eval.get("company_similarity", 0.0)
            avg_sim = (title_sim + company_sim) / 2.0
            duplicate_score = round(avg_sim * 100.0, 1)
            confidence_score = round(avg_sim * 95.0, 1)
            match_type = "fuzzy"

            if duplicate_score >= 90.0:
                confidence_level = "Very High"
            elif duplicate_score >= 75.0:
                confidence_level = "High"
            elif duplicate_score >= 50.0:
                confidence_level = "Medium"
            else:
                confidence_level = "Low"

        return {
            "identity_score": duplicate_score,
            "duplicate_score": duplicate_score,
            "similarity_score": duplicate_score,
            "confidence_score": confidence_score,
            "confidence_level": confidence_level,
            "match_type": match_type,
        }
