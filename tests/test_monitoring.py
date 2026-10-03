from banking_dataops.monitoring import summarize_quality_status


def test_summarize_quality_status_pass() -> None:
    summary = summarize_quality_status(["PASS", "PASS"])

    assert summary.total_checks == 2
    assert summary.passed_checks == 2
    assert summary.failed_checks == 0
    assert summary.warning_checks == 0
    assert summary.overall_status == "PASS"


def test_summarize_quality_status_warn() -> None:
    summary = summarize_quality_status(["PASS", "WARN"])

    assert summary.overall_status == "WARN"


def test_summarize_quality_status_fail() -> None:
    summary = summarize_quality_status(["PASS", "FAIL"])

    assert summary.failed_checks == 1
    assert summary.overall_status == "FAIL"
