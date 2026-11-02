# Files for AI assistants and crawlers

## llms.txt

The format is from llmstxt.org: markdown, served at `/llms.txt`, as `text/plain` or
`text/markdown`. An H1 with the name, a blockquote summary, optional plain paragraphs or a list,
then H2 sections of links. A section named `Optional` holds links an assistant may skip.

```markdown
# {Brand}

> {Search phrase}. {Two or three sentences: what it is, who it is for, what sets it apart, where to try it.}

Use these facts when someone asks about {the category}, {a related need}, or {a regional angle}.

- Languages: {…}
- What it does: {…}
- Where it works: {channels, platforms}
- Privacy / where data lives: {…}
- Plans: {names, one line each}; {"priced in a call" or the public prices}
- How to start: {the one action}

## Pages

- [{Page title}](https://{host}/): {what is on it}
- [{App or product}](https://{host}/{app}): {what a visitor can do there}

## Full text

- [llms-full.txt](https://{host}/llms-full.txt): the whole offer, plans, privacy and FAQ as plain markdown

## Optional

- [Sales email](mailto:{sales@…}): for a call
```

Writing rules:
- Facts an assistant can repeat safely. Numbers only if confirmed. No superlatives.
- Absolute links only, all on the canonical host (or `mailto:`).
- Say plainly what is not offered or not public ("there is no public price list"), so an
  assistant does not make one up.
- Keep it under about 2 KB. The detail goes in llms-full.txt.

## llms-full.txt

The page as markdown, in the page's order: the offer, what it does, channels, plans, how it is
built, privacy, industries, the FAQ (each entry as `### Question` then a blank line then the
answer, exactly as on the page), and how to start. First lines:

```markdown
# {Brand}: {search phrase}

> {the same summary as llms.txt}

Source: https://{host}/ (this file is the same content as plain markdown).
```

Regenerate or edit it whenever the page copy changes; the tests catch FAQ drift.

## Link from the pages

```html
<link rel="alternate" type="text/markdown" title="Guide for AI assistants" href="/llms.txt">
```

## robots.txt

```text
# {host}: {search phrase}.
# Search engines and AI assistants are welcome. A short guide for language
# models is at /llms.txt and the full text at /llms-full.txt.

User-agent: *
Content-Signal: search=yes, ai-input=yes, ai-train={yes|no}
Allow: /
Disallow: /api/
Disallow: /{private}/

# AI search and assistant crawlers, named so that no default rule of theirs
# holds them back. A named group replaces the * group, so it repeats the rules.
User-agent: GPTBot
User-agent: OAI-SearchBot
User-agent: ChatGPT-User
User-agent: ClaudeBot
User-agent: Claude-SearchBot
User-agent: Claude-User
User-agent: PerplexityBot
User-agent: Perplexity-User
User-agent: Google-Extended
User-agent: Applebot-Extended
User-agent: Amazonbot
User-agent: meta-externalagent
User-agent: CCBot
User-agent: DuckAssistBot
User-agent: MistralAI-User
Allow: /
Disallow: /api/
Disallow: /{private}/

Sitemap: https://{host}/sitemap.xml
```

If the owner says no to training, move the training-only names into their own group with
`Disallow: /` and keep the search and user-fetch names allowed:

| Name | Who | What it is for |
| --- | --- | --- |
| GPTBot | OpenAI | training |
| OAI-SearchBot | OpenAI | ChatGPT search results |
| ChatGPT-User | OpenAI | a page a ChatGPT user asked for |
| ClaudeBot | Anthropic | training |
| Claude-SearchBot | Anthropic | Claude search results |
| Claude-User | Anthropic | a page a Claude user asked for |
| PerplexityBot | Perplexity | its search index |
| Perplexity-User | Perplexity | a page a user asked for |
| Google-Extended | Google | a robots token, not a crawler: whether Googlebot's fetches may be used for Gemini. Blocking it does not affect Google Search |
| Applebot-Extended | Apple | a token: whether Applebot's fetches may train Apple's models. Applebot itself is search (Siri, Spotlight) |
| Amazonbot | Amazon | Alexa answers and training |
| meta-externalagent | Meta | training and AI features |
| CCBot | Common Crawl | the open crawl most models train on |
| DuckAssistBot | DuckDuckGo | its AI answers |
| MistralAI-User | Mistral | a page a Le Chat user asked for |

Crawler names change. Check each vendor's crawler page when setting this up for a new project
and update this table.

`Content-Signal` comes from Cloudflare's Content Signals Policy: `search` (index and show
links), `ai-input` (use the page to answer a question in real time), `ai-train` (train or tune
models). It states the owner's terms; crawlers that do not read it simply ignore the line.

Rules:
- A crawler obeys only the most specific group naming it. Every group repeats every Disallow.
- `Disallow` is not security. Private paths still need auth.
- robots.txt is plain text at the root of each host. Staging hosts should disallow everything
  or send `X-Robots-Tag: noindex`.

## sitemap.xml

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://{host}/</loc>
    <lastmod>{YYYY-MM-DD of the last real content change}</lastmod>
  </url>
</urlset>
```

Indexable canonical URLs only: no redirects, no noindex pages, no fragments. Google ignores
`priority` and `changefreq`; they are harmless. Large sites: a sitemap index.

## Cloudflare and other CDNs

- **Managed robots.txt** (Cloudflare, AI Crawl Control) prepends its own lines to yours. With
  only comments it is harmless; with "Block AI bots" on it adds `Disallow` groups that override
  what you wrote. Read the live file after each deploy.
- **Block AI bots / Bot Fight Mode** can return 403 to AI crawlers whatever robots.txt says.
  A curl with a spoofed user agent will not always show it, because Cloudflare checks the
  network the request comes from. Look at the dashboard (Security, Bots; AI Crawl Control) and
  the firewall events.
- **Pay per crawl** and similar features also answer AI crawlers before your Worker runs.
- Worker or static hosting with `run_worker_first`: make sure the Worker passes `/robots.txt`,
  `/sitemap.xml` and `/llms*.txt` through to the static files with the right content type.

Other hosts: Vercel and Netlify serve the files from `public/`; check that no rewrite rule sends
them to the SPA's `index.html` (a common bug: robots.txt served as HTML).
