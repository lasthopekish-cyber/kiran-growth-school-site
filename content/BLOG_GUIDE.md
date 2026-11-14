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

- `category` must be one of: `web` (website design), `solar`, `real-estate`, `education`, `bakery` (sweets & bakery), `video` (video editing, AI video), `ai`, `growth` (Meta/Google Ads, general).
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
7. **Internal links (3+):** link to one service page (`/services/website-development/`, `/services/meta-ads/`, `/services/google-ads/`, `/services/video-editing/`, `/services/ai-video-production/`, `/services/ai-avatar-videos/`, `/services/social-media-management/`, `/services/ai-automation/`), one industry page (`/solar-marketing-agency/`, `/real-estate-marketing-agency/`, `/education-marketing-agency/`, `/sweets-bakery-marketing-agency/`), one city page and, where relevant, an existing blog post.
   - City slugs: `delhi`, `delhi-ncr`, `noida`, `gurugram`, `ghaziabad`, `bhopal`, `rewa`, `satna`.
   - Every city has `/locations/<city>/`, `/locations/<city>/website-designer/` and `/locations/<city>/solar-marketing/`. **Website design posts must link to the city's `website-designer` page; solar posts must link to the city's `solar-marketing` page.** Use the target keyword as anchor text once (e.g. `[website designer in Bhopal](/locations/bhopal/website-designer/)`).
8. **End with a soft call to action**: call or WhatsApp +91 93998 51765 (write the number in full so it shows in search snippets).
9. Indian English, rupee symbol (₹), lakh/crore where natural.
10. **SEO basics:** target keyword in the title (near the start), in the description, in the first 100 words, in one `##` heading and in the slug. Mention the city naturally 3 to 6 times. Answer the searcher's question in the TL;DR.

## Daily plan

Three posts a day, taken from `content/blog-queue.md`: one website design (slot A), one solar (slot B), one rotating real estate / education / bakery / video / ads (slot C). Priority keywords to rank for, in every city (Delhi, Delhi NCR, Noida, Gurugram, Ghaziabad, Bhopal, Rewa, Satna):

- **Top priority:** best website designer / website developer / website design company in <city>; solar marketing agency / solar leads / solar company marketing in <city>
- **Also:** real estate marketing, education / coaching marketing, sweets & bakery marketing, video editing, AI video making, Meta Ads agency, Google Ads agency in <city>

## Topic bank (for refilling the queue)

**Website design**
- Website cost, website designer checklists, local SEO, redesigns, industry websites (solar, real estate, coaching, bakery, clinic) per city
- Website vs Instagram vs Justdial, Google Business Profile + website, website speed and mobile-first

**Education, bakery, video**
- Admission-season campaigns, coaching institute reels, school ads by city
- Festival campaigns for sweet shops, cake shop WhatsApp ordering, bakery Google Maps
- Video editing for reels and ads, AI video making, AI avatar videos by industry


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
