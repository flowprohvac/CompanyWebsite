# FlowProHVAC Website — Redesign + SEO Pages

This is the new site. Replace the contents of the `flowprohvac/CompanyWebsite` repo with this folder, push to `main`, and Cloudflare Pages will pick it up.

## What's in this folder

```
.
├── index.html                # Redesigned homepage
├── about.html
├── contact.html
├── google21c5c1945cfd3840.html  # Existing Google verification file (kept)
├── sitemap.xml
├── robots.txt
├── assets/
│   ├── styles.css            # Shared stylesheet
│   └── main.js               # Shared script (mobile menu + form UX)
├── services/                 # 9 service landing pages
│   ├── ac-repair.html
│   ├── ac-installation.html
│   ├── furnace-repair.html
│   ├── furnace-installation.html
│   ├── mini-split-installation.html
│   ├── maintenance-plans.html
│   ├── indoor-air-quality.html
│   ├── commercial-hvac.html
│   └── emergency-hvac.html
├── service-areas/            # 6 local SEO city pages
│   ├── corona-ca.html
│   ├── norco-ca.html
│   ├── eastvale-ca.html
│   ├── chino-hills-ca.html
│   ├── riverside-ca.html
│   └── ontario-ca.html
├── _generate.py              # Script that built service + city pages from templates
├── GBP-PLAYBOOK.md           # Google Business Profile optimization plan
└── README.md                 # This file
```

## Why this is set up this way

The old site was a single-page HTML file. It looks fine, but Google has nothing to rank — no separate URLs for "AC repair Corona" or "furnace repair Eastvale". Service-area HVAC is hyper-local: you need one page per service AND one page per city you want to show up in. That's why this has 9 service pages × cross-linked to 6 city pages.

Other improvements baked in:

- **Schema.org structured data** on every page (LocalBusiness, Service, FAQPage, BreadcrumbList). This is what makes you eligible for rich results and the Map Pack.
- **Open Graph tags** so Facebook/Messenger/Slack/iMessage previews look right.
- **Real internal linking** — every page links to relevant services and cities. This is critical for SEO.
- **Click-to-call** phone numbers everywhere, including a sticky mobile bottom bar.
- **Mobile-first** — header collapses to a hamburger, sticky "Call" button at bottom of screen on phones.
- **Faster** — single shared stylesheet instead of inline styles on every page.
- **Real meta titles + descriptions** on each page — these are what shows up in Google search results.

## REQUIRED: Drop your real logo files into these exact paths

The site's header and browser tab reference these three image files. The site will work without them (it just won't show a logo or favicon until they're added). Save **your actual logo PNG files** at these paths in the repo:

| Save as this path | What it is | Recommended size |
|---|---|---|
| `assets/logo.png` | Full horizontal logo with wordmark + tagline (used in desktop header) | 1100 × 320 px, transparent background |
| `assets/logo-icon.png` | F-mark only (used in mobile header) | 240 × 240 px, transparent background |
| `favicon.png` | Browser tab icon — same as logo-icon but small | 32 × 32 px (or 64 × 64) |
| `og-image.jpg` | Social-share preview card (Facebook, iMessage, Slack previews) | 1200 × 630 px |

**Quick how-to:** export each from your designer's source file at the sizes above. Drop the four files into the repo root and `assets/` folder as shown. Commit and push — Cloudflare deploys in 1–2 minutes and the logo + favicon will appear automatically.

There are some old reconstructed SVG files in `assets/` (logo-horizontal.svg, logo-icon.svg, etc.) that nothing references anymore — safe to delete after you add your real PNG files.

---

## Things YOU need to fill in before going live

Search the codebase for `1142668` and `<em>` placeholders. Specifically:

1. **CSLB License number** — appears in the footer of every page. Find and replace:
   - Search: `CSLB License #: 1142668`
   - Replace with: `CSLB License #: 1234567` (your actual number)

2. **Phone number area code (818)** — that's a Los Angeles area code on a Corona business. Either this is intentional (cell carried over from before) or worth swapping for a 951 (Corona) number. Whichever you decide, **be consistent everywhere** — website, GBP, all directories, business cards. If you change it, search the codebase for `8186254400` and `(818) 625-4400` and replace both formats.

3. **OG image** — the homepage references `https://flowprohvac.com/og-image.jpg`. Create a 1200×630 image (logo on brand background) and upload it to the repo root.

4. **Google Business Profile share link** on the homepage points to `https://share.google/jjxlaLvD2PdI9GatL`. Confirm this still resolves; otherwise replace with the direct GBP review link.

5. **Formspree form** — the contact form posts to `https://formspree.io/f/myzeyorb` (your existing endpoint). Test once you push live to make sure submissions still land in your inbox.

6. **Testimonials** — currently using the same fake-looking ones from the old site (first-name + initial). Replace with real Google review embeds **as soon as you have 10+ Google reviews**. See GBP-PLAYBOOK.md for how to get there.

## Deployment

Cloudflare Pages picks up the repo automatically. Steps:

```bash
# 1. Replace your local copy of the repo
cd path/to/CompanyWebsite
rm -rf *               # be careful — keep your .git folder
# Copy everything from this flowpro-site folder into the repo root

# 2. Commit & push
git add -A
git commit -m "Redesign: multi-page site with service + city pages, schema markup, mobile UX"
git push origin main

# Cloudflare will auto-build and deploy in 1-2 minutes
```

If you'd rather migrate one page at a time, the new `index.html` works standalone — you can push just that first, then add the `services/` and `service-areas/` folders.

## Post-deploy checklist

1. **Test it.** Open the site on your phone. Tap the phone number. Tap "Get a Free Estimate". Submit the form with a test message.
2. **Submit sitemap to Google Search Console.**
   - https://search.google.com/search-console
   - Add property → flowprohvac.com (already verified via the `google21c...` file)
   - Sitemaps → submit `sitemap.xml`
3. **Submit to Bing Webmaster Tools** (https://www.bing.com/webmasters).
4. **Test schema** with https://validator.schema.org/ — paste a URL and confirm no errors.
5. **Test mobile** with https://search.google.com/test/mobile-friendly.
6. **Test PageSpeed** with https://pagespeed.web.dev/ — should be 85+ on mobile.
7. **Open the GBP playbook (`GBP-PLAYBOOK.md`)** and start working through it.

## Regenerating service / city pages

If you want to edit content for all service pages at once (or add a new city), edit the data in `_generate.py` and re-run:

```bash
python3 _generate.py
```

It overwrites everything under `services/` and `service-areas/`. The homepage, about, and contact pages are hand-written and not touched.

## What's next (beyond the website)

This site fixes the foundation. The work that drives leads from here:

1. **Reviews + GBP** — see `GBP-PLAYBOOK.md`
2. **Google Local Service Ads** (Google Guaranteed) once you have 10+ reviews
3. **Real photos** of jobs in progress and your actual work truck — swap out the placeholder hero image at `/assets/images/truck-wrap.png` once you have real photos
4. **Truck wrap + yard signs** — free local impressions
5. **Maintenance plans** as a recurring revenue product
6. **Get the under-the-table employees on payroll + workers' comp** before scaling lead volume

## Current positioning (what the site emphasizes)

The site is positioned around three differentiators — these appear on the homepage, install pages, and city pages:

1. **Top American brands** — Carrier, Trane, Lennox, American Standard, Rheem
2. **10-year manufacturer parts warranty** on every new installation
3. **We'll beat any written estimate** from a licensed competitor on equivalent equipment

24/7 service has been removed throughout the site. The emergency-hvac page is now framed as "Same-Day Repair" — fast priority response during business hours (Mon–Sat, 7 AM – 7 PM).
