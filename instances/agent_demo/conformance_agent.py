#!/usr/bin/env python3
"""conformance_agent.py — C1-C5 gate over the agent-demo emitted fixtures.

Reuses the Sprint-0 validator VERBATIM over instances/agent_demo/artifacts/fixtures,
proving the additive decision:// records emitted by the real-LLM-agent overlay (and the
scene fixtures they ride on) stay schema-valid and the round-trip holds.

Usage:  (from instances/agent_demo)
  /home/rlg/relational-os/.venv/bin/python conformance_agent.py
"""
from __future__ import annotations
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SPRINT0 = HERE.parents[1] / "schema"
sys.path.insert(0, str(SPRINT0))
import conformance  # noqa: E402

FX = HERE / "artifacts/fixtures"
conformance.FIXTURES = FX
ok = conformance.Conformance().run()
print("\nAGENT-DEMO CONFORMANCE:", "ALL PASS" if ok else "FAILURES PRESENT")
sys.exit(0 if ok else 1)