from src.ropa import ROPA, ProcessingActivity
from src.dsar import DSARManager, DSARRequest, DSARType
from src.consent import ConsentManager, ConsentRecord

def test_ropa_validation_catches_missing_basis():
    r = ROPA()
    r.add(ProcessingActivity("a1", "test", "p", "", ["email"], ["c"], [],
                             365, []))
    report = r.validation_report()
    assert not report["valid"]

def test_dsar_created():
    m = DSARManager()
    m.create(DSARRequest("d1", "a@b.com", DSARType.ACCESS))
    assert len(m.requests) == 1

def test_consent_withdrawal():
    cm = ConsentManager()
    cm.record(ConsentRecord("u1", ["marketing"], True, "2024-01-01", "web"))
    assert cm.can_process("u1", "marketing") is True
    cm.withdraw("u1", "marketing")
    assert cm.can_process("u1", "marketing") is False
