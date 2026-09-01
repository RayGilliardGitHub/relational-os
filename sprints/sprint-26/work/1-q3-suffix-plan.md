# WORK 1 — engine edit: Q3 attention horizon-wide suffix (additive, _forecast_closure)

Add a module-level constant `_HORIZON_BAND_PHRASE` and append it as a suffix to the Q3
`attention_item["why"]` when a band + attention item exist, and reuse it in the do-nothing
summary so Q3/Q8/do-nothing agree VERBATIM by construction.

Edits (only in `adjudication_engine.py`, frozen functions untouched):
1. Define `_HORIZON_BAND_PHRASE` immediately above `_forecast_closure`:
     " — horizon-wide recorded band {lo}…{hi} across {n} projection periods
        (band_periods/band_horizon, same recorded σ)"
2. Inside the existing `if band is not None and attention_item is not None:` block, AFTER the
   Sprint-23/24 band phrase AND the Sprint-24 band_source phrase, append:
     if band_horizon is not None:
         attention_item["why"] += _HORIZON_BAND_PHRASE.format(
             lo=band_horizon["low"], hi=band_horizon["high"], n=len(band_periods))
   (band_horizon is always set whenever band is set, but guard anyway.)
3. Replace the do-nothing summary's inline horizon phrase (line ~1343) with the SAME constant
   so Q3/do-nothing agree verbatim by construction (output byte-identical — same text).

Guarantees: the old `why` stays a strict prefix; no-band/no-data orgs get no suffix.