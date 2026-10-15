import streamlit as st
import pandas as pd
from src.ropa import ROPA, ProcessingActivity
from src.dsar import DSARManager, DSARRequest, DSARType, DSARStatus
from src.right_to_forget import RightToForget
from src.consent import ConsentManager, ConsentRecord
from src.retention import retention_summary
from src.breach import DataBreach

st.set_page_config(page_title="GDPR Toolkit", layout="wide")
st.title("🇪🇺 GDPR Compliance Toolkit")

tabs = st.tabs(["📋 ROPA", "📨 DSAR", "🗑️ Erasure", "✅ Consent", "⏰ Retention", "🚨 Breach"])

with tabs[0]:
    st.subheader("Records of Processing Activities")
    ropa = ROPA()
    ropa.add(ProcessingActivity(
        id="act1", name="Customer onboarding",
        purpose="Регистрация клиента и предоставление услуг",
        legal_basis="contract",
        data_categories=["name", "email", "phone", "address"],
        data_subjects=["customers"],
        recipients=["CRM", "Billing"],
        retention_days=730,
        security_measures=["AES-256", "RBAC", "audit_log"]))
    ropa.add(ProcessingActivity(
        id="act2", name="Marketing emails",
        purpose="Рассылка маркетинговых материалов",
        legal_basis="consent",
        data_categories=["email", "preferences"],
        data_subjects=["prospects", "customers"],
        recipients=["Mailchimp"],
        retention_days=1825,
        security_measures=["TLS", "SCC"],
        transfers_outside_eu=True))
    st.dataframe(pd.DataFrame(ropa.all()))
    st.json(ropa.validation_report())

with tabs[1]:
    st.subheader("Data Subject Access Requests")
    mgr = DSARManager()
    mgr.create(DSARRequest("d1", "user@ex.com", DSARType.ACCESS))
    mgr.create(DSARRequest("d2", "user2@ex.com", DSARType.ERASURE))
    st.dataframe(pd.DataFrame([r.__dict__ for r in mgr.requests]))
    st.metric("Overdue", len(mgr.overdue()))

with tabs[2]:
    st.subheader("Right to be Forgotten")
    registry = {
        "CRM": {"type": "delete"},
        "Analytics": {"type": "anonymize"},
        "Billing": {"type": "retain", "reason": "Legal obligation (7 years)"},
        "Backups": {"type": "delete"},
    }
    rtf = RightToForget(registry)
    result = rtf.execute("user_123")
    st.json(result.__dict__)

with tabs[3]:
    st.subheader("Consent Management")
    cm = ConsentManager()
    cm.record(ConsentRecord("u1", ["marketing"], True, "2024-01-15", "website"))
    cm.record(ConsentRecord("u1", ["marketing"], False, "2024-06-20", "withdrawal"))
    st.write("Может ли обрабатывать marketing для u1?",
             cm.can_process("u1", "marketing"))
    st.dataframe(pd.DataFrame([r.__dict__ for r in cm.records]))

with tabs[4]:
    st.subheader("Retention Policies")
    st.dataframe(pd.DataFrame(retention_summary()))

with tabs[5]:
    st.subheader("Data Breach Notification")
    breach = DataBreach("b1", datetime_now := "2024-06-01T10:00:00",
                        "Утечка email базы", 500, ["email", "name"], "high")
    st.json(breach.__dict__)
    st.write("Уведомлять DPA?", breach.must_notify_dpa())
    st.write("Часов до deadline:", breach.hours_to_deadline())
