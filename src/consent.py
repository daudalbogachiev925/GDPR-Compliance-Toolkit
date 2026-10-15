from dataclasses import dataclass
from datetime import datetime
from typing import List

@dataclass
class ConsentRecord:
    subject_id: str
    purposes: List[str]
    granted: bool
    granted_at: str
    source: str  # website, app, call
    version: str = "1.0"

class ConsentManager:
    def __init__(self):
        self.records = []

    def record(self, consent: ConsentRecord):
        self.records.append(consent)

    def current_consent(self, subject_id, purpose):
        relevant = [r for r in self.records
                    if r.subject_id == subject_id and purpose in r.purposes]
        if not relevant:
            return None
        return max(relevant, key=lambda r: r.granted_at)

    def can_process(self, subject_id, purpose):
        c = self.current_consent(subject_id, purpose)
        return bool(c and c.granted)

    def withdraw(self, subject_id, purpose):
        self.records.append(ConsentRecord(
            subject_id, [purpose], False,
            datetime.utcnow().isoformat(), "withdrawal"))
