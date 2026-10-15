from dataclasses import dataclass, field
from datetime import datetime, timedelta

@dataclass
class DataBreach:
    id: str
    detected_at: str
    description: str
    affected_subjects: int
    data_categories: list
    severity: str  # low/medium/high/critical
    notified_dpa: bool = False
    notified_subjects: bool = False
    notification_deadline: str = field(default="")

    def __post_init__(self):
        if not self.notification_deadline:
            d = datetime.fromisoformat(self.detected_at) + timedelta(hours=72)
            self.notification_deadline = d.isoformat()

    def must_notify_dpa(self):
        return self.severity in ("high", "critical") or self.affected_subjects > 100

    def hours_to_deadline(self):
        deadline = datetime.fromisoformat(self.notification_deadline)
        return round((deadline - datetime.utcnow()).total_seconds() / 3600, 1)
