import re
from datetime import UTC, datetime
from typing import Any
from services.api.src.search.interfaces import IRankingEngine


class SearchRankingEngine(IRankingEngine):
    """Multi-field relevance scoring engine with term frequency, field weighting, and recency boost."""

    FIELD_WEIGHTS = {
        "title": 3.0,
        "company_name": 3.0,
        "gst_number": 2.5,
        "email": 2.5,
        "phone": 2.5,
        "tags": 1.5,
        "content_text": 1.0,
    }

    def score_and_rank(self, items: list[dict[str, Any]], parsed_query: dict[str, Any]) -> list[dict[str, Any]]:
        scored_items: list[dict[str, Any]] = []

        raw_q = parsed_query.get("raw_query", "").lower()
        terms = [t.lower() for t in parsed_query.get("terms", [])]
        field_specs = parsed_query.get("field_specs", {})

        for item in items:
            score = 0.0
            matched_fields: list[str] = []
            highlighted_match = ""

            title = str(item.get("title") or "").lower()
            company = str(item.get("company_name") or "").lower()
            gst = str(item.get("gst_number") or "").lower()
            email = str(item.get("email") or "").lower()
            phone = str(item.get("phone") or "").lower()
            content = str(item.get("content_text") or "").lower()

            # 1. Exact Match Boost
            if raw_q and (raw_q == title or raw_q == company or raw_q == gst or raw_q == email):
                score += 50.0
                matched_fields.append("Exact Match")
                highlighted_match = f"Exact match: {item.get('title') or item.get('company_name')}"

            # 2. Field Weight Scoring
            for term in terms:
                if not term:
                    continue
                if term in title:
                    score += 10.0 * self.FIELD_WEIGHTS["title"]
                    matched_fields.append("title")
                    if not highlighted_match:
                        highlighted_match = f"Match in title: {item.get('title')}"
                if term in company:
                    score += 10.0 * self.FIELD_WEIGHTS["company_name"]
                    matched_fields.append("company_name")
                    if not highlighted_match:
                        highlighted_match = f"Match in company: {item.get('company_name')}"
                if term in gst:
                    score += 15.0 * self.FIELD_WEIGHTS["gst_number"]
                    matched_fields.append("gst_number")
                    if not highlighted_match:
                        highlighted_match = f"GST match: {item.get('gst_number')}"
                if term in email:
                    score += 15.0 * self.FIELD_WEIGHTS["email"]
                    matched_fields.append("email")
                    if not highlighted_match:
                        highlighted_match = f"Email match: {item.get('email')}"
                if term in phone:
                    score += 15.0 * self.FIELD_WEIGHTS["phone"]
                    matched_fields.append("phone")
                    if not highlighted_match:
                        highlighted_match = f"Phone match: {item.get('phone')}"
                if term in content:
                    score += 5.0 * self.FIELD_WEIGHTS["content_text"]
                    matched_fields.append("content_text")
                    if not highlighted_match:
                        highlighted_match = f"Content match: ...{term}..."

            # 3. Field Specifiers Filter & Boost
            for f_key, f_val in field_specs.items():
                val_str = str(item.get(f_key) or "").lower()
                if f_val in val_str:
                    score += 25.0

            # 4. Recency Boost
            created_at = item.get("created_at")
            if isinstance(created_at, datetime):
                days_old = (datetime.now(UTC) - created_at).days
                recency_boost = max(0.0, 5.0 - (days_old * 0.1))
                score += recency_boost

            item_copy = dict(item)
            item_copy["score"] = round(score, 2)
            item_copy["matched_field"] = ", ".join(set(matched_fields)) if matched_fields else "Content"
            item_copy["highlighted_match"] = highlighted_match or f"Matched content query: '{raw_q}'"
            scored_items.append(item_copy)

        # Sort descending by score
        scored_items.sort(key=lambda x: x["score"], reverse=True)
        return scored_items
