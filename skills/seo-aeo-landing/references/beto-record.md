# Worked example: beto.sh, November 2026

Beto is Betopia Limited's own AI. beto.sh is a Cloudflare Worker with static assets (plain
HTML, no build step): a landing page at `/` and a chat app at `/chat`. The checks live in one
test file, `test/seo.test.ts`.

## What the owner asked

1. "Remove Betopia from SEO headers for beto site; promote Private AI for your Enterprise."
2. "Make beto AI ready website with llms.txt and other AEO ready features and JSON-LD for
   Google."

## What was done

| Piece | Value on beto.sh |
| --- | --- |
| Title | `Private AI for your enterprise · Beto` |
| Description | "Private AI for your enterprise: an AI of your own that knows your business, answers with sources in Bangla and English, runs where you choose, and works your website, phone line and front desk." |
| Open Graph | `og:site_name` Beto, `og:title` the phrase, mascot image, `summary_large_image` |
| Chat page | `Beto · Chat with a private AI`, its own description and OG tags |
| JSON-LD, home | `@graph`: WebSite `#website`, WebPage `#webpage`, Service `#service` (Brand Beto, Bengali and English, eight industries, OfferCatalog Starter / Business / Enterprise with no prices because they are scoped in a call), FAQPage `#faq` from the seven visible `<details>` entries |
| JSON-LD, chat | WebApplication, free, price 0, `isPartOf` the website |
| No Organization node | the owner wanted the product to stand without the parent company |
| `/llms.txt` | summary, seven facts, Pages, Sample company AIs, Full text, Optional (sales email) |
| `/llms-full.txt` | the whole landing page as markdown, FAQ verbatim |
| `/robots.txt` | `*` group plus one named group of 15 AI crawlers, both `Disallow: /api/` and `/desk/`, `Content-Signal: search=yes, ai-input=yes, ai-train=yes`, Sitemap |
| `/sitemap.xml` | `/` and `/chat` |
| Old landing | kept at `/beto/` with `noindex` |
| Preview path | `/next` 301 to `/` |
| Other hosts | `www.beto.sh` and `beto.betopia.dev` 301 to `beto.sh` except `/api/*` |
| Tests | 8: JSON-LD shape, FAQ equals the page, chat is a WebApplication, llms.txt shape and absolute links, llms-full has each FAQ entry, both pages link llms.txt, every robots group disallows the private paths, sitemap contents |

## Live checks after the deploy

- `/robots.txt`, `/sitemap.xml`, `/llms.txt`, `/llms-full.txt`: 200, right content types.
- One JSON-LD script on `/`, parses.
- Cloudflare's managed robots.txt prepended a comment-only block; no blocking groups.
- GPTBot, ClaudeBot, PerplexityBot and Googlebot user agents: 200 on `/` and `/llms.txt`.

## Lessons

- The project had a rule that pages never name the vendor platform behind the product, and it
  applied to metadata too. A grep of the static folder for those names ran before every deploy
  (the audit script's `--forbid`).
- The FAQ test strips tags and decodes `&amp;`, `&#39;` and `&rsquo;` before comparing, so an
  entity in the HTML does not read as a mismatch. Write the JSON from the page, not by hand.
- The training signal (`ai-train=yes`) was set and left as an open decision for the owner.
  Ask early.
- Markup and llms files repeat the page's claims to machines that quote them. Get numbers and
  capability claims confirmed by the owner before they go into either.
- One zone of the account was served to local visitors from a colo in another country, while
  another zone was served locally. Not an SEO issue as such, but speed is a ranking signal:
  check the `cf-ray` suffix (the colo) on the live host from the target market.
