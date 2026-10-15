from dataclasses import dataclass
from datetime import datetime

@dataclass
class ErasureResult:
    subject_id: str
    deleted_from: list
    anonymized_in: list
    retained_for_legal: list
    completed_at: str

class RightToForget:
    def __init__(self, storage_registry):
        """storage_registry: {system_name: {"type": "delete|anonymize|retain",
                                             "reason": "..."}}"""
        self.registry = storage_registry

    def execute(self, subject_id):
        deleted, anonymized, retained = [], [], []
        for system, config in self.registry.items():
            if config["type"] == "delete":
                deleted.append(system)
            elif config["type"] == "anonymize":
                anonymized.append(system)
            elif config["type"] == "retain":
                retained.append({"system": system, "reason": config["reason"]})
        return ErasureResult(subject_id, deleted, anonymized, retained,
                             datetime.utcnow().isoformat())
