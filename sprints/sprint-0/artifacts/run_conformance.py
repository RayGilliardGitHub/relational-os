#!/usr/bin/env python3
"""RelationalOS Sprint-0 conformance runner.

Usage:  ./.venv/bin/python run_conformance.py
Exit 0 iff all conformance checks (C1–C5) pass over the fixture set.
"""
import sys

import conformance


def main() -> int:
    ok = conformance.Conformance().run()
    print("\nRESULT:", "ALL PASS" if ok else "FAILURES PRESENT")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())