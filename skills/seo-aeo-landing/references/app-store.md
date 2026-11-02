# When the landing page sells a mobile app

App store optimisation (ASO) happens mostly in App Store Connect and Google Play Console, which
are the owner's accounts. What belongs in the landing project is making the page and the store
listings agree, and making links open the app.

## Say the same thing in both places

| Store field | Limit | Keep in step with |
| --- | --- | --- |
| App Store name | 30 characters | the page's brand plus the search phrase if it fits |
| App Store subtitle | 30 characters | the search phrase |
| App Store keywords | 100 characters, comma separated, no spaces, no words already in the name | the terms in the page's meta description |
| App Store promotional text | 170 characters, changeable without review | the page's current offer |
| Google Play title | 30 characters | as App Store name |
| Google Play short description | 80 characters | the meta description's first clause |
| Google Play full description | 4,000 characters, indexed for search | the page copy and llms-full.txt |
| Screenshots, preview video | per store | the page's hero and feature images |

Draft these as a table for the owner. Store changes go through the owner's accounts and review.
Do not invent ratings or download numbers for either place.

## Store badges

Use Apple's and Google's official badges, unmodified, linking to the store pages:
`https://apps.apple.com/app/id{APPLE_ID}` and
`https://play.google.com/store/apps/details?id={package.name}`. Give each an `alt` in the page
language. Add the store links to llms.txt under Pages.

## Smart app banner (iOS Safari)

```html
<meta name="apple-itunes-app" content="app-id={APPLE_ID}, app-argument=https://{host}/{path}">
```

Android has no equivalent meta tag; use a small, dismissible banner of your own if wanted.

## Links that open the app

- iOS universal links: `https://{host}/.well-known/apple-app-site-association`, JSON, no
  extension, served as `application/json`, no redirect:

  ```json
  { "applinks": { "details": [ { "appIDs": ["{TEAMID}.{bundle.id}"], "components": [ { "/": "/app/*" } ] } ] } }
  ```

- Android app links: `https://{host}/.well-known/assetlinks.json`:

  ```json
  [ { "relation": ["delegate_permission/common.handle_all_urls"],
      "target": { "namespace": "android_app", "package_name": "{package.name}",
        "sha256_cert_fingerprints": ["{AA:BB:…}"] } } ]
  ```

The team ID, bundle ID, package name and signing fingerprint come from the owner's developer
accounts. Make sure robots.txt does not block `/.well-known/` and the CDN serves these with the
right type.

## MobileApplication markup

```json
{ "@type": "MobileApplication", "@id": "https://{host}/#app", "name": "{App name}",
  "operatingSystem": "iOS 16+, Android 10+", "applicationCategory": "{BusinessApplication|…}",
  "description": "{…}", "image": "https://{host}/{icon}.png",
  "offers": { "@type": "Offer", "price": "0", "priceCurrency": "USD" },
  "downloadUrl": ["https://apps.apple.com/app/id{APPLE_ID}", "https://play.google.com/store/apps/details?id={package.name}"],
  "publisher": { "@id": "https://{host}/#org" } }
```

Add `aggregateRating` only if the page shows the store rating, it is current, and the owner
agrees to keep it updated.

## Checks

- Badges link to the right listing, in a new tab or not as the project prefers.
- `curl -sI https://{host}/.well-known/apple-app-site-association` gives 200 and
  `application/json`; same for `assetlinks.json`.
- Google's Statement List tester for assetlinks; Apple's AASA validator or a device test for
  universal links.
