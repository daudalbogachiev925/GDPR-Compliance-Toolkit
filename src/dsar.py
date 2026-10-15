from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum

class DSARType(str, Enum):
    ACCESS = "access"
    RECTIFICATION = "rectification"
    ERASURE = "erasure"
    RESTRICTION = "restriction"
    PORTABILITY = "portability"
    OBJECTION = "objection"

class DSARStatus(str, Enum):
    RECEIVED = "received"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    REJECTED = "rejected"

@dataclass
class DSARRequest:
    id: str
    subject_email: str
    request_type: DSARType
    status: DSARStatus = DSARStatus.RECEIVED
    received_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    due_date: str = field(default_factory=lambda: (datetime.utcnow() + timedelta(days=30)).isoformat())
    notes: str = ""

class DSARManager:
    def __init__(self):
        self.requests = []

    def create(self, dsar: DSARRequest):
        self.requests.append(dsar)

    def update_status(self, dsar_id, status):
        for r in self.requests:
            if r.id == dsar_id:
                r.status = status
                return True
        return False

    def overdue(self):
        now = datetime.utcnow().isoformat()
        return [r for r in self.requests
                if r.status != DSARStatus.COMPLETED and r.due_date < now]

    def days_left(self, dsar_id):
        for r in self.requests:
            if r.id == dsar_id:
                due = datetime.fromisoformat(r.due_date)
                return (due - datetime.utcnow()).days
        return None
