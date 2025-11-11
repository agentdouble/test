"""Utilities to load transactional data for the ABC KPI platform."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Optional

import pandas as pd


@dataclass(slots=True)
class DataSchema:
    """Describe the mandatory columns required by the platform."""

    date_column: str = "date"
    revenue_column: str = "revenue"
    lead_column: str = "leads"
    order_column: str = "orders"

    optional_columns: tuple[str, ...] = ("channel", "campaign", "product")

    def validate(self, frame: pd.DataFrame) -> None:
        """Validate that the dataframe contains at least the required columns."""
        missing = [col for col in self.required_columns if col not in frame.columns]
        if missing:
            raise ValueError(
                "Missing required columns: " + ", ".join(sorted(missing))
            )

    @property
    def required_columns(self) -> tuple[str, str, str, str]:
        return (self.date_column, self.revenue_column, self.lead_column, self.order_column)


def load_transactions(
    path: str | Path,
    *,
    schema: Optional[DataSchema] = None,
    date_format: Optional[str] = None,
    filters: Optional[Iterable[tuple[str, str | float | int]]] = None,
) -> pd.DataFrame:
    """Load a CSV file containing transactional information.

    Parameters
    ----------
    path:
        Path to the CSV file.
    schema:
        Optional schema definition. By default, :class:`DataSchema` is used.
    date_format:
        Optional strptime format. If provided, the date column will be parsed using
        the format; otherwise pandas will infer the format.
    filters:
        Optional iterable of (column, value) pairs used to filter the resulting
        dataframe.
    """

    csv_path = Path(path)
    if not csv_path.exists():
        raise FileNotFoundError(csv_path)

    schema = schema or DataSchema()

    frame = pd.read_csv(csv_path)

    # Parse the date column using pandas for robust handling of multiple formats.
    frame[schema.date_column] = pd.to_datetime(frame[schema.date_column], format=date_format)

    schema.validate(frame)

    if filters:
        for column, value in filters:
            if column not in frame.columns:
                raise KeyError(f"Unknown filter column: {column}")
            frame = frame.loc[frame[column] == value]

    return frame.reset_index(drop=True)


__all__ = ["DataSchema", "load_transactions"]
