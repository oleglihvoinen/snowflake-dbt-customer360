from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime
from difflib import SequenceMatcher
import re
from typing import Iterable


@dataclass(frozen=True)
class CustomerRecord:
    source_system: str
    source_customer_id: str
    customer_name: str | None
    email: str | None
    phone: str | None
    country_code: str | None
    updated_at: str


@dataclass(frozen=True)
class MatchEvidence:
    left_id: str
    right_id: str
    score: float
    reasons: tuple[str, ...]
    decision: str


def _norm_text(value: str | None) -> str:
    if not value:
        return ""
    return re.sub(r"[^a-z0-9]", "", value.casefold())


def _norm_email(value: str | None) -> str:
    return value.strip().casefold() if value else ""


def _norm_phone(value: str | None) -> str:
    return re.sub(r"\D", "", value or "")


def _similarity(a: str | None, b: str | None) -> float:
    left, right = _norm_text(a), _norm_text(b)
    if not left or not right:
        return 0.0
    return SequenceMatcher(None, left, right).ratio()


def compare(left: CustomerRecord, right: CustomerRecord) -> MatchEvidence:
    score = 0.0
    reasons: list[str] = []

    le, re_ = _norm_email(left.email), _norm_email(right.email)
    lp, rp = _norm_phone(left.phone), _norm_phone(right.phone)

    if le and re_ and le == re_:
        score += 0.62
        reasons.append("exact_email")
    if lp and rp and lp == rp:
        score += 0.48
        reasons.append("exact_phone")

    same_country = bool(
        left.country_code and right.country_code
        and left.country_code.casefold() == right.country_code.casefold()
    )
    name_similarity = _similarity(left.customer_name, right.customer_name)

    if same_country:
        score += 0.05
        reasons.append("same_country")
    if name_similarity >= 0.93:
        score += 0.48
        reasons.append("strong_name_similarity")
    elif name_similarity >= 0.82:
        score += 0.30
        reasons.append("moderate_name_similarity")

    # Conflicting strong identifiers must not be silently merged.
    hard_conflict = bool(le and re_ and le != re_ and lp and rp and lp != rp)
    if hard_conflict:
        return MatchEvidence(
            left.source_customer_id,
            right.source_customer_id,
            round(min(score, 0.49), 3),
            tuple(reasons + ["conflicting_email_and_phone"]),
            "reject",
        )

    decision = "match" if score >= 0.65 else "review" if score >= 0.50 else "reject"
    return MatchEvidence(
        left.source_customer_id,
        right.source_customer_id,
        round(score, 3),
        tuple(reasons),
        decision,
    )


class _UnionFind:
    def __init__(self, keys: Iterable[int]):
        self.parent = {key: key for key in keys}

    def find(self, key: int) -> int:
        root = key
        while self.parent[root] != root:
            root = self.parent[root]
        while self.parent[key] != key:
            nxt = self.parent[key]
            self.parent[key] = root
            key = nxt
        return root

    def union(self, left: int, right: int) -> None:
        a, b = self.find(left), self.find(right)
        if a != b:
            self.parent[b] = a


def resolve_entities(records: list[CustomerRecord]) -> tuple[list[list[CustomerRecord]], list[MatchEvidence]]:
    uf = _UnionFind(range(len(records)))
    evidence: list[MatchEvidence] = []

    for i, left in enumerate(records):
        for j in range(i + 1, len(records)):
            result = compare(left, records[j])
            evidence.append(result)
            if result.decision == "match":
                uf.union(i, j)

    groups: dict[int, list[CustomerRecord]] = {}
    for idx, record in enumerate(records):
        groups.setdefault(uf.find(idx), []).append(record)

    clusters = sorted(groups.values(), key=lambda rows: min(r.source_customer_id for r in rows))
    return clusters, evidence


DEFAULT_PRIORITY = {"CRM": 100, "ERP": 80, "OTHER": 10}


def _updated(record: CustomerRecord) -> datetime:
    return datetime.fromisoformat(record.updated_at.replace("Z", "+00:00"))


def survive(cluster: list[CustomerRecord], source_priority: dict[str, int] | None = None) -> dict:
    priority = source_priority or DEFAULT_PRIORITY

    def best(field: str):
        candidates = [r for r in cluster if getattr(r, field)]
        if not candidates:
            return None, None
        winner = max(
            candidates,
            key=lambda r: (priority.get(r.source_system, priority.get("OTHER", 0)), _updated(r)),
        )
        return getattr(winner, field), winner.source_system

    name, name_source = best("customer_name")
    email, email_source = best("email")
    phone, phone_source = best("phone")
    country, country_source = best("country_code")

    source_ids = sorted(f"{r.source_system}:{r.source_customer_id}" for r in cluster)
    return {
        "golden_id_seed": "|".join(source_ids),
        "source_records": source_ids,
        "customer_name": name,
        "email": email,
        "phone": phone,
        "country_code": country,
        "field_provenance": {
            "customer_name": name_source,
            "email": email_source,
            "phone": phone_source,
            "country_code": country_source,
        },
    }


def exception_queue(evidence: list[MatchEvidence]) -> list[dict]:
    return [
        asdict(item)
        for item in evidence
        if item.decision == "review"
    ]
