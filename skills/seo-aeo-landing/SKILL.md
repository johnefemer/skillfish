---
name: seo-aeo-landing
description: Make a landing page or marketing site findable by search engines and AI assistants (SEO and AEO, answer engine optimisation), end to end, the way Betopia did it for beto.sh. Covers the positioning choice first (what the buyer searches for, not the company name), head tags (title, description, canonical, Open Graph, Twitter, hreflang), JSON-LD structured data generated from what the page actually shows (WebSite, WebPage, Organization, Service or Product with offers, SoftwareApplication, FAQPage, BreadcrumbList, LocalBusiness), llms.txt and llms-full.txt for language models, robots.txt with named AI crawlers and content signals, sitemap.xml, canonical host redirects and noindex for old pages, tests that keep structured data and the visible page in step, an audit script for local files and the live site, live checks as AI crawlers, and the Search Console and share-debugger steps after launch. Includes app-store presence for pages that sell a mobile app (ASO basics, smart banners, deep-link files, MobileApplication schema). Use this whenever someone asks for SEO, AEO, GEO, "AI ready" or "LLM ready" pages, llms.txt, JSON-LD, schema.org, rich results, structured data, meta tags, Open Graph or share previews, robots.txt, AI crawlers (GPTBot, ClaudeBot, PerplexityBot), sitemaps, Search Console, or "make the site show up in Google or ChatGPT", on any landing page, product site or web app, even if they only say "fix the SEO headers" or "promote X in search".
---

# SEO and AEO for a landing page

This is the playbook Betopia used on beto.sh in November 2026, written so it works on any
landing page, product site or small marketing site, whatever the stack. Search engines read the
head tags, structured data, robots.txt and sitemap. AI assistants (ChatGPT, Claude, Perplexity,
Gemini, Copilot) read the same things, plus `llms.txt`, and they quote plain, factual text far
more readily than marketing copy.

Read these as you reach them:

- `references/head-tags.md`: the head block as a template, lengths, Open Graph image rules,
  hreflang for bilingual sites. Step 3.
- `references/structured-data.md`: JSON-LD templates by page type, how the nodes link, what
  Google still shows as rich results, and what never to mark up. Step 4.
- `references/ai-files.md`: `llms.txt`, `llms-full.txt`, robots.txt with AI crawlers and
  content signals, the sitemap, and CDN quirks (Cloudflare). Steps 5 and 6.
- `references/app-store.md`: only when the page sells a mobile app. Store badges, smart app
  banners, deep-link files, MobileApplication schema, keeping the store listing and the page
  saying the same thing.
- `references/tests.md`: tests that fail when the page and its structured data drift apart.
  Step 8.
- `references/beto-record.md`: what was actually done on beto.sh, with the files and the
  lessons. Use it as the worked example.

`python3 -I scripts/audit.py <site-root-or-url>` checks a built site folder or a live site:
head tags, JSON-LD, FAQ match, robots groups, sitemap, llms.txt, and (live) content types and
AI crawler access. Run it at step 9 and again after the deploy.

## Before you start: gates

- **Deploys need the owner's go.** Do the work, run the checks, then ask.
- **Allowing AI training is the owner's call**, not a default. Search and assistant access
  (`search=yes, ai-input=yes`) is what a landing page wants; `ai-train` is a business choice.
  Ask once, write down the answer.
- **Never invent facts for markup.** No ratings, review counts, prices, awards, client logos or
  founding dates that the page does not show and the owner has not confirmed. Fake
  `aggregateRating` gets a manual action from Google and gets quoted by AI as fact.
- **Google Search Console, Bing Webmaster Tools and the share debuggers are the user's
  accounts.** Tell them what to submit; do not sign in for them.
- **CDN dashboard switches** (Cloudflare "Block AI bots", managed robots.txt, bot fight mode)
  are account settings. Report what you find; change nothing without a yes.
- **Respect project rules about names.** Some projects must not name a vendor, platform or
  parent company in anything a visitor sees, metadata included. Grep for it before deploy.

## 1. Discover

| Fact | Where it comes from |
| --- | --- |
| Canonical host (one, https, with or without www) | Domain config, existing canonical tags, the owner |
| Other hosts serving the same build | Previews, staging, old domains, `*.pages.dev`, `*.vercel.app`, `workers.dev` |
| Pages and which are public | Router, `public/`, the nav; private ones: admin, desk, API, thank-you, drafts |
| What the buyer searches for | The owner's words, the hero line, the offer. Usually a category ("private AI for your enterprise"), not the brand |
| Brand, parent company, product names | Page copy; and whether the parent should appear at all |
| Languages and regions | `<html lang>`, copy, the market |
| Facts AI may quote | Plans, channels, languages, where it runs, how to start, contact |
| FAQ | The visible FAQ on the page. Structured data copies it word for word |
| Prices | Public or "priced in a call". Only public prices go in markup |
| Social image | An existing 1200x630 image, or one to make |
| Stack | Static HTML, SSR framework (Next, Astro, Nuxt), SPA. SPAs need server-rendered head tags or prerendering |
| Hosting and CDN | Cloudflare adds its own robots.txt lines and may block AI bots |
| A mobile app | Store links, bundle IDs. If yes, read `references/app-store.md` |

## 2. Decide

Settle these with the owner before writing tags. One line each in the project docs.

1. **The search phrase.** Title and description lead with the phrase the buyer would type; the
   brand goes last (`Private AI for your enterprise · Beto`). One phrase per page.
2. **Which name appears.** Product brand only, or product plus parent company. On beto.sh the
   owner removed the parent company from every SEO header so the product stood on its own.
3. **Indexable pages.** Usually the home page and the main app or product pages. Old or
   duplicate pages get `noindex`; preview paths get a 301.
4. **AI access.** Search and answer use: yes. Training: the owner decides.
5. **Private paths.** Everything under `/api/`, admin, staff tools, form endpoints: disallowed in
   every robots group.

## 3. Head tags

Per indexable page: `<html lang>`, `<title>`, meta description, canonical, Open Graph,
Twitter card, theme colour, and `<link rel="alternate" type="text/markdown" href="/llms.txt">`.
Bilingual pages add hreflang. Templates and lengths: `references/head-tags.md`.

Rules that bite: the canonical is absolute and points at the canonical host; `og:image` is an
absolute URL; head tags must be in the server HTML, not injected by client JavaScript.

## 4. Structured data

One `<script type="application/ld+json">` per page holding an `@graph`, nodes linked by `@id`
(`https://host/#website`, `#webpage`, `#service`, `#faq`). Pick nodes from
`references/structured-data.md`:

- every page: `WebSite` (home only, or referenced by `@id`), `WebPage`
- the offer: `Service` with `OfferCatalog`, or `Product` with `Offer`, or `SoftwareApplication`
  / `WebApplication` for an app page
- the company: `Organization` (or `LocalBusiness` with address and hours, if it has a counter)
- the FAQ: `FAQPage`, generated from the visible FAQ, word for word
- deeper pages: `BreadcrumbList`

Generate the FAQ JSON-LD from the page's own FAQ markup (a build step, a script, or by hand
with a test that compares them). Never mark up text the visitor cannot see.

## 5. Files for AI assistants

- `/llms.txt`: a markdown guide for language models: `# Name`, a `>` summary, a short list of
  facts, then `##` sections of links (absolute URLs). The format is from llmstxt.org.
- `/llms-full.txt`: the whole offer as plain markdown, including the FAQ verbatim, so an
  assistant can answer without rendering the page.
- `<link rel="alternate" type="text/markdown" title="Guide for AI assistants" href="/llms.txt">`
  on every page that the guide describes.

Templates and writing rules: `references/ai-files.md`. Write facts, not slogans: "Bangla and
English, typed or spoken" gets quoted; "seamless multilingual magic" does not.

## 6. robots.txt and sitemap.xml

- robots.txt: a `*` group, then one named group listing the AI crawlers, **repeating every
  rule** (a named group replaces `*` for that bot, it does not add to it). Content signals line
  if the owner wants to state AI use. `Sitemap:` with an absolute URL.
- sitemap.xml: indexable pages only, absolute canonical URLs, `lastmod` as the real date of the
  last content change.

Template, crawler list with what each one does, and Cloudflare notes: `references/ai-files.md`.

## 7. Hosts, redirects and noindex

- Every other host 301s to the canonical host, keeping the path (API paths may stay on any host
  if integrations call them).
- Preview or renamed paths (`/next/`, `/v2/`) 301 to the real page.
- Old pages kept for reference: `<meta name="robots" content="noindex">`, and out of the
  sitemap and llms.txt.
- Staging and preview hosts: `X-Robots-Tag: noindex` header, or basic auth.

## 8. Tests

Add tests so the facts cannot drift (`references/tests.md` has templates for vitest, plain
Node and pytest):

- JSON-LD parses, has the expected node types, and its URLs use the canonical host.
- FAQPage equals the visible FAQ, question and answer, word for word.
- llms-full.txt contains every FAQ entry.
- llms.txt starts with `# ` and `> `, and every link is absolute.
- Every robots group disallows the private paths, and robots names the sitemap.
- The sitemap lists exactly the indexable pages.
- Each indexable page links llms.txt and has one canonical.

## 9. Audit, deploy, verify live

1. `python3 -I scripts/audit.py <built-site-folder> --host https://example.com` before the deploy.
   Add `--forbid "vendorname|platform"` when the project has a no-names rule.
2. Run the project's own checks, then ask for the deploy.
3. After the deploy: `python3 -I scripts/audit.py https://example.com`. It fetches each page in
   the sitemap, checks content types (`text/plain` or `text/markdown` for llms files,
   `application/xml` or `text/xml` for the sitemap), and fetches `/` and `/llms.txt` with the
   GPTBot, ClaudeBot, PerplexityBot and Googlebot user agents.
4. Read the live robots.txt yourself. A CDN may prepend its own lines (Cloudflare's managed
   robots.txt adds a comment block, and with "Block AI bots" on, `Disallow` groups for AI
   crawlers). If the live file blocks what the repo allows, report it with the dashboard
   setting to change.
5. A 200 for a spoofed user agent is a good sign, not proof: real crawlers come from their own
   networks, and bot management can treat them differently.

## 10. After launch (the user does these)

- Google Search Console: add the property, submit `/sitemap.xml`, URL Inspection then
  "Request indexing" for the home page.
- Rich Results Test (search.google.com/test/rich-results) and the Schema Markup Validator
  (validator.schema.org) on each page.
- Bing Webmaster Tools: submit the sitemap; Bing feeds Copilot and several assistants.
  IndexNow is optional for frequent updates.
- Share previews: Facebook Sharing Debugger, LinkedIn Post Inspector, and a test post in
  WhatsApp or Slack. Each caches the old image until re-scraped.
- A month later: Search Console queries and pages. If the search phrase is not showing, revisit
  step 2.

## Report

End with: what is live (files, pages, deploy version), what the audit printed, what the live
check as AI crawlers returned, the decisions still open (training, unconfirmed claims, old
pages), and the after-launch steps for the user.

## Lessons from beto.sh

- Leading with the category phrase ("Private AI for your enterprise") instead of the brand was
  the owner's main ask. Do it in title, description, og:title, WebPage name and llms.txt alike.
- A named robots group replaces `*`; forgetting to repeat `Disallow: /api/` there opens the API
  to exactly the bots you named.
- Cloudflare's managed robots.txt prepends a comment block to yours. Harmless when it is only
  comments; check after every deploy.
- Generate the FAQ markup from the page and test it. Hand-copied FAQ JSON drifts within a week.
- Google shows FAQ rich results only for a few authoritative sites since 2023. FAQPage is still
  worth having: it is how assistants pick up the answers. Do not promise rich results.
- Workers or Vite projects without `node:fs` in tests: import the files with `?raw`.
- Keep the old landing page reachable if the owner wants it, but `noindex` it and keep it out
  of the sitemap and llms.txt, or it competes with the new one.
