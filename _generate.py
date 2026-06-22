"""Generate FlowProHVAC service and city pages from shared templates.

Run from the site root:
    python3 _generate.py

Idempotent — overwrites generated files. The homepage, about, contact, sitemap,
robots, and assets are hand-written and not touched.
"""

from pathlib import Path
from textwrap import dedent

ROOT = Path(__file__).parent
PHONE = "(818) 625-4400"
PHONE_HREF = "tel:+18186254400"
EMAIL = "ayazabbas@flowprohvac.com"
SITE = "https://flowprohvac.com"
YEAR = 2026

# ---------------- shared partials ----------------

HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link rel="icon" type="image/png" href="/favicon.png">
  <link rel="apple-touch-icon" href="/favicon.png">
  <title>{title}</title>
  <meta name="description" content="{description}">
  <link rel="canonical" href="{canonical}">

  <meta property="og:type" content="website">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{description}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:site_name" content="FlowProHVAC">
  <meta name="twitter:card" content="summary_large_image">

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
  <link rel="stylesheet" href="/assets/styles.css">

  {schema}
</head>
<body>
"""

HEADER = """
<header>
  <div class="container header-inner">
    <div class="logo">
      <span class="logo-icon"><i class="fa-solid fa-wind"></i></span>
      <a href="/"><span class="accent">Flow</span>ProHVAC</a>
    </div>
    <nav class="primary" aria-label="Primary">
      <ul>
        <li><a href="/">Home</a></li>
        <li class="has-dropdown">
          <a href="/#services">Services ▾</a>
          <ul class="dropdown">
            <li><a href="/services/ac-repair.html">AC Repair</a></li>
            <li><a href="/services/ac-installation.html">AC Installation</a></li>
            <li><a href="/services/furnace-repair.html">Furnace Repair</a></li>
            <li><a href="/services/furnace-installation.html">Furnace Installation</a></li>
            <li><a href="/services/mini-split-installation.html">Mini-Split Installation</a></li>
            <li><a href="/services/maintenance-plans.html">Maintenance Plans</a></li>
            <li><a href="/services/indoor-air-quality.html">Indoor Air Quality</a></li>
            <li><a href="/services/commercial-hvac.html">Commercial HVAC</a></li>
            <li><a href="/services/emergency-hvac.html">Same-Day Repair</a></li>
          </ul>
        </li>
        <li class="has-dropdown">
          <a href="/#service-areas">Service Areas ▾</a>
          <ul class="dropdown">
            <li><a href="/service-areas/corona-ca.html">Corona</a></li>
            <li><a href="/service-areas/norco-ca.html">Norco</a></li>
            <li><a href="/service-areas/eastvale-ca.html">Eastvale</a></li>
            <li><a href="/service-areas/chino-hills-ca.html">Chino Hills</a></li>
            <li><a href="/service-areas/riverside-ca.html">Riverside</a></li>
            <li><a href="/service-areas/ontario-ca.html">Ontario</a></li>
          </ul>
        </li>
        <li><a href="/about.html">About</a></li>
        <li><a href="/contact.html">Contact</a></li>
      </ul>
    </nav>
    <div class="header-cta">
      <a class="call-link" href="tel:+18186254400"><i class="fa-solid fa-phone"></i> <span>(818) 625-4400</span></a>
      <button class="menu-btn" aria-label="Open menu">☰</button>
    </div>
  </div>
</header>
"""

FOOTER = """
<footer>
  <div class="container">
    <div class="grid">
      <div class="brand-block">
        <h4>FlowProHVAC</h4>
        <p>Family-owned HVAC contractor serving Corona and the Inland Empire since 1994. Licensed, bonded, and insured.</p>
        <p class="license">CSLB License #: 1142668</p>
      </div>
      <div>
        <h4>Services</h4>
        <ul>
          <li><a href="/services/ac-repair.html">AC Repair</a></li>
          <li><a href="/services/ac-installation.html">AC Installation</a></li>
          <li><a href="/services/furnace-repair.html">Furnace Repair</a></li>
          <li><a href="/services/furnace-installation.html">Furnace Installation</a></li>
          <li><a href="/services/mini-split-installation.html">Mini-Split Installation</a></li>
          <li><a href="/services/maintenance-plans.html">Maintenance Plans</a></li>
          <li><a href="/services/indoor-air-quality.html">Indoor Air Quality</a></li>
          <li><a href="/services/commercial-hvac.html">Commercial HVAC</a></li>
          <li><a href="/services/emergency-hvac.html">Same-Day Repair</a></li>
        </ul>
      </div>
      <div>
        <h4>Service Areas</h4>
        <ul>
          <li><a href="/service-areas/corona-ca.html">Corona, CA</a></li>
          <li><a href="/service-areas/norco-ca.html">Norco, CA</a></li>
          <li><a href="/service-areas/eastvale-ca.html">Eastvale, CA</a></li>
          <li><a href="/service-areas/chino-hills-ca.html">Chino Hills, CA</a></li>
          <li><a href="/service-areas/riverside-ca.html">Riverside, CA</a></li>
          <li><a href="/service-areas/ontario-ca.html">Ontario, CA</a></li>
        </ul>
      </div>
      <div>
        <h4>Contact</h4>
        <ul>
          <li><a href="tel:+18186254400">(818) 625-4400</a></li>
          <li><a href="mailto:ayazabbas@flowprohvac.com">ayazabbas@flowprohvac.com</a></li>
          <li>Corona, CA 92882</li>
          <li>Mon–Sat: 7 AM – 7 PM</li>
          <li><a href="/about.html">About</a></li>
          <li><a href="/contact.html">Contact</a></li>
        </ul>
      </div>
    </div>
    <div class="copyright">&copy; {year} FlowProHVAC. All rights reserved.</div>
  </div>
</footer>

<a class="sticky-call" href="tel:+18186254400"><i class="fa-solid fa-phone"></i> Call (818) 625-4400</a>
<script src="/assets/main.js" defer></script>
</body>
</html>
""".replace("{year}", str(YEAR))


def page_hero(title, subtitle, breadcrumbs):
    """breadcrumbs: list of (label, href|None)"""
    crumb_html = ""
    for i, (label, href) in enumerate(breadcrumbs):
        if href:
            crumb_html += f'<a href="{href}">{label}</a>'
        else:
            crumb_html += f"<span>{label}</span>"
        if i < len(breadcrumbs) - 1:
            crumb_html += '<span class="sep">›</span>'

    return f"""
<section class="page-hero">
  <div class="container">
    <div class="breadcrumb">{crumb_html}</div>
    <h1>{title}</h1>
    <p>{subtitle}</p>
    <div class="cta-row" style="margin-top:20px; display:flex; gap:10px; flex-wrap:wrap;">
      <a href="{PHONE_HREF}" class="btn"><i class="fa-solid fa-phone"></i> Call {PHONE}</a>
      <a href="/contact.html" class="btn btn-outline">Request Estimate</a>
    </div>
  </div>
</section>
"""


FINAL_CTA = """
<section class="section">
  <div class="container">
    <div class="cta-banner">
      <div>
        <h3>Ready to schedule service?</h3>
        <p>Talk to a real technician. Same-day appointments often available.</p>
      </div>
      <div class="actions">
        <a class="btn" href="tel:+18186254400"><i class="fa-solid fa-phone"></i> (818) 625-4400</a>
        <a class="btn btn-outline" href="/contact.html">Request Estimate</a>
      </div>
    </div>
  </div>
</section>
"""


def breadcrumb_schema(items):
    """items: list of (name, url)"""
    elements = []
    for i, (name, url) in enumerate(items, start=1):
        elements.append({
            "@type": "ListItem",
            "position": i,
            "name": name,
            "item": url
        })
    import json
    obj = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": elements}
    return f'<script type="application/ld+json">{json.dumps(obj)}</script>'


def service_schema(name, description, url):
    import json
    obj = {
        "@context": "https://schema.org",
        "@type": "Service",
        "name": name,
        "description": description,
        "url": url,
        "provider": {"@type": "HVACBusiness", "name": "FlowProHVAC", "telephone": "+1-818-625-4400", "url": SITE + "/"},
        "areaServed": [
            {"@type": "City", "name": "Corona, CA"},
            {"@type": "City", "name": "Norco, CA"},
            {"@type": "City", "name": "Eastvale, CA"},
            {"@type": "City", "name": "Chino Hills, CA"},
            {"@type": "City", "name": "Riverside, CA"},
            {"@type": "City", "name": "Ontario, CA"}
        ]
    }
    return f'<script type="application/ld+json">{json.dumps(obj)}</script>'


# ---------------- SERVICE PAGES ----------------

SERVICES = [
    {
        "slug": "ac-repair",
        "h1": "AC Repair in Corona & the Inland Empire",
        "title": "AC Repair in Corona, CA | FlowProHVAC",
        "desc": "Fast, honest AC repair in Corona and surrounding cities. 30+ years of experience. Licensed & insured. Same-day service often available. Call (818) 625-4400.",
        "subtitle": "Same-day diagnosis and repair from a licensed local technician with 30+ years of experience.",
        "intro": "When your air conditioner stops cooling — or starts making sounds it didn't make yesterday — you don't want a salesperson, you want a technician who knows what they're looking at. We've been repairing AC systems in Corona and the surrounding Inland Empire for over 30 years.",
        "sections": [
            ("Common AC problems we fix", [
                "AC running but not cooling",
                "AC not turning on at all",
                "Frozen evaporator coil or ice on the lines",
                "Loud humming, buzzing, or grinding noises",
                "Short cycling (turns on and off too frequently)",
                "Water leaking around the indoor unit",
                "Weak airflow from the vents",
                "Capacitor and contactor failures",
                "Refrigerant leaks and recharges (R-410A and R-22 replacements)",
                "Thermostat troubleshooting and replacement",
            ]),
            ("How our AC repair visit works", [
                "We arrive in the agreed-upon window and call ahead.",
                "We diagnose the actual problem — no guesswork, no upsells.",
                "We explain what's wrong in plain English and quote the repair before any work begins.",
                "Most repairs are completed the same visit. If a part needs to be ordered, we tell you upfront.",
                "We test the system top to bottom before we leave.",
            ]),
        ],
        "faqs": [
            ("How much does AC repair cost in Corona?",
             "A basic service call and minor repair typically lands in the $150 – $400 range. More involved repairs — like a compressor replacement or refrigerant leak — cost more. We give you a written price before doing any work."),
            ("Do you repair all AC brands?",
             "Yes. We service all major brands including Carrier, Trane, Lennox, Goodman, Rheem, York, American Standard, and more."),
            ("Should I repair or replace my AC?",
             "If your system is under 10 years old and the repair is less than 30 – 40% of replacement cost, repair is usually the right call. We'll give you the honest math, not a pressure pitch."),
            ("Do you offer same-day AC repair?",
             "Most weekdays during cooling season, yes. Call as early in the day as possible and we'll do everything we can to get out same-day."),
        ],
    },
    {
        "slug": "ac-installation",
        "h1": "AC Installation in Corona, CA — American Brands, 10-Year Warranty",
        "title": "AC Installation in Corona, CA | Carrier, Trane, Lennox | 10-Yr Warranty",
        "desc": "New AC installation in Corona, CA. We install top American brands — Carrier, Trane, Lennox, American Standard, Rheem — with a 10-year manufacturer parts warranty. Free estimates. We'll beat any written quote. Call (818) 625-4400.",
        "subtitle": "Top American brands installed by a licensed technician with 30+ years of experience. 10-year parts warranty. We'll beat any written estimate.",
        "intro": "A new AC system is a big purchase, and we treat it that way. For over 30 years, FlowProHVAC has installed central air conditioning systems across Corona and the Inland Empire — and we install only top American brands like Carrier, Trane, Lennox, American Standard, and Rheem. Every new install is backed by a 10-year manufacturer parts warranty, and if you bring us a written estimate from another licensed contractor, we'll beat it.",
        "sections": [
            ("Top American brands we install", [
                "Carrier — proven reliability, wide range of efficiency tiers",
                "Trane — built tough, excellent dealer support",
                "Lennox — top-end efficiency and quiet operation",
                "American Standard — premium build, strong warranty",
                "Rheem — strong value, long-lasting compressors",
                "We recommend the brand and model that fits your home and your budget — not what we get the biggest commission on",
            ]),
            ("What's included in every new AC install", [
                "Free in-home estimate and load calculation (Manual J)",
                "Removal and proper disposal of your old system",
                "New outdoor condenser, indoor coil, and refrigerant lines (as needed)",
                "Refrigerant line flush or replacement",
                "Thermostat installation or upgrade",
                "Electrical and condensate drain connections",
                "Full system commissioning and performance testing",
                "10-year manufacturer parts warranty registration",
                "Walk-through of how to use and maintain the system",
            ]),
            ("10-year parts warranty — what it means", [
                "Every new AC we install is covered by a 10-year manufacturer parts warranty when registered properly",
                "We handle the registration for you on installation day",
                "Parts covered include the compressor, coils, and most internal components",
                "Labor warranty is separate — ask us about our labor warranty terms",
            ]),
            ("We'll beat any written estimate", [
                "Bring us a written, itemized estimate from another licensed California HVAC contractor",
                "Same equipment, same scope of work — we'll beat the price",
                "No bait-and-switch on equipment quality or warranty coverage",
                "This isn't a stunt — it's how we earn your business when you're comparing options",
            ]),
            ("Why right-sizing matters as much as brand", [
                "An oversized AC short-cycles, costs more to run, and never dehumidifies properly",
                "An undersized AC runs constantly and never gets your house comfortable",
                "We do a real load calculation — square footage alone isn't enough",
            ]),
        ],
        "faqs": [
            ("How much does a new AC system cost in Corona?",
             "A typical single-family home in Corona will land in the $7,000 – $14,000 range for a complete replacement, depending on size, SEER rating, and ductwork condition. We give a detailed, itemized written estimate — and if you have a quote from another company, we'll beat it."),
            ("What brands do you install?",
             "We install top American brands — Carrier, Trane, Lennox, American Standard, and Rheem — and we recommend the right brand for your home and budget rather than pushing one brand on every customer."),
            ("What does the 10-year warranty cover?",
             "Every new AC install comes with a 10-year manufacturer parts warranty when properly registered. We handle the registration for you. Coverage typically includes the compressor, coils, and most internal components. Labor warranty terms are separate — ask us when we provide the estimate."),
            ("Will you really beat any other estimate?",
             "Yes, on equivalent installs. Bring us a written, itemized estimate from a licensed California HVAC contractor for the same equipment and scope, and we'll beat it. We won't quietly downgrade equipment to win on price."),
            ("How long does a new AC installation take?",
             "Most straightforward residential replacements are completed in one day. Larger jobs or ones requiring duct modifications may take two."),
            ("What SEER rating should I get?",
             "For most Inland Empire homes, a SEER2 rating of 15 – 17 is the sweet spot between upfront cost and energy savings. Higher-SEER systems make sense for larger homes or if you plan to stay long-term."),
            ("Do you offer financing?",
             "Yes — ask about financing options when we give you the estimate."),
        ],
    },
    {
        "slug": "furnace-repair",
        "h1": "Furnace & Heating Repair in Corona, CA",
        "title": "Furnace Repair in Corona, CA | Same-Day Service | FlowProHVAC",
        "desc": "Furnace not heating, short cycling, or making noise? Honest furnace repair in Corona & the Inland Empire. Same-day priority service. 30+ years experience. Licensed & insured. Call (818) 625-4400.",
        "subtitle": "Diagnosed correctly, repaired safely. Gas furnaces, heat pumps, and electric heat — we work on all of it. Same-day priority service.",
        "intro": "Heating problems get worse the longer they're ignored, and a few of them — like cracked heat exchangers — can be dangerous. Our techs diagnose the actual problem, explain what's going on, and get your heat back on safely. Most repair calls are handled the same day you call.",
        "sections": [
            ("Common furnace problems we repair", [
                "Furnace won't turn on",
                "Furnace blowing cold air",
                "Pilot light or igniter not working",
                "Short cycling (turns on and off too frequently)",
                "Strange smells from the vents",
                "Loud banging, rumbling, or screeching",
                "Carbon monoxide concerns",
                "Cracked heat exchanger inspection",
                "Flame sensor cleaning and replacement",
                "Thermostat and control board issues",
            ]),
            ("Why CO and heat exchanger checks matter", [
                "A cracked heat exchanger can leak carbon monoxide into your home — invisible and odorless.",
                "Every repair visit, we visually inspect the exchanger and verify safe combustion.",
                "If we ever find a safety issue, we shut the system down and tell you straight.",
            ]),
        ],
        "faqs": [
            ("Can you come out today for furnace repair?",
             "Most days during the heating season, yes. Call us as early as possible at (818) 625-4400 and we'll do everything we can to get out the same day."),
            ("How much does furnace repair cost?",
             "Most furnace repairs land in the $200 – $600 range. We give a written quote before any work — no surprises."),
            ("My furnace is old — should I repair or replace?",
             "If your furnace is over 15 years old and the repair is significant, replacement may be more economical. We'll give you both numbers and let you decide. New furnaces come with a 10-year manufacturer parts warranty when we install."),
            ("Will you match a competitor's repair quote?",
             "For installations and major repairs, yes — bring us a written estimate from a licensed competitor and we'll beat it."),
        ],
    },
    {
        "slug": "furnace-installation",
        "h1": "Furnace Installation in Corona, CA — American Brands, 10-Year Warranty",
        "title": "Furnace Installation in Corona, CA | Carrier, Trane, Lennox | 10-Yr Warranty",
        "desc": "Energy-efficient furnace installation in Corona & the Inland Empire. Top American brands — Carrier, Trane, Lennox, American Standard, Rheem — with 10-year parts warranty. Free estimate. We'll beat any written quote. Call (818) 625-4400.",
        "subtitle": "Top American brands installed by a licensed local contractor. 10-year parts warranty. We'll beat any written estimate.",
        "intro": "A new furnace should last 15 – 20 years when installed right. Sizing, gas pressure, venting, and combustion air all need to be correct on day one. We've been installing furnaces in Corona and the Inland Empire for over three decades — and we install only top American brands like Carrier, Trane, Lennox, American Standard, and Rheem. Every install is backed by a 10-year manufacturer parts warranty, and we'll beat any written estimate from a licensed competitor.",
        "sections": [
            ("Top American brands we install", [
                "Carrier — proven reliability across full efficiency range",
                "Trane — exceptional durability and dealer support",
                "Lennox — high-efficiency leadership and quiet operation",
                "American Standard — premium build quality and strong warranty",
                "Rheem — strong value with excellent reliability",
                "We recommend the right brand and tier for your home — not the one with the biggest commission",
            ]),
            ("10-year parts warranty — what it covers", [
                "Every new furnace install includes a 10-year manufacturer parts warranty when properly registered",
                "We register the warranty for you on installation day",
                "Covers the heat exchanger, blower motor, and major internal components",
                "Labor warranty terms are separate — ask us when we estimate",
            ]),
            ("What's included with a new furnace install", [
                "Free in-home estimate with sizing calculation",
                "Removal and disposal of the old unit",
                "New high-efficiency gas furnace properly sized for your home",
                "Gas line and venting modifications as needed",
                "New thermostat installation or upgrade",
                "Full safety check including CO levels and combustion analysis",
                "10-year manufacturer parts warranty registration",
            ]),
            ("We'll beat any written estimate", [
                "Bring us a written, itemized estimate from any licensed California HVAC contractor",
                "Same brand and equivalent equipment — we'll beat the price",
                "No quietly downgrading equipment to win on price",
            ]),
            ("Single-stage, two-stage, or modulating?", [
                "Single-stage furnaces are the most affordable and work fine in our climate",
                "Two-stage furnaces offer quieter operation and better temperature evenness",
                "Modulating furnaces are the top tier — most efficient and most comfortable, highest upfront cost",
                "We'll walk you through what makes sense for your house and budget",
            ]),
        ],
        "faqs": [
            ("How much does a new furnace cost in Corona?",
             "Most residential furnace installations in Corona land in the $4,500 – $9,000 range, depending on size, efficiency, and complexity. Itemized estimate provided — and we'll beat any written competitor quote."),
            ("What brands do you install?",
             "Top American brands — Carrier, Trane, Lennox, American Standard, and Rheem. We recommend the right one for your home and budget."),
            ("What does the 10-year warranty cover?",
             "Every new furnace install comes with a 10-year manufacturer parts warranty when properly registered. We handle the registration. Coverage typically includes the heat exchanger, blower motor, and major internal components. Labor warranty terms are separate."),
            ("Will you really beat any other estimate?",
             "Yes, on equivalent installs. Bring us a written, itemized estimate from a licensed California HVAC contractor for the same equipment and scope, and we'll beat it."),
            ("How long does installation take?",
             "Most replacements are completed in one day."),
            ("What efficiency rating should I get?",
             "For our climate, 80% AFUE is the budget pick and 95%+ AFUE makes sense if you want lower bills and plan to stay long-term."),
        ],
    },
    {
        "slug": "mini-split-installation",
        "h1": "Ductless Mini-Split Installation in Corona, CA",
        "title": "Mini-Split Installation in Corona, CA | 10-Year Warranty | FlowProHVAC",
        "desc": "Ductless mini-split installation in Corona and the Inland Empire — for ADUs, garages, additions, and homes without ductwork. 10-year manufacturer parts warranty. We'll beat any written quote. Call (818) 625-4400.",
        "subtitle": "Heating and cooling for rooms your central system can't reach — installed cleanly and properly. 10-year parts warranty. We'll beat any written estimate.",
        "intro": "Ductless mini-splits are the right answer for a lot of situations central HVAC can't solve well: garage conversions, ADUs, room additions, sun-baked bedrooms, home offices, and older homes without ductwork. We install single-zone and multi-zone systems throughout the Inland Empire.",
        "sections": [
            ("When a mini-split is the right call", [
                "ADU or garage conversion that needs its own heating and cooling",
                "Room addition that wasn't included in the original ductwork",
                "A bedroom or office that's always too hot or too cold",
                "Older home without ducts where retrofit ductwork is impractical",
                "Targeted comfort in a single zone instead of cooling the whole house",
            ]),
            ("What our mini-split install includes", [
                "Free in-home estimate and load calculation",
                "Outdoor condenser placement and mounting",
                "Indoor head units in chosen locations",
                "Refrigerant line set, drain line, and electrical",
                "Clean wall penetrations and proper line-set covers outside",
                "System startup, charge verification, and walk-through",
            ]),
            ("Brands we install", [
                "Mitsubishi, Daikin, LG, Fujitsu, Carrier, and other major brands",
                "Mini-split technology is dominated by Japanese manufacturers — we install the brands that actually last in this category",
            ]),
            ("10-year parts warranty + price match", [
                "Every new mini-split install includes a 10-year manufacturer parts warranty when properly registered",
                "We handle the warranty registration on installation day",
                "Bring a written estimate from another licensed contractor — we'll beat it on equivalent equipment",
            ]),
        ],
        "faqs": [
            ("How much does a mini-split cost installed?",
             "A single-zone mini-split installation typically runs $3,500 – $6,500 depending on capacity and complexity. Multi-zone systems cost more. We'll beat any written competitor quote on equivalent equipment."),
            ("Can a mini-split heat my home too?",
             "Yes — modern mini-splits are heat pumps and provide both heating and cooling from the same unit."),
            ("What does the warranty cover?",
             "A 10-year manufacturer parts warranty when we register it for you on install day. Covers the compressor and major internal components. Labor warranty is separate."),
        ],
    },
    {
        "slug": "maintenance-plans",
        "h1": "HVAC Maintenance Plans in Corona, CA",
        "title": "HVAC Maintenance Plans in Corona, CA | FlowProHVAC",
        "desc": "Affordable HVAC maintenance plans in Corona and the Inland Empire. Twice-yearly tune-ups, priority service, and repair discounts. Call (818) 625-4400.",
        "subtitle": "Two visits a year, priority booking, and a system that lasts longer and runs cheaper.",
        "intro": "Most HVAC failures we see are preventable. A neglected system loses efficiency every year and tends to break down at the worst possible time. A simple twice-a-year tune-up catches small issues early and adds years to the equipment's life.",
        "sections": [
            ("What's included in a tune-up visit", [
                "Inspect and clean the condenser coil",
                "Inspect the evaporator coil",
                "Check refrigerant charge and pressures",
                "Inspect electrical connections, capacitors, and contactors",
                "Check thermostat calibration",
                "Inspect and clean the burners (heating tune-up)",
                "Combustion analysis and CO check (heating tune-up)",
                "Inspect the heat exchanger for cracks",
                "Replace the air filter",
                "Verify temperature differential and airflow",
            ]),
            ("Why a maintenance plan pays for itself", [
                "Catches small problems before they become breakdowns",
                "Keeps efficiency high — neglected systems use 10 – 25% more electricity",
                "Extends equipment life by years",
                "Required by most manufacturer warranties",
                "Plan members get priority scheduling and discounts on any repairs",
            ]),
        ],
        "faqs": [
            ("How much does a maintenance plan cost?",
             "Plans typically run around $15 – $25 per month or $180 – $250 per year per system, depending on what's included. Ask us for current pricing in your area."),
            ("How often should HVAC be serviced?",
             "Twice a year — once before cooling season (spring) and once before heating season (fall)."),
        ],
    },
    {
        "slug": "indoor-air-quality",
        "h1": "Indoor Air Quality Services in Corona, CA",
        "title": "Indoor Air Quality in Corona, CA | FlowProHVAC",
        "desc": "Improve the air your family breathes. Whole-home filtration, UV lights, duct sealing, and humidity control in Corona and the Inland Empire. Call (818) 625-4400.",
        "subtitle": "Whole-home solutions for allergies, dust, and the dry Inland Empire climate.",
        "intro": "Indoor air can be 2 – 5 times worse than outdoor air, and the Inland Empire's dust, allergens, and wildfire smoke don't help. We help homeowners improve filtration, kill mold and bacteria, control humidity, and seal duct leaks that pull contaminants into the system.",
        "sections": [
            ("Indoor air quality services we offer", [
                "High-MERV media filter cabinets",
                "HEPA-grade whole-home filtration",
                "UV air purification (kills mold and bacteria inside the air handler)",
                "Whole-home humidifiers and dehumidifiers",
                "Duct sealing and duct cleaning",
                "Fresh-air ventilation systems (ERV/HRV)",
            ]),
            ("Signs you have an indoor air quality problem", [
                "Excessive dust returning quickly after cleaning",
                "Allergy or asthma symptoms that worsen indoors",
                "Musty or stale smells",
                "Rooms with very different humidity levels",
                "Visible mold around vents or in the air handler",
            ]),
        ],
        "faqs": [
            ("Do I need duct cleaning?",
             "Duct cleaning isn't necessary for most homes. It is worth doing if you've had construction, smoke damage, rodents in the ducts, or visible mold. We'll tell you honestly if your system needs it."),
            ("What MERV rating should I use?",
             "MERV 11 – 13 is the sweet spot for most homes — good filtration without restricting airflow. Going higher requires a system designed for it."),
        ],
    },
    {
        "slug": "commercial-hvac",
        "h1": "Commercial HVAC in Corona & Southern California",
        "title": "Commercial HVAC in Corona, CA | American Brands, 10-Yr Warranty | FlowProHVAC",
        "desc": "Commercial HVAC service, repair, and installation in Corona and throughout California. Offices, retail, light industrial. American brand equipment with 10-year parts warranty. We'll beat any written quote. Call (818) 625-4400.",
        "subtitle": "Service, repair, and installation for offices, retail, light industrial, and multi-tenant buildings.",
        "intro": "Commercial HVAC downtime costs you customers, employees, and tenants. We've been the go-to HVAC partner for property managers and small business owners across Southern California for over 30 years — and we travel statewide for larger commercial projects.",
        "sections": [
            ("Commercial systems we work on", [
                "Rooftop package units (RTUs)",
                "Split systems and VRF/VRV systems",
                "Mini-splits and multi-zone ductless",
                "Walk-in cooler and freezer support equipment",
                "Make-up air units",
                "Server room and IT closet cooling",
            ]),
            ("Who we work with", [
                "Property management companies",
                "Retail tenants and shopping centers",
                "Restaurants and quick-serve food",
                "Medical and dental offices",
                "Light industrial and warehouses",
            ]),
            ("Commercial services", [
                "Same-day priority commercial HVAC repair during business hours",
                "Planned preventative maintenance contracts",
                "New rooftop unit installations and replacements",
                "Tenant improvement HVAC builds",
            ]),
            ("American brand equipment, 10-year parts warranty", [
                "We install top American brands — Carrier, Trane, Lennox, American Standard, Rheem",
                "Every new commercial install includes a 10-year manufacturer parts warranty",
                "Bring us a written estimate from a licensed competitor — we'll beat it on equivalent equipment",
            ]),
        ],
        "faqs": [
            ("Do you offer commercial maintenance contracts?",
             "Yes. We do quarterly, semi-annual, and annual planned maintenance contracts customized to your equipment and operating hours."),
            ("Do you do statewide commercial work?",
             "Yes — we travel for commercial installs and major service across California."),
            ("What brands do you install on commercial jobs?",
             "Top American brands — Carrier, Trane, Lennox, American Standard, and Rheem. Every new install includes a 10-year manufacturer parts warranty."),
            ("Will you beat another HVAC bid?",
             "Yes — bring us a written, itemized estimate from a licensed California HVAC contractor for equivalent equipment and we'll beat it."),
        ],
    },
    {
        "slug": "emergency-hvac",
        "h1": "Same-Day HVAC Repair in Corona, CA",
        "title": "Same-Day HVAC Repair in Corona, CA | FlowProHVAC",
        "desc": "Fast same-day HVAC repair in Corona and the Inland Empire. Priority response during business hours. 30+ years experience. Licensed & insured. We'll beat any written estimate. Call (818) 625-4400.",
        "subtitle": "Fast priority response during business hours. Most repairs done the same day we get the call.",
        "intro": "When your AC quits in a heatwave or your furnace dies in a cold snap, you need a real technician at your door fast — not next week. We prioritize urgent repair calls during our business hours and most are diagnosed and fixed the same day. And if you have a written estimate from another HVAC company, bring it — we'll beat it.",
        "sections": [
            ("When to call us right away", [
                "No cooling during high heat",
                "No heat in cold weather",
                "Burning smell from the system",
                "Suspected gas leak (also call your gas company immediately)",
                "Carbon monoxide detector going off",
                "Water leaking heavily from the system",
                "Frozen pipes or coils",
                "System making loud unusual noises",
            ]),
            ("How our priority repair calls work", [
                "Call us at (818) 625-4400 as early as possible — first calls of the day get the fastest response",
                "A real person picks up — usually the technician who'll be on the job",
                "We give you a realistic arrival window, not a vague 'sometime today'",
                "We arrive with the truck stocked for the most common repairs",
                "Upfront pricing — we tell you the cost before we start any work",
                "If you have a written estimate from another company, we'll beat it",
            ]),
            ("Our hours", [
                "Monday through Saturday, 7 AM to 7 PM",
                "Outside of those hours we don't take service calls — we believe in doing the job right with a rested crew",
                "Closed Sundays",
            ]),
        ],
        "faqs": [
            ("Can you come out today?",
             "Most days during cooling and heating seasons, yes — especially if you call early in the day. We prioritize urgent calls and most are completed the same day."),
            ("Do you charge extra for same-day or priority service?",
             "No. Same-day service is part of how we work — no rush fees. Standard service-call pricing applies and we tell you the cost before we start."),
            ("Do you do 24/7 emergency service?",
             "No, not currently. Our hours are Monday through Saturday, 7 AM to 7 PM. We prioritize urgent calls during business hours so most repairs are still completed the same day you call."),
            ("How fast can you get here?",
             "Response times depend on where you are and what's happening in our schedule. We give you a realistic ETA when you call — never a promise we can't keep."),
            ("Will you beat another HVAC company's price?",
             "Yes. Bring us a written estimate from any licensed local competitor and we'll beat it. Quality of work doesn't change — only the price."),
        ],
    },
]


def render_faq(faqs):
    items = ""
    for q, a in faqs:
        items += f"<details><summary>{q}</summary><p>{a}</p></details>\n"
    return f'<section class="section bg-gray"><div class="container"><div class="section-head"><h2>Frequently Asked Questions</h2></div><div class="faq">{items}</div></div></section>'


def faq_schema(faqs):
    import json
    obj = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q,
             "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in faqs
        ],
    }
    return f'<script type="application/ld+json">{json.dumps(obj)}</script>'


def render_service_page(svc):
    url = f"{SITE}/services/{svc['slug']}.html"

    sections_html = ""
    for heading, items in svc["sections"]:
        sections_html += f"<h2>{heading}</h2><ul>"
        for it in items:
            sections_html += f"<li>{it}</li>"
        sections_html += "</ul>"

    bc_items = [("Home", f"{SITE}/"), ("Services", f"{SITE}/#services"), (svc["h1"], url)]
    schemas = (
        breadcrumb_schema(bc_items)
        + service_schema(svc["h1"], svc["desc"], url)
        + faq_schema(svc["faqs"])
    )

    bc_render = [
        ("Home", "/"),
        ("Services", "/#services"),
        (svc["h1"].split(" in ")[0], None),  # short label, no link
    ]

    body = HEAD.format(
        title=svc["title"], description=svc["desc"], canonical=url, schema=schemas
    )
    body += HEADER
    body += page_hero(svc["h1"], svc["subtitle"], bc_render)
    body += f"""
<section class="section">
  <div class="container-sm prose">
    <p style="font-size:1.1rem; color:var(--text);">{svc["intro"]}</p>
    {sections_html}
    <h2>Service area</h2>
    <p>We serve Corona and the surrounding western Inland Empire — Norco, Eastvale, Chino Hills, Riverside, Ontario, and nearby cities. Not sure if you're in our area? <a href="/contact.html">Reach out</a>.</p>
  </div>
</section>
"""
    body += render_faq(svc["faqs"])
    body += FINAL_CTA
    body += FOOTER
    return body


# ---------------- CITY PAGES ----------------

CITIES = [
    {
        "slug": "corona-ca", "name": "Corona", "zip": "92882",
        "intro": "Corona is home base. We've been working on HVAC systems in Corona for over 30 years — from the older neighborhoods near downtown to the newer developments off Foothill, Green River, and Eagle Glen. We know the climate, we know the housing stock, and we know what tends to go wrong.",
        "neighborhoods": ["Sierra Del Oro", "South Corona", "Eagle Glen", "Cresta Verde", "Coronita", "Dos Lagos", "Green River", "Temescal Valley"],
    },
    {
        "slug": "norco-ca", "name": "Norco", "zip": "92860",
        "intro": "Norco's a quick drive from our shop and a city we've served for decades. Larger lots, horse properties, and detached buildings mean we frequently install mini-splits for tack rooms, casitas, and converted spaces alongside the main home's central system.",
        "neighborhoods": ["Downtown Norco", "Norco Hills", "North Norco", "Hidden Valley"],
    },
    {
        "slug": "eastvale-ca", "name": "Eastvale", "zip": "92880",
        "intro": "Eastvale is one of the newer cities in the Inland Empire and most homes are large two-story builds from the early 2000s onward. Two-story zoning issues, attic temperatures over 130°F in summer, and original-builder equipment that's now hitting end of life — we see all of it weekly.",
        "neighborhoods": ["The Ranch", "Roosevelt", "Citrus", "Eastvale Gateway"],
    },
    {
        "slug": "chino-hills-ca", "name": "Chino Hills", "zip": "91709",
        "intro": "Chino Hills has a mix of older custom homes and newer tract communities, and we serve both. Steep lots and elevation changes mean some homes deal with airflow imbalance — bedrooms hotter than the living room — and we help homeowners solve it with zoning, duct work, or targeted mini-splits.",
        "neighborhoods": ["Carbon Canyon", "Los Serranos", "Soquel Canyon", "Sleepy Hollow"],
    },
    {
        "slug": "riverside-ca", "name": "Riverside", "zip": "92501",
        "intro": "Riverside is one of our most-served cities, especially the western neighborhoods. Older homes in Wood Streets and Mission Inn area, plus newer construction in La Sierra and Orangecrest. Each comes with its own HVAC quirks and we've worked on all of them.",
        "neighborhoods": ["Wood Streets", "Mission Inn", "Canyon Crest", "La Sierra", "Orangecrest", "Arlington"],
    },
    {
        "slug": "ontario-ca", "name": "Ontario", "zip": "91761",
        "intro": "Ontario has a strong mix of residential and commercial work. Newer master-planned communities like Ontario Ranch on the south side, established neighborhoods to the north, and a major commercial corridor where we handle a lot of light commercial rooftop unit service.",
        "neighborhoods": ["Ontario Ranch", "Downtown Ontario", "North Ontario", "Westwind"],
    },
]


def render_city_page(c):
    url = f"{SITE}/service-areas/{c['slug']}.html"
    title = f"HVAC in {c['name']}, CA | Carrier, Trane, Lennox | 10-Yr Warranty | FlowProHVAC"
    desc = (f"Family-owned HVAC contractor serving {c['name']}, CA since 1994. AC and "
            f"furnace repair, installation of top American brands (Carrier, Trane, Lennox) "
            f"with 10-year parts warranty. We'll beat any written estimate. "
            f"Call (818) 625-4400.")
    h1 = f"HVAC Services in {c['name']}, CA"
    subtitle = (f"Repair, installation, and maintenance from a licensed local contractor "
                f"with 30+ years of experience in {c['name']} and the Inland Empire. "
                f"American brands, 10-year warranty, we'll beat any written quote.")

    bc_items = [("Home", f"{SITE}/"), ("Service Areas", f"{SITE}/#service-areas"), (h1, url)]
    schemas = breadcrumb_schema(bc_items)

    bc_render = [("Home", "/"), ("Service Areas", "/#service-areas"), (c["name"], None)]

    neighborhoods_html = ", ".join(c["neighborhoods"])

    body = HEAD.format(title=title, description=desc, canonical=url, schema=schemas)
    body += HEADER
    body += page_hero(h1, subtitle, bc_render)
    body += f"""
<section class="section">
  <div class="container-sm prose">
    <p style="font-size:1.1rem;">{c["intro"]}</p>

    <h2>HVAC services we provide in {c["name"]}</h2>
    <ul>
      <li><a href="/services/ac-repair.html">AC repair</a> — fast, honest diagnosis and repair</li>
      <li><a href="/services/ac-installation.html">AC installation</a> — properly sized, properly installed</li>
      <li><a href="/services/furnace-repair.html">Furnace repair</a> — safe and quick</li>
      <li><a href="/services/furnace-installation.html">Furnace installation</a> — high-efficiency replacements</li>
      <li><a href="/services/mini-split-installation.html">Mini-split installation</a> — for ADUs, additions, and zoned cooling</li>
      <li><a href="/services/maintenance-plans.html">Maintenance plans</a> — twice-yearly tune-ups</li>
      <li><a href="/services/indoor-air-quality.html">Indoor air quality</a> — filtration, UV, humidity</li>
      <li><a href="/services/commercial-hvac.html">Commercial HVAC</a> — for {c["name"]} businesses and property managers</li>
      <li><a href="/services/emergency-hvac.html">Same-day priority repair</a></li>
    </ul>

    <h2>Neighborhoods we serve in {c["name"]}</h2>
    <p>{neighborhoods_html}, and surrounding areas of {c["name"]}, CA {c["zip"]}.</p>

    <h2>Why {c["name"]} homeowners choose FlowProHVAC</h2>
    <ul>
      <li><strong>Top American brand equipment</strong> — we install Carrier, Trane, Lennox, American Standard, and Rheem</li>
      <li><strong>10-year manufacturer parts warranty</strong> on every new installation</li>
      <li><strong>We'll beat any written estimate</strong> from a licensed competitor on equivalent equipment</li>
      <li>Family-owned and locally based — we're not a national chain</li>
      <li>30+ years of HVAC experience across the Inland Empire</li>
      <li>Licensed, bonded, and insured in California (CSLB #1142668)</li>
      <li>Real technicians answering the phone, not call-center scripts</li>
      <li>Honest pricing — we tell you the cost before any work begins</li>
      <li>Same-day priority service during business hours (Mon–Sat, 7 AM – 7 PM)</li>
    </ul>

    <h2>Schedule HVAC service in {c["name"]}</h2>
    <p>Call us at <a href="{PHONE_HREF}">{PHONE}</a> or <a href="/contact.html">request an estimate online</a>. We respond quickly and we'll give you a realistic appointment window — not a vague "sometime today."</p>
  </div>
</section>
"""
    body += FINAL_CTA
    body += FOOTER
    return body


# ---------------- WRITE ----------------

def main():
    services_dir = ROOT / "services"
    cities_dir = ROOT / "service-areas"
    services_dir.mkdir(exist_ok=True)
    cities_dir.mkdir(exist_ok=True)

    for svc in SERVICES:
        path = services_dir / f"{svc['slug']}.html"
        path.write_text(render_service_page(svc))
        print(f"wrote {path}")

    for c in CITIES:
        path = cities_dir / f"{c['slug']}.html"
        path.write_text(render_city_page(c))
        print(f"wrote {path}")


if __name__ == "__main__":
    main()
