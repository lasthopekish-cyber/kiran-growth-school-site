#!/usr/bin/env python3
"""Static site builder for kirangrowthschool.online.

Usage:  python3 build/build.py
Reads build/data.py and content/blog/*.md, writes HTML pages, sitemap.xml,
robots.txt, llms.txt and blog/feed.xml into the repo root.
Blog posts with a future `date:` are skipped until that date (IST).
"""
import json, os, re, sys, html, datetime, urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "build"))
from data import SITE, SERVICES, INDUSTRIES, CITIES, COURSES, HOME_FAQ, OTHER_INDUSTRIES  # noqa: E402

try:
    import markdown  # pip install markdown
except ImportError:
    sys.exit("Missing dependency: pip install markdown")

IST = datetime.timezone(datetime.timedelta(hours=5, minutes=30))
TODAY = datetime.datetime.now(IST).date()
ORIG = json.load(open(ROOT / "build" / "svgs_orig.json"))
U = SITE["url"]
E = html.escape

# ------------------------------------------------------------------ icons
def _ico(body, sw="2.2"):
    return f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{body}</svg>'

I = {
    "brand": ORIG["d1c0a6"], "phone": ORIG["169f0e"], "wa": ORIG["220ef0"], "burger": ORIG["46eca8"],
    "check": ORIG["72aa37"], "tick": ORIG["02eeb5"], "google": ORIG["003ea0"], "meta": ORIG["5cc34a"],
    "video": ORIG["4f84f7"], "insta": ORIG["8174e2"], "linkedin": ORIG["106a91"], "mail": ORIG["def1ba"], "clock": ORIG["68dfee"],
    "web": _ico('<rect x="2.5" y="4" width="19" height="15" rx="3"/><path d="M2.5 8.5h19M6 6.3h.01M8.5 6.3h.01M7 12.5h6M7 15.5h10"/>'),
    "avatar": _ico('<circle cx="12" cy="8.5" r="3.6"/><path d="M5 20c.9-3.6 3.7-5.5 7-5.5s6.1 1.9 7 5.5"/><path d="M18.5 3.5l.7 1.6 1.6.7-1.6.7-.7 1.6-.7-1.6-1.6-.7 1.6-.7z" fill="currentColor"/>'),
    "bolt": _ico('<path d="M13 2.5L4.5 13.5H11l-1 8 8.5-11H12z"/>'),
    "sun": _ico('<circle cx="12" cy="12" r="4.2"/><path d="M12 2v2.5M12 19.5V22M2 12h2.5M19.5 12H22M4.9 4.9l1.8 1.8M17.3 17.3l1.8 1.8M4.9 19.1l1.8-1.8M17.3 6.7l1.8-1.8"/>'),
    "building": _ico('<path d="M4 21V5.5L12 3v18M12 8.5l8 2.5V21M2.5 21h19M7 8h2M7 11.5h2M7 15h2M15 13h2M15 16.5h2"/>'),
    "pin": _ico('<path d="M12 21s-7-6.2-7-11.5A7 7 0 0 1 19 9.5C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/>'),
    "arrow": _ico('<path d="M5 12h14M13 6l6 6-6 6"/>'),
    "book": _ico('<path d="M4 4.5A2.5 2.5 0 0 1 6.5 2H20v17H6.5A2.5 2.5 0 0 0 4 21.5zM4 21.5A2.5 2.5 0 0 1 6.5 19H20"/>'),
    "chart": _ico('<path d="M3 21h18M6 17V11M11 17V6M16 17v-4M21 17V8"/>'),
}

def wa(msg):
    return f"https://wa.me/{SITE['wa']}?text=" + urllib.parse.quote(msg)

def wa_btn(msg, label, cls="b-wa", extra=""):
    return f'<a class="btn {cls}" href="{E(wa(msg))}" target="_blank" rel="noopener"{extra}>{I["wa"]}{label}</a>'

# ------------------------------------------------------------------ layout
NAV = [("/services/", "Services"), ("/solar-marketing-agency/", "Solar"), ("/real-estate-marketing-agency/", "Real Estate"),
       ("/locations/", "Locations"), ("/blog/", "Blog")]

def header(active):
    links = "".join(f'<a href="{h}"{" class=\"on\"" if active == h else ""}>{t}</a>' for h, t in NAV)
    links += f'<a class="course-tab{" on" if active == "/courses/" else ""}" href="/courses/">Courses</a>'
    mob = "".join(f'<a href="{h}">{t}</a>' for h, t in NAV) + '<a href="/courses/">Courses</a><a href="/about/">About</a><a href="/contact/">Contact</a>' + f'<a href="tel:{SITE["phone_e164"]}">Call {SITE["phone"]}</a>'
    tick_items = [("#ffc626", "Performance marketing for solar & real estate"), ("#1fd39b", "Meta Ads · Google Ads · Websites"),
                  ("#ff6fb5", "AI videos · AI avatars · AI automation"), ("#5ec8ff", "Delhi NCR · Gurugram · Ghaziabad · Bhopal · Rewa · Satna"),
                  ("#ff5a36", f"WhatsApp {SITE['phone']}")]
    tick = "".join(f'<span><span class="dot" style="display:inline-block;width:10px;height:10px;border-radius:50%;background:{c}"></span>{E(t)}</span>' for c, t in tick_items) * 2
    return f'''<div class="ticker" aria-hidden="true"><div class="row">{tick}</div></div>
<header class="nav">
  <div class="wrap">
    <a class="brand" href="/" aria-label="Kiran Growth School home">{I["brand"]}<div><b>Kiran Growth School</b><small>PERFORMANCE MARKETING AGENCY</small></div></a>
    <nav class="menu" aria-label="Main">{links}</nav>
    <a class="callpill" href="tel:{SITE["phone_e164"]}">{I["phone"]}{SITE["phone"]}</a>
    {wa_btn("Hi Kiran Growth School, I have an enquiry.", "<span>WhatsApp us</span>")}
    <button class="burger" id="burger" type="button" aria-label="Open menu" aria-expanded="false">{I["burger"]}</button>
  </div>
  <div class="mob" id="mob"><div class="wrap">{mob}</div></div>
</header>'''

def footer():
    svc = "".join(f'<li><a href="/services/{s["slug"]}/">{E(s["name"])}</a></li>' for s in SERVICES)
    loc = "".join(f'<li><a href="/locations/{c["slug"]}/">{E(c["name"])}</a></li>' for c in CITIES)
    return f'''<footer>
  <div class="fstrip" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i><i></i></div>
  <div class="wrap">
    <div class="fcta"><h2>More leads for your solar or real estate business? Let's talk.</h2>{wa_btn("Hi Kiran Growth School, I want more leads for my business.", SITE["phone"])}</div>
    <div class="fcols">
      <div><a class="brand" href="/">{I["brand"]}<div><b>Kiran Growth School</b><small>PERFORMANCE MARKETING AGENCY</small></div></a>
        <p>Performance marketing agency for solar companies and real estate businesses: Meta Ads, Google Ads, websites, AI videos, AI avatar videos and AI automation. Founded by {SITE["founder"]}.</p>
        <div class="soc"><a href="{SITE["linkedin"]}" target="_blank" rel="noopener" style="color:var(--sky);display:inline-flex;align-items:center;gap:8px;padding:8px 12px;border-radius:12px;border:2px solid #4a4462;font-weight:800;font-size:.86rem;text-decoration:none">{I["linkedin"]}LinkedIn</a></div></div>
      <div style="--c:var(--sun)"><h4>Services</h4><ul>{svc}</ul></div>
      <div style="--c:var(--mint)"><h4>Company</h4><ul><li><a href="/about/">About us</a></li><li><a href="/contact/">Contact</a></li><li><a href="/solar-marketing-agency/">Solar marketing</a></li><li><a href="/real-estate-marketing-agency/">Real estate marketing</a></li><li><a href="/blog/">Blog</a></li><li><a href="/courses/">Courses</a></li></ul></div>
      <div style="--c:var(--pink)"><h4>Locations</h4><ul>{loc}</ul></div>
      <div style="--c:var(--sky)"><h4>Contact</h4><ul><li><a href="{E(wa("Hi Kiran Growth School, I have an enquiry."))}" target="_blank" rel="noopener">WhatsApp {SITE["phone"]}</a></li><li><a href="tel:{SITE["phone_e164"]}">Call {SITE["phone"]}</a></li><li style="color:#c9c4d8;font-weight:600;font-size:.95rem;overflow-wrap:anywhere">{SITE["email"]}</li><li style="color:#c9c4d8;font-weight:600;font-size:.95rem">{SITE["hours"]}</li></ul></div>
    </div>
    <div class="fbot"><span>© {TODAY.year} Kiran Growth School. All rights reserved.</span><span>Founded by {SITE["founder"]}</span></div>
  </div>
</footer>
<a class="fab" href="{E(wa("Hi Kiran Growth School, I have an enquiry."))}" target="_blank" rel="noopener" aria-label="Chat on WhatsApp">{I["wa"]}<span>Chat with us</span></a>'''

ORG_ID = U + "/#organization"
def org_schema():
    return {
        "@type": ["Organization", "ProfessionalService"], "@id": ORG_ID, "name": SITE["name"], "url": U + "/",
        "logo": U + "/assets/img/logo.png", "image": U + "/assets/img/og-default.jpg",
        "description": "Performance marketing agency for solar companies and real estate businesses: Meta Ads, Google Ads, website design, AI videos, AI avatar videos and AI automation.",
        "telephone": SITE["phone_e164"], "email": SITE["email"], "priceRange": "₹₹",
        "founder": {"@type": "Person", "name": SITE["founder"], "sameAs": [SITE["linkedin"]]},
        "areaServed": [{"@type": "City", "name": c["name"]} for c in CITIES if c["slug"] != "delhi-ncr"] + [{"@type": "Place", "name": "Delhi NCR"}, {"@type": "Country", "name": "India"}],
        "knowsAbout": ["Performance marketing", "Meta Ads", "Google Ads", "Solar lead generation", "PM Surya Ghar Muft Bijli Yojana", "Real estate marketing", "RERA-compliant advertising", "Website design", "AI video production", "AI avatar videos", "AI automation", "WhatsApp automation"],
        "contactPoint": {"@type": "ContactPoint", "telephone": SITE["phone_e164"], "contactType": "sales", "availableLanguage": ["English", "Hindi"]},
        "sameAs": [SITE["linkedin"]],
        "openingHours": "Mo-Sa 10:00-19:00",
    }

def crumbs_schema(items):
    return {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": U + h} for i, (h, n) in enumerate(items)]}

def faq_schema(faq):
    return {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}

def crumbs_html(items):
    out = []
    for i, (h, n) in enumerate(items):
        out.append(f'<a href="{h}">{E(n)}</a>' if i < len(items) - 1 else f'<span aria-current="page">{E(n)}</span>')
    return '<nav class="crumbs" aria-label="Breadcrumb">' + ' <span>/</span> '.join(out) + '</nav>'

def page(path, title, desc, body, active=None, schema=None, og_type="website", og_img="/assets/img/og-default.jpg", extra_head=""):
    graph = [org_schema(), {"@type": "WebSite", "@id": U + "/#website", "url": U + "/", "name": SITE["name"], "publisher": {"@id": ORG_ID}, "inLanguage": "en-IN"}]
    graph += schema or []
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False)
    verif = ""
    if path == "/" and SITE.get("google_verification"):
        verif += "\n" + f'<meta name="google-site-verification" content="{E(SITE["google_verification"])}">'
    if path == "/" and SITE.get("bing_verification"):
        verif += "\n" + f'<meta name="msvalidate.01" content="{E(SITE["bing_verification"])}">'
    full = f'''<!doctype html>
<html lang="en-IN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<link rel="canonical" href="{U}{path}">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="Kiran Growth School">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(desc)}">
<meta property="og:url" content="{U}{path}">
<meta property="og:image" content="{U}{og_img}">
<meta property="og:locale" content="en_IN">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#fbf6ec">
<meta name="geo.region" content="IN-DL">{verif}
<link rel="icon" href="/assets/img/favicon.svg" type="image/svg+xml">
<link rel="alternate" type="application/rss+xml" title="Kiran Growth School Blog" href="/blog/feed.xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Unbounded:wght@500;700;800;900&family=Figtree:wght@400;500;600;700;800&family=Space+Mono:wght@700&display=swap">
<link rel="stylesheet" href="/assets/css/site.css?v={TODAY:%Y%m%d}">
{extra_head}<script type="application/ld+json">{ld}</script>
</head>
<body>
{header(active)}
<main id="main">
{body}
</main>
{footer()}
<script src="/assets/js/site.js?v={TODAY:%Y%m%d}" defer></script>
</body>
</html>
'''
    out = ROOT / path.lstrip("/")
    if path.endswith("/"):
        out = out / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(full, encoding="utf-8")
    PAGES.append(path)

PAGES = []

# ------------------------------------------------------------------ shared blocks
def tag(text, c="var(--coral)"):
    return f'<span class="tag" style="--c:{c}"><i></i>{text}</span>'

def faq_block(faq, title='Questions? <span class="hl hy">Answered.</span>'):
    items = "".join(f'<details{" open" if i == 0 else ""}><summary>{E(q)}<b>+</b></summary><p>{E(a)}</p></details>' for i, (q, a) in enumerate(faq))
    return f'''<section class="sec" id="faq" style="padding-top:0"><div class="wrap faqw">
<div>{tag("FAQ", "var(--blue)")}<h2 style="margin-top:18px">{title}</h2><p style="margin-top:18px;color:var(--ink2)">Anything else? Ask us on WhatsApp.</p><div style="margin-top:24px">{wa_btn("Hi, I have a question for Kiran Growth School.", "Ask on WhatsApp")}</div></div>
<div class="faq">{items}</div></div></section>'''

def contact_block(interest_default=None):
    opts = ["Meta Ads", "Google Ads", "Website design", "Social media marketing", "AI videos", "AI avatar videos", "AI automation", "Complete performance marketing", "Courses (Meta Ads / AI)"]
    opt_html = "".join(f'<option{" selected" if o == interest_default else ""}>{E(o)}</option>' for o in opts)
    btypes = ["Solar company / installer", "Real estate builder", "Real estate broker / channel partner", "Other business", "Student / learner"]
    bt_html = "".join(f"<option>{E(b)}</option>" for b in btypes)
    return f'''<section class="sec" id="contact" style="padding-top:0">
  <div class="wrap cbox">
    <div class="form">
      {tag("Enquiry form")}
      <h2 style="font-size:clamp(1.7rem,3.4vw,2.5rem);margin-top:16px">Get your <span class="hl hm">free growth plan</span></h2>
      <form id="enq" novalidate>
        <div class="r2"><label for="nm">Your name<input id="nm" placeholder="e.g. Rahul Sharma" autocomplete="name"></label><label for="pn">Phone<input id="pn" placeholder="10-digit number" inputmode="tel" autocomplete="tel"></label></div>
        <div class="r2"><label for="ct">City<input id="ct" placeholder="e.g. Gurugram"></label><label for="tp">Business<select id="tp">{bt_html}</select></label></div>
        <label for="it">Interested in<select id="it">{opt_html}</select></label>
        <label for="ms">Message (optional)<textarea id="ms" placeholder="Monthly budget, projects, current lead sources..."></textarea></label>
        <a id="send" class="btn b-wa" href="{E(wa("Hi Kiran Growth School, new website enquiry."))}" target="_blank" rel="noopener">{I["wa"]}Send enquiry on WhatsApp</a>
        <p class="note">Opens WhatsApp with your details filled in. Just press send.</p>
      </form>
    </div>
    <div class="cinfo">
      <div class="ci" style="--c:var(--wa)"><i>{I["wa"]}</i><div><small>WhatsApp (all enquiries)</small><b>{SITE["phone"]}</b></div><button class="copy" type="button" data-copy="{SITE["phone_e164"]}">Copy</button></div>
      <div class="ci" style="--c:var(--sun)"><i>{I["phone"]}</i><div><small>Call</small><b>{SITE["phone"]}</b></div><button class="copy" type="button" data-copy="{SITE["phone_e164"]}">Copy</button></div>
      <div class="ci" style="--c:var(--violet);--fc:#fff"><i>{I["mail"]}</i><div><small>Email</small><b>{SITE["email"]}</b></div><button class="copy" type="button" data-copy="{SITE["email"]}">Copy</button></div>
      <div class="ci" style="--c:var(--pink)"><i>{I["clock"]}</i><div><small>Hours</small><b style="user-select:text">{SITE["hours"]}</b></div></div>
    </div>
  </div>
</section>'''

def cta_band(h, p, msg):
    return f'''<section class="sec" style="padding-top:0"><div class="wrap"><div class="cta"><div class="in">
{tag("Free growth plan", "var(--mint)")}<h2 style="margin-top:18px">{h}</h2><p>{p}</p>
<div class="ctas">{wa_btn(msg, "Chat on WhatsApp")}<a class="btn b-white" href="tel:{SITE["phone_e164"]}">{I["phone"]}Call {SITE["phone"]}</a></div>
</div></div></div></section>'''

def svc_cards(highlight=None):
    cards = []
    for i, s in enumerate(SERVICES):
        chips = "".join(f"<span>{E(c)}</span>" for c in s["chips"][:4])
        wide = " w" if len(SERVICES) % 3 == 1 and i >= len(SERVICES) - 4 else ""
        cards.append(f'<article class="s{wide}" style="--bg:{s["bg"]};--c:{s["c"]}"><div class="ic">{I[s["icon"]]}</div><h3>{E(s["name"])}</h3><p>{E(s["short"])}. {E(s["lead"].split(". ")[0])}.</p><div class="chips">{chips}</div><a class="more" href="/services/{s["slug"]}/">Explore {E(s["name"])} →</a></article>')
    cards.append(f'<article class="s audit"><div><h3>Get a free growth audit</h3><p>Send your business details on WhatsApp. We review your ads, website and follow-up process, and reply with a channel plan for your city.</p></div>{wa_btn("Hi, I would like a free growth audit. My business is: ", "Request free audit", "b-sun")}</article>')
    return '<div class="svc">' + "".join(cards) + "</div>"

def industry_cards():
    sol, re_ = INDUSTRIES["solar"], INDUSTRIES["real-estate"]
    return f'''<div class="ind">
<div class="indc solar"><span class="tag" style="--c:var(--coral)"><i></i>Solar & EPC</span><h3>Solar installers & EPC companies</h3><p>Rooftop solar, PM Surya Ghar subsidy leads, housing societies and commercial rooftops.</p><ul>{"".join(f"<li>{E(o)}</li>" for o in sol["offer"][:4])}</ul><a class="btn b-white" href="/{sol["slug"]}/">Solar marketing →</a></div>
<div class="indc re"><span class="tag" style="--c:var(--blue)"><i></i>Real estate</span><h3>Builders, brokers & channel partners</h3><p>Project launches, ready-to-move inventory, plots and commercial spaces with RERA-compliant ads.</p><ul>{"".join(f"<li>{E(o)}</li>" for o in re_["offer"][:4])}</ul><a class="btn b-white" href="/{re_["slug"]}/">Real estate marketing →</a></div>
</div>'''

def other_industries(city=None):
    where = f" in {city}" if city else ""
    cards = "".join(f'<div class="card"><h3>{E(t)}</h3><p>{E(d)}</p></div>' for t, d in OTHER_INDUSTRIES)
    return f'''<section class="sec" style="padding-top:0"><div class="wrap"><div class="head"><div>{tag("Other industries", "var(--sky)")}<h2>A full-service digital marketing agency{E(where)}</h2></div><p>Solar and real estate are our specialities, and the same performance marketing system works for many other businesses{E(where)}.</p></div><div class="grid3">{cards}</div></div></section>'''

def city_links(prefix="/locations/"):
    return '<div class="citylinks">' + "".join(f'<a href="{prefix}{c["slug"]}/">{I["pin"].replace("<svg ", "<svg style=\"width:16px;height:16px;vertical-align:-3px;margin-right:6px\" ")}{E(c["name"])}</a>' for c in CITIES) + "</div>"

def steps_block():
    st = [("var(--sun)", "", "Message on WhatsApp", "Tell us your business, city and goal. All enquiries come to +91 93998 51765."),
          ("var(--mint)", "", "Free audit & plan", "We review your ads, website and follow-up, then share a channel and budget plan."),
          ("var(--pink)", "", "Launch in 7 to 10 days", "Tracking, landing pages, creatives and campaigns go live."),
          ("var(--blue)", ";--fc:#fff", "Weekly optimisation", "Weekly reports on cost per lead, qualified leads and site visits, with clear next steps.")]
    items = "".join(f'<div class="step" style="--c:{c}{fc}"><span class="no">{i + 1}</span><h3>{t}</h3><p>{p}</p></div>' for i, (c, fc, t, p) in enumerate(st))
    return f'<section class="sec" id="process" style="padding-top:0"><div class="wrap"><div class="head"><div>{tag("How it works", "var(--sun)")}<h2>From hello to <span class="hl hb">leads</span></h2></div></div><div class="steps">{items}</div></div></section>'

# ------------------------------------------------------------------ blog
def parse_post(fp):
    raw = fp.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", raw, re.S)
    if not m:
        raise ValueError(f"{fp.name}: missing front matter")
    meta, faq = {}, []
    for line in m.group(1).splitlines():
        if not line.strip():
            continue
        k, _, v = line.partition(":")
        k, v = k.strip(), v.strip()
        if k == "faq":
            q, _, a = v.partition("||")
            faq.append((q.strip(), a.strip()))
        else:
            meta[k] = v.strip('"')
    for req in ("title", "description", "date", "category"):
        if req not in meta:
            raise ValueError(f"{fp.name}: missing {req}")
    meta["slug"] = meta.get("slug") or fp.stem
    meta["date_obj"] = datetime.date.fromisoformat(meta["date"])
    meta["faq"] = faq
    meta["tags"] = [t.strip() for t in meta.get("tags", "").split(",") if t.strip()]
    meta["body_md"] = m.group(2)
    meta["html"] = markdown.markdown(m.group(2), extensions=["tables", "sane_lists", "toc"])
    words = len(re.findall(r"\w+", m.group(2)))
    meta["mins"] = max(3, round(words / 200))
    meta["words"] = words
    return meta

CAT = {"solar": ("Solar marketing", "var(--sun)"), "real-estate": ("Real estate marketing", "var(--mint)"),
       "ai": ("AI & automation", "var(--pink)"), "growth": ("Growth strategy", "var(--sky)")}

def load_posts():
    posts = []
    for fp in sorted((ROOT / "content" / "blog").glob("*.md")):
        p = parse_post(fp)
        if p["date_obj"] <= TODAY:
            posts.append(p)
    posts.sort(key=lambda p: (p["date_obj"], int(p.get("order", "0") or 0)), reverse=True)
    return posts

def post_card(p):
    cat, c = CAT.get(p["category"], ("Insights", "var(--sky)"))
    return f'<a class="card" href="/blog/{p["slug"]}/" style="--bg:var(--white)"><small style="color:var(--ink)"><span style="display:inline-block;width:9px;height:9px;border-radius:50%;background:{c};border:1.5px solid var(--ink);margin-right:6px"></span>{cat} · {p["date_obj"]:%d %b %Y}</small><h3>{E(p["title"])}</h3><p>{E(p["description"])}</p><span class="more">Read · {p["mins"]} min →</span></a>'

# ------------------------------------------------------------------ pages
def build_home(posts):
    s = SITE
    body = f'''<section class="hero" id="top">
  <div class="wrap">
    <div>
      {tag("Performance marketing agency · Delhi NCR & MP", "var(--mint)")}
      <h1>More <span class="hl hy">leads</span> for <span class="hl hb">solar</span> &amp; <span class="hl hc">real estate</span> businesses.</h1>
      <p class="lead">Kiran Growth School is a performance marketing agency for solar installers, builders, brokers and channel partners in Delhi, Gurugram, Ghaziabad, Bhopal, Rewa and Satna. Meta Ads, Google Ads, high-converting websites, AI videos, AI avatar videos and AI automation, all tracked to real enquiries on WhatsApp.</p>
      <div class="ctas">
        {wa_btn("Hi, I'd like a free growth plan for my business.", "Get a free growth plan")}
        <a class="btn b-sun" href="/services/">See all services</a>
      </div>
      <div class="mini">
        <div><i style="background:var(--sun)">{I["sun"]}</i><div><b>Solar</b><br><span>PM Surya Ghar leads</span></div></div>
        <div><i style="background:var(--mint)">{I["building"]}</i><div><b>Real estate</b><br><span>Site-visit focused</span></div></div>
        <div><i style="background:var(--pink)">{I["bolt"]}</i><div><b>AI-first</b><br><span>Videos & automation</span></div></div>
      </div>
    </div>
    <div class="photo" id="photo">
      <div class="stage">
        <div class="pframe"><img src="/assets/img/sitanshu-hero.webp" alt="Sitanshu Tripathi, founder of Kiran Growth School performance marketing agency" width="900" height="878" fetchpriority="high"></div>
        <div class="sticker st1"><small>Founder</small><b>{s["founder"]}</b></div>
        <div class="sticker st2"><small>All enquiries on</small><b>WhatsApp</b></div>
        <div class="sticker st3"><b>Meta · Google · AI</b></div>
      </div>
    </div>
  </div>
</section>

<div class="plat" aria-label="Platforms we use"><div class="row">{"".join(f'<span><b style="display:inline-grid;place-items:center;width:40px;height:40px;border-radius:12px;background:{c};color:#14111f;border:2.5px solid #14111f">{ic}</b>{t}</span>' for c, ic, t in [("#ffc626", I["google"], "Google Ads"), ("#1fd39b", I["meta"], "Meta Ads"), ("#ff6fb5", I["insta"], "Instagram"), ("#5ec8ff", I["video"], "YouTube"), ("#ff5a36", I["wa"], "WhatsApp Business"), ("#ffffff", I["web"], "Websites"), ("#ffc626", I["avatar"], "AI Avatars"), ("#1fd39b", I["bolt"], "AI Automation")] * 2)}</div></div>

<section class="sec" id="industries">
  <div class="wrap">
    <div class="head"><div>{tag("Who we grow", "var(--blue)")}<h2>Built for <span class="hl hm">high-ticket</span> local businesses</h2></div><p>Solar and real estate buyers research for weeks, compare online and decide on trust and speed. Our whole system is designed for that buying journey.</p></div>
    {industry_cards()}
  </div>
</section>

{other_industries()}

<section class="sec" id="services" style="padding-top:10px">
  <div class="wrap">
    <div class="head"><div>{tag("Services", "var(--coral)")}<h2>Performance marketing that <span class="hl hc">pays back</span></h2></div><p>Every service is planned around one number: cost per qualified lead. Not likes, not impressions.</p></div>
    {svc_cards()}
  </div>
</section>

<section class="nums" aria-label="How we work"><div class="wrap">
  <div class="n"><b>7</b><span>Core services under one roof</span></div>
  <div class="n"><b>7</b><span>Focus cities across Delhi NCR & MP</span></div>
  <div class="n"><b>24×7</b><span>Instant WhatsApp replies with automation</span></div>
  <div class="n"><b>Weekly</b><span>Reports on leads and cost per lead</span></div>
</div></section>

<section class="sec" id="locations">
  <div class="wrap">
    <div class="head"><div>{tag("Where we work", "var(--pink)")}<h2>Local campaigns, <span class="hl hp">city by city</span></h2></div><p>Each city has its own DISCOM, RERA authority, micro-markets and buyer language. We plan campaigns around those differences.</p></div>
    {city_links()}
  </div>
</section>

<section class="sec founder" id="founder">
  <div class="wrap">
    <div class="fimg"><div class="fr"><img src="/assets/img/sitanshu-studio.webp" alt="Sitanshu Tripathi in the studio" loading="lazy" width="900" height="878"></div><div class="name"><b>{s["founder"]}</b><span>Founder, Kiran Growth School</span></div></div>
    <div>
      {tag("Meet the founder", "var(--sun)")}
      <h2>The team behind <span class="hl hy">Kiran Growth School</span></h2>
      <p class="quote">"Good marketing is measured in leads and sales, not likes. We build every campaign around that."</p>
      <div class="bio">
        <p>{s["founder"]} has 7+ years of experience in digital marketing and education. Kiran Growth School runs performance marketing for businesses, and teaches the same skills to the next generation of marketers.</p>
        <p>The team works the way modern growth teams do: data-led ad buying, fast creative testing with AI, and automation that makes sure every enquiry is answered.</p>
      </div>
      <div style="margin-top:28px"><a class="btn b-white" href="{s["linkedin"]}" target="_blank" rel="noopener" style="margin-right:12px">Connect on LinkedIn</a>{wa_btn("Hi Sitanshu, I'd like to discuss marketing for my business.", "Talk to us", "b-sun")}</div>
    </div>
  </div>
</section>

{steps_block()}

<section class="sec" style="padding-top:0">
  <div class="wrap">
    <div class="head"><div>{tag("From the blog", "var(--mint)")}<h2>Playbooks for <span class="hl hm">solar & real estate</span></h2></div><p><a href="/blog/" style="font-weight:800">See all articles →</a></p></div>
    <div class="grid3">{"".join(post_card(p) for p in posts[:6])}</div>
  </div>
</section>

<section class="sec" style="padding-top:0">
  <div class="wrap">
    <div class="paths" style="grid-template-columns:1fr">
      <div class="path b" style="flex-direction:row;flex-wrap:wrap;align-items:center;justify-content:space-between"><div style="max-width:40em"><span class="k">Also from us</span><h3 style="margin-top:12px">Want to learn it yourself?</h3><p style="margin-top:8px">Our academy runs live Meta Ads and AI Tools &amp; Website Design courses (₹25,000 each), taught by people who run campaigns every day.</p></div><a class="btn b-white" href="/courses/">View courses →</a></div>
    </div>
  </div>
</section>

{faq_block(HOME_FAQ)}
{cta_band('Your next customer is searching <span class="hl hy">right now</span>', "Tell us what you sell and where. We'll show you how to reach the buyers already looking for it.", "Hi Kiran Growth School, I'd like to get started.")}
{contact_block("Complete performance marketing")}'''
    page("/", "Performance & Digital Marketing Agency in Delhi NCR, Gurugram & Bhopal | Kiran Growth School",
         "Performance and digital marketing agency in Delhi NCR, Gurugram, Ghaziabad, Bhopal, Rewa and Satna, specialising in solar and real estate. Meta Ads, Google Ads, websites, social media, AI videos and AI automation. WhatsApp +91 93998 51765.",
         body, active="/", schema=[faq_schema(HOME_FAQ)])

def build_services():
    body = f'''<section class="phero"><div class="wrap">{crumbs_html([("/", "Home"), ("/services/", "Services")])}
<h1>Performance marketing <span class="hl hc">services</span></h1>
<p class="lead">Seven services, one goal: more qualified enquiries for your solar or real estate business, at a cost per lead that makes sense. Pick one, or let us run the full system.</p>
<div class="ctas">{wa_btn("Hi, I want to discuss your services.", "Discuss on WhatsApp")}</div></div></section>
<section class="sec"><div class="wrap">{svc_cards()}</div></section>
{steps_block()}
{contact_block()}'''
    page("/services/", "Performance Marketing Services | Meta Ads, Google Ads, Websites, AI Video & Automation",
         "Meta Ads, Google Ads, website design, AI video production, AI avatar videos and AI automation for solar and real estate businesses in Delhi NCR and Madhya Pradesh.",
         body, active="/services/", schema=[crumbs_schema([("/", "Home"), ("/services/", "Services")])])
    for s in SERVICES:
        path = f"/services/{s['slug']}/"
        pts = "".join(f'<div class="card"><h3>{E(t)}</h3><p>{E(d)}</p></div>' for t, d in s["points"])
        chips = "".join(f"<span>{E(c)}</span>" for c in s["chips"])
        others = "".join(f'<a class="card" href="/services/{o["slug"]}/" style="--bg:{o["bg"]}"><h3>{E(o["name"])}</h3><p>{E(o["short"])}</p><span class="more">Learn more →</span></a>' for o in SERVICES if o is not s)
        cr = [("/", "Home"), ("/services/", "Services"), (path, s["name"])]
        body = f'''<section class="phero"><div class="wrap">{crumbs_html(cr)}
<h1>{s["h1"]}</h1><p class="lead">{E(s["lead"])}</p>
<div class="chips" style="margin-top:18px">{chips}</div>
<div class="ctas">{wa_btn(f"Hi, I'm interested in {s['name']} for my business.", f"Get a {E(s['name'])} plan")}<a class="btn b-white" href="#how">How we do it</a></div></div></section>
<section class="sec" id="how"><div class="wrap"><div class="head"><div>{tag("How we do it", s["c"])}<h2>What's included</h2></div><p>Built for solar installers, builders, brokers and channel partners. Available in Delhi NCR, Gurugram, Ghaziabad, Bhopal, Rewa, Satna and across India.</p></div>
<div class="grid3">{pts}</div></div></section>
<section class="sec" style="padding-top:0"><div class="wrap"><div class="head"><div>{tag("Industries", "var(--blue)")}<h2>{E(s["name"])} for <span class="hl hy">solar</span> &amp; <span class="hl hm">real estate</span></h2></div></div>{industry_cards()}</div></section>
<section class="sec" style="padding-top:0"><div class="wrap"><div class="head"><div>{tag("Cities", "var(--pink)")}<h2>{E(s["name"])} by city</h2></div></div>{city_links()}</div></section>
{faq_block(s["faq"])}
<section class="sec" style="padding-top:0"><div class="wrap"><div class="head"><div>{tag("Other services", "var(--mint)")}<h2>Works best together</h2></div></div><div class="grid3">{others}</div></div></section>
{contact_block({"meta-ads": "Meta Ads", "google-ads": "Google Ads", "website-design": "Website design", "ai-video-production": "AI videos", "ai-avatar-videos": "AI avatar videos", "social-media-marketing": "Social media marketing", "ai-automation": "AI automation"}[s["slug"]])}'''
        svc_ld = {"@type": "Service", "name": s["name"], "serviceType": s["name"], "description": s["desc"], "provider": {"@id": ORG_ID},
                  "areaServed": [c["name"] for c in CITIES], "audience": {"@type": "BusinessAudience", "audienceType": "Solar companies, real estate builders, brokers and channel partners"}}
        page(path, s["title"] + " | Kiran Growth School", s["desc"], body, active="/services/", schema=[svc_ld, faq_schema(s["faq"]), crumbs_schema(cr)])

def build_industries(posts):
    for key, ind in INDUSTRIES.items():
        path = f"/{ind['slug']}/"
        pains = "".join(f'<div class="card"><h3>{E(t)}</h3><p>{E(d)}</p></div>' for t, d in ind["pains"])
        offer = "".join(f"<li>{E(o)}</li>" for o in ind["offer"])
        kw = "".join(f"<span>{E(k)}</span>" for k in ind["keywords"])
        rel = [p for p in posts if p["category"] == key][:6] or posts[:3]
        city_cards = "".join(
            f'<a class="card" href="/locations/{c["slug"]}/#{key}"><small>{E(c["state"])}</small><h3>{E(ind["name"])} marketing in {E(c["name"])}</h3><p>{E(c["solar_angle"] if key == "solar" else c["re_angle"])[:150]}…</p><span class="more">{E(c["name"])} playbook →</span></a>'
            for c in CITIES)
        faq = ([
            ("What is the best way to get solar leads in India?", "Combine Google Search ads for people already searching for rooftop solar, Meta lead and WhatsApp ads to create demand around PM Surya Ghar savings, a fast website with a savings calculator, and instant WhatsApp follow-up. Qualify every lead by monthly bill, roof ownership and DISCOM."),
            ("How much subsidy does PM Surya Ghar give?", "Central financial assistance is 60% of system cost up to 2 kW and 40% of the additional cost from 2 to 3 kW, capped at ₹78,000 for 3 kW and above (about ₹30,000 for 1 kW and ₹60,000 for 2 kW). Some states add extra support. Always confirm current figures on the official PM Surya Ghar portal."),
            ("Can you run ads for both residential and commercial solar?", "Yes. Residential PM Surya Ghar campaigns, housing society (RWA) campaigns and commercial and industrial rooftop campaigns are run separately because buyers, budgets and messages are different."),
            ("Do you work with solar EPCs in Madhya Pradesh?", "Yes, including Bhopal, Rewa and Satna, with Hindi-first creatives and campaigns that cover nearby towns."),
        ] if key == "solar" else [
            ("Do real estate ads need a RERA number?", "Yes. State RERA authorities, including UP RERA, HRERA, Delhi RERA and MP RERA, expect registered projects to show their RERA registration number and website in advertisements, and several have issued specific advertising directions. We add it to every ad and landing page."),
            ("Are Meta Ads good for real estate in India?", "Yes, especially for new launches, plots and mid-segment housing. Lead forms with qualifying questions, click-to-WhatsApp ads and video walkthroughs work well when followed up within minutes."),
            ("Do you work with brokers and channel partners?", "Yes. Channel partners can run their own ads for the projects they are mandated on, as long as the creatives and claims are approved and RERA-compliant."),
            ("Can you get NRI buyers?", "We can target NRI audiences in the Gulf, UK, US and elsewhere on Meta, Google and YouTube for projects that suit them, with timezone-aware WhatsApp follow-up."),
        ])
        cr = [("/", "Home"), (path, f"{ind['name']} marketing")]
        body = f'''<section class="phero"><div class="wrap">{crumbs_html(cr)}
<h1>{ind["h1"]}</h1><p class="lead">{E(ind["lead"])}</p>
<div class="ctas">{wa_btn(f"Hi, I run a {ind['name'].lower()} business and want more leads.", "Get a free growth plan")}<a class="btn b-white" href="#cities">See city playbooks</a></div>
{'<div class="facts"><div><b>50 lakh+</b><span>Homes with rooftop solar under PM Surya Ghar (Aug 2026)</span></div><div><b>₹78,000</b><span>Maximum central subsidy per household</span></div><div><b>300 units</b><span>Free electricity per month target</span></div><div><b>1 crore</b><span>Household target under the scheme</span></div></div>' if key == "solar" else '<div class="facts"><div><b>RERA</b><span>Registration number on every ad & page</span></div><div><b>Exclusive</b><span>Your own leads, not shared portal leads</span></div><div><b>Site visits</b><span>Optimised and tracked to the ad</span></div><div><b>Hindi + English</b><span>Creatives for every buyer</span></div></div>'}
</div></section>
<section class="sec"><div class="wrap"><div class="head"><div>{tag("Problems we fix", "var(--coral)")}<h2>Why most {E(ind["name"].lower())} ads <span class="hl hc">underperform</span></h2></div></div><div class="grid2">{pains}</div></div></section>
<section class="sec" style="padding-top:0"><div class="wrap"><div class="head"><div>{tag("What we market", "var(--sun)")}<h2>Campaigns we run</h2></div><p>Search terms we target include:</p></div>
<div class="grid2"><div class="card"><ul style="margin:0;padding-left:1.1em;display:grid;gap:8px;font-weight:700">{offer}</ul></div><div class="card"><div class="kw">{kw}</div></div></div></div></section>
<section class="sec" style="padding-top:0"><div class="wrap"><div class="head"><div>{tag("The system", "var(--blue)")}<h2>Seven services, <span class="hl hb">one system</span></h2></div></div>{svc_cards()}</div></section>
<section class="sec" id="cities" style="padding-top:0"><div class="wrap"><div class="head"><div>{tag("City playbooks", "var(--pink)")}<h2>{E(ind["name"])} marketing by city</h2></div></div><div class="grid3">{city_cards}</div></div></section>
<section class="sec" style="padding-top:0"><div class="wrap"><div class="head"><div>{tag("Read", "var(--mint)")}<h2>{E(ind["name"])} marketing guides</h2></div></div><div class="grid3">{"".join(post_card(p) for p in rel)}</div></div></section>
{faq_block(faq)}
{contact_block("Complete performance marketing")}'''
        sld = {"@type": "Service", "name": f"{ind['name']} marketing", "serviceType": f"{ind['name']} lead generation and performance marketing", "description": ind["desc"], "provider": {"@id": ORG_ID}, "areaServed": [c["name"] for c in CITIES]}
        page(path, ind["title"] + " | Kiran Growth School", ind["desc"], body, active=path, schema=[sld, faq_schema(faq), crumbs_schema(cr)])

def build_locations(posts):
    cr = [("/", "Home"), ("/locations/", "Locations")]
    cards = "".join(f'<a class="card" href="/locations/{c["slug"]}/"><small>{E(c["state"])}</small><h3>Performance marketing agency in {E(c["name"])}</h3><p>{E(c["intro"])}</p><span class="more">Solar & real estate in {E(c["name"])} →</span></a>' for c in CITIES)
    body = f'''<section class="phero"><div class="wrap">{crumbs_html(cr)}<h1>Performance marketing in <span class="hl hp">your city</span></h1>
<p class="lead">We run solar and real estate campaigns in Delhi, across Delhi NCR (Gurugram, Ghaziabad, Noida, Faridabad) and in Madhya Pradesh (Bhopal, Rewa, Satna). Each city page covers local DISCOMs, RERA rules and micro-markets.</p></div></section>
<section class="sec"><div class="wrap"><div class="grid3">{cards}</div></div></section>{contact_block()}'''
    page("/locations/", "Performance Marketing Agency Locations | Delhi NCR, Gurugram, Ghaziabad, Bhopal, Rewa, Satna",
         "Solar and real estate performance marketing in Delhi, Delhi NCR, Gurugram, Ghaziabad, Bhopal, Rewa and Satna. Meta Ads, Google Ads, websites, AI videos and automation.",
         body, active="/locations/", schema=[crumbs_schema(cr)])
    for c in CITIES:
        path = f"/locations/{c['slug']}/"
        n = c["name"]
        crc = cr + [(path, n)]
        micro = "".join(f"<span>{E(m)}</span>" for m in c["micro"])
        sol_kw = [f"solar company in {n}", f"rooftop solar {n}", f"solar subsidy {n}", f"solar installer near me {n}", f"PM Surya Ghar {n}"]
        re_kw = [f"real estate marketing {n}", f"property leads {n}", f"builder digital marketing {n}", f"flats in {n}" if c["region"] == "NCR" else f"plots in {n}"]
        rel = [p for p in posts if n.lower() in (p["title"] + " " + " ".join(p["tags"])).lower()][:3] or posts[:3]
        faq = [
            (f"Which is a good digital marketing agency in {n}?", f"Choose an agency that works inside your own ad accounts, tracks cost per qualified lead, builds landing pages and follows up fast on WhatsApp. Kiran Growth School offers Meta Ads, Google Ads, websites, social media, AI videos and automation for businesses in {n}, with a focus on solar and real estate."),
            (f"Which is the best performance marketing agency in {n} for solar companies?", f"Look for an agency that understands {c['discom']} net-metering, PM Surya Ghar subsidy rules and local buyer language, and that tracks cost per qualified lead, not just clicks. Kiran Growth School runs Meta Ads, Google Ads, websites and WhatsApp automation for solar installers in {n}."),
            (f"Can you generate real estate leads in {n}?", f"Yes. We run RERA-compliant Meta and Google campaigns for builders, brokers and channel partners in {n}, with project landing pages and instant WhatsApp follow-up to book site visits."),
            (f"Do I need an office visit to work with you in {n}?", "No. Most work happens over WhatsApp, calls and shared dashboards. We can meet in person when needed."),
            (f"What does it cost to run ads in {n}?", "Ad spend is paid directly to Meta or Google and can start small for testing. Our management fee depends on scope. Message us on WhatsApp with your goals for a quote."),
        ]
        body = f'''<section class="phero"><div class="wrap">{crumbs_html(crc)}
<h1>Digital &amp; performance marketing agency in <span class="hl hy">{E(n)}</span></h1>
<p class="lead">{E(c["intro"])} Kiran Growth School is a digital and performance marketing agency serving businesses in {E(n)}: Meta Ads, Google Ads, website design, social media marketing, AI videos, AI avatar videos and AI automation, with special expertise in solar companies and real estate.</p>
<div class="ctas">{wa_btn(f"Hi, I'm in {n} and want more leads for my business.", f"Free growth plan for {E(n)}")}<a class="btn b-white" href="#solar">Solar</a><a class="btn b-white" href="#real-estate">Real estate</a></div>
<div class="facts"><div><b>{E(c["state"])}</b><span>State / region</span></div><div><b>{E(c["rera"])}</b><span>RERA authority for property ads</span></div><div style="grid-column:span 2"><b style="font-size:1rem">{E(c["discom"])}</b><span>DISCOM(s) for solar net metering</span></div></div>
</div></section>
<section class="sec" id="solar"><div class="wrap"><div class="ind"><div class="indc solar">{tag("Solar marketing in " + E(n), "var(--coral)")}<h3>Solar lead generation in {E(n)}</h3><p>{E(c["solar_angle"])}</p>
<ul><li>PM Surya Ghar subsidy campaigns with bill-based lead qualification</li><li>Google Search ads for "{E(sol_kw[0])}" and "{E(sol_kw[1])}"</li><li>Housing society and commercial rooftop campaigns</li><li>Instant WhatsApp replies with subsidy and savings info</li></ul><a class="btn b-white" href="/solar-marketing-agency/">Full solar playbook →</a></div>
<div class="indc re" id="real-estate">{tag("Real estate marketing in " + E(n), "var(--blue)")}<h3>Property leads in {E(n)}</h3><p>{E(c["re_angle"])}</p>
<ul><li>{E(c["rera"])}-compliant ads and landing pages</li><li>Project microsites and AI walkthrough videos</li><li>Lead forms and click-to-WhatsApp ads that book site visits</li><li>Separate campaigns per project and micro-market</li></ul><a class="btn b-white" href="/real-estate-marketing-agency/">Full real estate playbook →</a></div></div></div></section>
<section class="sec" style="padding-top:0"><div class="wrap"><div class="head"><div>{tag("Micro-markets", "var(--pink)")}<h2>Areas we target in and around {E(n)}</h2></div><p>Ads are targeted by locality and radius, not just city name, so budget goes to the buyers who can actually visit.</p></div><div class="kw">{micro}</div>
<div class="head" style="margin-top:44px;margin-bottom:20px"><div><h3>Popular searches we target</h3></div></div><div class="kw">{"".join(f"<span>{E(k)}</span>" for k in sol_kw + re_kw)}</div></div></section>
<section class="sec" style="padding-top:0"><div class="wrap"><div class="head"><div>{tag("Services in " + E(n), "var(--coral)")}<h2>Everything you need to grow in {E(n)}</h2></div></div>{svc_cards()}
<div class="citylinks" style="margin-top:28px">{"".join(f'<a href="/services/{sv["slug"]}/">{E(sv["name"])} agency in {E(n)}</a>' for sv in SERVICES)}</div></div></section>
{other_industries(n)}
<section class="sec" style="padding-top:0"><div class="wrap"><div class="head"><div>{tag("Read", "var(--mint)")}<h2>Guides for {E(n)} businesses</h2></div></div><div class="grid3">{"".join(post_card(p) for p in rel)}</div></div></section>
{faq_block(faq)}
<section class="sec" style="padding-top:0"><div class="wrap"><div class="head"><div><h2 style="font-size:1.6rem">Other cities</h2></div></div>{city_links()}</div></section>
{contact_block("Complete performance marketing")}'''
        ld = {"@type": "Service", "name": f"Digital and performance marketing agency in {n}", "serviceType": "Performance marketing for solar and real estate", "provider": {"@id": ORG_ID},
              "areaServed": {"@type": "City" if c["slug"] != "delhi-ncr" else "Place", "name": n}, "description": f"Meta Ads, Google Ads, website design, AI videos and AI automation for solar companies and real estate businesses in {n}."}
        page(path, f"Digital Marketing Agency in {n} | Performance Marketing, Meta & Google Ads | Kiran Growth School",
             f"Digital and performance marketing agency in {n}: Meta Ads, Google Ads, website design, social media, AI videos and WhatsApp automation. Specialists in solar and real estate leads. WhatsApp +91 93998 51765.",
             body, active="/locations/", schema=[ld, faq_schema(faq), crumbs_schema(crc)])

def build_courses():
    cr = [("/", "Home"), ("/courses/", "Courses")]
    cards = ""
    for co in COURSES:
        mods = "".join(f"<li>{I['tick']}{E(m)}</li>" for m in co["mods"])
        cards += f'''<article class="course" style="--c:{co["c"]};--fc:#fff">
<div class="ph"><img src="/assets/img/{co["img"]}" alt="{E(co["alt"])}" loading="lazy"><div class="tg"><span>{co["tag"]}</span><span>Classroom + Online</span></div></div>
<div class="body"><div><h2 style="font-size:clamp(1.45rem,2.4vw,1.85rem);font-weight:900">{E(co["name"])}</h2><p class="sub">{E(co["sub"])}</p></div><ul class="mods">{mods}</ul>
<div class="price"><div><small>Course fee</small><b>{co["fee"]}</b></div>{wa_btn(f"Hi, I want to enrol in the {co['name']} course ({co['fee']}). Please share batch details.", "Enquire now")}</div></div></article>'''
    faq = [("What do the courses cost?", "Meta Ads & Digital Marketing is ₹25,000 and AI Tools & Website Design is ₹25,000. Message us on WhatsApp for batch dates and combo offers."),
           ("Do I need any experience?", "No. Both courses start from the basics and build up to advanced, practical work. You need a laptop and internet."),
           ("Online or classroom?", "We run both classroom workshops and online sessions. Tell us what suits you and we'll suggest a batch."),
           ("Will I get a certificate?", "Yes, after completing the course projects, along with a portfolio you can show employers or clients.")]
    body = f'''<section class="phero"><div class="wrap">{crumbs_html(cr)}<h1>Learn performance marketing from <span class="hl hv">people who run it</span></h1>
<p class="lead">Kiran Growth School's academy teaches the same playbooks our agency uses for clients: Meta Ads, Google Ads basics, AI tools and website design. Live, practical and project-based.</p>
<div class="ctas">{wa_btn("Hi, please share upcoming batch dates for your courses.", "Get batch dates")}</div></div></section>
<section class="sec academy"><div class="wrap"><div class="courses">{cards}</div>
<div class="incl"><div class="inc" style="--c:var(--sun)"><i>{I["check"]}</i><div><b>Live practicals</b><span>Real ad accounts and tools in class</span></div></div><div class="inc" style="--c:var(--mint)"><i>{I["check"]}</i><div><b>Certificate</b><span>After completing course projects</span></div></div><div class="inc" style="--c:var(--pink)"><i>{I["check"]}</i><div><b>Portfolio</b><span>Campaigns and sites you can show</span></div></div><div class="inc" style="--c:var(--sky)"><i>{I["check"]}</i><div><b>Mentor support</b><span>Doubt solving and career guidance</span></div></div></div></div></section>
<section class="sec"><div class="wrap"><div class="head"><div>{tag("Inside the classroom", "var(--pink)")}<h2>Learning that feels <span class="hl hp">alive</span></h2></div></div>
<div class="gal"><figure style="--c:var(--sun)"><img src="/assets/img/workshop.jpg" alt="Students in an interactive workshop" loading="lazy"><figcaption><b>Interactive workshops</b><span>Activities, role-plays and live discussion</span></figcaption></figure><figure style="--c:var(--mint)"><img src="/assets/img/ai-session.jpg" alt="AI session on opportunity and risk" loading="lazy" style="object-position:50% 20%"><figcaption><b>AI sessions</b><span>Opportunity, risk and real-world use</span></figcaption></figure></div></div></section>
{faq_block(faq)}
{contact_block("Courses (Meta Ads / AI)")}'''
    course_ld = [{"@type": "Course", "name": co["name"], "description": co["sub"], "provider": {"@id": ORG_ID},
                  "offers": {"@type": "Offer", "price": "25000", "priceCurrency": "INR", "category": "Paid"},
                  "hasCourseInstance": {"@type": "CourseInstance", "courseMode": ["Onsite", "Online"]}} for co in COURSES]
    page("/courses/", "Digital Marketing Courses | Meta Ads & AI Tools Courses (₹25,000) | Kiran Growth School",
         "Live Meta Ads & Digital Marketing and AI Tools & Website Design courses, ₹25,000 each. Classroom and online batches with certificate. Enquire on WhatsApp +91 93998 51765.",
         body, active="/courses/", schema=course_ld + [faq_schema(faq), crumbs_schema(cr)])

def build_blog(posts):
    cr = [("/", "Home"), ("/blog/", "Blog")]
    body = f'''<section class="phero"><div class="wrap">{crumbs_html(cr)}<h1>Growth playbooks for <span class="hl hy">solar</span> &amp; <span class="hl hm">real estate</span></h1>
<p class="lead">Practical guides on PM Surya Ghar, solar lead generation, real estate ads, RERA-compliant marketing, Meta Ads, Google Ads, AI videos and automation. New articles every day.</p></div></section>
<section class="sec"><div class="wrap"><div class="grid3">{"".join(post_card(p) for p in posts)}</div></div></section>
{contact_block()}'''
    ld = {"@type": "Blog", "name": "Kiran Growth School Blog", "url": U + "/blog/", "publisher": {"@id": ORG_ID},
          "blogPost": [{"@type": "BlogPosting", "headline": p["title"], "url": f"{U}/blog/{p['slug']}/", "datePublished": p["date"]} for p in posts[:30]]}
    page("/blog/", "Solar & Real Estate Marketing Blog | PM Surya Ghar, Meta Ads, Google Ads | Kiran Growth School",
         "Guides on solar lead generation, PM Surya Ghar, real estate marketing, RERA-compliant ads, Meta Ads, Google Ads, AI videos and automation for Indian businesses.",
         body, active="/blog/", schema=[ld, crumbs_schema(cr)])
    for i, p in enumerate(posts):
        path = f"/blog/{p['slug']}/"
        cat, c = CAT.get(p["category"], ("Insights", "var(--sky)"))
        crp = cr + [(path, p["title"])]
        rel = [q for q in posts if q is not p and q["category"] == p["category"]][:3]
        rel += [q for q in posts if q is not p and q not in rel][: 3 - len(rel)]
        svc_link = {"solar": ("/solar-marketing-agency/", "Solar marketing services"), "real-estate": ("/real-estate-marketing-agency/", "Real estate marketing services")}.get(p["category"], ("/services/", "All services"))
        html_body = p["html"]
        # inline CTA after the 3rd h2
        parts = re.split(r"(?=<h2)", html_body)
        if len(parts) > 4:
            parts.insert(3, f'<div class="inline-cta"><h3>Want this done for your business?</h3><p>We run Meta Ads, Google Ads, websites and WhatsApp automation for solar and real estate businesses in Delhi NCR and MP.</p>{wa_btn("Hi, I read your article " + chr(34) + p["title"] + chr(34) + " and want help with my marketing.", "Get a free growth plan", "b-sun")}</div>')
        html_body = "".join(parts)
        faq_html = ""
        if p["faq"]:
            faq_html = '<h2 id="faq">Frequently asked questions</h2>' + "".join(f"<h3>{E(q)}</h3><p>{E(a)}</p>" for q, a in p["faq"])
        tldr = f'<div class="tldr"><b>Quick answer</b><p>{E(p["tldr"])}</p></div>' if p.get("tldr") else ""
        body = f'''<section class="phero"><div class="wrap">{crumbs_html(crp)}
<div style="margin-top:18px">{tag(cat, c)}</div><h1 style="max-width:26ch">{E(p["title"])}</h1><p class="lead">{E(p["description"])}</p>
<div class="meta"><span>By Kiran Growth School team</span><span>·</span><time datetime="{p["date"]}">{p["date_obj"]:%d %B %Y}</time><span>·</span><span>{p["mins"]} min read</span></div></div></section>
<section class="sec" style="padding-top:50px"><div class="wrap post-layout"><article class="prose">{tldr}{html_body}{faq_html}
<div class="inline-cta"><h3>Need more leads this month?</h3><p>Message us your business, city and budget. We reply with a practical plan, free.</p>{wa_btn("Hi Kiran Growth School, I want more leads for my business.", "WhatsApp +91 93998 51765", "b-sun")}</div></article>
<aside class="side"><div class="card"><small>Work with us</small><h3>{svc_link[1]}</h3><p>Meta Ads, Google Ads, websites, AI videos and automation, built for your industry.</p><a class="more" href="{svc_link[0]}">Learn more →</a></div>
<div class="card"><small>Related</small>{"".join(f'<a href="/blog/{q["slug"]}/" style="font-weight:700;text-decoration:none;display:block;padding:8px 0;border-bottom:1px dashed #cfc6b2">{E(q["title"])}</a>' for q in rel)}</div>
<div class="card" style="box-shadow:5px 5px 0 var(--mint)"><small>Cities</small>{"".join(f'<a href="/locations/{c2["slug"]}/" style="font-weight:700;text-decoration:none;display:block;padding:4px 0">{E(c2["name"])}</a>' for c2 in CITIES)}</div></aside></div></section>
<section class="sec" style="padding-top:0"><div class="wrap"><div class="head"><div>{tag("Keep reading", "var(--mint)")}<h2>More playbooks</h2></div></div><div class="grid3">{"".join(post_card(q) for q in rel)}</div></div></section>
{contact_block()}'''
        art = {"@type": "BlogPosting", "headline": p["title"], "description": p["description"], "datePublished": p["date"], "dateModified": p.get("updated", p["date"]),
               "author": {"@type": "Organization", "name": "Kiran Growth School", "url": U + "/"}, "publisher": {"@id": ORG_ID},
               "mainEntityOfPage": f"{U}{path}", "image": U + "/assets/img/og-default.jpg", "inLanguage": "en-IN", "wordCount": p["words"],
               "keywords": ", ".join(p["tags"]), "articleSection": cat}
        sch = [art, crumbs_schema(crp)] + ([faq_schema(p["faq"])] if p["faq"] else [])
        page(path, p["title"] + " | Kiran Growth School", p["description"], body, active="/blog/", schema=sch, og_type="article",
             extra_head=f'<meta property="article:published_time" content="{p["date"]}">\n')
    # RSS
    items = "".join(f"<item><title>{E(p['title'])}</title><link>{U}/blog/{p['slug']}/</link><guid>{U}/blog/{p['slug']}/</guid><pubDate>{datetime.datetime.combine(p['date_obj'], datetime.time(9, 0), IST):%a, %d %b %Y %H:%M:%S +0530}</pubDate><description>{E(p['description'])}</description></item>" for p in posts[:50])
    (ROOT / "blog" / "feed.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?><rss version="2.0"><channel><title>Kiran Growth School Blog</title><link>{U}/blog/</link><description>Solar and real estate marketing playbooks</description><language>en-in</language>{items}</channel></rss>', encoding="utf-8")

def build_about():
    cr = [("/", "Home"), ("/about/", "About")]
    s = SITE
    body = f'''<section class="phero"><div class="wrap">{crumbs_html(cr)}<h1>About <span class="hl hy">Kiran Growth School</span></h1>
<p class="lead">Kiran Growth School is a digital and performance marketing agency founded by {s["founder"]}. We help businesses in Delhi NCR and Madhya Pradesh get more enquiries from Meta Ads, Google Ads, websites, social media, AI videos and AI automation, with deep focus on solar companies and real estate.</p>
<div class="ctas">{wa_btn("Hi Kiran Growth School, I'd like to know more about your agency.", "Talk to us")}<a class="btn b-white" href="/services/">Our services</a></div></div></section>
<section class="sec founder"><div class="wrap">
<div class="fimg"><div class="fr"><img src="/assets/img/sitanshu-studio.webp" alt="{s["founder"]}, founder of Kiran Growth School" loading="lazy" width="900" height="878"></div><div class="name"><b>{s["founder"]}</b><span>Founder</span></div></div>
<div>{tag("Our story", "var(--sun)")}<h2>Marketing measured in <span class="hl hy">leads and sales</span></h2>
<div class="bio" style="margin-top:22px"><p>{s["founder"]} has 7+ years of experience in digital marketing and education. Kiran Growth School started by teaching practical marketing and grew into an agency that runs campaigns for businesses.</p>
<p>Today the agency focuses on performance marketing: every campaign is planned around cost per qualified lead, and every enquiry is routed to WhatsApp so it can be answered fast. Our academy still runs live courses, taught from the same playbooks.</p></div>
<div style="margin-top:26px"><a class="btn b-white" href="{s["linkedin"]}" target="_blank" rel="noopener">{s["founder"]} on LinkedIn</a></div></div></div></section>
<section class="sec"><div class="wrap"><div class="head"><div>{tag("How we work", "var(--blue)")}<h2>What you can expect</h2></div></div><div class="grid3">
<div class="card"><h3>Your accounts, your data</h3><p>We work inside your own Meta, Google and website accounts. You keep everything.</p></div>
<div class="card"><h3>Weekly, honest reporting</h3><p>Cost per lead, lead quality and what changed, in plain language. No vanity metrics.</p></div>
<div class="card"><h3>Speed on WhatsApp</h3><p>Every enquiry goes to WhatsApp, with automation so no lead waits.</p></div>
<div class="card"><h3>Industry knowledge</h3><p>Subsidy rules for solar, RERA rules for property, and local buyer behaviour in each city.</p></div>
<div class="card"><h3>AI where it helps</h3><p>AI videos, avatars and automation to test faster and follow up better, with humans checking every claim.</p></div>
<div class="card"><h3>No fake promises</h3><p>We don't guarantee rankings or lead counts. We commit to tracking, testing and transparency.</p></div>
</div></div></section>
<section class="sec" style="padding-top:0"><div class="wrap"><div class="head"><div>{tag("Where we work", "var(--pink)")}<h2>Cities we serve</h2></div></div>{city_links()}</div></section>
{contact_block()}'''
    ld = {"@type": "AboutPage", "url": U + "/about/", "name": "About Kiran Growth School", "about": {"@id": ORG_ID}}
    page("/about/", "About Kiran Growth School | Digital & Performance Marketing Agency founded by Sitanshu Tripathi",
         "Kiran Growth School is a digital and performance marketing agency founded by Sitanshu Tripathi, serving Delhi NCR and Madhya Pradesh with Meta Ads, Google Ads, websites, social media, AI videos and automation.",
         body, schema=[ld, crumbs_schema(cr)])

def build_contact():
    cr = [("/", "Home"), ("/contact/", "Contact")]
    body = f'''<section class="phero"><div class="wrap">{crumbs_html(cr)}<h1>Contact <span class="hl hm">Kiran Growth School</span></h1>
<p class="lead">All enquiries are handled on WhatsApp at {SITE["phone"]}. Send your business name, city and what you want to grow, and we'll reply with a free plan. You can also call or email.</p>
<div class="ctas">{wa_btn("Hi Kiran Growth School, I have an enquiry.", "WhatsApp " + SITE["phone"])}<a class="btn b-white" href="tel:{SITE["phone_e164"]}">{I["phone"]}Call now</a></div></div></section>
<div style="height:60px"></div>
{contact_block()}
<section class="sec" style="padding-top:0"><div class="wrap"><div class="head"><div>{tag("Service areas", "var(--pink)")}<h2>We work with businesses in</h2></div></div>{city_links()}</div></section>'''
    ld = {"@type": "ContactPage", "url": U + "/contact/", "name": "Contact Kiran Growth School", "about": {"@id": ORG_ID}}
    page("/contact/", "Contact Kiran Growth School | WhatsApp +91 93998 51765 | Marketing Agency",
         "Contact Kiran Growth School, a digital and performance marketing agency. WhatsApp or call +91 93998 51765, email founder@kirangrowthschool.com. Mon to Sat, 10 AM to 7 PM.",
         body, schema=[ld, crumbs_schema(cr)])

def build_404():
    body = f'<section class="phero"><div class="wrap"><h1>Page not <span class="hl hc">found</span></h1><p class="lead">The page you were looking for has moved. Try the links below or message us on WhatsApp.</p><div class="ctas"><a class="btn b-sun" href="/">Home</a><a class="btn b-white" href="/services/">Services</a><a class="btn b-white" href="/blog/">Blog</a>{wa_btn("Hi, I could not find a page on your website.", "WhatsApp us")}</div></div></section>'
    page("/404.html", "Page not found | Kiran Growth School", "Page not found.", body)
    PAGES.remove("/404.html")

def build_meta_files(posts):
    lastmod = TODAY.isoformat()
    post_dates = {f"/blog/{p['slug']}/": p.get("updated", p["date"]) for p in posts}
    def pri(p):
        return "1.0" if p == "/" else "0.9" if p.startswith(("/services/", "/solar", "/real-estate", "/locations/")) else "0.7" if p.startswith("/blog/") else "0.5"
    urls = "".join(f"<url><loc>{U}{p}</loc><lastmod>{post_dates.get(p, lastmod)}</lastmod><priority>{pri(p)}</priority></url>" for p in PAGES)
    (ROOT / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n', encoding="utf-8")
    bots = ["GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "Claude-SearchBot", "Claude-User", "anthropic-ai", "PerplexityBot", "Perplexity-User", "Google-Extended", "Bingbot", "Applebot", "Applebot-Extended", "CCBot", "meta-externalagent"]
    robots = "User-agent: *\nAllow: /\n\n" + "".join(f"User-agent: {b}\nAllow: /\n\n" for b in bots) + f"Sitemap: {U}/sitemap.xml\n"
    (ROOT / "robots.txt").write_text(robots, encoding="utf-8")
    svc = "\n".join(f"- [{s['name']}]({U}/services/{s['slug']}/): {s['desc']}" for s in SERVICES)
    loc = "\n".join(f"- [Performance marketing agency in {c['name']}]({U}/locations/{c['slug']}/): solar and real estate marketing in {c['name']} ({c['state']}). DISCOM: {c['discom']}. RERA: {c['rera']}." for c in CITIES)
    blog = "\n".join(f"- [{p['title']}]({U}/blog/{p['slug']}/): {p['description']}" for p in posts)
    llms = f"""# Kiran Growth School

> Kiran Growth School is a performance marketing agency in India for solar companies and real estate businesses. Services: Meta Ads (Facebook & Instagram), Google Ads, website design, AI video production, AI avatar videos and AI automation (WhatsApp bots, CRM and follow-up). Serves Delhi, Delhi NCR (Gurugram, Ghaziabad, Noida, Faridabad) and Madhya Pradesh (Bhopal, Rewa, Satna). Founded by {SITE['founder']}. All enquiries: WhatsApp {SITE['phone']} (https://wa.me/{SITE['wa']}).

Key facts:
- Primary business: performance marketing agency (lead generation for solar installers/EPCs, real estate builders, brokers and channel partners).
- Secondary: an academy with two courses, Meta Ads & Digital Marketing (₹25,000) and AI Tools & Website Design (₹25,000).
- Contact: WhatsApp / call {SITE['phone']}, email {SITE['email']}, {SITE['hours']}.
- Founder: {SITE['founder']} ({SITE['linkedin']}).

## Industries
- [Solar marketing agency]({U}/solar-marketing-agency/): rooftop solar and PM Surya Ghar subsidy lead generation for installers and EPCs.
- [Real estate marketing agency]({U}/real-estate-marketing-agency/): RERA-compliant property lead generation for builders, brokers and channel partners.

## Services
{svc}

## Locations
{loc}

## Blog
{blog}

## Optional
- [Courses]({U}/courses/): Meta Ads & Digital Marketing and AI Tools & Website Design, ₹25,000 each.
- [Sitemap]({U}/sitemap.xml)
"""
    (ROOT / "llms.txt").write_text(llms, encoding="utf-8")

def main():
    posts = load_posts()
    build_home(posts)
    build_services()
    build_industries(posts)
    build_locations(posts)
    build_courses()
    build_about()
    build_contact()
    build_blog(posts)
    build_404()
    build_meta_files(posts)
    print(f"Built {len(PAGES)} pages, {len(posts)} published posts ({TODAY} IST)")

if __name__ == "__main__":
    main()
