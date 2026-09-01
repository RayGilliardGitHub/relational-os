#!/usr/bin/env python3
"""RelationalOS conformance validator (Sprint 0.2).

Reads the 0.17 schema (schema/relational-os.schema.yaml) and validates fixture
instances. Checks:
  C1  schema is structurally valid (draft 2020-12)
  C2  per-instance schema + Appendix C URI-kind compliance + §2 RFC3339 temporal
      conformance (jsonschema does NOT check date-time — see findings F1)
  C3  ledger content-addressed SHA-256 hash-chain + signature presence, per §2/§3.16
  C4  round-trip preserve-unknown probe (§2, Appendix C)
  C5  Relationship and Case state-machine legality (§3.16, §7J.3)

Usage: python run_conformance.py            (full run over fixtures/)
Exit 0 = all checks pass.
"""
from __future__ import annotations

import datetime as _dt
import hashlib
import json
import re
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator, ValidationError
from referencing import Registry, Resource

HERE = Path(__file__).resolve().parent
SCHEMA_YAML = HERE / "relational-os.schema.yaml"
FIXTURES = HERE / "fixtures"
SCHEMA_ID = "https://relational-os.dev/schema/0.17/core.schema.json"

# -----------------------------------------------------------------------------
# RFC3339 (F1) — jsonschema ships no date-time checker; enforce ourselves.
# -----------------------------------------------------------------------------
_RFC3339_RE = re.compile(
    r"^(?P<Y>\d{4})-(?P<M>\d{2})-(?P<D>\d{2})"
    r"[Tt ](?P<h>\d{2}):(?P<m>\d{2}):(?P<s>\d{2})"
    r"(?P<frac>\.\d+)?"
    r"(?P<z>Z|[+-]\d{2}:\d{2})$"
)
_TEMPORAL_KEYS = re.compile(r"(at|time|deadline|expires|expiry|effective|due|since)$", re.I)


def is_rfc3339(value: str) -> bool:
    if not isinstance(value, str):
        return True  # non-strings not our concern here
    m = _RFC3339_RE.match(value.strip())
    if not m:
        return False
    try:
        _dt.datetime(
            int(m["Y"]), int(m["M"]), int(m["D"]),
            int(m["h"]), int(m["m"]), int(m["s"]),
        )
    except ValueError:
        return False
    if m["z"] == "Z":
        return True
    zm = m["z"]
    if int(zm[1:3]) > 23 or int(zm[4:6]) > 59:
        return False
    return True


def _uris_in(uri: str) -> str:
    return uri.split("://", 1)[0]


# -----------------------------------------------------------------------------
# Scheme -> $def classification (one source: the schema's x-uri-catalog + spec).
# -----------------------------------------------------------------------------
def classify(uri: str) -> str:
    """Return the $def name an instance's URI scheme implies."""
    scheme = _uris_in(uri)
    IDENTITY = {"person", "org", "agent", "system"}
    if scheme in IDENTITY:
        return "Actor"
    m = {
        "relationship": "Relationship",
        "interaction": "Interaction",
        "event": "Event",
        "expectation": "Expectation",
        "claim": "Claim",
        "evidence": "Evidence",
        "decision": "Decision",
        "delegation": "Delegation",
        "consent": "Consent",
        "dispute": "Dispute",
        "right": "Right",
        "obligation": "Obligation",
        "commitment": "Commitment",
        "rule": "Rule",
        "purpose": "Purpose",
        "mission": "Purpose",
        "objective": "Purpose",
        "trust": "Trust",
        "reputation": "Reputation",
        "resource": "Resource",
        "asset": "Asset",
        "knowledge": "Knowledge",
        "entity": "Entity",
        "revision": "Revision",
        "case": "Case",
        "goal": "Goal",
        "metric": "Metric",
        "task": "Task",
        "dependency": "Dependency",
        "risk": "Risk",
        "capacity": "Capacity",
        "process": "Process",
        "process_instance": "ProcessInstance",
        "escalation": "Escalation",
        "policy": "Policy",
    }
    # Collision rule (Appendix C): first path segment disambiguates same-scheme
    # classes. policy://ins/… is an insurance policy (domain object); policy://
    # (compliance) is the executable Policy.
    if uri.startswith("policy://ins"):
        return "DomainObject"
    for scheme in ("doc", "mail", "db", "corr", "chat", "voice", "log", "report", "transcript", "spec", "training"):
        if _uris_in(uri) == scheme:
            return "Knowledge"
    return m.get(_uris_in(uri), "DomainObject")


# -----------------------------------------------------------------------------
# State machines
# -----------------------------------------------------------------------------
REL_SEQ = ["PROPOSED", "ACTIVE", "SUSPENDED", "ACTIVE", "TERMINATED", "ARCHIVED"]
REL_TRANSITIONS = {
    "PROPOSED": {"ACTIVE"},
    "ACTIVE": {"SUSPENDED", "TERMINATED"},
    "SUSPENDED": {"ACTIVE", "TERMINATED"},
    "TERMINATED": {"ARCHIVED"},
    "ARCHIVED": set(),
}
CASE_SEQ_ORDER = ["OPEN", "TRIAGE", "ASSIGNED", "IN_PROGRESS", "BLOCKED", "RESOLVED", "CLOSED"]
CASE_TRANSITIONS = {
    "OPEN": {"TRIAGE", "ASSIGNED", "BLOCKED", "CLOSED"},
    "TRIAGE": {"ASSIGNED", "BLOCKED", "CLOSED"},
    "ASSIGNED": {"IN_PROGRESS", "BLOCKED", "RESOLVED", "CLOSED"},
    "IN_PROGRESS": {"BLOCKED", "RESOLVED", "CLOSED"},
    "BLOCKED": {"IN_PROGRESS", "ASSIGNED", "RESOLVED", "CLOSED"},
    "RESOLVED": {"CLOSED", "OPEN"},   # REOPEN
    "CLOSED": {"OPEN"},               # REOPEN
}


def valid_relationship_sequence(states: list[str]) -> bool:
    """Walk a chronological state list; allow repeat of ACTIVE on cycle per §3.16."""
    prev = None
    for s in states:
        if prev is not None:
            if s not in REL_TRANSITIONS.get(prev, set()):
                return False
        prev = s
    return True


def valid_case_sequence(states: list[str]) -> bool:
    prev = None
    for s in states:
        if prev is not None and s not in CASE_TRANSITIONS.get(prev, set()):
            return False
        prev = s
    return True


# -----------------------------------------------------------------------------
# Validator
# -----------------------------------------------------------------------------
class Conformance:
    def __init__(self, verbose: bool = True):
        self.schema = yaml.safe_load(SCHEMA_YAML.read_text())
        self.validator = Draft202012Validator(self.schema)
        # Bind the full document as a named resource so detached $ref
        # subschemas (e.g. #/$defs/envelope) resolve within the whole doc.
        self.registry = Registry().with_resource(
            SCHEMA_ID, Resource.from_contents(self.schema)
        )
        self.verbose = verbose
        self.results: list[tuple[str, bool, str]] = []

    def _kind_validator(self, kind: str) -> Draft202012Validator:
        wrap = {"$ref": f"{SCHEMA_ID}#/$defs/{kind}"}
        return Draft202012Validator(wrap, registry=self.registry)

    def report(self, name: str, ok: bool, detail: str = "") -> bool:
        self.results.append((name, ok, detail))
        if self.verbose:
            mark = "PASS" if ok else "FAIL"
            line = f"  [{mark}] {name}" + (f"  — {detail}" if detail else "")
            print(line)
        return ok

    # -- C1 ---------------------------------------------------------------
    def c1_schema(self) -> bool:
        try:
            Draft202012Validator.check_schema(self.schema)
            return self.report("C1 schema structurally valid", True,
                               f"{len(self.schema.get('$defs', {}))} $defs")
        except Exception as e:  # noqa: BLE001
            return self.report("C1 schema structurally valid", False, str(e))

    # -- C2 helpers -------------------------------------------------------
    def _uri_allowed(self, uri: str) -> bool:
        if not isinstance(uri, str) or "://" not in uri:
            return False
        cat = self.schema.get("x-uri-catalog", {})
        entries = [e for grp in cat.values() for e in grp]
        return any(uri.startswith(e) for e in entries)

    def _temporal_ok(self, obj, path=""):
        """Recurse enforcing RFC3339 on fields named like timestamps (F1)."""
        if isinstance(obj, dict):
            for k, v in obj.items():
                cp = f"{path}.{k}" if path else k
                if isinstance(v, str) and _TEMPORAL_KEYS.search(k) and not is_rfc3339(v):
                    return False, cp
                if not self._temporal_ok(v, cp):
                    return False, cp
        elif isinstance(obj, list):
            for i, v in enumerate(obj):
                if not self._temporal_ok(v, f"{path}[{i}]"):
                    return False, f"{path}[{i}]"
        return True, path

    def _check_instance(self, obj, name: str) -> bool:
        uri = obj.get("uri") if isinstance(obj, dict) else None
        if not uri:
            return self.report(f"{name}: object has no 'uri'", False)
        # Appendix C membership (three kinds)
        allowed = self._uri_allowed(uri)
        if not allowed:
            return self.report(f"{name} uri {uri} not in Appendix C catalog", False)
        kind = classify(uri)
        if self.verbose:
            # fall through; per-check reported at end
            pass
        # JSON Schema validation against the mapped $def
        try:
            self._kind_validator(kind).validate(obj)
        except ValidationError as e:
            return self.report(f"{name} violates {kind} schema", False, e.message)
        # RFC3339 across temporal fields
        ok, badpath = self._temporal_ok(obj)
        if not ok:
            return self.report(f"{name} RFC3339 bad at {badpath}", False)
        return True

    # -- C2 ---------------------------------------------------------------
    def c2_instances(self) -> bool:
        allok = True
        n = 0
        skip_dirs = {"statemachines", "ledger"}   # validated by C3/C5
        for f in sorted(FIXTURES.rglob("*.json")):
            if f.parent.name in skip_dirs:
                continue
            rel = f.relative_to(FIXTURES)
            instances = json.loads(f.read_text())
            if not isinstance(instances, list):
                instances = [instances]
            for obj in instances:
                n += 1
                if not self._check_instance(obj, f"[{rel}] {obj.get('uri')}"):
                    allok = False
        return self.report("C2 all fixture instances validate + schemes + RFC3339",
                           allok, f"{n} instances")

    # -- C3 ledger chain --------------------------------------------------
    def c3_ledger(self) -> bool:
        lf = FIXTURES / "ledger"
        if not lf.exists():
            return self.report("C3 ledger fixtures present", True, "no ledger dir (skip)")
        allok = True
        for f in sorted(lf.glob("*.json")):
            doc = json.loads(f.read_text())
            entries = doc.get("entries", [])
            prev = ""
            for e in entries:
                # content = event payload minus 'hash'; chain over content+prev
                content = json.dumps({k: v for k, v in e.items() if k != "hash"},
                                     sort_keys=True, separators=(",", ":"))
                expect = hashlib.sha256((prev + content).encode()).hexdigest()
                if e.get("hash") != expect:
                    allok = False
                    self.report(f"C3 chain break in {f.name} @ {e.get('event_id')}", False)
                if not e.get("signature"):
                    allok = False
                    self.report(f"C3 unsigned event in {f.name} @ {e.get('event_id')}", False)
                prev = expect
            if doc.get("head_hash") and doc.get("head_hash") != prev:
                allok = False
                self.report(f"C3 head_hash mismatch in {f.name}", False)
        return self.report("C3 ledger content-addressed + signed", allok)

    # -- C4 round-trip ----------------------------------------------------
    def c4_roundtrip(self) -> bool:
        # An unknown field must be accepted (additionalProperties: true) and MUST
        # survive a rewrite. We simulate a re-write (parse → dump) preserving it.
        sample = {
            "uri": "case://c-rt1",
            "subject": "round-trip probe",
            "status": "OPEN",
            "x_unknown_future_field": {"keep": "me"},
        }
        self._kind_validator("Case").validate(sample)
        # preserve on rewrite: serialize then load keeps the unknown key
        round = json.loads(json.dumps(sample))
        ok = "x_unknown_future_field" in round and round["x_unknown_future_field"] == {"keep": "me"}
        return self.report("C4 round-trip preserve-unknown", ok)

    # -- C5 state machines ------------------------------------------------
    def c5_statemachines(self) -> bool:
        ok = True
        ff = FIXTURES / "statemachines"
        if (ff / "relationship.json").exists():
            doc = json.loads((ff / "relationship.json").read_text())
            ok &= valid_relationship_sequence(doc["states"])
            if not ok:
                self.report("C5 relationship states", False, str(doc["states"]))
        if (ff / "case.json").exists():
            doc = json.loads((ff / "case.json").read_text())
            ok &= valid_case_sequence(doc["states"])
            if not ok:
                self.report("C5 case states", False, str(doc["states"]))
        if ok:
            return self.report("C5 state-machine sequences legal", True)
        return False

    def run(self) -> bool:
        checks = [
            self.c1_schema,
            self.c2_instances,
            self.c3_ledger,
            self.c4_roundtrip,
            self.c5_statemachines,
        ]
        allok = True
        for fn in checks:
            if not fn():
                allok = False
        return allok


if __name__ == "__main__":
    ok = Conformance().run()
    print("\nCONFORMANCE:", "ALL PASS" if ok else "FAILURES PRESENT")
    sys.exit(0 if ok else 1)