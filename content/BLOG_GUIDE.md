# Blog guide (for humans and the daily scheduled blog task)

Every post is one Markdown file in `content/blog/`, named `<slug>.md`. The slug becomes the URL: `/blog/<slug>/`.

## Front matter template

```
---
title: Clear, specific title with the main keyword (55-70 characters ideal)
description: One or two sentences, 140-160 characters, with the keyword and city where natural.
date: 2026-11-12
order: 1
category: solar
tags: comma, separated, keywords, city names
tldr: A 2-3 sentence direct answer to the main question. AI search tools often quote this.
faq: Question one? || Short, direct answer.
faq: Question two? || Short, direct answer.
faq: Question three? || Short, direct answer.
---
```

- `category` must be one of: `solar`, `real-estate`, `ai`, `growth`.
- `order` sorts posts published on the same date (higher = shown first).
- No colons inside `title`, `description` or `tldr` values except the first one after the key (the parser splits on the first colon only, so colons later in the line are fine).
- Body: Markdown with `##` and `###` headings, lists and tables. Do not repeat the title as an H1.

## Rules

1. **Accuracy first.** Check facts that change (PM Surya Ghar subsidy and installation counts, state top-ups, RERA rules, ad platform policies) with a web search on the day of writing, and say "as of <month year>" for numbers that move. Point readers to official sources (pmsuryaghar.gov.in, state RERA sites, MNRE).
2. **No made-up results.** Never invent client names, case studies, testimonials, lead costs or "we generated X leads" claims. Use ranges and conditions, or say results vary.
3. **No legal or financial advice.** For RERA, tax or loan topics, add "general information, not legal advice".
4. **Never say "free solar panels".** Say "subsidy up to ₹78,000" (or the current cap).
5. **Unique topic.** Before writing, list `content/blog/` and do not repeat a topic or slug that already exists. A new angle on the same theme is fine (different city, different buyer, different channel).
6. **Length:** 900-1,400 words. Short paragraphs, at least one table or checklist, a TL;DR, and 3 FAQs.
7. **Internal links (3+):** link to one service page (`/services/meta-ads/`, `/services/google-ads/`, `/services/website-design/`, `/services/ai-video-production/`, `/services/ai-avatar-videos/`, `/services/ai-automation/`), one industry page (`/solar-marketing-agency/` or `/real-estate-marketing-agency/`), one city page (`/locations/delhi/`, `/locations/delhi-ncr/`, `/locations/gurugram/`, `/locations/ghaziabad/`, `/locations/bhopal/`, `/locations/rewa/`, `/locations/satna/`) and, where relevant, an existing blog post.
8. **End with a soft call to action** to WhatsApp +91 93998 51765.
9. Indian English, rupee symbol (₹), lakh/crore where natural.

## Topic bank (rotate; one solar/PM Surya Ghar + one real estate per day)

**Solar / PM Surya Ghar**
- PM Surya Ghar application steps explained for homeowners in a specific city/DISCOM
- Net metering process with BSES / Tata Power-DDL / DHBVN / PVVNL / MP DISCOMs
- 1 kW vs 2 kW vs 3 kW: which size and how much subsidy
- Solar loans under PM Surya Ghar: how installers can use them in sales
- Housing society (RWA) rooftop solar: how to sell to committees
- Commercial and industrial rooftop solar marketing (factories, schools, hospitals)
- PM-KUSUM solar pumps: marketing to farmers in MP
- Solar seasonality: planning ad budgets for summer peaks
- Google Business Profile for solar installers
- Solar referral programmes and WhatsApp campaigns
- Objection handling scripts: monsoon, maintenance, roof leaks, payback
- State top-ups (UP, Haryana, Delhi, MP): check current status before writing

**Real estate**
- Meta Ads for plots and farmhouses
- Google Ads for new launches in a specific corridor
- Ghaziabad / Raj Nagar Extension / Indirapuram buyer journeys
- Bhopal Kolar Road / Narmadapuram Road / Ayodhya Bypass markets
- NRI real estate marketing for NCR and MP projects
- Channel partner marketing systems and approved creative kits
- Site-visit conversion: follow-up scripts and automation
- Real estate video marketing: walkthroughs, drone, AI avatars
- Real estate CRM and lead scoring
- Pre-launch vs launch vs ready-to-move campaign differences (RERA-compliant)
- Commercial shops and office space marketing

**AI and growth (occasional)**
- AI avatar videos, AI ad creatives, AI automation workflows, website and SEO for AI search

## Publish

```bash
python3 build/build.py
git add -A && git commit -m "Blog: <titles>" && git push origin main
```
