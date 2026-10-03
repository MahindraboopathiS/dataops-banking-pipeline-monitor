from banking_dataops.quality_checks import get_quality_checks, status_from_failed_rows


def test_status_from_failed_rows() -> None:
    assert status_from_failed_rows(0) == "PASS"
    assert status_from_failed_rows(1) == "FAIL"
    assert status_from_failed_rows(1, warn_only=True) == "WARN"


def test_quality_checks_are_configured() -> None:
    checks = get_quality_checks()

    assert len(checks) >= 7
    assert len({check.control_id for check in checks}) == len(checks)

    for check in checks:
        assert check.control_id.startswith("CTRL-")
        assert check.check_name
        assert check.severity in {"high", "medium", "low"}
        assert "SELECT" in check.query.upper()
