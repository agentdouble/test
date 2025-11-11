"""Command line interface for the ABC KPI analytical platform."""
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable

from abckpi_platform import KPIEngine, format_report, load_transactions
from abckpi_platform.reporting import format_grouped_report


def _coerce_value(value: str) -> str | float | int:
    try:
        int_value = int(value)
    except ValueError:
        try:
            float_value = float(value)
        except ValueError:
            return value
        else:
            return float_value
    else:
        return int_value


def parse_filters(values: Iterable[str]) -> list[tuple[str, str | float | int]]:
    filters: list[tuple[str, str | float | int]] = []
    for value in values:
        if "=" not in value:
            raise argparse.ArgumentTypeError(
                f"Invalid filter '{value}'. Expected the form column=value"
            )
        column, raw_value = value.split("=", 1)
        filters.append((column, _coerce_value(raw_value)))
    return filters


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("dataset", type=Path, help="Path to the CSV dataset")
    parser.add_argument("--currency", default="€", help="Currency symbol for the report")
    parser.add_argument(
        "--filter",
        dest="filters",
        metavar="COLUMN=VALUE",
        action="append",
        default=[],
        help="Filter the dataset by equality. Can be provided multiple times.",
    )
    parser.add_argument(
        "--dimension",
        dest="dimension",
        help="Optional column used to build a segmented report.",
    )
    return parser


def main(args: list[str] | None = None) -> str:
    parser = build_parser()
    options = parser.parse_args(args=args)

    filters = parse_filters(options.filters)

    frame = load_transactions(options.dataset, filters=filters)

    engine = KPIEngine(frame, currency=options.currency)
    summary = engine.compute()
    output = [format_report(summary)]

    if options.dimension:
        grouped = engine.by_dimension(options.dimension)
        output.append(format_grouped_report(grouped))

    report = "\n\n".join(output)
    print(report)
    return report


if __name__ == "__main__":
    main()
