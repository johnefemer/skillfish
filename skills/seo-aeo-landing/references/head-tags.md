# Head tags

## Template

Replace every `{…}`. Keep the order; it is easy to review.

```html
<!doctype html>
<html lang="{en}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{Search phrase} · {Brand}</title>
<meta name="description" content="{Search phrase}: {what it is, who it is for, the one or two facts that set it apart}.">
<meta name="theme-color" content="{#hex}">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="canonical" href="https://{host}/{path}">
<link rel="alternate" type="text/markdown" title="Guide for AI assistants" href="/llms.txt">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{Brand}">
<meta property="og:url" content="https://{host}/{path}">
<meta property="og:title" content="{Search phrase}">
<meta property="og:description" content="{One sentence for a share card}">
<meta property="og:image" content="https://{host}/{og-image}.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{What the image shows}">
<meta property="og:locale" content="{en_US}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{Search phrase}">
<meta name="twitter:description" content="{Same sentence as og:description}">
<meta name="twitter:image" content="https://{host}/{og-image}.jpg">
<script type="application/ld+json">{ … see structured-data.md … }</script>
</head>
```

## Lengths and wording

| Tag | Aim | Why |
| --- | --- | --- |
| title | 30-60 characters, phrase first, brand last | Google cuts around 600 px; the phrase must survive the cut |
| description | 120-160 characters, phrase in the first 10 words | Snippets cut near 155-160; assistants quote the first sentence |
| og:title | the phrase, no brand needed (`og:site_name` carries it) | Share cards show the site name separately |
| og:description | one sentence, under 110 characters | Cards cut early on phones |

One `<h1>` per page, saying the same thing as the title in human words. Headings in order
(`h2` under `h1`), so assistants can split the page into answerable sections.

## Open Graph image

- 1200x630, JPEG or PNG, under about 1 MB, absolute https URL.
- Text on the image large enough to read at 300 px wide, or no text at all.
- Same image on every page is fine for a landing site; a distinct one per main page is better.
- After changing it, re-scrape in the Facebook Sharing Debugger and LinkedIn Post Inspector.

## Canonical and hosts

- Absolute, https, the canonical host, the clean path (`/chat`, not `/chat/index.html`).
- One canonical per page. A page whose canonical points elsewhere is a duplicate; keep it out of
  the sitemap.
- Old pages: `<meta name="robots" content="noindex">` and no canonical to themselves.

## Two languages

If the page exists in two languages at two URLs:

```html
<link rel="alternate" hreflang="en" href="https://{host}/">
<link rel="alternate" hreflang="bn" href="https://{host}/bn/">
<link rel="alternate" hreflang="x-default" href="https://{host}/">
```

Each language page lists all of them, itself included. If one URL switches language with
JavaScript, there is nothing to hreflang: set `<html lang>` to the default, list both languages in
`WebSite.inLanguage`, and write llms.txt in the default language with the other noted.

## Single-page apps

Crawlers and share scrapers often read only the server HTML. If head tags are set by client
JavaScript, either render them on the server (framework metadata API), prerender the routes,
or keep a static head in `index.html` that is right for the main page.

Framework pointers:
- Next.js App Router: `export const metadata` / `generateMetadata`, `app/robots.ts`,
  `app/sitemap.ts`; JSON-LD as a `<script type="application/ld+json">` in the page component.
- Astro / Nuxt / SvelteKit: the head in the page or layout; robots and sitemap as static files
  or endpoints.
- Plain HTML on a CDN or Worker: write the tags in the file; serve robots, sitemap and llms files
  from the static folder.
