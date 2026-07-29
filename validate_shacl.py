"""
SHACL compliance check for dataproduct-dprod.ttl against dprod-shapes.ttl.

Requirements:
    pip install pyshacl

Usage:
    python validate_shacl.py
    python validate_shacl.py --data path/to/data.ttl --shapes path/to/shapes.ttl
"""

import argparse
import sys
from pathlib import Path

try:
    from pyshacl import validate
except ImportError:
    print("ERROR: pyshacl is not installed. Run:  pip install pyshacl", file=sys.stderr)
    sys.exit(1)


def run_validation(data_path: Path, shapes_path: Path, ont_path: Path | None) -> int:
    """
    Run SHACL validation and print a human-readable report.

    Returns 0 on conformance, 1 on violation, 2 on error.
    """
    print(f"Data graph  : {data_path}")
    print(f"Shapes graph: {shapes_path}")
    if ont_path:
        print(f"Ontology    : {ont_path}")
    print()

    kwargs = dict(
        shacl_graph=str(shapes_path),
        data_graph_format="turtle",
        shacl_graph_format="turtle",
        inference="rdfs",   # apply RDFS inference so subclass/domain/range reasoning works
        serialize_report_graph=True,
        debug=False,
    )
    if ont_path:
        kwargs["ont_graph"] = str(ont_path)
        kwargs["ont_graph_format"] = "turtle"

    try:
        conforms, report_graph, report_text = validate(str(data_path), **kwargs)
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR during validation: {exc}", file=sys.stderr)
        return 2

    if conforms:
        print("✅  CONFORMS — no SHACL violations found.")
    else:
        print("❌  VIOLATIONS found:\n")
        print(report_text)

    return 0 if conforms else 1


def main() -> None:
    here = Path(__file__).parent

    parser = argparse.ArgumentParser(description="SHACL compliance checker for DPROD data product.")
    parser.add_argument(
        "--data",
        type=Path,
        default=here / "dataproduct-dprod.ttl",
        help="Path to the data graph (default: dataproduct-dprod.ttl)",
    )
    parser.add_argument(
        "--shapes",
        type=Path,
        default=here / "dprod-shapes.ttl",
        help="Path to the SHACL shapes graph (default: dprod-shapes.ttl)",
    )
    parser.add_argument(
        "--ontology",
        type=Path,
        default=here / "dprod-ontology.ttl",
        help="Optional ontology graph for inference (default: dprod-ontology.ttl if present)",
    )
    args = parser.parse_args()

    for label, path in [("data", args.data), ("shapes", args.shapes)]:
        if not path.exists():
            print(f"ERROR: {label} file not found: {path}", file=sys.stderr)
            sys.exit(2)

    ont_path = args.ontology if args.ontology.exists() else None
    if args.ontology and not ont_path:
        print(f"WARNING: ontology file not found ({args.ontology}), skipping inference.")

    sys.exit(run_validation(args.data, args.shapes, ont_path))


if __name__ == "__main__":
    main()
