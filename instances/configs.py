"""Per-sector configs for RelationalOS sector instances (multi-sector dogfood).

One config per sector family (the 11 non-financial families from SPEC Appendix B; the
Financial family is already provisioned at instances/financial/). Each config is passed
to sector_scene.build_scene(cfg, sub); the platform mechanics are identical, the domain
vocabulary is the config. URIs are derived from cfg['label'].
"""
from __future__ import annotations


def _priors(lag: str, good: str, p: float):
    # (is_good, slug, price, committed_due, settled_at)  — two late (lag) + one on-time (good)
    return [
        (False, f"{lag}Q3", p,        "2026-08-31T00:00:00Z", "2026-09-02T00:00:00Z"),
        (True,  f"{good}Q3", p,       "2026-08-31T00:00:00Z", "2026-08-30T00:00:00Z"),
        (False, f"{lag}Q4", round(p * 0.8, 2), "2026-09-15T00:00:00Z", "2026-09-17T00:00:00Z"),
    ]


def _rallied(good: str, p: float):
    return (f"{good}R", p, "2026-11-15T00:00:00Z", "2026-11-12T00:00:00Z")


def _b(x):
    return str(x).split("/")[-1]


def mk(label, sector, company, company_name, client, good, lag, owner, operator,
       outcome, caps, *, root, recommended, task_objective, task_importance,
       goal_text, learning_why, policy_change, esc_trigger, tradeoff, rec_option,
       gate_option, expected_impact, bank_role="provider", client_role="client",
       roles=("operator", "partner"), price=2_000_000.0, floor=0.4,
       good_seed=0.60, lag_seed=0.90, target=0.95, trust_target=0.9,
       attestation="business-license", prov_source=None, prov_procedure="anchor-conformance",
       policy_name=None, policy_cond=None, purpose=None, need=None, offer_note=None):
    L = label
    lc = _b(lag)
    gc = _b(good)
    gl, ll = good, lag
    priors = _priors(lc, gc, price)
    rallied = _rallied(gc, price)
    value_target = round(sum(x[2] for x in priors) + rallied[1], 2)
    claim = f"{outcome} reliability"
    conf = {
        # full, consistent identity URIs (built from bare-or-full suffixes)
        "company": f"org://{L}/{_b(company)}",
        "client": f"org://{L}/{_b(client)}",
        "partner_good": f"org://{L}/{_b(good)}",
        "partner_lag": f"org://{L}/{_b(lag)}",
        "owner": f"person://{L}/{_b(owner)}",
        "operator": f"agent://{L}/{_b(operator)}",
        "label": L, "sector": sector, "company_name": company_name,
        "attestation": attestation,
        "bank_role": bank_role, "client_role": client_role,
        "net_owner_role": roles[0], "partner_role": roles[1],
        "purpose": f"{sector.lower()} operating relationship",
        "net_purpose": f"{sector.lower()} partner network",
        "outcome": outcome, "outcome_title": f"Committed {outcome}".capitalize(),
        "case_subject": f"committed {outcome} below target on time",
        "claim": claim,
        "expect_cond": f"fully deliver the committed {outcome} by its committed deadline",
        "policy_name": policy_name or f"{L} allocation",
        "policy_cond": policy_cond or "a new committed delivery is to be allocated",
        "caps": caps, "need": need or f"committed {outcome}",
        "offer_note": offer_note or f"{sector.lower()} partner delivery line",
        "good_seed": good_seed, "lag_seed": lag_seed, "floor": floor,
        "price": price, "priors": priors, "rallied": rallied,
        "target": target, "trust_target": trust_target, "value_target": value_target,
        "root": root, "recommended": recommended, "esc_trigger": esc_trigger,
        "task_objective": task_objective, "task_importance": task_importance,
        "goal_text": goal_text, "learning_why": learning_why,
        "policy_change": policy_change,
        "policy_final": policy_change + " (learned 2026-09-01)",
        "m_on_name": f"Committed-{outcome} on-time rate".capitalize(),
        "m_on_def": f"share of committed {outcome} deliveries verified on time",
        "m_trust_name": "Partner scoped-trust score",
        "m_trust_def": "best scoped Trust on the partner network (per §5)",
        "m_val_name": "Settled committed value",
        "m_val_def": "value of EXCHANGE events settled this period",
        "rec_option": rec_option, "gate_option": gate_option,
        "tradeoff": tradeoff, "expected_impact": expected_impact,
        "prov_source": prov_source or f"signed committed-{outcome} record + {L} anchor",
        "prov_procedure": prov_procedure,
        "brand": BRANDS.get(L, {}),
    }
    return conf


# ===========================================================================
# Company-branding component (Sprint 7) — additive `brand` fields on the
# company `org://` actor (URI cap / frozen ontology held: a field, not a noun).
# Rendered into every generated cockpit/BI report + a per-instance branding.md.
# Keys are chosen to NEVER end in the C2 RFC3339 probe suffixes
# (at|time|deadline|expires|expiry|effective|due|since) so the additive object
# is validated by the RFC3339 recurrence unchanged.
# ===========================================================================
BRANDS = {
    # ---------------- Technology ----------------
    "tech": {
        "tagline": "The cloud that keeps its word.",
        "mission": "Deliver platform upgrades and integrated cloud environments reliably, on time, so every enterprise customer can trust us to keep their business moving.",
        "vision": "A world where enterprises stop managing delivery risk and start compounding the value of reliably shipped software.",
        "values": [
            ("Trust over speed", "We earn enterprise confidence one verified, on-time delivery at a time."),
            ("Verify, don't assume", "Evidence outranks opinion; on-time is a ledger fact, not a promise."),
            ("Customer success", "Our win is our customer's fleet running clean on the scheduled date."),
            ("Candour", "We say what is true about a release even when it is inconvenient."),
            ("Engineering depth", "Hard problems are where we live."),
        ],
        "about": "VantageCloud is a technology operator that runs and integrates enterprise cloud platforms. We take committed platform-upgrade deployments and make them land — on time, verified, with the audit trail to prove it. Born out of a simple frustration, that a contract is only as good as the schedule it shipped on, we build trust the same way we build systems: observably, incrementally, and without shortcuts.",
        "fast_facts": [
            "Founded 2012, enterprise cloud operations",
            "1,400+ integrator partners across 3 regional clouds",
            "99.2% committed-deployment on-time track record",
        ],
        "history": [
            ("2012", "Founded in Austin, TX to end late software cutovers."),
            ("2016", "Opened the platform-upgrade business that became our core."),
            ("2021", "Standardized every delivery on ledger-verifiable on-time evidence."),
        ],
        "leadership": [
            ("Adrian Cross", "Chief Executive", "Former reliability engineer who founded VantageCloud on the principle that uptime is a commitment."),
            ("Priya Raman", "Chief Digital Office", "Runs the deployment practice and the platform-upgrade portfolio."),
        ],
        "products_services": [
            "Platform-upgrade deployment and cutover",
            "Cloud environment integration and migration",
            "Delivery-reliability engineering and audit",
        ],
        "testimonials": [
            ("Our quarterly upgrades used to be a gamble. VantageCloud made them a scheduled fact.", "Enterprise platform director, retail"),
        ],
        "trust": [
            ("99.2% committed-deployment on-time rate (2025)", "VantageCloud delivery ledger"),
            ("SOC 2 Type II attestation", "independent audit"),
        ],
        "locations": "Austin, TX (HQ) · regional delivery hubs in Europe and Asia-Pacific",
        "faq": [
            ("What does an on-time guarantee actually prove?", "We anchor every committed deployment to ledger-verified evidence, so 'on time' is auditable, not asserted."),
            ("Do you take over existing environments?", "Yes — integration and migration are core, and they are treated as committed deployments with the same evidence bar."),
        ],
        "contact": "partners@vantagecloud.example · +1-512-555-0142",
        "careers": "Build the cloud that keeps its word: reliability engineers, delivery leads, platform architects.",
        "investors": "Privately held. Delivery-reliability data and growth material on request.",
        "press": "newsroom@vantagecloud.example — media kit, release history, leadership interviews.",
        "esg": "Carbon-aware scheduling for our own cloud estate; open tooling grants; 1-1-1 model for engineering time.",
        "legal": ["Privacy", "Terms", "California Rights", "Do Not Sell or Share"],
        "nav": ["About", "Products & Services", "Customers", "Careers", "Investors", "Press", "Sustainability", "Contact"],
        "cookie_consent": "Accept All · Reject All · Preferences (link to Privacy)",
        "design": {
            "palette": [("Deep Indigo", "#2B2D72"), ("Signal Cyan", "#00A8E8"), ("Cloud White", "#F7F9FC"), ("Verified Green", "#1FA05A")],
            "typography": {"heading": "Sans-serif geometric (e.g. Space Grotesk)", "body": "Humanist sans (e.g. Inter)"},
            "logo": {"wordmark": "VANTAGECLOUD in letterspaced caps", "character": "a cloud-chevron mark", "usage": "clear space = x-height; never recolor outside light/dark approved pairs"},
            "imagery": "Clean data scenes: dashboards, server rooms, abstract cloud geometry — optimistic and precise",
            "tone": "Confident and precise; evidence-first; never hype.",
        },
    },
    # ---------------- Healthcare / Pharma ----------------
    "hlth": {
        "tagline": "Supply that heals, on schedule.",
        "mission": "Move committed pharmaceutical supply reliably and on time so care facilities always have the medicine they ordered, exactly when they ordered it.",
        "vision": "A healthcare supply chain so dependable that a pharmacy's worry is one less thing in the operating room.",
        "values": [
            ("Patients first", "Every shipment carries a patient at the other end."),
            ("On-time is safety", "A delayed essential medicine is a clinical risk, not an inventory hiccup."),
            ("Evidence-based", "We verify every delivery against the ledger; nothing ships on trust alone."),
            ("Compassion", "We treat supply failures as care failures, and fix the system, not the blame."),
            ("Accountability", "If a delivery misses, we say so, we learn, and the policy changes."),
        ],
        "about": "Lumen Health is a healthcare and pharmaceutical supply operator. We run committed pharmaceutical distribution for care facilities — and we treat an on-time release the same way clinicians treat a vital sign: it is either within range, or it gets immediate, documented attention. By anchoring each committed delivery to ledger evidence, we give pharmacies and their patients the rarest thing in the supply chain — certainty.",
        "fast_facts": [
            "Founded 2009, pharmaceutical distribution",
            "3,200+ care facilities served",
            "Cold-chain and schedule-critical delivery practice",
        ],
        "history": [
            ("2009", "Founded in Minneapolis to fix fragile pharma distribution."),
            ("2015", "Launched the committed pharmaceutical-delivery line."),
            ("2022", "Placed every committed delivery under ledger-verified on-time evidence."),
        ],
        "leadership": [
            ("Dana Okafor", "Chief Operating Officer", "Former hospital pharmacy director who joined Lumen to put reliability at the centre of supply."),
            ("Marco Beltran", "VP, Distribution", "Owns the distributor network and the on-time bar."),
        ],
        "products_services": [
            "Committed pharmaceutical supply and distribution",
            "Cold-chain logistics",
            "Supply-reliability assurance for care facilities",
        ],
        "testimonials": [
            ("Since Lumen, 'reorder' is boring again. That is exactly what I want it to be.", "Facility pharmacy director"),
        ],
        "trust": [
            ("99.4% committed pharmacy-delivery on-time rate (2025)", "Lumen delivery ledger"),
            ("GDP (Good Distribution Practice) aligned cold-chain", "third-party audit"),
        ],
        "locations": "Minneapolis, MN (HQ) · regional depots across the Midwest",
        "faq": [
            ("How do you prove a delivery was on time?", "Each committed delivery anchors to a signed ledger event with a verified completion time — auditable end to end."),
            ("Do you handle temperature-sensitive product?", "Yes, cold-chain is a first-class service with its own verification and reporting."),
        ],
        "contact": "supply@lumenhealth.example · +1-612-555-0177",
        "careers": "Help us make healthcare supply boring again: distribution leads, cold-chain specialists, supply ops.",
        "investors": "Privately held. On-time and reliability reporting available on request.",
        "press": "media@lumenhealth.example — spokespeople and reliability data.",
        "esg": "Cold-chain energy efficiency, temperature-monitoring transparency, community medication-access grants.",
        "legal": ["Privacy", "Terms", "Health Privacy Notice", "State Rights"],
        "nav": ["About", "What We Do", "Facilities", "Careers", "Investors", "Press", "Sustainability", "Contact"],
        "cookie_consent": "Accept All · Reject All · Health-Privacy Preferences (links)",
        "design": {
            "palette": [("Healing Teal", "#0E8575"), ("Clinical White", "#FDFDFD"), ("Patient Warmth", "#F2C14E"), ("Trust Navy", "#14324A")],
            "typography": {"heading": "Clean serif (e.g. Lora)", "body": "Open sans-serif (e.g. Source Sans 3)"},
            "logo": {"wordmark": "Lumen Health in rounded friendly caps", "character": "a pulse-line leaf mark", "usage": "clear space around the leaf; calm tones only"},
            "imagery": "Human and calm: clinicians, care settings, organized supply — never sterile or alarming",
            "tone": "Calm, caring, and rigorous; speaks in outcomes for patients.",
        },
    },
    # ---------------- Food / Bev / Consumer ----------------
    "food": {
        "tagline": "Fresh on the shelf, right on schedule.",
        "mission": "Deliver committed restock shipments reliably and on time so retailers can promise their own customers freshness and never run dry.",
        "vision": "A pantry where nothing runs out because the shipment was late — only because it sold.",
        "values": [
            ("Freshness is a promise", "On-time restock keeps quality at the centre of the shelf."),
            ("Shelf truth", "We ship to the schedule, because an empty shelf costs everyone."),
            ("Fair to partners", "Reliable volume in, honest communication out."),
            ("Reduce waste", "Right amount, right time, right place — less product thrown away."),
            ("Taste and trust", "Consumers trust a stocked shelf; we protect that every run."),
        ],
        "about": "Maplehurst Foods moves committed restock shipments and consumer goods so retailers keep the shelf full. Our origin story is a produce manager's complaint — that good food kept arriving a day late and getting pushed to markdown. We built a restock operation on the opposite principle: committed delivery is verified, on time, and the shelf is the report card.",
        "fast_facts": [
            "Founded 2004, food & beverage distribution",
            "8,500+ retail shelves served",
            "Own-brand consumer staples line",
        ],
        "history": [
            ("2004", "Founded in Cincinnati around a refrigerated truck and a promise."),
            ("2011", "Expanded from produce to the full food-and-bev restock line."),
            ("2020", "Automated restock scheduling to keep the shelf on time at scale."),
        ],
        "leadership": [
            ("Sofia Marchetti", "Chief Executive", "Third-generation food distributor who built Maplehurst around freshness."),
            ("Andre Whitfield", "Chief Supply Officer", "Owns the distributor network running today's restock."),
        ],
        "products_services": [
            "Retail restock shipments (frozen, fresh, grocery)",
            "Consumer-brand staples manufactured in-house",
            "Shelf-on-time logistics for retailers",
        ],
        "testimonials": [
            ("Markdown went from a weekly guessing game to a rounding error.", "Regional grocery chain buyer"),
        ],
        "trust": [
            ("99.1% committed restock on-time rate (2025)", "Maplehurst delivery ledger"),
            ("FSSC 22000 food-safety certification", "third-party audit"),
        ],
        "locations": "Cincinnati, OH (HQ) · distribution centres in 6 states",
        "faq": [
            ("What makes Maplehurst 'on time' different?", "Every committed shipment is tracked to a verified ledger completion — 'on time' is a measured fact, not a promise."),
            ("Can you handle frozen and fresh in one order?", "Yes, our restock service spans the temperature range with verification on every leg."),
        ],
        "contact": "orders@maplehurst.example · +1-513-555-0163",
        "careers": "Keep good food out of the markdown bin: logistics, food-safety, supply planning, route operations.",
        "investors": "Privately held; family-owned. On-time reliability data on request.",
        "press": "news@maplehurst.example — brand and freshness stories.",
        "esg": "Waste-reduction routing, food-recovery donations, fuel-efficient fleet, sustainable packaging for own-brand.",
        "legal": ["Privacy", "Terms", "California Rights", "Do Not Sell or Share"],
        "nav": ["About", "Our Brands", "For Retailers", "Sustainability", "Careers", "Press", "Contact"],
        "cookie_consent": "Accept All · Reject All · Preferences (link to Privacy)",
        "design": {
            "palette": [("Orchard Green", "#4E7C2A"), ("Cream Butter", "#F6EFD9"), ("Berry Red", "#A63C3C"), ("Midnight Cocoa", "#2A1F1A")],
            "typography": {"heading": "Warm friendly sans (e.g. Quicksand)", "body": "Humanist sans (e.g. Lato)"},
            "logo": {"wordmark": "Maplehurst in rounded case", "character": "a maple-leaf/apple mark", "usage": "clear space generous; food photography must keep greens true"},
            "imagery": "Bright, appetising, real food; family tables; full shelves — warmth and freshness",
            "tone": "Warm, genuine, modest; talks about freshness and the people who depend on it.",
        },
    },
    # ---------------- Retail ----------------
    "retail": {
        "tagline": "Stock for every store, on time.",
        "mission": "Deliver committed store replenishment reliably and on time so every HardVale customer finds what they came for, every day, at every store.",
        "vision": "Shoppers who never think about whether the shelf will be there — because it always is.",
        "values": [
            ("Customer first", "Behind every pallet is a shopper who chose us."),
            ("Shelf faith", "We guard the simple promise that the item will be there."),
            ("Efficient by habit", "We move stock efficiently so prices stay fair."),
            ("Community store", "Our stores are neighbourhoods; we stock them like neighbours."),
            ("Own the outcome", "A store that runs out is our problem to solve, not an excuse to make."),
        ],
        "about": "HardVale Stores runs a chain of community retail stores and the replenishment operation that keeps their shelves honest. We take committed store replenishment deliveries and make them land so reliably that running out of a staple stops being a plot point in our shoppers' day. Every delivery is verified, every store is a promise, every shelf is the metric.",
        "fast_facts": [
            "Founded 1996, retail stores",
            "460+ stores across the region",
            "Committed replenishment delivery network",
        ],
        "history": [
            ("1996", "Opened the first HardVale store in a converted warehouse."),
            ("2008", "Built our own replenishment logistics to end bare shelves."),
            ("2019", "Digitised every restock run to ledger-verified on-time evidence."),
        ],
        "leadership": [
            ("Elena Vasquez", "Chief Executive", "Retail lifer who has run stores, buying, and now the whole chain."),
            ("Tyrone Grant", "Chief Merchandising Officer", "Connects what shoppers want to what the shelf holds."),
        ],
        "products_services": [
            "Community retail stores",
            "Store replenishment and distribution",
            "Efficient price leadership on essentials",
        ],
        "testimonials": [
            ("I can count on the staples always being there. That is why I keep coming back.", "HardVale shopper"),
        ],
        "trust": [
            ("99.0% committed store-replenishment on-time rate (2025)", "HardVale logistics ledger"),
            ("5-year shopper satisfaction programme", "independent survey"),
        ],
        "locations": "Regional HQ + 460+ stores; distribution parks in 4 states",
        "faq": [
            ("How do you keep shelves full?", "Every committed replenishment is tracked to a verified on-time ledger completion; stores below target get immediate attention, not excuses."),
            ("Do you deliver to stores every day?", "Cadence varies by store and category; the committed deliveries on those cadences are the ones we verify."),
        ],
        "contact": "care@hardvale.example · +1-800-STOCKED",
        "careers": "Grow with a store that keeps its promise: store ops, logistics, buying, sustainability.",
        "investors": "Privately held. Store-level reliability data shared with partners on request.",
        "press": "press@hardvale.example — new stores, community programs, reliability stories.",
        "esg": "Waste-less replenishment, community food programs, efficient fleet, sustainable packaging for own-brand.",
        "legal": ["Privacy", "Terms", "California Rights", "Do Not Sell or Share", "Accessibility"],
        "nav": ["About", "Stores", "Our Brands", "Careers", "Investors", "Press", "Sustainability", "Contact"],
        "cookie_consent": "Accept All · Reject All · Preferences (link to Privacy)",
        "design": {
            "palette": [("Bullseye Red", "#C8102E"), ("Navy Briefcase", "#1F2A44"), ("Shelf Grey", "#E6E3DC"), ("Fresh White", "#FFFFFF")],
            "typography": {"heading": "Bold condensed sans (e.g. Barlow Condensed)", "body": "Open sans (e.g. Work Sans)"},
            "logo": {"wordmark": "HARDVALE (bold)", "character": "a target/chevron mark", "usage": "clear space fixed; red on white or navy on white primary"},
            "imagery": "Bright store scenes, stocked shelves, real shoppers — energy and value",
            "tone": "Friendly, confident, plain-spoken; about the shopper's day going well.",
        },
    },
    # ---------------- Energy / Chemicals ----------------
    "enrg": {
        "tagline": "Energy that arrives when it's supposed to.",
        "mission": "Deliver committed refined-products tanker and chemical cargoes reliably and on time so term customers can run their operations without a barrel of uncertainty.",
        "vision": "An energy market where 'it's on the water' means it will be there — measured, verified, and on the agreed date.",
        "values": [
            ("Dependability", "A charter is a commitment; delivering late is a failure, not a forecast."),
            ("Safety first", "On time never means cutting corners on the creole, the tank, or the port."),
            ("Evidence over rumor", "We prove when cargoes arrive with ledger-verified records."),
            ("Stewardship", "We move energy responsibly and report the footprint."),
            ("Partnership", "Term customers plan around us; we honour that trust."),
        ],
        "about": "Basinline Energy is a refined-products and chemicals logistics operator. We take committed tanker deliveries and make discharge dates as firm as a bank statement, backing every arrival with ledger-verified evidence. For term customers whose whole plant schedule hinges on a cargo, our on-time record is not a marketing line — it is the working relationship.",
        "fast_facts": [
            "Founded 1998, energy & chemicals logistics",
            "Fleet of 40+ contracted tankers",
            "Terminal and refining connections across the Gulf",
        ],
        "history": [
            ("1998", "Founded in Houston as a fuel-hauling operation."),
            ("2010", "Entered refined-products tanker chartering."),
            ("2023", "Verifying every cargo discharge against the ledger for on-time proof."),
        ],
        "leadership": [
            ("Wade Okonkwo", "Chief Executive", "25 years in energy shipping; built Basinline on discharge reliability."),
            ("Lena Alvarado", "Chief Supply Officer", "Runs the tanker network and terminal relationships."),
        ],
        "products_services": [
            "Refined-products tanker delivery",
            "Chemical cargo logistics",
            "Terminal discharge coordination",
        ],
        "testimonials": [
            ("Basinline's discharge dates are the only ones in the market I'd build a schedule around.", "Term customer, refining"),
        ],
        "trust": [
            ("98.7% committed tanker discharge on-time rate (2025)", "Basinline discharge ledger"),
            ("OCIMF/ISGOTT-aligned tanker safety programme", "audited annually"),
        ],
        "locations": "Houston, TX (HQ) · Gulf terminals; global charter coverage to order",
        "faq": [
            ("Why is your on-time claim credible?", "Every cargo discharge is anchored to a signed ledger event with a verified completion time — auditable, not asserted."),
            ("Do you coordinate the terminal side too?", "Yes, we manage both vessel and terminal, so the commitment covers the full landing."),
        ],
        "contact": "charter@basinline.example · +1-713-555-0149",
        "careers": "Keep the barrels moving on schedule: marine ops, chartering, terminal logistics, safety.",
        "investors": "Privately held. Fleet and reliability data shared on request.",
        "press": "media@basinline.example — safety and reliability reporting.",
        "esg": "Emissions-tracking per voyage, ballast and spill stewardship, port-community partnerships.",
        "legal": ["Privacy", "Terms", "Caifornia Rights", "Do Not Sell or Share"],
        "nav": ["About", "What We Move", "Terminals", "Safety", "Careers", "Investors", "Press", "Contact"],
        "cookie_consent": "Accept All · Reject All · Preferences (link to Privacy)",
        "design": {
            "palette": [("Pipeline Black", "#1B1E24"), ("Refinery Amber", "#F2A124"), ("Marine Steel", "#5B6470"), ("Terminal Teal", "#0E7C86")],
            "typography": {"heading": "Strong industrial sans (e.g. Archivo)", "body": "Neutral sans (e.g. Roboto)"},
            "logo": {"wordmark": "BASINLINE in strong caps", "character": "a tanker/pipeline chevron mark", "usage": "clear space wide; dark-on-light, amber as accent only"},
            "imagery": "Open-water tankers, terminals, pipelines at scale — powerful and engineered",
            "tone": "Solid, understated, exact; heavy on measured facts over adjectives.",
        },
    },
    # ---------------- Aerospace / Defense / Aviation ----------------
    "aero": {
        "tagline": "Subsystems on the line, on the date.",
        "mission": "Deliver committed airframe subsystems and flight-critical components reliably and on time so aviation customers can keep their programmes on schedule and their fleets flying.",
        "vision": "Aerospace programmes where subsystem delivery is the dependable core, not the critical-path risk.",
        "values": [
            ("Zero compromises", "Flight-critical means the evidence bar is non-negotiable."),
            ("Schedule integrity", "A late subsystem can ground a programme; we protect the date."),
            ("Verification culture", "We prove readiness with data before anything is in the build."),
            ("Partnership", "Fleet customers plan years ahead; we keep those plans honest."),
            ("Stewardship", "We build responsibly — safety, export control, and ISO-grade process."),
        ],
        "about": "Valiant Aero is an aerospace, defense, and aviation subsystem operator. We take committed airframe-subsystem deliveries and bring them in on the building date — integrated, verified, and traceable to the part. For programmes where a missed subsystem is a schedule domino, we make delivery reliability the least anxious part of the build.",
        "fast_facts": [
            "Founded 2001, aerospace subsystems",
            "Component-level to subsystem integration scope",
            "Fleet and programme customers on 3 continents",
        ],
        "history": [
            ("2001", "Founded near Dayton for precision aerospace work."),
            ("2013", "Won our first major airframe-subsystem programme."),
            ("2021", "Placed every committed subsystem delivery under ledger-verified evidence."),
        ],
        "leadership": [
            ("Colonel (ret.) Marta Reyes", "Chief Executive", "Former programme manager who runs Valiant Aero on delivery integrity."),
            ("Erik Lindqvist", "Chief Program Officer", "Owns subsystem integration across all active programmes."),
        ],
        "products_services": [
            "Airframe-subsystem design and delivery",
            "Flight-critical component integration",
            "Aerospace programme schedule assurance",
        ],
        "testimonials": [
            ("Valiant Aero is the subsystem partner we can build our master schedule around.", "Fleet programme lead"),
        ],
        "trust": [
            ("98.9% committed airframe-subsystem on-time rate (2025)", "Valiant delivery ledger"),
            ("AS9100 aerospace quality certification", "third-party audit"),
        ],
        "locations": "Near Dayton, OH (HQ) · integration hangars and partner facilities on 3 continents",
        "faq": [
            ("How does on-time delivery work with flight certification?", "Verification and certification gates are built into the schedule; our on-time evidence covers the committed delivery on the agreed date."),
            ("Do you handle classified work?", "Yes, we hold appropriate clearances and follow export-control process at every stage."),
        ],
        "contact": "programs@valiantaero.example · +1-937-555-0104",
        "careers": "Keep programmes on schedule and fleets flying: engineering, program mgmt, quality, integration.",
        "investors": "Privately held. Programme-and-reliability reporting shared with defence customers under NDA.",
        "press": "media@valiantaero.example — schedule, quality, and programme announcements.",
        "esg": "ISO-grade process, responsible export control, engineering education partnerships.",
        "legal": ["Privacy", "Terms", "Export-Control Notice", "California Rights", "Do Not Sell or Share"],
        "nav": ["About", "Capabilities", "Programmes", "Quality", "Careers", "Investors", "Press", "Contact"],
        "cookie_consent": "Accept All · Reject All · Security Preferences (links)",
        "design": {
            "palette": [("Flightline Grey", "#39434E"), ("Signal Orange", "#F26522"), ("Runway White", "#F4F6F8"), ("Missile Teal", "#0F6E6E")],
            "typography": {"heading": "Sharp technical sans (e.g. Chivo)", "body": "Technical sans (e.g. Roboto Mono for data, Source Sans for prose)"},
            "logo": {"wordmark": "VALIANT AERO in angular caps", "character": "a chevron/wing mark", "usage": "clear space wide; orange as a discipline accent only"},
            "imagery": "Precision and scale: airframes, integration bays, flightline — engineered and controlled",
            "tone": "Precise, disciplined, confident; about programme integrity and schedule.",
        },
    },
    # ---------------- Telecom ----------------
    "telco": {
        "tagline": "Coverage where you need it, on schedule.",
        "mission": "Deliver committed cell-site buildouts reliably and on time so metropolitan communities and subscribers get the coverage they were promised, when they were promised it.",
        "vision": "A connected city where 'we're building coverage' means the tower is coming up on the scheduled date.",
        "values": [
            ("Coverage is a promise", "A site on time means a neighbourhood connected on time."),
            ("Build it right", "Speed never trades away a safe, code-compliant handover."),
            ("Evidence in hand", "We verify every energized site against the ledger."),
            ("Subscriber trust", "People count on us to make the signal real; we protect that."),
            ("Metro partnership", "We build with the community, not around it."),
        ],
        "about": "NimbusCom is a telecom operator that builds and lights up cellular coverage. We take committed cell-site buildouts and energize them on schedule — verified, code-compliant, ready to carry traffic. Between the promise on a coverage map and the bars on a subscriber's phone, there is a site that has to come up on the date; that handover is the work we are built for.",
        "fast_facts": [
            "Founded 2003, mobile network operator",
            "2,100+ cell sites lit",
            "Metropolitan coverage across 3 metro regions",
        ],
        "history": [
            ("2003", "Founded rolling out metro coverage."),
            ("2011", "Accelerated the cell-site buildout business."),
            ("2022", "Verifying every energized handover against the ledger."),
        ],
        "leadership": [
            ("CEO — Lena Park", "Chief Executive", "Ran network engineering for years before leading NimbusCom."),
            ("Tanaji Rao", "Chief Network Officer", "Owns buildout schedule and handover integrity."),
        ],
        "products_services": [
            "Mobile network operation",
            "Cell-site buildout and erection",
            "Coverage expansion and modernization",
        ],
        "testimonials": [
            ("NimbusCom lit the site on the exact date they committed. Our coverage story changed that day.", "Metro community liaison"),
        ],
        "trust": [
            ("98.8% committed cell-site on-time rate (2025)", "NimbusCom buildout ledger"),
            ("FCC-compliant, code-certified site handovers", "independent inspection"),
        ],
        "locations": "Metro HQ across 3 regions; build teams dispatched per site programme",
        "faq": [
            ("What counts as 'on time' for a site?", "The committed energization date, verified by a signed ledger event at handover — measured, not promised."),
            ("Do you handle permits and community outreach?", "Yes, buildout includes permitting, outreach, and code handover, all on a schedule."),
        ],
        "contact": "coverage@nimbuscom.example · +1-512-555-0110",
        "careers": "Light up whole neighbourhoods: site engineering, buildout ops, network, field coordination.",
        "investors": "Privately held. Coverage and buildout reliability shared on request.",
        "press": "news@nimbuscom.example — new sites and coverage announcements.",
        "esg": "Carbon-aware build scheduling, site-power efficiency, community digital-inclusion grants.",
        "legal": ["Privacy", "Terms", "California Rights", "Do Not Sell or Share", "Health & Safety"],
        "nav": ["About", "Coverage", "Buildout", "Community", "Careers", "Investors", "Press", "Contact"],
        "cookie_consent": "Accept All · Reject All · Preferences (link to Privacy)",
        "design": {
            "palette": [("Signal Purple", "#5A2F8A"), ("Lumen Blue", "#1E7BD8"), ("Dark Sky", "#101A2E"), ("Zing Yellow", "#F5B700")],
            "typography": {"heading": "Modern geometric sans (e.g. Nunito Sans)", "body": "Open sans (e.g. Roboto)"},
            "logo": {"wordmark": "nimbuscom", "character": "a tower/signal-wave mark", "usage": "clear space fixed; purple+blue standard, yellow for energy accents"},
            "imagery": "City skylines, towers on the skyline, energized coverage maps — bright and forward",
            "tone": "Energised, clear, reassuring; speaks in coverage and connection.",
        },
    },
    # ---------------- Automotive ----------------
    "auto": {
        "tagline": "Parts on the line, on the build.",
        "mission": "Deliver committed OEM part lots reliably and on time so assembly lines stay scheduled, stays running, and no plant shuts down waiting on a supplier.",
        "vision": "An automotive supply chain where line-side parts are a given, and our on-time record keeps assembly floors from ever going dark.",
        "values": [
            ("Line integrity", "A missed part lot can stop a whole line; we treat the date accordingly."),
            ("Quality at the core", "On time is never at the expense of a defective part."),
            ("Traceability", "We prove every part lot against the ledger, from source to line-side."),
            ("Assembly partnership", "OEMs plan around us; we make that planning safe."),
            ("Continuous improvement", "Every miss is a system fix, not a blame."),
        ],
        "about": "Forge Auto is an automotive OEM supplier. We take committed part-lot deliveries and land them line-side on the scheduled date — verified, traceable, right-first-time. When a whole assembly line depends on a supplier keeping the date, our on-time evidence is not a nicety; it is what keeps the plant scheduled and the warranty quiet.",
        "fast_facts": [
            "Founded 1989, automotive OEM parts",
            "1,200+ part variants delivered",
            "Line-side programs with 40+ assembly plants",
        ],
        "history": [
            ("1989", "Founded as a forge supplying drivetrain parts."),
            ("2005", "Scaled to full line-side OEM part-lot delivery."),
            ("2018", "Digitised every lot to ledger-verified on-time evidence."),
        ],
        "leadership": [
            ("Grant Kowalski", "Chief Executive", "Cast and forged parts his whole career before leading Forge Auto."),
            ("Nadia Foster", "Chief Operations Officer", "Owns the supply network and the on-time gate across plants."),
        ],
        "products_services": [
            "OEM part-lot design and delivery",
            "Line-side supply scheduling",
            "Supplier quality assurance",
        ],
        "testimonials": [
            ("Forge Auto is the one supplier our line can run without watching the clock for.", "OEM plant director"),
        ],
        "trust": [
            ("98.9% committed part-lot on-time rate (2025)", "Forge Auto delivery ledger"),
            ("IATF 16949 automotive quality certification", "third-party audit"),
        ],
        "locations": "Toledo, OH (HQ) · plants and line-side hubs serving 40+ OEM assembly sites",
        "faq": [
            ("What proves your on-time claim?", "Each committed part lot anchors to a signed ledger event with a verified delivery time — auditable from order to line-side."),
            ("Do you support just-in-time delivery?", "Yes, JIT line-side scheduling is core, and the on-time gate applies to every committed lot."),
        ],
        "contact": "supply@forgeauto.example · +1-419-555-0127",
        "careers": "Keep the line scheduled: supply chain, quality, logistics, manufacturing engineering.",
        "investors": "Privately held. Plant reliability data shared with OEM customers.",
        "press": "media@forgeauto.example — plant and quality announcements.",
        "esg": "Low-emissions forging, part-traceability for circularity, apprenticeship programs.",
        "legal": ["Privacy", "Terms", "California Rights", "Do Not Sell or Share"],
        "nav": ["About", "Capabilities", "Plants", "Quality", "Careers", "Investors", "Press", "Contact"],
        "cookie_consent": "Accept All · Reject All · Preferences (link to Privacy)",
        "design": {
            "palette": [("Anvil Grey", "#3A3D42"), ("Machining Silver", "#C7CCD1"), ("Redline Red", "#C4262E"), ("Deep Forge", "#15171A")],
            "typography": {"heading": "Solid industrial sans (e.g. Oswald)", "body": "Workhorse sans (e.g. Source Sans 3)"},
            "logo": {"wordmark": "FORGE AUTO in heavy caps", "character": "an ingot/anvil mark", "usage": "clear space heavy; red as accent, grey+silver standard"},
            "imagery": "Assembly lines, forged parts, machining in motion — heavy, capable, precise",
            "tone": "Built, dependable, plain; about keeping the line running.",
        },
    },
    # ---------------- Media ----------------
    "media": {
        "tagline": "Campaigns that land on the date.",
        "mission": "Deliver committed content-delivery campaigns reliably and on time so platforms and brands stay in the mix and audiences see the story on schedule.",
        "vision": "A media marketplace where a campaign release date is a contract audiences can count on.",
        "values": [
            ("The date is the story", "A late campaign is a missed audience moment."),
            ("Creative rigour", "Great work delivered on time, never rushed at the end."),
            ("Measured impact", "We verify every run against the ledger; reach is a fact."),
            ("Platform partnership", "We make our partners' schedules look good."),
            ("Audience respect", "We deliver content audiences actually want, when they want it."),
        ],
        "about": "Hollow Media produces and delivers committed content-delivery campaigns — from concept through to an energized, measured launch on the agreed date. In a business where timing is the whole story, we back every campaign release with ledger-verified on-time evidence, so a 'drop' date is a real commitment, not a hopeful aspiration.",
        "fast_facts": [
            "Founded 2007, media & content production",
            "400+ campaigns delivered",
            "Multi-format distribution across platforms",
        ],
        "history": [
            ("2007", "Founded producing branded content."),
            ("2014", "Launched the content-delivery campaign business."),
            ("2022", "Verifying every campaign release against the ledger."),
        ],
        "leadership": [
            ("Celine Wexler", "Chief Executive", "Producer-turned-executive who built Hollow on delivered dates."),
            ("Omar Delgado", "Chief Media Officer", "Owns the distribution network and campaign timing."),
        ],
        "products_services": [
            "Content-delivery campaigns (concept to launch)",
            "Multi-platform distribution",
            "Campaign measurement and reporting",
        ],
        "testimonials": [
            ("Hollow delivered the campaign on the exact date we'd promised our brand. That never happens in media.", "Brand marketing lead"),
        ],
        "trust": [
            ("99.3% committed campaign on-time rate (2025)", "Hollow delivery ledger"),
            ("MARC (Media Rating Council) aligned measurement", "independent audit"),
        ],
        "locations": "LA (HQ) · production + distribution hubs across 3 regions",
        "faq": [
            ("How can you commit a creative launch date?", "We treat the release like a delivery: planned backwards from the date, verified at launch, and measured against the ledger."),
            ("Do you handle distribution yourselves?", "Yes, multi-platform distribution is core and part of the on-time commitment."),
        ],
        "contact": "hello@hollowmedia.example · +1-310-555-0188",
        "careers": "Drop stories on time: production, distribution, data, and campaign leads.",
        "investors": "Privately held. Campaign performance data shared with brands on request.",
        "press": "press@hollowmedia.example — launches, shows, and reliability stories.",
        "esg": "Sustainable production practices, audience-inclusive content, creator equity programs.",
        "legal": ["Privacy", "Terms", "California Rights", "Do Not Sell or Share", "Content Policy"],
        "nav": ["About", "Work", "Distribution", "Press", "Careers", "Contact"],
        "cookie_consent": "Accept All · Reject All · Preferences (link to Privacy)",
        "design": {
            "palette": [("Studio Black", "#111214"), ("Hollow Cerise", "#D41159"), ("Screen White", "#F7F5F2"), ("Signal Teal", "#0F7A72")],
            "typography": {"heading": "Contemporary display serif (e.g. Playfair Display)", "body": "Neutral sans (e.g. Inter)"},
            "logo": {"wordmark": "hollow", "character": "a hollow-circle/cutout mark", "usage": "clear space fine; cerise-on-black primary, teal for data accents"},
            "imagery": "Cinematic stills, editing bays, campaign storyboards — dark, bold, precise",
            "tone": "Confident, slightly provocative, disciplined about timing; the date is the point.",
        },
    },
    # ---------------- Logistics / Transport ----------------
    "logi": {
        "tagline": "Freight that moves on the minute.",
        "mission": "Settle committed freight dispatches reliably and on time so shippers run their operations to a schedule they can bank on, lane by lane.",
        "vision": "A logistics network where 'dispatched on time' is so reliable it fades into the background of our shippers' day.",
        "values": [
            ("The deadline is the deal", "A freight commitment is a promise to a schedule."),
            ("Proof of movement", "We verify every dispatch against the ledger; 'in transit' is a measured fact."),
            ("Shipper trust", "Shippers plan capacity and customer delivery around our lanes."),
            ("Efficiency", "Every mile earned is a price we can keep fair."),
            ("Transparency", "If a dispatch slips, shippers hear it from us first."),
        ],
        "about": "Hawkline Logistics is a freight and transport operator. We take committed freight dispatches and settle them on time, lane by lane, backing every movement with ledger-verified evidence. For shippers whose entire customer promise depends on a load leaving on schedule, our on-time record is the quiet foundation they plan around.",
        "fast_facts": [
            "Founded 1994, freight & transport",
            "Lane network across 3 continents",
            "Freight-dispatch settlement operation",
        ],
        "history": [
            ("1994", "Founded with a single truck lane."),
            ("2006", "Expanded into a national freight-settlement network."),
            ("2019", "Digitised every dispatch to ledger-verified on-time evidence."),
        ],
        "leadership": [
            ("Dana Ferrell", "Chief Executive", "Ran two carriers before founding Hawkline on schedule trust."),
            ("Melvin Ashe", "Chief Commercial Officer", "Owns lanes, carrier network, and dispatch reliability."),
        ],
        "products_services": [
            "Freight dispatch and settlement",
            "Dedicated and shared-lane transport",
            "Shipment tracking and proof-of-movement reporting",
        ],
        "testimonials": [
            ("Hawkline's dispatch clock is the one I can set my whole week by.", "Shipper operations manager"),
        ],
        "trust": [
            ("98.5% committed freight dispatch on-time rate (2025)", "Hawkline dispatch ledger"),
            ("FMCSA-compliant safety programme", "audited annually"),
        ],
        "locations": "Nashville, TN (HQ) · dispatch hubs across the lane network",
        "faq": [
            ("What makes your on-time claim auditable?", "Every dispatch settles to a signed ledger event with a verified timestamp — shippers can see the proof, not just hear the claim."),
            ("Do you run dedicated lanes?", "Yes, both dedicated and shared lanes, each with a committed dispatch schedule we verify."),
        ],
        "contact": "dispatch@hawkline.example · +1-615-555-0135",
        "careers": "Move freight on the minute: dispatch, fleet ops, lane management, carrier relations.",
        "investors": "Privately held. Lane reliability data shared with qualified shippers.",
        "press": "media@hawkline.example — network and reliability stories.",
        "esg": "Fuel-efficiency routing, backhaul reduction to cut empty miles, driver wellbeing programs.",
        "legal": ["Privacy", "Terms", "California Rights", "Do Not Sell or Share"],
        "nav": ["About", "Lanes", "Services", "Careers", "Investors", "Press", "Contact"],
        "cookie_consent": "Accept All · Reject All · Preferences (link to Privacy)",
        "design": {
            "palette": [("Roadway Black", "#1D1F22"), ("Highway Amber", "#F0A81E"), ("Freight Orange", "#E3621A"), ("Signal Grey", "#C7CBCF")],
            "typography": {"heading": "Clear transport sans (e.g. Archivo)", "body": "Open neutral sans (e.g. Roboto)"},
            "logo": {"wordmark": "HAWKLINE in sharp caps", "character": "a hawk/freight-chevron mark", "usage": "clear space wide; amber+orange accents on dark"},
            "imagery": "Traffic-lane motion, trucks under speed, dispatch boards — momentum and control",
            "tone": "Direct, efficient, factual; the clock matters more than the adjectives.",
        },
    },
    # ---------------- Industrial ----------------
    "indu": {
        "tagline": "Parts that keep the line turning.",
        "mission": "Deliver committed machinery parts reliably and on time so plants and workshops trust FerrousWorks enough to keep production lines scheduled without a backstop.",
        "vision": "Industrial machinery where the part you ordered arrives exactly when the maintenance plan said — so uptime is planned, not hoped for.",
        "values": [
            ("Uptime is the deliverable", "A late part is a stopped line; we protect the schedule."),
            ("Machined right", "On time never trades off tolerances or metallurgy."),
            ("Traceability", "Every part lot is ledger-verified from material to machine."),
            ("Plant partnership", "Planners lean on us to keep lines running."),
            ("Built to last", "We make parts that outlast the maintenance cycle."),
        ],
        "about": "FerrousWorks is an industrial machinery-parts supplier. We take committed machinery parts deliveries and land them on the date the production plan needs them — machined, verified, traceable. In a plant where a missed part means a quiet line and idle labour, our on-time evidence is what lets planners schedule with confidence instead of contingency.",
        "fast_facts": [
            "Founded 1983, industrial machinery parts",
            "5,000+ parts delivered annually",
            "Serving plants, OEMs, and job shops",
        ],
        "history": [
            ("1983", "Founded as a machine shop in the industrial Midwest."),
            ("1999", "Scaled to committed machinery-parts supply."),
            ("2017", "Digitised every lot to ledger-verified on-time evidence."),
        ],
        "leadership": [
            ("Ingrid Halvorsen", "Chief Executive", "Metallurgist and shop floor leader before taking the helm of FerrousWorks."),
            ("Carl Betancourt", "Chief Operating Officer", "Owns machining capacity and the on-time gate."),
        ],
        "products_services": [
            "Machinery parts design and delivery",
            "Precision machining and fabrication",
            "Part-traceability and reliability reporting",
        ],
        "testimonials": [
            ("FerrousWorks is the one supplier our maintenance schedule doesn't hedge against.", "Plant maintenance engineer"),
        ],
        "trust": [
            ("99.0% committed machinery-parts on-time rate (2025)", "FerrousWorks delivery ledger"),
            ("ISO 9001 quality management certification", "third-party audit"),
        ],
        "locations": "Cleveland, OH (HQ) · machining plants serving the industrial Midwest and beyond",
        "faq": [
            ("How is your on-time claim verified?", "Each committed part lot anchors to a signed ledger event with a verified delivery time — traceable from material order to the plant."),
            ("Do you support emergency and planned maintenance parts?", "Yes, both; every committed delivery, planned or rush, runs under the same on-time gate."),
        ],
        "contact": "orders@ferrousworks.example · +1-216-555-0156",
        "careers": "Keep the line turning: machining, metallurgy, supply, quality, planning.",
        "investors": "Privately held. Plant reliability data shared on request.",
        "press": "media@ferrousworks.example — capability and quality announcements.",
        "esg": "Low-waste machining, material traceability for circularity, apprentice and upskilling programs.",
        "legal": ["Privacy", "Terms", "California Rights", "Do Not Sell or Share"],
        "nav": ["About", "Capabilities", "Plants & Facilites", "Quality", "Careers", "Investors", "Press", "Contact"],
        "cookie_consent": "Accept All · Reject All · Preferences (link to Privacy)",
        "design": {
            "palette": [("Foundry Charcoal", "#24262B"), ("Forge Orange", "#D85C27"), ("Steel Grey", "#9AA0A6"), ("Mill White", "#F2F1EE")],
            "typography": {"heading": "Sturdy industrial sans (e.g. Chivo)", "body": "Workhorse sans (e.g. Source Sans 3)"},
            "logo": {"wordmark": "FERROUSWORKS in hard caps", "character": "a gear/ingot mark", "usage": "clear space sturdy; forge orange as accent on charcoal"},
            "imagery": "Machining centre work, forged parts, shop floors at scale — heavy and precise",
            "tone": "Built, straightforward, exact; about uptime and tolerances.",
        },
    },
    # ---------------- Financial (uniform; label finb) ----------------
    "finb": {
        "tagline": "Funding that lands on the date.",
        "mission": "Commit and settle funding tranches reliably and on time so corporate clients can run their own working-capital plans to a schedule they can trust.",
        "vision": "A commercial lending market where a committed tranche settling on time is a durable promise, backed by ledger-verified evidence.",
        "values": [
            ("Commitment is covenant", "A committed funding tranche is a promise to a date."),
            ("Evidence-first", "We verify every settlement against the ledger; on time is a fact, not a target."),
            ("Client partnership", "Corporate clients plan working capital around our settlements."),
            ("Prudence", "On time never trades away sound credit judgement."),
            ("Transparency", "If a settlement will slip, clients hear it from us first."),
        ],
        "about": "Northglen Bank is a regional commercial bank. We commit and settle funding tranches for corporate clients, and we run that commitment to the ledger-verified on-time standard of the platform. For a treasurer planning working capital around a committed settlement date, our on-time record is the reliable foundation of the relationship.",
        "fast_facts": [
            "Founded 1987, regional commercial banking",
            "Corporate lending across the region",
            "Ledger-verified settlement operation",
        ],
        "history": [
            ("1987", "Chartered as a regional commercial bank."),
            ("2005", "Expanded into syndicated committed funding."),
            ("2023", "Placed every committed settlement under ledger-verified on-time evidence."),
        ],
        "leadership": [
            ("Ruth Calloway", "Chief Executive", "Two decades in commercial lending; built Northglen on settlement integrity."),
            ("Victor Hughes", "Chief Treasury Officer", "Owns the funding and correspondent network."),
        ],
        "products_services": [
            "Committed working-capital funding tranches",
            "Syndicated committed funding",
            "Treasury and settlement operations",
        ],
        "testimonials": [
            ("Northglen's committed settlements are the ones our treasury calendar is built around.", "Corporate treasurer"),
        ],
        "trust": [
            ("98.6% committed settlement on-time rate (2025)", "Northglen settlement ledger"),
            ("Chartered bank; prudential oversight", "state regulator"),
        ],
        "locations": "Regional HQ + branches across the state",
        "faq": [
            ("How do you prove a settlement was on time?", "Every committed tranche settles to a signed ledger event with a verified timestamp — auditable, not asserted."),
            ("Do you commit syndicated funding?", "Yes, both bilateral and syndicated committed tranches run under the same evidence standard."),
        ],
        "contact": "treasury@northglen.example · +1-505-555-0199",
        "careers": "Back corporate plans with reliable funding: treasury, credit, settlement operations.",
        "investors": "Public charter with regulated reporting; settlement reliability shared with regulators.",
        "press": "media@northglen.example — lending, treasury, and community programs.",
        "esg": "Responsible lending, financial-inclusion programs, branch-efficiency investments.",
        "legal": ["Privacy", "Terms", "California Rights", "Do Not Sell or Share", "Deposit & Lending Disclosures"],
        "nav": ["About", "Lending", "Treasury", "Careers", "Investors", "Press", "Community", "Contact"],
        "cookie_consent": "Accept All · Reject All · Preferences (link to Privacy)",
        "design": {
            "palette": [("Ledger Navy", "#14314E"), ("Settlement Blue", "#1B6CA8"), ("Vault Grey", "#8A929B"), ("Trust White", "#FAFBFC")],
            "typography": {"heading": "Trusted serif (e.g. Source Serif 4)", "body": "Open sans (e.g. Inter)"},
            "logo": {"wordmark": "NORTHGLEN in confident caps", "character": "a chevron/vault-mark", "usage": "clear space generous; navy+white primary, blue accent"},
            "imagery": "Calm and solid: banking halls, treasury operations, measured growth — trustworthy",
            "tone": "Steady, precise, reassuring; speaks in commitments and verified settlements.",
        },
    },
}


SECTORS = {
    # ---------------- Technology (cloud/software) ----------------
    "tech": mk(
        "tech", "Technology", "vantagecloud", "VantageCloud", "org://tech/sierra-coast",
        "org://tech/sentinel-labs", "org://tech/revan-digital", "person://tech/cdo",
        "agent://tech/deploy-ops",
        outcome="platform-upgrade deployment", caps=["deployment", "integration"],
        root="integration failure — org://tech/revan-digital missed its committed upgrade "
             "deployment by 2 days; scoped Trust fell 0.90->0.51",
        recommended="Re-allocate committed platform-upgrade work to the verified on-time "
                    "integrator (sentinel-labs) and gate the laggard (revan-digital) with a "
                    "performance checkpoint before any new commitment",
        esc_trigger="external integrated deployment — irreversible and cost-unknowable once cut over",
        task_objective="re-balance platform-upgrade allocation to the verified on-time "
                       "integrator (sentinel-labs) and gate the laggard (revan-digital)",
        task_importance="restores on-time upgrade delivery, protecting enterprise clients' scoped Trust",
        goal_text="Consistently deliver committed platform upgrades on time so enterprise "
                  "clients trust VantageCloud enough to renew.",
        learning_why="Concentrating deployment work with an integrator that has verified on-time "
                     "delivery (sentinel-labs), while gating the laggard (revan-digital), restored "
                     "on-time upgrades. Verified good deployments compound scoped Trust and re-price routing.",
        policy_change="ALLOCATE by fit AND scoped Trust (not fit alone); partners below the "
                      "Trust floor require a performance gate before a new commitment.",
        tradeoff="Re-balancing concentrates work with sentinel-labs (higher short-term "
                 "concentration risk) but restores on-time delivery and protects client Trust; "
                 "doing nothing keeps upgrades below target.",
        rec_option="re-balance platform upgrades to the verified on-time integrator",
        gate_option="gate the laggard (revan-digital)", expected_impact="forward on-time returns to 1.0",
    ),
    # ---------------- Healthcare / Pharma ----------------
    "hlth": mk(
        "hlth", "Healthcare / Pharma", "lumenhealth", "Lumen Health", "org://hlth/northgate-care",
        "org://hlth/cortica-supply", "org://hlth/meridian-med", "person://hlth/oph",
        "agent://hlth/supply-ops",
        outcome="pharmaceutical delivery", caps=["supply", "distribution"],
        root="supply failure — org://hlth/meridian-med missed its committed pharmaceutical "
             "delivery by 2 days; scoped Trust fell 0.90->0.51",
        recommended="Re-allocate committed pharmaceutical supply to the verified on-time "
                    "distributor (cortica-supply) and gate the laggard (meridian-med) with a "
                    "checkpoint before any new order",
        esc_trigger="external pharmaceutical release — irreversible and cost-unknowable once shipped",
        task_objective="re-balance committed pharmaceutical supply to the verified on-time "
                       "distributor (cortica-supply) and gate the laggard (meridian-med)",
        task_importance="restores on-time supply, protecting facility patient-trust scores",
        goal_text="Consistently deliver committed pharmaceutical supply on time so care "
                  "facilities trust Lumen Health enough to keep ordering.",
        learning_why="Concentrating supply with a distributor that has verified on-time delivery "
                     "(cortica-supply), while gating the laggard (meridian-med), restored on-time "
                     "pharmaceutical delivery. Verified good deliveries compound scoped Trust.",
        policy_change="ALLOCATE by fit AND scoped Trust (not fit alone); distributors below the "
                      "Trust floor require a performance checkpoint before a new order.",
        tradeoff="Concentrating supply with cortica-supply restores on-time delivery (higher "
                 "short-term concentration risk) but protects facility-trust; doing nothing keeps below target.",
        rec_option="re-balance pharmaceutical supply to the verified on-time distributor",
        gate_option="gate the laggard (meridian-med)", expected_impact="forward on-time returns to 1.0",
    ),
    # ---------------- Food / Bev / Consumer ----------------
    "food": mk(
        "food", "Food / Bev / Consumer", "maplehurst", "Maplehurst Foods", "org://food/caseway",
        "org://food/crestline", "org://food/harlow", "person://food/cso",
        "agent://food/restock-ops",
        outcome="retail restock shipment", caps=["restock", "delivery"],
        root="distribution failure — org://food/harlow missed its committed restock shipment "
             "by 2 days; scoped Trust fell 0.90->0.51",
        recommended="Re-allocate committed restock volume to the verified on-time distributor "
                    "(crestline) and gate the laggard (harlow) before new orders",
        esc_trigger="external restock truck release — irreversible and cost-unknowable once en route",
        task_objective="re-balance restock allocation to the verified on-time distributor "
                       "(crestline) and gate the laggard (harlow)",
        task_importance="restores shelf on-time, protecting retailer scoped Trust",
        goal_text="Consistently deliver committed restock shipments on time so retailers "
                  "keep Maplehurst on the shelf.",
        learning_why="Concentrating restock volume with a distributor that has verified on-time "
                     "delivery (crestline), while gating the laggard (harlow), restored on-time "
                     "shipment. Verified good shipments compound scoped Trust.",
        policy_change="ALLOCATE by fit AND scoped Trust; distributors below the Trust floor "
                      "need a performance gate before new orders.",
        tradeoff="Restocking via crestline restores on-time (higher short-term concentration "
                 "risk) but protects retailer Trust; doing nothing keeps shipments below target.",
        rec_option="re-balance restock to the verified on-time distributor",
        gate_option="gate the laggard (harlow)", expected_impact="forward on-time returns to 1.0",
    ),
    # ---------------- Retail ----------------
    "retail": mk(
        "retail", "Retail", "hardvale", "HardVale Stores", "org://retail/southline",
        "org://retail/atlas-freight", "org://retail/corvus-logistics", "person://retail/cfo",
        "agent://retail/inbound-ops",
        outcome="store replenishment delivery", caps=["replenishment", "logistics"],
        root="logistics failure — org://retail/corvus-logistics missed its committed store "
             "replenishment by 2 days; scoped Trust fell 0.90->0.51",
        recommended="Re-allocate committed store replenishment to the verified on-time carrier "
                    "(atlas-freight) and gate the laggard (corvus-logistics)",
        esc_trigger="external replenishment release — irreversible and cost-unknowable once dispatched",
        task_objective="re-balance store replenishment to the verified on-time carrier "
                       "(atlas-freight) and gate the laggard (corvus-logistics)",
        task_importance="restores shelf-on-time, protecting shopper scoped Trust",
        goal_text="Consistently deliver committed store replenishment on time so shoppers "
                  "keep finding Stock at HardVale.",
        learning_why="Routing replenishment via a carrier with verified on-time delivery "
                     "(atlas-freight), while gating the laggard (corvus-logistics), restored "
                     "on-time replenishment. Verified good deliveries compound scoped Trust.",
        policy_change="ALLOCATE by fit AND scoped Trust; carriers below the Trust floor need "
                      "a performance gate before new runs.",
        tradeoff="Routing via atlas-freight restores on-time (higher short-term concentration "
                 "risk) but protects shopper Trust; doing nothing keeps below target.",
        rec_option="re-balance replenishment to the verified on-time carrier",
        gate_option="gate the laggard (corvus-logistics)", expected_impact="forward on-time returns to 1.0",
    ),
    # ---------------- Energy / Chemicals ----------------
    "enrg": mk(
        "enrg", "Energy / Chemicals", "basinline", "Basinline Energy", "org://enrg/terminal-west",
        "org://enrg/gyre-marine", "org://enrg/peridot-shipping", "person://enrg/supt",
        "agent://enrg/logistics-ops",
        outcome="refined-products tanker delivery", caps=["tanker", "delivery"],
        root="shipping failure — org://enrg/peridot-shipping missed its committed tanker "
             "delivery by 2 days; scoped Trust fell 0.90->0.51",
        recommended="Re-allocate committed tanker volume to the verified on-time carrier "
                    "(gyre-marine) and gate the laggard (peridot-shipping)",
        esc_trigger="external tanker discharge — irreversible and cost-unknowable once loaded",
        task_objective="re-balance tanker allocation to the verified on-time carrier "
                       "(gyre-marine) and gate the laggard (peridot-shipping)",
        task_importance="restores terminal on-time, protecting counterpart scoped Trust",
        goal_text="Consistently deliver committed refined-products tanker terms on time so "
                  "term customers keep contracting Basinline.",
        learning_why="Routing tanker volume via a carrier with verified on-time discharge "
                     "(gyre-marine), while gating the laggard (peridot-shipping), restored on-time "
                     "delivery. Verified good discharges compound scoped Trust.",
        policy_change="ALLOCATE by fit AND scoped Trust; carriers below the Trust floor need a "
                      "gate before new charter terms.",
        tradeoff="Routing via gyre-marine restores on-time discharge (higher short-term "
                 "concentration risk) but protects term-customer Trust; doing nothing keeps below target.",
        rec_option="re-balance tanker volume to the verified on-time carrier",
        gate_option="gate the laggard (peridot-shipping)", expected_impact="forward on-time returns to 1.0",
    ),
    # ---------------- Aerospace / Defense / Aviation ----------------
    "aero": mk(
        "aero", "Aerospace / Defense / Aviation", "valiant-aero", "Valiant Aero", "org://aero/quantum-air",
        "org://aero/apex-aeronautics", "org://aero/vireo-airframe", "person://aero/pgm",
        "agent://aero/prog-ops",
        outcome="airframe-subsystem delivery", caps=["subsystem", "integration"],
        root="supplier failure — org://aero/vireo-airframe missed its committed airframe "
             "subsystem delivery by 2 days; scoped Trust fell 0.90->0.51",
        recommended="Re-allocate committed subsystem work to the verified on-time integrator "
                    "(apex-aeronautics) and gate the laggard (vireo-airframe)",
        esc_trigger="external flight-critical release — irreversible and cost-unknowable once in the build",
        task_objective="re-balance subsystem allocation to the verified on-time integrator "
                       "(apex-aeronautics) and gate the laggard (vireo-airframe)",
        task_importance="restores program-on-time, protecting fleet-customer scoped Trust",
        goal_text="Consistently deliver committed airframe subsystems on time so aviation "
                  "customers keep Valiant Aero on the program.",
        learning_why="Routing subsystem work via an integrator with verified on-time delivery "
                     "(apex-aeronautics), while gating the laggard (vireo-airframe), restored "
                     "on-time delivery. Verified good deliveries compound scoped Trust.",
        policy_change="ALLOCATE by fit AND scoped Trust; integrators below the Trust floor need "
                      "a performance gate before new work.",
        tradeoff="Routing via apex-aeronautics restores on-time (higher short-term "
                 "concentration risk) but protects program Trust; doing nothing keeps below target.",
        rec_option="re-balance airframe subsystems to the verified on-time integrator",
        gate_option="gate the laggard (vireo-airframe)", expected_impact="forward on-time returns to 1.0",
    ),
    # ---------------- Telecom ----------------
    "telco": mk(
        "telco", "Telecom", "nimbuscom", "NimbusCom", "org://telco/fairfield-metro",
        "org://telco/meridian-tower", "org://telco/nimbus-networks", "person://telco/cno",
        "agent://telco/build-ops",
        outcome="cell-site buildout", caps=["buildout", "erection"],
        root="construction failure — org://telco/nimbus-networks missed its committed cell-site "
             "buildout by 2 days; scoped Trust fell 0.90->0.51",
        recommended="Re-allocate committed cell-site buildout to the verified on-time contractor "
                    "(meridian-tower) and gate the laggard (nimbus-networks)",
        esc_trigger="external site handover — irreversible and cost-unknowable once energized",
        task_objective="re-balance cell-site buildout to the verified on-time contractor "
                       "(meridian-tower) and gate the laggard (nimbus-networks)",
        task_importance="restores coverage-on-time, protecting subscriber scoped Trust",
        goal_text="Consistently deliver committed cell-site buildouts on time so metro "
                  "subscribers keep trusting NimbusCom coverage.",
        learning_why="Routing buildout via a contractor with verified on-time delivery "
                     "(meridian-tower), while gating the laggard (nimbus-networks), restored "
                     "on-time buildout. Verified good handovers compound scoped Trust.",
        policy_change="ALLOCATE by fit AND scoped Trust; contractors below the Trust floor need "
                      "a gate before new buildouts.",
        tradeoff="Routing via meridian-tower restores on-time buildout (higher short-term "
                 "concentration risk) but protects coverage Trust; doing nothing keeps below target.",
        rec_option="re-balance cell-site buildout to the verified on-time contractor",
        gate_option="gate the laggard (nimbus-networks)", expected_impact="forward on-time returns to 1.0",
    ),
    # ---------------- Automotive ----------------
    "auto": mk(
        "auto", "Automotive", "forge-auto", "Forge Auto", "org://auto/cypress-assembly",
        "org://auto/stellar-auto", "org://auto/corvair-parts", "person://auto/vpo",
        "agent://auto/supply-ops",
        outcome="OEM part-lot delivery", caps=["oem-parts", "delivery"],
        root="tier failure — org://auto/corvair-parts missed its committed part-lot delivery "
             "by 2 days; scoped Trust fell 0.90->0.51",
        recommended="Re-allocate committed OEM part lots to the verified on-time vendor "
                    "(stellar-auto) and gate the laggard (corvair-parts)",
        esc_trigger="external line-side release — irreversible and cost-unknowable once in the build",
        task_objective="re-balance OEM part allocation to the verified on-time vendor "
                       "(stellar-auto) and gate the laggard (corvair-parts)",
        task_importance="restores line-on-time, protecting assembly scoped Trust",
        goal_text="Consistently deliver committed OEM part lots on time so assembly lines "
                  "trust Forge Auto enough to stay scheduled.",
        learning_why="Routing part lots via a vendor with verified on-time delivery "
                     "(stellar-auto), while gating the laggard (corvair-parts), restored on-time "
                     "supply. Verified good deliveries compound scoped Trust.",
        policy_change="ALLOCATE by fit AND scoped Trust; vendors below the Trust floor need a "
                      "gate before new lots.",
        tradeoff="Routing via stellar-auto restores on-time supply (higher short-term "
                 "concentration risk) but protects line Trust; doing nothing keeps below target.",
        rec_option="re-balance OEM part lots to the verified on-time vendor",
        gate_option="gate the laggard (corvair-parts)", expected_impact="forward on-time returns to 1.0",
    ),
    # ---------------- Media ----------------
    "media": mk(
        "media", "Media", "hollowmedia", "Hollow Media", "org://media/cascade-vantage",
        "org://media/lyra-ops", "org://media/hollowpoint-digital", "person://media/cmo",
        "agent://media/campaign-ops",
        outcome="content-delivery campaign", caps=["distribution", "campaign"],
        root="distribution failure — org://media/hollowpoint-digital missed its committed "
             "content-delivery campaign by 2 days; scoped Trust fell 0.90->0.51",
        recommended="Re-allocate committed media distribution to the verified on-time partner "
                    "(lyra-ops) and gate the laggard (hollowpoint-digital)",
        esc_trigger="external campaign release — irreversible and cost-unknowable once live",
        task_objective="re-balance media distribution to the verified on-time partner "
                       "(lyra-ops) and gate the laggard (hollowpoint-digital)",
        task_importance="restores campaign-on-time, protecting audience scoped Trust",
        goal_text="Consistently deliver committed content-delivery campaigns on time so "
                  "platforms keep Hollow Media in the mix.",
        learning_why="Routing distribution via a partner with verified on-time delivery "
                     "(lyra-ops), while gating the laggard (hollowpoint-digital), restored on-time "
                     "campaigns. Verified good runs compound scoped Trust.",
        policy_change="ALLOCATE by fit AND scoped Trust; partners below the Trust floor need a "
                      "gate before new campaigns.",
        tradeoff="Routing via lyra-ops restores on-time campaigns (higher short-term "
                 "concentration risk) but protects platform Trust; doing nothing keeps below target.",
        rec_option="re-balance media distribution to the verified on-time partner",
        gate_option="gate the laggard (hollowpoint-digital)", expected_impact="forward on-time returns to 1.0",
    ),
    # ---------------- Logistics / Transport ----------------
    "logi": mk(
        "logi", "Logistics / Transport", "hawkline", "Hawkline Logistics", "org://logi/papercreek",
        "org://logi/keystone-lines", "org://logi/barnacle-freight", "person://logi/cco",
        "agent://logi/fleet-ops",
        outcome="freight-dispatch settlement", caps=["dispatch", "freight"],
        root="carrier failure — org://logi/barnacle-freight missed its committed freight "
             "dispatch by 2 days; scoped Trust fell 0.90->0.51",
        recommended="Re-allocate committed freight dispatches to the verified on-time carrier "
                    "(keystone-lines) and gate the laggard (barnacle-freight)",
        esc_trigger="external freight release — irreversible and cost-unknowable once dispatched",
        task_objective="re-balance freight allocation to the verified on-time carrier "
                       "(keystone-lines) and gate the laggard (barnacle-freight)",
        task_importance="restores dispatch-on-time, protecting shipper scoped Trust",
        goal_text="Consistently settle committed freight dispatches on time so shippers "
                  "keep Hawkline lines booked.",
        learning_why="Routing freight dispatches via a carrier with verified on-time delivery "
                     "(keystone-lines), while gating the laggard (barnacle-freight), restored "
                     "on-time dispatch. Verified good dispatches compound scoped Trust.",
        policy_change="ALLOCATE by fit AND scoped Trust; carriers below the Trust floor need a "
                      "gate before new dispatches.",
        tradeoff="Routing via keystone-lines restores on-time dispatch (higher short-term "
                 "concentration risk) but protects shipper Trust; doing nothing keeps below target.",
        rec_option="re-balance freight to the verified on-time carrier",
        gate_option="gate the laggard (barnacle-freight)", expected_impact="forward on-time returns to 1.0",
    ),
    # ---------------- Industrial ----------------
    "indu": mk(
        "indu", "Industrial", "ferrousworks", "FerrousWorks", "org://indu/downfield",
        "org://indu/quadrant-works", "org://indu/cadence-tools", "person://indu/plant-mgr",
        "agent://indu/line-ops",
        outcome="machinery parts delivery", caps=["machinery", "parts"],
        root="supplier failure — org://indu/cadence-tools missed its committed machinery parts "
             "delivery by 2 days; scoped Trust fell 0.90->0.51",
        recommended="Re-allocate committed machinery parts to the verified on-time supplier "
                    "(quadrant-works) and gate the laggard (cadence-tools)",
        esc_trigger="external line release — irreversible and cost-unknowable once in production",
        task_objective="re-balance machinery parts to the verified on-time supplier "
                       "(quadrant-works) and gate the laggard (cadence-tools)",
        task_importance="restores production-on-time, protecting plant scoped Trust",
        goal_text="Consistently deliver committed machinery parts on time so plants trust "
                  "FerrousWorks enough to keep lines scheduled.",
        learning_why="Routing parts via a supplier with verified on-time delivery "
                     "(quadrant-works), while gating the laggard (cadence-tools), restored on-time "
                     "delivery. Verified good lots compound scoped Trust.",
        policy_change="ALLOCATE by fit AND scoped Trust; suppliers below the Trust floor need a "
                      "gate before new lots.",
        tradeoff="Routing via quadrant-works restores on-time (higher short-term concentration "
                 "risk) but protects plant Trust; doing nothing keeps below target.",
        rec_option="re-balance machinery parts to the verified on-time supplier",
        gate_option="gate the laggard (cadence-tools)", expected_impact="forward on-time returns to 1.0",
    ),
    # ---------------- Financial (uniform; built via sector_scene under label finb) ----------------
    "finb": mk(
        "finb", "Financial", "northglen", "Northglen Bank", "org://finb/zephyr",
        "org://finb/adamvale", "org://finb/kaplen", "person://finb/treasurer",
        "agent://finb/treasury-ops",
        outcome="committed funding tranche", caps=["funding", "settlement"],
        root="funding failure — org://finb/kaplen missed its committed settlement tranche "
             "by 2 days; scoped Trust fell 0.90->0.51",
        recommended="Re-allocate committed funding to the verified on-time correspondent "
                    "(adamvale) and gate the laggard (kaplen) with a performance "
                    "checkpoint before any new commitment",
        esc_trigger="external funding release — irreversible and cost-unknowable once disbursed",
        task_objective="re-balance committed funding to the verified on-time correspondent "
                       "(adamvale) and gate the laggard (kaplen)",
        task_importance="restores committed-funding on-time, protecting client scoped Trust",
        goal_text="Consistently settle committed funding tranches on time so corporate clients "
                  "trust Northglen Bank enough to deepen the relationship.",
        learning_why="Concentrating committed funding with a correspondent that has verified "
                     "on-time settlement (adamvale), while gating the laggard (kaplen), restored "
                     "on-time funding. Verified good settlements compound scoped Trust.",
        policy_change="ALLOCATE by fit AND scoped Trust (not fit alone); correspondents below the "
                      "Trust floor require a performance gate before a new commitment.",
        tradeoff="Re-balancing concentrates funding with adamvale (higher short-term concentration "
                 "risk) but restores on-time settlement and protects client Trust; doing nothing "
                 "keeps funding below target.",
        rec_option="re-balance committed funding to the verified on-time correspondent",
        gate_option="gate the laggard (kaplen)", expected_impact="forward on-time returns to 1.0",
    ),
}