"""Reporting utilities for the ABC KPI platform."""
from __future__ import annotations

from typing import Iterable, Mapping

from .kpi_engine import KPIResult


def format_report(results: Iterable[KPIResult]) -> str:
    """Return a human friendly textual representation of KPI results."""
    lines = ["=== KPI SUMMARY ==="]
    for result in results:
        lines.append(
            f"- {result.name}: {result.value:,.2f} {result.unit} — {result.description}"
        )
    return "\n".join(lines)


def format_grouped_report(grouped: Mapping[str, Iterable[KPIResult]]) -> str:
    """Return a multi-section string summarising KPIs for each group."""
    sections: list[str] = []
    for group, results in grouped.items():
        sections.append(f"\n## {group}")
        sections.append(format_report(results))
    return "\n".join(sections)


__all__ = ["format_report", "format_grouped_report"]
