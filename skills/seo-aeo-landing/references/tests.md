# Tests that keep the page and its markup in step

Pick the template for the project's test runner. Adapt the FAQ regex to the page's FAQ markup
and the private paths to the project.

## Vitest (Vite, Workers, any TypeScript project)

Projects whose types have no `node:fs` (Cloudflare Workers) can import files as text with `?raw`.
Add `declare module '*?raw' { const text: string; export default text }` to a `.d.ts` the tests
see.

```ts
import { describe, expect, it } from 'vitest'
import homeHtml from '../public/index.html?raw'
import llmsFull from '../public/llms-full.txt?raw'
import llms from '../public/llms.txt?raw'
import robots from '../public/robots.txt?raw'
import sitemap from '../public/sitemap.xml?raw'

const HOST = 'https://example.com/'
const PRIVATE = ['/api/', '/admin/']
const text = (h: string) => h.replace(/<[^>]+>/g, '').replace(/&amp;/g, '&').replace(/&#39;|&rsquo;/g, "'").replace(/&quot;/g, '"').trim()
const ldOf = (html: string) =>
  [...html.matchAll(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/g)].map((m) => JSON.parse(m[1]))
const faq = [...homeHtml.matchAll(/<details[^>]*><summary>(.*?)<\/summary><p>(.*?)<\/p><\/details>/g)].map((m) => ({ q: text(m[1]), a: text(m[2]) }))

describe('structured data', () => {
  const graph = ldOf(homeHtml)[0]['@graph'] as Array<Record<string, any>>
  const byType = (t: string) => graph.find((n) => n['@type'] === t)!

  it('describes the site and the page on the canonical host', () => {
    expect(byType('WebSite').url).toBe(HOST)
    for (const n of graph) if (n['@id']) expect(n['@id']).toMatch(new RegExp('^' + HOST))
  })

  it('carries the visible FAQ word for word', () => {
    expect(faq.length).toBeGreaterThan(0)
    const ld = byType('FAQPage').mainEntity.map((q: any) => ({ q: q.name, a: q.acceptedAnswer.text }))
    expect(ld).toEqual(faq)
  })
})

describe('llms.txt', () => {
  it('has a title, a summary and absolute links', () => {
    expect(llms).toMatch(/^# .+\n\n> .+/)
    for (const [, href] of llms.matchAll(/\]\(([^)]+)\)/g)) expect(href).toMatch(new RegExp(`^(${HOST}|mailto:)`))
  })
  it('repeats the FAQ in the full text', () => {
    for (const { q, a } of faq) expect(llmsFull).toContain(`### ${q}\n\n${a}`)
  })
  it('is linked from the page', () => expect(homeHtml).toContain('href="/llms.txt"'))
})

describe('robots and sitemap', () => {
  it('keeps private paths out of every group and names the sitemap', () => {
    for (const group of robots.split(/\n\n+/).filter((g) => g.includes('User-agent:')))
      for (const p of PRIVATE) expect(group).toContain(`Disallow: ${p}`)
    expect(robots).toContain(`Sitemap: ${HOST}sitemap.xml`)
  })
  it('lists the indexable pages', () => expect(sitemap).toContain(`<loc>${HOST}</loc>`))
})
```

## Plain Node (no framework, `node --test`)

```js
import { test } from 'node:test'
import assert from 'node:assert/strict'
import { readFileSync } from 'node:fs'
const read = (p) => readFileSync(new URL('../public/' + p, import.meta.url), 'utf8')
// … the same checks as above, with assert.equal / assert.match / assert.deepEqual
```

## Python projects (pytest)

```python
import json, re, pathlib
ROOT = pathlib.Path(__file__).parent.parent / "public"
def test_faq_matches():
    html = (ROOT / "index.html").read_text()
    blocks = [json.loads(m) for m in re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)]
    ...
```

Or run the skill's audit script in CI: `python3 -I scripts/audit.py public --host https://example.com`
exits non-zero on any FAIL.

## Next.js and other generated heads

Test the generated output, not the source: build, then run the audit script on `.next/server/app`
HTML or on `next start` with the live mode, or render the page in a test and read the head.
