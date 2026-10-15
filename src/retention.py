from datetime import datetime, timedelta

RETENTION_POLICIES = {
    "customer_profile": 730,
    "transaction": 2555,
    "support_ticket": 1095,
    "marketing_consent": 1825,
    "log": 90,
}

def should_delete(record_date, category):
    if category not in RETENTION_POLICIES:
        return False
    days = RETENTION_POLICIES[category]
    d = datetime.fromisoformat(record_date) if isinstance(record_date, str) else record_date
    return (datetime.utcnow() - d).days > days

def retention_summary():
    return [{"category": k, "retention_days": v, "retention_years": round(v / 365, 1)}
            for k, v in RETENTION_POLICIES.items()]
