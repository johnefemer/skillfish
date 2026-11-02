#!/usr/bin/env python3
"""SEO and AEO audit for a landing site: a built folder or a live URL.

  python3 -I audit.py public --host https://example.com
  python3 -I audit.py https://example.com
  python3 -I audit.py https://example.com --pages / /chat --private /api/ /admin/ --forbid "vendor|platform"

Checks each page (from the sitemap, or --pages): lang, title, description, one canonical on the
host, Open Graph and Twitter tags, one h1, llms.txt link, JSON-LD that parses with @ids on the
host, FAQPage entries visible on the page. Then robots.txt (every group disallows the private
paths, sitemap named, AI crawlers named), sitemap.xml, llms.txt and llms-full.txt. Live mode
also checks content types and fetches / and /llms.txt as AI crawlers.

Standard library only. Prints PASS, WARN and FAIL lines; exits 1 if anything FAILs.
"""

import argparse
import html
import json
import pathlib
import re
import sys
import urllib.error
import urllib.request
from html.parser import HTMLParser

AI_BOTS = ["GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "Claude-SearchBot", "Claude-User",
           "PerplexityBot", "Perplexity-User", "Google-Extended", "Applebot-Extended"]
PROBE_UAS = {
    "GPTBot": "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; GPTBot/1.2; +https://openai.com/gptbot)",
    "ClaudeBot": "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; ClaudeBot/1.0; +claudebot@anthropic.com)",
    "PerplexityBot": "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; PerplexityBot/1.0; +https://perplexity.ai/perplexitybot)",
    "Googlebot": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
}

results = {"PASS": 0, "WARN": 0, "FAIL": 0}


def say(level, where, msg):
    results[level] += 1
    print(f"{level:4}  {where:22} {msg}")


def check(ok, where, good, bad, level="FAIL"):
    say("PASS" if ok else level, where, good if ok else bad)
    return ok


# ---------- reading the site ----------

class Source:
    def __init__(self, target, host):
        self.live = re.match(r"^https?://", target) is not None
        self.root = None if self.live else pathlib.Path(target)
        self.host = (host or (target if self.live else "")).rstrip("/")

    def get(self, path, ua=None):
        """(status, content_type, text) for a site path."""
        if self.live:
            req = urllib.request.Request(self.host + path, headers={"User-Agent": ua or "seo-aeo-audit/1.0"})
            try:
                with urllib.request.urlopen(req, timeout=20) as r:
                    return r.status, r.headers.get("content-type", ""), r.read().decode("utf-8", "replace")
            except urllib.error.HTTPError as e:
                return e.code, e.headers.get("content-type", ""), ""
            except Exception as e:  # network errors
                return 0, "", str(e)
        clean = path.split("#")[0].split("?")[0].lstrip("/")
        for cand in ([clean] if "." in clean.split("/")[-1] else [f"{clean}/index.html".lstrip("/"), f"{clean}.html", clean]):
            f = self.root / cand if cand else self.root / "index.html"
            if f.is_file():
                return 200, "", f.read_text("utf-8", "replace")
        return 404, "", ""


class Head(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.meta, self.links, self.ld, self.h1, self.lang = {}, [], [], 0, None
        self.title, self._in, self._buf, self.text = None, None, [], []
        self._skip = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "html":
            self.lang = a.get("lang")
        elif tag == "meta":
            k = a.get("property") or a.get("name")
            if k:
                self.meta.setdefault(k.lower(), []).append(a.get("content", ""))
        elif tag == "link":
            self.links.append(a)
        elif tag == "title":
            self._in, self._buf = "title", []
        elif tag == "script" and a.get("type") == "application/ld+json":
            self._in, self._buf = "ld", []
        elif tag in ("script", "style", "template"):
            self._skip += 1
        elif tag == "h1":
            self.h1 += 1

    def handle_endtag(self, tag):
        if tag == "title" and self._in == "title":
            self.title, self._in = "".join(self._buf).strip(), None
        elif tag == "script" and self._in == "ld":
            self.ld.append("".join(self._buf)); self._in = None
        elif tag in ("script", "style", "template") and self._skip:
            self._skip -= 1

    def handle_data(self, data):
        if self._in:
            self._buf.append(data)
        elif not self._skip:
            self.text.append(data)


norm = lambda s: re.sub(r"\s+", " ", html.unescape(s or "")).replace("’", "'").replace("‘", "'").strip()


def nodes(block):
    if isinstance(block, list):
        for b in block:
            yield from nodes(b)
    elif isinstance(block, dict):
        if "@graph" in block:
            yield from nodes(block["@graph"])
        else:
            yield block


# ---------- checks ----------

def check_page(src, path, forbid):
    where = path
    status, ctype, body = src.get(path)
    if not check(status == 200, where, "found", f"status {status}"):
        return
    if src.live:
        check("text/html" in ctype, where, "served as HTML", f"content-type {ctype!r}")
    h = Head(); h.feed(body)
    check(bool(h.lang), where, f"html lang={h.lang}", "no <html lang>")
    t = h.title or ""
    if check(bool(t), where, f"title ({len(t)} chars)", "no <title>"):
        if not 30 <= len(t) <= 65:
            say("WARN", where, f"title is {len(t)} chars; aim for 30-60, search phrase first")
    d = (h.meta.get("description") or [""])[0]
    if check(bool(d), where, f"description ({len(d)} chars)", "no meta description"):
        if not 110 <= len(d) <= 170:
            say("WARN", where, f"description is {len(d)} chars; aim for 120-160")
    robots = " ".join(h.meta.get("robots", [])).lower()
    noindex = "noindex" in robots
    if noindex:
        say("WARN", where, "noindex: should not be in the sitemap")
    canon = [l.get("href", "") for l in h.links if (l.get("rel") or "").lower() == "canonical"]
    if check(len(canon) == 1, where, "one canonical", f"{len(canon)} canonical tags"):
        c = canon[0]
        check(c.startswith("https://") and (not src.host or c.startswith(src.host)), where,
              f"canonical {c}", f"canonical {c!r} is not absolute https on {src.host or 'the host'}")
    for k in ("og:title", "og:description", "og:url", "og:image", "og:type", "twitter:card"):
        check(k in h.meta, where, f"{k}", f"missing {k}", "WARN" if k in ("og:type", "twitter:card", "og:url") else "FAIL")
    img = (h.meta.get("og:image") or [""])[0]
    if img and not img.startswith("http"):
        say("FAIL", where, f"og:image {img!r} is not an absolute URL")
    check(h.h1 == 1, where, "one h1", f"{h.h1} h1 elements", "WARN")
    check(any((l.get("href") == "/llms.txt" or str(l.get("href", "")).endswith("/llms.txt")) for l in h.links), where,
          "links llms.txt", "no <link rel=alternate href=/llms.txt>", "WARN")
    visible = norm(" ".join(h.text))
    if not h.ld:
        say("WARN" if noindex else "FAIL", where, "no JSON-LD")
    for i, raw in enumerate(h.ld):
        try:
            data = json.loads(raw)
        except json.JSONDecodeError as e:
            say("FAIL", where, f"JSON-LD block {i + 1} does not parse: {e}")
            continue
        ns = list(nodes(data))
        types = [n.get("@type") for n in ns]
        say("PASS", where, f"JSON-LD: {', '.join(map(str, types))}")
        for n in ns:
            nid = n.get("@id")
            if nid and src.host and not nid.startswith(src.host):
                say("WARN", where, f"@id {nid} is not on {src.host}")
            if n.get("aggregateRating") or n.get("review"):
                say("WARN", where, f"{n.get('@type')} has ratings or reviews: confirm they are real and shown on the page")
            if n.get("@type") == "FAQPage":
                qs = n.get("mainEntity") or []
                missing = [q.get("name") for q in qs if norm(q.get("name")) not in visible
                           or norm((q.get("acceptedAnswer") or {}).get("text")) not in visible]
                check(qs and not missing, where, f"FAQPage: {len(qs)} entries, all visible",
                      f"FAQPage entries not visible word for word: {missing[:3]}")
    if forbid:
        m = re.search(forbid, body, re.I)
        check(not m, where, "no forbidden names", f"forbidden name {m.group(0)!r} in the page" if m else "")
    return noindex


def robots_groups(text):
    groups, cur, last_ua = [], None, False
    for line in text.splitlines():
        line = line.split("#")[0].strip()
        if not line or ":" not in line:
            continue
        k, v = [x.strip() for x in line.split(":", 1)]
        k = k.lower()
        if k == "user-agent":
            if not last_ua:
                cur = {"agents": [], "rules": []}; groups.append(cur)
            cur["agents"].append(v); last_ua = True
        else:
            last_ua = False
            if cur is not None and k in ("allow", "disallow"):
                cur["rules"].append((k, v))
    return groups


def check_robots(src, private):
    status, ctype, body = src.get("/robots.txt")
    if not check(status == 200, "/robots.txt", "found", f"status {status}"):
        return []
    if src.live:
        check("text/plain" in ctype, "/robots.txt", "text/plain", f"content-type {ctype!r}")
    groups = robots_groups(body)
    named = {a.lower() for g in groups for a in g["agents"]}
    for g in groups:
        label = ",".join(g["agents"])[:40]
        if ("disallow", "/") in g["rules"]:
            say("WARN", "/robots.txt", f"group {label} disallows the whole site")
            continue
        missing = [p for p in private if ("disallow", p) not in g["rules"]]
        check(not missing, "/robots.txt", f"group {label}: private paths disallowed",
              f"group {label} does not disallow {missing} (a named group replaces *)")
    absent = [b for b in AI_BOTS if b.lower() not in named]
    check(not absent, "/robots.txt", "AI crawlers named", f"not named: {', '.join(absent)}", "WARN")
    check(re.search(r"^content-signal:", body, re.I | re.M) is not None, "/robots.txt", "content signals stated",
          "no Content-Signal line (optional: states search / ai-input / ai-train terms)", "WARN")
    sm = re.findall(r"^sitemap:\s*(\S+)", body, re.I | re.M)
    check(bool(sm) and all(s.startswith("http") for s in sm), "/robots.txt", f"sitemap {sm[0] if sm else ''}",
          "no absolute Sitemap: line")
    if src.live and body.lstrip().startswith("#") and "cloudflare" in body.lower():
        say("WARN", "/robots.txt", "a CDN block is prepended: read it, it may add Disallow groups")
    return groups


def check_sitemap(src):
    status, ctype, body = src.get("/sitemap.xml")
    if not check(status == 200, "/sitemap.xml", "found", f"status {status}"):
        return []
    if src.live:
        check("xml" in ctype, "/sitemap.xml", "XML", f"content-type {ctype!r}", "WARN")
    locs = re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", body)
    check(bool(locs), "/sitemap.xml", f"{len(locs)} URLs", "no <loc> entries")
    for l in locs:
        if src.host and not l.startswith(src.host):
            say("FAIL", "/sitemap.xml", f"{l} is not on {src.host}")
        if "#" in l:
            say("FAIL", "/sitemap.xml", f"{l} has a fragment")
    return locs


def check_llms(src):
    status, ctype, body = src.get("/llms.txt")
    if check(status == 200, "/llms.txt", "found", f"status {status}"):
        if src.live:
            check("text/plain" in ctype or "markdown" in ctype, "/llms.txt", "plain text or markdown", f"content-type {ctype!r}")
        check(re.match(r"^# .+\n\n> .+", body) is not None, "/llms.txt", "title and summary", "does not start with '# Name', a blank line, '> summary'")
        check(re.search(r"^## ", body, re.M) is not None, "/llms.txt", "has ## sections of links", "no ## sections", "WARN")
        rel = [h for h in re.findall(r"\]\(([^)]+)\)", body) if not re.match(r"^(https?://|mailto:)", h)]
        check(not rel, "/llms.txt", "links absolute", f"relative links: {rel[:3]}")
        if len(body) > 4000:
            say("WARN", "/llms.txt", f"{len(body)} bytes; keep it short, the detail goes in llms-full.txt")
    status, ctype, full = src.get("/llms-full.txt")
    check(status == 200, "/llms-full.txt", f"found ({len(full)} bytes)", f"status {status}", "WARN")
    return full if status == 200 else ""


def check_faq_in_full(src, pages, full):
    if not full:
        return
    for p in pages:
        _, _, body = src.get(p)
        h = Head(); h.feed(body)
        for raw in h.ld:
            try:
                for n in nodes(json.loads(raw)):
                    if n.get("@type") == "FAQPage":
                        missing = [q.get("name") for q in n.get("mainEntity") or [] if norm(q.get("name")) not in norm(full)]
                        check(not missing, "/llms-full.txt", f"carries the FAQ of {p}", f"FAQ questions missing: {missing[:3]}", "WARN")
            except json.JSONDecodeError:
                pass


def check_bots(src):
    for name, ua in PROBE_UAS.items():
        for path in ("/", "/llms.txt"):
            status, _, _ = src.get(path, ua)
            check(status == 200, f"as {name}", f"{path} {status}", f"{path} returned {status}: a bot rule or WAF blocks it")
    say("PASS", "note", "a 200 for a spoofed user agent is a good sign, not proof; check the CDN's bot settings")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("target", help="built site folder, or https://host")
    ap.add_argument("--host", help="canonical origin, e.g. https://example.com (required for a folder)")
    ap.add_argument("--pages", nargs="*", help="paths to check (default: the sitemap's, else /)")
    ap.add_argument("--private", nargs="*", default=["/api/"], help="paths every robots group must disallow")
    ap.add_argument("--forbid", help="regex of names that must not appear in pages (e.g. a vendor)")
    a = ap.parse_args()
    src = Source(a.target, a.host)
    if not src.live and not src.host:
        say("WARN", "setup", "no --host: canonical and URL host checks are skipped")
    print(f"Auditing {a.target}" + (f" for {src.host}" if src.host else ""))
    check_robots(src, a.private)
    locs = check_sitemap(src)
    pages = a.pages or ([re.sub(r"^https?://[^/]+", "", l) or "/" for l in locs] if locs else ["/"])
    for p in pages:
        if check_page(src, p, a.forbid) and p in [re.sub(r"^https?://[^/]+", "", l) or "/" for l in locs]:
            say("FAIL", p, "is noindex but listed in the sitemap")
    full = check_llms(src)
    check_faq_in_full(src, pages, full)
    if src.live:
        check_bots(src)
    print(f"\n{results['PASS']} pass, {results['WARN']} warn, {results['FAIL']} fail")
    sys.exit(1 if results["FAIL"] else 0)


if __name__ == "__main__":
    main()
