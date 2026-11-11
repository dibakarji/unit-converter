#!/usr/bin/env python3
"""Convert between common units: length, weight, temperature, and data."""

import argparse

LENGTH = {
    "mm": 0.001, "cm": 0.01, "m": 1.0, "km": 1000.0,
    "in": 0.0254, "ft": 0.3048, "yd": 0.9144, "mi": 1609.344,
}
WEIGHT = {
    "mg": 0.000001, "g": 0.001, "kg": 1.0, "t": 1000.0,
    "oz": 0.0283495, "lb": 0.453592,
}
DATA = {unit: 1024 ** i for i, unit in enumerate(["b", "kb", "mb", "gb", "tb"])}

GROUPS = {"length": LENGTH, "weight": WEIGHT, "data": DATA}


def convert_temperature(value: float, src: str, dst: str) -> float:
    celsius = {"c": value, "f": (value - 32) * 5 / 9, "k": value - 273.15}[src]
    return {"c": celsius, "f": celsius * 9 / 5 + 32, "k": celsius + 273.15}[dst]


def find_group(unit: str):
    unit = unit.lower()
    for name, table in GROUPS.items():
        if unit in table:
            return name, unit
    if unit in ("c", "f", "k"):
        return "temperature", unit
    return None, None


def convert(value: float, src: str, dst: str) -> float:
    src_group, s = find_group(src)
    dst_group, d = find_group(dst)
    if src_group is None or dst_group is None:
        raise ValueError(f"Unknown unit: {src if src_group is None else dst}")
    if src_group != dst_group:
        raise ValueError(f"Cannot convert between {src_group} and {dst_group}")

    if src_group == "temperature":
        return convert_temperature(value, s, d)
    table = GROUPS[src_group]
    return value * table[s] / table[d]


def main():
    parser = argparse.ArgumentParser(description="Unit converter")
    parser.add_argument("value", type=float, help="Value to convert")
    parser.add_argument("src", help="Source unit (m, ft, kg, lb, c, f, MB...)")
    parser.add_argument("dst", help="Target unit")
    args = parser.parse_args()

    try:
        result = convert(args.value, args.src, args.dst)
    except ValueError as e:
        parser.error(str(e))

    print(f"{args.value:g} {args.src} = {result:,.6g} {args.dst}")


if __name__ == "__main__":
    main()
