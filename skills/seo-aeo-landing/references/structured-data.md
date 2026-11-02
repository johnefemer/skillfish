# Structured data (JSON-LD)

## Shape

One script per page, one `@graph`, nodes linked by `@id`. IDs are the page URL plus a fragment,
so they are unique and stable.

```json
{
  "@context": "https://schema.org",
  "@graph": [
    { "@type": "WebSite", "@id": "https://{host}/#website", "url": "https://{host}/", "name": "{Brand}",
      "description": "{meta description}", "inLanguage": ["en"],
      "publisher": { "@id": "https://{host}/#org" } },
    { "@type": "WebPage", "@id": "https://{host}/#webpage", "url": "https://{host}/", "name": "{Search phrase}",
      "description": "{meta description}", "isPartOf": { "@id": "https://{host}/#website" },
      "about": { "@id": "https://{host}/#service" },
      "primaryImageOfPage": { "@type": "ImageObject", "url": "https://{host}/{og-image}.jpg" }, "inLanguage": "en" },
    { "@type": "Organization", "@id": "https://{host}/#org", "name": "{Company}", "url": "https://{host}/",
      "logo": "https://{host}/logo.png", "email": "{sales@…}",
      "sameAs": ["https://www.linkedin.com/company/{…}", "https://www.facebook.com/{…}"] }
  ]
}
```

Leave `Organization` out when the owner does not want the company named (beto.sh used only a
`Brand` inside `Service`). Leave out any property you cannot fill truthfully.

## The offer: pick one

**A service sold in plans, priced in a call** (no public prices):

```json
{ "@type": "Service", "@id": "https://{host}/#service", "name": "{Search phrase}",
  "serviceType": "{category}", "description": "{…}", "url": "https://{host}/",
  "brand": { "@type": "Brand", "name": "{Brand}", "logo": "https://{host}/logo.svg" },
  "provider": { "@id": "https://{host}/#org" },
  "areaServed": "Worldwide", "availableLanguage": ["English"],
  "audience": { "@type": "BusinessAudience", "audienceType": "{who buys}" },
  "category": ["{industry}", "{industry}"],
  "hasOfferCatalog": { "@type": "OfferCatalog", "name": "Plans",
    "itemListElement": [
      { "@type": "Offer", "name": "{Plan}", "description": "{one line}",
        "itemOffered": { "@type": "Service", "name": "{Brand}, {Plan} plan", "description": "{what is in it}" } }
    ] } }
```

No `price` on an Offer without a public price. Plan names and lines must match the page.

**A product with public prices:**

```json
{ "@type": "Product", "@id": "https://{host}/#product", "name": "{…}", "description": "{…}",
  "image": "https://{host}/{…}.jpg", "brand": { "@type": "Brand", "name": "{Brand}" },
  "offers": { "@type": "Offer", "price": "49.00", "priceCurrency": "USD",
    "availability": "https://schema.org/InStock", "url": "https://{host}/#pricing" } }
```

Several prices: `"offers": { "@type": "AggregateOffer", "lowPrice": …, "highPrice": …, "offerCount": … }`.

**A web app page** (the app runs in the browser):

```json
{ "@type": "WebApplication", "@id": "https://{host}/{app}#app", "name": "{…}", "url": "https://{host}/{app}",
  "description": "{…}", "applicationCategory": "BusinessApplication", "operatingSystem": "Any (web browser)",
  "inLanguage": ["en"], "isAccessibleForFree": true,
  "offers": { "@type": "Offer", "price": "0", "priceCurrency": "USD" },
  "isPartOf": { "@id": "https://{host}/#website" } }
```

Mobile apps: `MobileApplication`, see `app-store.md`.

**A place customers visit:** `LocalBusiness` (or a subtype: `Restaurant`, `MedicalClinic`, …)
with `address` (PostalAddress), `geo`, `telephone`, `openingHoursSpecification`. Only real,
current values.

## FAQ

```json
{ "@type": "FAQPage", "@id": "https://{host}/#faq", "url": "https://{host}/#faq",
  "mainEntity": [
    { "@type": "Question", "name": "{question, exactly as shown}",
      "acceptedAnswer": { "@type": "Answer", "text": "{answer, exactly as shown}" } }
  ] }
```

Generate it from the visible FAQ (for example `<details><summary>Q</summary><p>A</p></details>`)
and test that they match (see `tests.md`). Plain text in `text`: strip tags, decode entities.

Google limited FAQ rich results to a few authoritative government and health sites in 2023,
and dropped HowTo rich results. Keep FAQPage anyway for assistants and for understanding; do not
promise the owner FAQ snippets in Google.

## Deeper pages

```json
{ "@type": "BreadcrumbList", "itemListElement": [
  { "@type": "ListItem", "position": 1, "name": "Home", "item": "https://{host}/" },
  { "@type": "ListItem", "position": 2, "name": "{Section}", "item": "https://{host}/{section}" } ] }
```

Articles and blog posts: `Article` / `BlogPosting` with `headline`, `datePublished`,
`dateModified`, `author` (a real `Person` or the `Organization`), `image`.

## Never

- `aggregateRating` or `review` that the page does not show, or that are not from real customers.
- Prices, awards, certifications, client names or numbers the owner has not confirmed.
- Text hidden from visitors, or keyword lists in `description`.
- `Event` markup for an event that has passed.
- Several conflicting scripts describing the same thing (a plugin's and yours). One graph.

## Checking

- `python3 -I scripts/audit.py` parses every block and checks the FAQ against the page.
- Rich Results Test for what Google can show; validator.schema.org for schema errors in
  everything else.
