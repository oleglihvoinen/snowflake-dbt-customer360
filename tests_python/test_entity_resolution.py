from src.entity_resolution import (
    CustomerRecord,
    compare,
    exception_queue,
    resolve_entities,
    survive,
)


def rec(source, key, name, email, phone, country="FI", updated="2026-01-01T00:00:00+00:00"):
    return CustomerRecord(source, key, name, email, phone, country, updated)


def test_exact_email_links_cross_system_records():
    a = rec("CRM", "C1", "Acme Oy", "info@acme.fi", "+35840111222")
    b = rec("ERP", "E9", "ACME OY", "INFO@ACME.FI", "040111222")
    result = compare(a, b)
    assert result.decision == "match"
    assert "exact_email" in result.reasons


def test_conflicting_strong_identifiers_are_not_merged():
    a = rec("CRM", "C1", "Nordic Tools Oy", "a@example.com", "040111111")
    b = rec("ERP", "E1", "Nordic Tools Oy", "b@example.com", "040222222")
    assert compare(a, b).decision == "reject"


def test_ambiguous_similarity_goes_to_stewardship_queue():
    a = rec("CRM", "C1", "Nordic Facility Services", None, "040111111")
    b = rec("ERP", "E1", "Nordic Facility Service", None, "040222222")
    item = compare(a, b)
    assert item.decision == "review"
    assert exception_queue([item])[0]["decision"] == "review"


def test_survivorship_is_field_level_and_explainable():
    cluster = [
        rec("ERP", "E1", "Old ERP Name", "erp@example.com", "040111111", updated="2026-05-01T00:00:00+00:00"),
        rec("CRM", "C1", "CRM Name", None, "040999999", updated="2026-04-01T00:00:00+00:00"),
    ]
    golden = survive(cluster)
    assert golden["customer_name"] == "CRM Name"
    assert golden["email"] == "erp@example.com"
    assert golden["field_provenance"]["email"] == "ERP"


def test_transitive_entity_clusters_are_resolved():
    rows = [
        rec("CRM", "C1", "Acme", "a@acme.fi", "040111111"),
        rec("ERP", "E1", "Acme Oy", "a@acme.fi", None),
        rec("OTHER", "X1", "Acme Oy", None, "040111111"),
    ]
    clusters, _ = resolve_entities(rows)
    assert len(clusters) == 1
