# SEO playbook: go-live, sitelinks and backlinks

Nobody can guarantee a top-3 ranking. Rankings come from three things: a technically clean site (done), useful content published consistently (2 blogs a day, running), and **trust signals from other websites** (backlinks, reviews, citations), which need the steps below.

## 1. Go live (once)

**Hostinger Git auto-deploy (recommended)**
1. hPanel → Websites → kirangrowthschool.online → **Files → File Manager**: back up, then empty `public_html` (Hostinger needs an empty folder for Git deploy).
2. hPanel → **Advanced → Git** → Repository `https://github.com/lasthopekish-cyber/kiran-growth-school-site.git`, Branch `main`, Directory: leave empty → **Create**.
3. Click **Deploy** once, then **Auto Deployment** → copy the webhook URL → GitHub repo → Settings → Webhooks → Add webhook → paste URL, content type `application/json`, "Just the push event" → Add.
4. Every push to `main` (including the daily blogs) now goes live automatically.

Check: https://kirangrowthschool.online/sitemap.xml and https://kirangrowthschool.online/blog/ should load.

## 2. Google and Bing (once, 15 minutes)

1. **Google Search Console** → Add property → URL prefix `https://kirangrowthschool.online/` → HTML tag method → copy the `content="..."` value into `google_verification` in `build/data.py` → rebuild and push → Verify. Then **Sitemaps → submit `sitemap.xml`**.
2. **Bing Webmaster Tools** → Import from Google Search Console (one click), or use the meta tag (`bing_verification`). Submit the sitemap. Bing powers ChatGPT search results, so this matters for AI visibility.
3. After going live, run `python3 build/indexnow.py` to notify Bing of every URL.

## 3. Sitelinks

Google chooses sitelinks automatically; they can't be added manually. The site already does what helps:
- Clear top navigation (Services, Solar, Real Estate, Locations, Blog, Courses) and footer links (About, Contact, every service and city)
- Breadcrumb structured data on every page
- Unique, descriptive page titles
- Strong internal linking from home to each section

What you can do: search for **"Kiran Growth School"** regularly so brand searches grow, and keep page titles stable. Sitelinks usually appear once the site gets steady branded searches.

## 4. Google Business Profile (most important for "near me" and city searches)

Create at https://business.google.com:
- Name: **Kiran Growth School**
- Category: **Marketing agency** (add: Internet marketing service, Advertising agency, Website designer, Social media agency)
- Service areas: Delhi, Gurugram, Ghaziabad, Noida, Faridabad, Bhopal, Rewa, Satna
- Phone: +91 93998 51765 · Website: https://kirangrowthschool.online/
- Add services (same names as the website), 10+ photos, and post weekly (reuse blog posts).
- Ask every client for a Google review. Reviews are a top local ranking factor.

## 5. Citations and backlinks (use the exact same name, phone and website everywhere)

**NAP block to copy:**
```
Kiran Growth School
Digital & performance marketing agency (Meta Ads, Google Ads, websites, social media, AI videos, AI automation) for solar, real estate and local businesses.
Phone / WhatsApp: +91 93998 51765
Website: https://kirangrowthschool.online/
Email: founder@kirangrowthschool.com
Areas: Delhi NCR, Gurugram, Ghaziabad, Bhopal, Rewa, Satna
```

**Week 1: free business listings**
- [ ] Google Business Profile
- [ ] Bing Places (bingplaces.com, import from Google)
- [ ] Apple Business Connect
- [ ] Justdial
- [ ] Sulekha
- [ ] IndiaMART (service listing)
- [ ] LinkedIn company page (link to website; add Sitanshu as employee)
- [ ] Facebook page and Instagram bio link
- [ ] YouTube channel (link in description of every video)

**Week 2: agency directories (strong for "marketing agency" searches)**
- [ ] Clutch.co
- [ ] GoodFirms
- [ ] DesignRush
- [ ] Sortlist
- [ ] TechBehemoths
- [ ] Crunchbase

**Ongoing: earned links**
- [ ] Ask every client to add "Marketing by Kiran Growth School" with a link in their website footer
- [ ] Guest articles on solar and real estate industry blogs (offer the existing blog posts as fresh, rewritten guides)
- [ ] Get listed on solar installer and real estate partner directories your clients use
- [ ] Answer questions on Quora and Reddit (r/india, r/solar) with genuine help and a link only when relevant
- [ ] Speak at or sponsor local business events, colleges and associations (CREDAI chapters, solar associations) and ask for a link from the event page
- [ ] Share every new blog on LinkedIn (Sitanshu's profile and the company page)

**Avoid:** buying links, link farms, PBNs, "1,000 backlinks for ₹999" offers and comment spam. These can get the site penalised.

## 6. Monthly check

- Search Console: impressions, top queries, pages not indexed
- Google Business Profile: calls, website clicks, new reviews
- Which blog posts get traffic → write more on those topics
