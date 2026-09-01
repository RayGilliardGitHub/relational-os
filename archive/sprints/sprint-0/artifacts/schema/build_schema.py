#!/usr/bin/env python3
"""Resolve the canonical YAML schema (incl. anchors/merge keys) to JSON.

One source of truth (Appendix G.11: no schema drift). Reads
relational-os.schema.yaml, yaml.safe_load resolves anchors, writes the portable
JSON artifact. Exits non-zero on parse error.
"""
import json
import sys
import yaml

SRC = "schema/relational-os.schema.yaml"
OUT = "schema/relational-os.schema.json"


def main() -> int:
    with open(SRC, "r", encoding="utf-8") as f:
        schema = yaml.safe_load(f)
    if not isinstance(schema, dict):
        print("FATAL: schema root is not a mapping", file=sys.stderr)
        return 1
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(schema, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"WROTE {OUT} — {len(json.dumps(schema))} bytes, {len(schema.get('$defs', {}))} $defs")
    return 0


if __name__ == "__main__":
    sys.exit(main())