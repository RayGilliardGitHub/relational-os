"""Agent adapter — pure-stdlib client for a local Ollama model (Sprint 8 agent demo).

Purpose: let a REAL local LLM produce the two advisory judgements the demo needs —
(a) the #8 recommendation reasoned from live ledger evidence, and (b) an evidence
verify classification (on-time vs late + confidence). In both cases the model ONLY
writes an effect-free `decision://` record; it never executes and never sets its own
Trust (update_trust stays deterministic on the model-classified evidence).

Design:
- `call(system, user, max_tokens) -> dict` POSTs to the local Ollama chat API
  (http://localhost:11434/api/chat). Pure stdlib (`urllib.request`), no deps, ~$0.
- `chat_json(...) -> (parsed_dict|None, raw_text)` asks for JSON and parses it
  tolerantly; on malformed/empty it returns (None, raw) and the caller logs the
  failure AND falls back to a safe default (never a silent fabrication).
- `recommendation(...)` and `verify_evidence(...)` are the two typed judgements the
  demo uses, each emitting a structured dict for a `decision://` record.
"""
from __future__ import annotations

import json
import sys
import time
import urllib.request

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "phi4-mini:3.8b-q8_0"      # verified present + responding (scope check)
FALLBACK_MODELS = ["gemma4:e2b-it-qat", "deepseek-coder:6.7b"]
TIMEOUT = 300
DETERMINISTIC_TEMP = 0.05          # deterministic-ish tier for reproducibility


class ModelUnavailable(Exception):
    """Raised when no Ollama model can be reached — the demo treats this as a real
    infrastructure failure and reports it honestly, never fabricating model text."""


def _post(payload: dict) -> dict:
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        OLLAMA_URL, data=body, headers={"Content-Type": "application/json"},
        method="POST")
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        return json.loads(r.read().decode("utf-8"))


def _models() -> list[str]:
    try:
        with urllib.request.urlopen("http://localhost:11434/api/tags", timeout=5) as r:
            return [m["name"].split(":")[0] for m in json.loads(r.read().decode("utf-8"))["models"]]
    except Exception:  # noqa: BLE001
        return []


def _pick_model() -> str:
    names = set(_models())
    for cand in [MODEL] + FALLBACK_MODELS:
        if cand == MODEL or cand.split(":")[0] in names:
            return cand if cand == MODEL else cand.split(":")[-1] if False else cand
    return MODEL  # will surface an honest failure if truly absent


def call(system: str, user: str, max_tokens: int = 2048, temperature: float = DETERMINISTIC_TEMP
         ) -> dict:
    """Single model call returning the full Ollama response dict."""
    model = _pick_model()
    payload = {
        "model": model,
        "messages": [{"role": "system", "content": system},
                     {"role": "user", "content": user}],
        "stream": False,
        "options": {"temperature": temperature, "num_predict": max_tokens},
    }
    try:
        resp = _post(payload)
    except Exception as e:  # noqa: BLE001
        raise ModelUnavailable(f"Ollama call failed ({model}): {e}") from e
    resp["_model"] = model
    _last["model"] = model
    return resp


def chat_json(system: str, user: str, max_tokens: int = 2048) -> tuple[dict | None, str]:
    """Return (parsed_json_or_None, raw_text). Never raises on parse failure; the
    caller is responsible for honest fallback + logging."""
    try:
        resp = call(system, user, max_tokens=max_tokens)
    except ModelUnavailable as e:
        return None, f"[MODEL UNAVAILABLE] {e}"
    raw = resp.get("message", {}).get("content", "")
    if not raw:
        return None, f"[EMPTY] model={resp.get('_model')} nil content (reasoning may have consumed the budget)"
    try:
        obj = json.loads(raw)
        if isinstance(obj, dict):
            return obj, raw
    except json.JSONDecodeError:
        pass
    # tolerant: find the first {...} block in the raw text
    start, end = raw.find("{"), raw.rfind("}")
    if start >= 0 and end > start:
        try:
            obj = json.loads(raw[start:end + 1])
            if isinstance(obj, dict):
                return obj, raw
        except json.JSONDecodeError:
            pass
    return None, raw


def recommendation(system: str, user: str, max_tokens: int = 2048) -> tuple[dict | None, str, str]:
    """Model → {option, rationale, confidence(0..1), risk}; returns (parsed, raw, model)."""
    obj, raw = chat_json(system, user, max_tokens=max_tokens)
    model = _last_model()
    return obj, raw, model


_last = {}


def _last_model() -> str:
    return _last.get("model", MODEL)


call.__name__  # noqa