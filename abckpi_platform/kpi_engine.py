"""Core KPI engine for the ABC KPI platform."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping

import pandas as pd


@dataclass(slots=True)
class KPIResult:
    """Represents a computed KPI."""

    name: str
    value: float
    unit: str
    description: str


class KPIEngine:
    """Compute business KPIs from transactional data."""

    def __init__(self, frame: pd.DataFrame, *, currency: str = "€") -> None:
        self._frame = frame
        self.currency = currency

        # Pre-computed aggregates for efficiency.
        self._revenue_total = float(frame["revenue"].sum())
        self._order_total = int(frame["orders"].sum())
        self._lead_total = int(frame["leads"].sum())

    def compute(self) -> list[KPIResult]:
        """Compute the default KPI set."""

        results = [
            KPIResult(
                name="Total Revenue",
                value=self._revenue_total,
                unit=self.currency,
                description="Sum of revenue across all transactions.",
            ),
            KPIResult(
                name="Orders",
                value=float(self._order_total),
                unit="orders",
                description="Total number of orders.",
            ),
            KPIResult(
                name="Leads",
                value=float(self._lead_total),
                unit="leads",
                description="Total marketing leads captured.",
            ),
            KPIResult(
                name="Conversion Rate",
                value=self._compute_conversion_rate(),
                unit="%",
                description="Orders divided by leads.",
            ),
            KPIResult(
                name="Average Order Value",
                value=self._compute_average_order_value(),
                unit=self.currency,
                description="Revenue divided by number of orders.",
            ),
            KPIResult(
                name="Revenue per Lead",
                value=self._compute_revenue_per_lead(),
                unit=self.currency,
                description="Revenue divided by number of leads.",
            ),
        ]

        return results

    def by_dimension(self, column: str) -> Mapping[str, list[KPIResult]]:
        """Compute KPIs grouped by the provided column."""
        if column not in self._frame.columns:
            raise KeyError(f"Unknown dimension: {column}")

        grouped = self._frame.groupby(column)
        report: dict[str, list[KPIResult]] = {}

        for dimension_value, frame in grouped:
            engine = KPIEngine(frame, currency=self.currency)
            report[str(dimension_value)] = engine.compute()

        return report

    def _compute_conversion_rate(self) -> float:
        if self._lead_total == 0:
            return 0.0
        return round((self._order_total / self._lead_total) * 100, 2)

    def _compute_average_order_value(self) -> float:
        if self._order_total == 0:
            return 0.0
        return round(self._revenue_total / self._order_total, 2)

    def _compute_revenue_per_lead(self) -> float:
        if self._lead_total == 0:
            return 0.0
        return round(self._revenue_total / self._lead_total, 2)


__all__ = ["KPIEngine", "KPIResult"]
