# WORK 3 — new runner `run_forecast_horizon2_demo.py` (exit 0 = ALL PASS)

Drives the SAME ≥5 fresh orgs as Sprint 25 (reusing its builders/constants for byte-identity
source data):
  deli-forecast (higher-is-better deteriorating, recorded variances, NO band_variance — last-point
                band 0.71…0.89 σ0.09; band_horizon 0.71…0.93)
  deli-varmax   (band_variance:"all", σ0.18; band_horizon 0.62…1.02 — widens past 0.98)
  deli-varmax-cap (same band + RECORDED capacity 500.0 resolutions/day, load 0.72)
  deli-flat2    (recorded series, NO variance — no-band control)
  deli          (no-data)
and asserts Sprint 26:
  (a) full §7L Q1–Q10 on each
  (b) Q3 forecast-attention `why` KEEPS the Sprint-23/24 string as a strict prefix AND now carries
      the horizon-wide range suffix — deli-forecast's why == exact pre-Sprint-26 why + the shared
      horizon suffix (strongest byte-identity); varmax/varmax-cap why endswith the suffix.
  (c) do-nothing summary keeps Sprint-23/24 string as strict prefix + carries the horizon phrase.
  (d) deli-varmax-cap Q9 gains `capacity_planning_attention` {flag:False, why naming 500.0/load
      0.72 + horizon band 0.62…1.02 + derived headroom}; OTHER orgs carry NO such key
      (byte-identical superset).
  (e) band_periods/band_horizon/band_capacity_attention still present + unchanged on fc/vm/vmc;
      no-band/no-data orgs carry none (byte-identical).
  (f) determinism on re-run (dict + render).
  (g) no §6 overrule (Q8 recommendation unchanged).
  (h) no wall-clock / no invented number (sigma still a recorded |variance|; flag from recorded
      capacity+load+band).
Emits fixtures + artifacts/adjudication/reports/cockpit-forecast-horizon2.md.