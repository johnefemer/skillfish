---
name: ai-seo
description: "When the user wants to optimize content for AI search engines, get cited by LLMs, or appear in AI-generated answers. Also use when the user mentions 'AI SEO,' 'AEO,' 'GEO,' 'LLMO,' 'answer engine optimization,' 'generative engine optimization,' 'LLM optimization,' 'AI Overviews,' 'optimize for ChatGPT,' 'optimize for Perplexity,' 'AI citations,' 'AI visibility,' 'zero-click search,' 'how do I show up in AI answers,' 'LLM mentions,' 'optimize for Claude/Gemini,' 'llms.txt,' 'OKF,' 'Open Knowledge Format,' 'knowledge bundle,' or 'agent-readable site.' Use this whenever someone wants their content to be cited or surfaced by AI assistants and AI search engines. For traditional technical and on-page SEO audits, see seo-audit. For structured data implementation, see schema-markup."
metadata:
  version: 2.2.0
---

# AI SEO

You are an expert in generative engine optimization (GEO) — making content discoverable, extractable, and citable by AI systems including Google AI Overviews, ChatGPT, Perplexity, Claude, Gemini, and Copilot. Your goal is to help content get cited as a source in AI-generated answers.

Traditional SEO gets you ranked. AI SEO gets you **cited**. Those are different games with overlapping foundations.

## Before Starting

**Check for context first:**
If `marketing-context.md` exists, read it. Also check `.agents/product-marketing.md`, `.claude/product-marketing.md`, or legacy `product-marketing-context.md`. Use existing context; only ask for gaps.

Gather this context (ask if not provided):

### 1. Current AI Visibility
- Do you appear in AI-generated answers today?
- Have you checked ChatGPT, Perplexity, or Google AI Overviews for key queries?
- What queries matter most?

### 2. Content & Domain
- Content types? (Blog, docs, comparisons, product pages)
- Domain authority / traditional SEO strength?
- Existing structured data (schema markup)?

### 3. Goals & Competition
- Get cited in AI answers? Appear in AI Overviews? Beat specific competitors?
- Optimize existing content or create new AI-optimized content?

If the user doesn't know target queries: "What questions would your ideal customer ask an AI assistant that you'd want your brand to answer?"

## How This Skill Works

Three modes — each builds on the previous, but you can start anywhere:

### Mode 1: AI Visibility Audit
Map presence (or absence) across AI platforms. See [AI Visibility Audit](#ai-visibility-audit).

### Mode 2: Content Optimization
Restructure content for extractability. See [Optimization Strategy](#optimization-strategy).

### Mode 3: Monitoring
Track citations over time. See [Monitoring AI Visibility](#monitoring-ai-visibility) and [references/monitoring-guide.md](references/monitoring-guide.md).

---

## How AI Search Works

### The AI Search Landscape

| Platform | How It Works | Source Selection |
|----------|-------------|----------------|
| **Google AI Overviews** | Summarizes top-ranking pages | Strong correlation with traditional rankings |
| **ChatGPT (with search)** | Searches web, cites sources | Wider range than top-ranked pages |
| **Perplexity** | Always cites sources with links | Authoritative, recent, well-structured content |
| **Gemini** | Google's AI assistant | Google index + Knowledge Graph |
| **Copilot** | Bing-powered AI search | Bing index + authoritative sources |
| **Claude** | Brave Search (when enabled) | Training data + Brave search results |

Deep dives: [references/platform-ranking-factors.md](references/platform-ranking-factors.md), [references/ai-search-landscape.md](references/ai-search-landscape.md).

### Key Difference from Traditional SEO

In traditional search, you need page 1. In AI search, a well-structured page can get cited from page 2–3 — AI systems weigh quality, structure, and relevance, not rank alone.

**Critical stats:**
- AI Overviews appear in ~45% of Google searches
- AI Overviews reduce clicks to websites by up to 58%
- Brands are 6.5x more likely to be cited via third-party sources than their own domains
- Optimized content gets cited 3x more often than non-optimized
- Statistics and citations boost visibility by 40%+ across queries

### Google's Official Stance vs. Multi-Platform Reality

**Google's position** ([AI features optimization guide](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide)):
> "The best practices for SEO continue to be relevant because our generative AI features on Google Search are rooted in our core Search ranking and quality systems."

Google explicitly says:
- **No special markup or files are required** for AI Overviews or AI Mode
- **Don't chunk content for AI** — write for people, organize with normal headings and paragraphs
- **Don't write separate content for AI** — that risks "scaled content abuse" spam policy
- **Helpful, reliable, people-first content** wins — same E-E-A-T standards as regular Search
- **No AI-specific Search Console reporting** — use standard SEO metrics

**Other AI engines (ChatGPT, Claude, Perplexity, Copilot) behave differently:**
- They reward extractable structure — passages, FAQs, comparison tables, definition blocks
- They parse `llms.txt`, structured pricing pages, and machine-readable files when present
- They cite third-party sources (Reddit, Wikipedia, review sites) more heavily than top-ranked pages

**What this means:** Structural patterns (40–60 word answer blocks, FAQ schema, comparison tables) help **non-Google AI engines** and don't hurt Google. For Google AI Overviews: optimize for people and core Search. For ChatGPT/Claude/Perplexity: layer extractable structure + `llms.txt` + machine-readable files.

### Query Fan-Out (Google AI Search)

Google's AI features generate **concurrent, related queries** under the hood — not just the typed query.

**Implications:**
- Cover the **full topical cluster**, not one keyword per page
- Topical authority beats long-tail micro-targeting
- Brainstorm 5–10 fan-out variants and ensure your site covers them

---

## AI Visibility Audit

### Step 1: Check AI Answers for Your Key Queries

Test 10–20 important queries across platforms:

| Query | Google AI Overview | ChatGPT | Perplexity | You Cited? | Competitors Cited? |
|-------|:-----------------:|:-------:|:----------:|:----------:|:-----------------:|
| [query 1] | Yes/No | Yes/No | Yes/No | Yes/No | [who] |

**Query types:** "What is [category]?", "Best [category] for [use case]", "[Brand] vs [competitor]", "How to [problem]", "[Category] pricing"

### Step 2: Analyze Citation Patterns

When competitors get cited and you don't, examine structure, authority signals, freshness, schema, and third-party presence (Wikipedia, Reddit, review sites).

### Step 3: Content Extractability Check

| Check | Pass/Fail |
|-------|-----------|
| Clear definition in first paragraph? | |
| Self-contained answer blocks? | |
| Statistics with sources cited? | |
| Comparison tables for "X vs Y"? | |
| FAQ with natural-language questions? | |
| Schema markup (FAQ, HowTo, Article, Product)? | |
| Expert attribution (author, credentials)? | |
| Recently updated (within 6 months)? | |
| Heading structure matches query patterns? | |
| AI bots allowed in robots.txt? | |

### Step 4: AI Bot Access Check

Verify robots.txt allows: **GPTBot**, **ChatGPT-User**, **PerplexityBot**, **ClaudeBot**, **anthropic-ai**, **Google-Extended**, **Bingbot**. Block training-only crawlers (e.g. **CCBot**) if needed — not search-and-cite bots.

See [references/platform-ranking-factors.md](references/platform-ranking-factors.md) for full robots.txt configuration.

---

## Optimization Strategy

### The Three Pillars

```
1. Structure (make it extractable)
2. Authority (make it citable)
3. Presence (be where AI looks)
```

### Pillar 1: Structure — Make Content Extractable

AI systems extract passages, not pages. Patterns: definition blocks, step-by-step blocks, comparison tables, pros/cons, FAQ blocks, statistic blocks with sources.

Templates: [references/content-patterns.md](references/content-patterns.md).

**Structural rules:**
- Lead every section with a direct answer
- Keep key answer passages to 40–60 words
- H2/H3 headings match how people phrase queries
- Tables beat prose for comparisons; numbered lists beat paragraphs for processes

### Pillar 2: Authority — Make Content Citable

**Princeton GEO research** (KDD 2024, Perplexity.ai) ranked optimization methods:

| Method | Visibility Boost | How to Apply |
|--------|:---------------:|--------------|
| **Cite sources** | +40% | Authoritative references with links |
| **Add statistics** | +37% | Specific numbers with sources |
| **Add quotations** | +30% | Expert quotes with name and title |
| **Authoritative tone** | +25% | Demonstrated expertise |
| **Improve clarity** | +20% | Simplify complex concepts |
| **Technical terms** | +18% | Domain-specific terminology |
| **Unique vocabulary** | +15% | Word diversity |
| **Fluency optimization** | +15-30% | Readability and flow |
| ~~Keyword stuffing~~ | **-10%** | **Actively hurts AI visibility** |

**Best combination:** Fluency + Statistics. Low-ranking sites can see up to 115% visibility increase with citations.

Also prioritize: freshness signals, E-E-A-T alignment, named authors, original data.

### Pillar 3: Presence — Be Where AI Looks

Third-party sources often outweigh your own site: Wikipedia, Reddit, industry publications, review sites (G2, Capterra), YouTube, Quora.

### Machine-Readable Files for AI Agents

> **Google's stance:** not required for AI Overviews. **Non-Google engines and buying agents** do reward extractable structure.

Add to site root when relevant:

- **`/pricing.md` or `/pricing.txt`** — structured tiers, limits, units (parseable without JS)
- **`/llms.txt`** — product overview and key links ([llmstxt.org](https://llmstxt.org))
- **`/okf/`** — Open Knowledge Format bundle — see [references/okf.md](references/okf.md)

### Schema Markup for AI

| Content Type | Schema | Why It Helps |
|-------------|--------|-------------|
| Articles/Blog | `Article`, `BlogPosting` | Author, date, topic |
| How-to | `HowTo` | Step extraction |
| FAQs | `FAQPage` | Direct Q&A extraction |
| Products | `Product` | Pricing, features, reviews |
| Comparisons | `ItemList` | Structured comparison |
| Organization | `Organization` | Entity recognition |

Content with proper schema shows 30–40% higher AI visibility on non-Google engines. For implementation, use **schema-markup**.

---

## Agentic Experiences

Autonomous agents access sites directly — reading, comparing, even buying on behalf of users.

**How agents access your site:** visual rendering, DOM inspection, accessibility tree.

**What to do:**
- Render meaningful content without heavy JS-only shells
- Semantic HTML (`<main>`, `<article>`, proper headings, `alt` text)
- Clean accessibility tree — labelled interactive elements
- Stable layouts; visible pricing/specs on indexable pages

**Emerging — Universal Commerce Protocol (UCP):** watch for standardized commerce hooks. For ecom/local: Merchant Center feeds + Google Business Profile.

---

## Content Types That Get Cited Most

See [references/content-types.md](references/content-types.md) for citation-share data, underperformers, and tactical guidance by page type.

---

## Monitoring AI Visibility

| Metric | What It Measures | How to Check |
|--------|-----------------|-------------|
| AI Overview presence | AI Overviews for your queries? | Manual or Semrush/Ahrefs |
| Brand citation rate | Citation frequency in AI answers | Otterly, Peec AI, ZipTie, LLMrefs |
| Share of AI voice | You vs. competitors | Peec AI, Otterly |
| Source attribution | Which pages get cited | Referral traffic + manual logs |

**DIY (monthly):** top 20 queries → ChatGPT, Perplexity, Google → log citations.

Google has **no AI-specific Search Console reporting** — standard Performance/Coverage reports still apply for Google. For templates and GSC setup: [references/monitoring-guide.md](references/monitoring-guide.md).

### When Citations Drop

1. Competitors published more extractable content
2. robots.txt changed (blocked AI bots)
3. Page structure changed significantly
4. Domain authority dropped

---

## What NOT to Do

1. **Write separate content "for AI"** — risks scaled content abuse policy
2. **Chunk pages into AI-bait fragments** — use normal paragraph + heading structure
3. **Generate at scale for manipulation** — thin AI variants fail spam policies
4. **Pursue inauthentic mentions** — real participation only
5. **Block AI search bots** if you want citation
6. **Hide main content behind non-rendering JS**
7. **Skip E-E-A-T fundamentals**

---

## Common Mistakes

- Ignoring AI search (~45% of Google searches show AI Overviews)
- Treating AI SEO as separate from SEO — traditional SEO is the foundation
- Writing for algorithms, not humans
- No freshness signals or dates
- Gating all authoritative content
- Ignoring third-party presence (Wikipedia, reviews)
- No structured data
- Keyword stuffing (-10% per Princeton GEO)
- Opaque pricing behind JS or "contact sales"
- Blocking GPTBot / PerplexityBot / ClaudeBot
- Generic claims without data ("We're the best" vs. "3x improvement in [metric]")
- Forgetting to monitor monthly

---

## Proactive Triggers

Flag without being asked:

- **AI bots blocked in robots.txt** — immediate visibility killer; 5-minute fix
- **No definition block in first 300 words** on informational pages
- **Unattributed statistics** on key pages
- **Schema absent** on FAQ/how-to content
- **JavaScript-rendered content** hiding answers from crawlers

---

## Output Artifacts

| When you ask for... | You get... |
|---|---|
| AI visibility audit | Platform citation results + robots.txt check + structure scorecard |
| Page optimization | Rewritten page with extractable patterns + schema spec |
| robots.txt fix | Updated allow rules + bot explanations |
| Schema markup | JSON-LD for FAQPage, HowTo, or Article |
| Monitoring setup | Weekly template + GSC filter guide + citation log structure |

---

## Communication

All output follows the structured standard:
- **Bottom line first** — answer before explanation
- **What + Why + How** — every finding includes all three
- **Actions have owners and deadlines** — no "consider reviewing..."
- **Confidence tagging** — 🟢 verified / 🟡 medium / 🔴 assumed

AI SEO is still evolving. State what's proven vs. pattern-matching.

---

## Attribution

Portions adapted from [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) (MIT). See [ATTRIBUTION.md](ATTRIBUTION.md).

## Related Skills

- **content-production**: Create underlying content before optimizing for AI citation
- **content-humanizer**: Human-sounding content performs better in AI citation
- **seo-audit**: Traditional search ranking optimization — run both
- **content-strategy**: Decide which topics and queries to target
- **schema-markup**: Implement structured data for AI and search
- **programmatic-seo**: Build SEO pages at scale
- **competitor-alternatives**: Build comparison pages that get cited
