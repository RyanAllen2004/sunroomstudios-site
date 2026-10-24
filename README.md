# Sunroom Studios site

Landing page, product pages and starter SEO guides for Sunroom Studios (printable games and puzzles sold on Etsy).

**Status: DRAFT, not published.** All copy is marked DRAFT. Nothing here has been published to GitHub Pages; Ryan reviews and publishes.

Plain HTML + one stylesheet (`css/style.css`) + two tiny scripts. No framework, no build step, no dependencies, no paid services, no checkout, no forms, no cookies, no analytics. No secrets or API keys exist in this repo and none should ever be added (`tools/check-site.py` scans for them).

## What's here

| Path | What |
|---|---|
| `index.html` | Home: offer hub and bio-link target |
| `products/*.html` | One page per listing (8) |
| `freebies.html` | Links out to the Gumroad Christmas Market word search |
| `articles/` | Guides index + 3 SEO articles (Christmas party games, large print word search, New Year's Eve party games) |
| `about.html` | About and contact (sunroomstudiosus@gmail.com) |
| `js/site-config.js` | **The one place for prices and outbound URLs** |
| `js/site.js` | Fills prices/links from the config and swaps in preview images when they exist |
| `assets/<CODE>/` | One folder per listing; drop `preview-1.jpg` in it |
| `assets/fonts/` | Self-hosted Fraunces + Figtree (OFL), so visitors never hit a font server |
| `template/product-template.html` | Starting point for a new product page |
| `tools/check-site.py` | Link, image-slot, config and secret check |
| `tools/make-sitemap.py` | Writes `sitemap.xml` + `robots.txt` once the public address is known |

## Preview locally

```
python3 -m http.server 8000
```
Then open http://localhost:8000. (Serve over http rather than double-clicking, so fonts load.)
Check before every commit: `python3 tools/check-site.py`

## Updating

**Change a price: one line.** Edit the listing's line in `js/site-config.js`:
```js
"DIG-009": { price: "2.99", etsy: "" },
```
Every price on the site (home cards, product page, related cards) reads from that line. With JavaScript off, prices show "See Etsy".

**Add the real Etsy link:** paste the listing URL into `etsy: ""` on the same line. Until it is filled the button reads "Buy on Etsy · link added at publish" and does nothing. Also fill `etsyShop` and `gumroadWordSearch` at the top of that file.

**Add a preview image:** save it as `assets/<CODE>/preview-1.jpg` (e.g. `assets/DIG-009/preview-1.jpg`). It appears automatically in the arched slot on the product page and the home card; no HTML edit. Use your own product images only, never stock photos.

**Add a new product (one page from the template):**
1. Copy `template/product-template.html` to `products/<slug>.html`.
2. Find/replace `REPLACE_CODE` (e.g. `DIG-020`), then fill the other `REPLACE_` texts (name, blurb, description, promises).
3. Add `"DIG-020": { price: "x.xx", etsy: "" }` to `js/site-config.js`.
4. Add a card for it on `index.html` (copy any `<a class="card">` block) and create `assets/DIG-020/`.
5. Run `python3 tools/check-site.py`.

**Add an article:** copy one in `articles/`, change the text, and add a card to `articles/index.html` and `index.html`.

**Edit copy:** each product page has "What the listing promises" and "Details to fill in" (contents, counts, pages, format, ages, difficulty). They deliberately say "Not stated yet": fill them only with facts from the live Etsy listing. Never invent puzzle counts, page counts, difficulty claims or reviews.

## Publish checklist (Ryan)

1. Fill the URLs in `js/site-config.js` and confirm the prices match Etsy.
2. Replace every DRAFT item: `grep -rn "DRAFT\|Not stated yet\|REPLACE_" --include=*.html .` lists them. Delete the "Draft" tags once copy is approved.
3. Remove the draft banner and the `noindex` tag (each is a single line marked `DRAFT-ONLY`):
   `grep -rl DRAFT-ONLY --include=*.html . | xargs sed -i '/DRAFT-ONLY/d'`
   (Without this the site will not appear in search engines.)
4. Add preview images to `assets/<CODE>/`.
5. Write the bio on `about.html`.
6. Once you know the public address: `python3 tools/make-sitemap.py https://<address>`
7. `python3 tools/check-site.py`, commit, then enable GitHub Pages from the repo settings (this is deliberately not done for you).

## Open items for review

- Titles for **DIG-008** and **DIG-001** were not supplied; their pages are placeholders.
- **Scavenger Hunt** and **Trivia & Bingo** have no listing code yet. They use the temporary keys `SCAVENGER-HUNT` / `TRIVIA-BINGO` (config keys and `assets/` folders). Rename them when real codes exist (config key, folder, `data-price`/`data-buy`/`data-img` in their pages and cards).
- The articles link only to listings whose theme follows from the title. Scavenger Hunt and Trivia & Bingo are linked as "check the page for theme"; confirm their themes before describing them further.
- DIG-011 is treated as the large-print listing; confirm it is a word search before saying so.
- Until preview images exist, the browser console shows 404s for `preview-1.jpg`; harmless, and they stop once the images are added.
