from dataclasses import dataclass, field, asdict
from typing import List
from datetime import datetime

@dataclass
class ProcessingActivity:
    id: str
    name: str
    purpose: str
    legal_basis: str  # consent, contract, legal, vital, public, legitimate
    data_categories: List[str]
    data_subjects: List[str]  # customers, employees, prospects
    recipients: List[str]
    retention_days: int
    security_measures: List[str]
    transfers_outside_eu: bool = False
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())

    def to_dict(self):
        return asdict(self)

class ROPA:
    """Records of Processing Activities (Art. 30 GDPR)."""
    def __init__(self):
        self.activities = []

    def add(self, activity: ProcessingActivity):
        self.activities.append(activity)

    def all(self):
        return [a.to_dict() for a in self.activities]

    def by_basis(self, basis):
        return [a.to_dict() for a in self.activities if a.legal_basis == basis]

    def with_cross_border(self):
        return [a.to_dict() for a in self.activities if a.transfers_outside_eu]

    def validation_report(self):
        errors = []
        for a in self.activities:
            if not a.legal_basis:
                errors.append(f"{a.id}: отсутствует legal basis")
            if not a.data_categories:
                errors.append(f"{a.id}: отсутствуют data categories")
            if a.retention_days <= 0:
                errors.append(f"{a.id}: некорректный retention")
            if a.transfers_outside_eu and "SCC" not in " ".join(a.security_measures):
                errors.append(f"{a.id}: cross-border transfer без SCC")
        return {"valid": len(errors) == 0, "errors": errors}
