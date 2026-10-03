"""Incident report generation for failed data-quality checks."""

from __future__ import annotations

from pathlib import Path

from banking_dataops.config import load_settings
from banking_dataops.quality_checks import QualityCheckResult, run_quality_checks


def generate_incident_markdown(results: list[QualityCheckResult]) -> str:
    """Generate a markdown incident report from failed or warning checks."""

    relevant = [result for result in results if result.status in {"FAIL", "WARN"}]
    if not relevant:
        return ""

    lines = [
        "# Generated DataOps Incident Report",
        "",
        "## Scope",
        "",
        "Synthetic local portfolio environment. No real client, bank, insurance or health data.",
        "",
        "## Failed or warning controls",
        "",
        "| Control | Status | Severity | Failed rows |",
        "|---|---|---:|---:|",
    ]
    for result in relevant:
        lines.append(
            f"| {result.control_id} — {result.check_name} | "
            f"{result.status} | {result.severity} | {result.failed_rows} |"
        )

    lines.extend(
        [
            "",
            "## Triage steps",
            "",
            "1. Review the failed control.",
            "2. Identify affected table and row pattern.",
            "3. Re-run the relevant SQL query manually.",
            "4. Decide whether to regenerate data, adjust validation or document a known issue.",
            "5. Update the runbook if the failure mode is new.",
            "",
            "## Public-safety note",
            "",
            "Do not paste real operational data into this report.",
        ]
    )
    return "\n".join(lines) + "\n"


def write_incident_report(markdown: str, output_path: Path) -> None:
    """Write markdown incident report."""

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(markdown, encoding="utf-8")


def main() -> None:
    """CLI entry point."""

    settings = load_settings()
    markdown = generate_incident_markdown(run_quality_checks(settings))
    if not markdown:
        print("No incident generated.")
        return
    output_path = settings.output_dir / "incident_report.md"
    write_incident_report(markdown, output_path)
    print(f"Incident report written to {output_path}")


if __name__ == "__main__":
    main()
