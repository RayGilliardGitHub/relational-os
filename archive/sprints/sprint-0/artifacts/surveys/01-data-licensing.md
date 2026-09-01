# Survey 1 — Market & Social Intelligence: Data-Source & Licensing Reality
**Sprint 0 / §7I | RelationalOS | 2026-09-01**
**DoD:** a ranked source matrix (cost / ToS / rate-limit per source) and a default ingestion set chosen.
**Status per §8:** deliverable #1 — **DONE (gating, written report).**

## Purpose
§7I ingests external signals (news + social + reputation/employee platforms) as
**Claims-with-provenance** that inform decisions but never auto-execute. This survey
establishes what is actually licensable, at what cost/limit, and a resilient fallback,
so the reference stack (Appendix G.17) is grounded in real access reality rather than
assumption. Given Raymond's hard ~$10/mo operating cap, the finding matters: most of
the "obvious" social/first-party sources are **not** viable at that budget.

## Method
Sources were searched (2026-09-01) against official/authoritative documentation;
pricing is volatile and flagged as of the search date. Where a platform has no licensed
commercial API, that is called out explicitly (and is itself the finding).

## Ranked source matrix (by viability for RelationalOS at the stated budget)
Columns: **C** cost class · **L** licensed/official · **R** rate limit · **S** sentiment-usability · **Rank** 1=base.

| Rank | Source | L | C | Rate limit / ToS | Sentiment-usability | Notes |
|---|---|---|---|---|---|---|
| 1 | **GDELT 2.0** (open global news/graph) | free, open | $0 | No hard public cap; hourly DOCs/Events; full DB on Google BigQuery at $3–20/TB query cost | Medium — derived tone/sentiment scores built in | The resilient base: 100% free/open, cross-news aggregator, ideal emergency fallback. *gdeltproject.org/data.html* |
| 2 | **SEC EDGAR** (company/regulatory filings) | official | $0 | Fair-use; JSON/XBRL/EFTS full-text; no API key, rate-limited informally (~10 req/s polite) | n/a — structured filings, not sentiment | Free authoritative regulatory/news substitute for company risk surface. *sec.gov/search-filings/edgar-application-programming-interfaces* |
| 3 | **Reuters (Reuters Connect) / AP / wires** | licensed | $ high (quoted) | Enterprise license; per-outlet/hostinger; not self-serve | High — highest editorial quality | Best quality; **unaffordable** at the $10/mo cap → Phase-B procurement, not Sprint-0 ingest. *reutersconnect.com; reutersagency.com* |
| 4 | **X (Twitter) API** | official but **pay-per-use** | $0 base + ~$0.005/read | Feb-2026: no free/new tier; per-call; ~3M post reads/mo cap [postproxy.dev; xpoz.ai] | High if paid | **Not viable at budget.** Reading 10k tweets ≈ $50. Batch/derived resale prohibited without enterprise deal. |
| 5 | **Reddit Data API** | official | enterprise/opaque | Commercial + scale redistribution + AI-training needs a commercial agreement; free tier limited | High (forum sentiment) | **Not viable at budget**; for production use, enterprise sales. *prowlo.com/blog/reddit-data-api* |
| 6 | **LinkedIn** | official API **gated** | n/a | No scraping/automation (User Agreement); official API restricted (no lead-gen, no re-sell); approval-gated | High but restricted | **Not ingestible** at scale; use only the sanctioned Partner/Platform APIs. *linkedin.com/legal/l/api-terms-of-use* |
| 7 | **Facebook / Instagram Graph API** | official | $0 base | Business/Creator content; app review mandatory; IG ≈ 200 requests/hr per account; Marketing-to-BUC rate limits | Medium — business acct insights | Consumer content not broadly exposed; requires the business's own consent/OAuth. *developers.facebook.com/docs/graph-api/overview/rate-limiting* |
| 8 | **TikTok Research API** | official | free, **academic-only** | Non-profit US/EU universities; no commercial use; open-science publication | High | **Research-only**; explicit no-commercial. *developers.tiktok.com/products/research-api* |
| 9 | **Yelp** | official | Places free / **Insights paid** | Places API public reviews; Insights API is a paid B2B data license | Medium-high | Business internally; paid Insights for B2B analysis. *docs.developer.yelp.com; business.yelp.com/data* |
| 10 | **Trustpilot / Google Reviews / Glassdoor** | **no licensed public API** (except via 3rd-party aggregators) | paid aggregator | Scraping violates ToS; only vendor (Apify/DataForSEO) or enterprise licensing | High | **Sensitive** (esp. Glassdoor = employee sentiment). Only via licensed aggregator + minimum PII. *apify.com; dataforseo.com* |
| 11 | **Regulatory/business newswires** (BusinessWire, GlobeNewswire) | paid distribution + RSS | $ low for RSS | Terms vary; headlines via RSS free | Medium | Cheap headline+entity signal; body requires license. |

**Confidence note:** platform pricing/policies are volatile (X changed its model Feb-2026);
all cost/limit figures are "as of 2026-09-01" and MUST be re-verified at procurement time
(this is why Sprint-0 treats them as live findings, not fixed contract detail).

## Chosen default ingestion set (resilient fallback-first)
Given the §10 budget and the "ingest as Claims-with-provenance, never auto-execute"
guardrail (§7I.4):
1. **GDELT 2.0** — base, open, free, cross-source news+social-spike signal for entity/
   signal typing and anomaly baselines. → normalizes to EXTERNAL Events (§3.16).
2. **SEC EDGAR (EFTS + XBRL)** — free company/regulatory event feed for the business,
   competitors, suppliers (10-K/10-Q/8-K/S-1), replacing paid news for structured risk.
3. **Regulatory-wire RSS (BusinessWire/GlobeNewswire)** — cheap headline+entity layer.
4. **Review/employee platforms** — ONLY via a licensed aggregator, and subject to the
   Survey-4 data boundary (minimum PII; Glassdoor treated as sensitive employee data).
5. **Reuters/AP + X/LinkedIn/TikTok/Reddit** — registered as **Phase-B** (funded after
   the S2 revenue service); NOT Sprint-0 ingest. If later needed at scale, budget a
   per-source license or an aggregator (LiteLLM/GDELT stay the cost floor).

## Findings for spec (feed notes/findings.md)
- §7I.1's assumption that "(licensed/official APIs) within terms" covers the realistic
  social intake is **optimistic at the operating budget**: of §7I.1's named sources,
  only GDELT + SEC EDGAR + regulatory RSS + the business's own Yelp/OAuth channels are
  commercially ingestible at ~$10/mo. X/LinkedIn/TikTok/Reddit/Glassdoor are enterprise-
  priced or non-commercial.
- **Spec action (Appendix G.17):** ground the ingest set to GDELT + EDGAR + RSS as the
  default, with licensed news/social as a Phase-B tier. The high-quality licensed tier
  remains the right *eventual* answer (quality), but the resilient base is what Sprint-0+
  actually stands up.

## References
1. GDELT Project — *Data: Querying, Analyzing and Downloading*, gdeltproject.org/data.html
2. SEC — *EDGAR Application Programming Interfaces*, sec.gov/search-filings/edgar-application-programming-interfaces
3. Reuters — Reuters Connect / reutersagency.com (licensed agency platform)
4. X/Twitter API pricing 2026 — postproxy.dev/blog/x-api-pricing-2026; xpoz.ai; socialcrawl.dev
5. Reddit Data API / commercial use — prowlo.com/blog/reddit-data-api; octolens.com/blog/reddit-api-pricing
6. LinkedIn API & User Agreement, LinkedIn ToS — linkedin.com/legal/l/api-terms-of-use
7. Meta — *Rate Limits, Graph API*, developers.facebook.com/docs/graph-api/overview/rate-limiting
8. TikTok — *Research Tools: Access & Eligibility*, developers.tiktok.com/products/research-api
9. Yelp — Places API docs; Yelp Insights API (data licensing), docs.developer.yelp.com; business.yelp.com/data
10. Apify (review scraping) / DataForSEO (Trustpilot API) — apify.com; dataforseo.com

---
*Gating survey complete. Next: Survey 2 (jurisdiction & tax-filing).*