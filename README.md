# MemoryCare website

Static marketing site for MemoryCare. No build step: open `index.html` in a browser, or serve the folder:

```sh
python3 -m http.server 8000
```

## Files

- `index.html` — home page
- `privacy.html`, `terms.html` — Privacy Policy and Terms of Use (Australian law)
- `styles.css` — brand tokens (greens, mint, type) at the top; light and dark themes
- `script.js` — mobile menu, "larger text" toggle, feature tabs, scroll fade-in, footer year
- `assets/screens/` — phone mockups cut from the App Store screenshots (600px wide WebP, transparent corners)
- `assets/favicon.svg` — green heart app icon
- `sitemap.xml`, `robots.txt` — for Google Search Console (update `<lastmod>` when a page changes; add new pages to the sitemap)
- `assets/og-image.png` — 1200 × 630 social link preview (Open Graph / X card), used by all pages

## Updating screenshots

Each file in `assets/screens/` is the full iPhone (bezel included) with a transparent background, so it sits on any section color. To swap one, export a new screen at the same name and size (600 × ~1258).

| File | Used in |
| --- | --- |
| `home.webp` | Hero, "For them" tabs |
| `dashboard.webp` | Hero (back phone), "For families" tabs |
| `tasks.webp`, `checkin.webp` | "For them" tabs (`checkin` also in the download section) |
| `sos.webp`, `fall.webp` | Safety section |
| `medications.webp`, `location.webp`, `insights.webp` | "For families" tabs |
| `games.webp` | Brain games section |

## Still to do

- Replace the App Store / Google Play buttons with the official badges and real store links (marked `TODO` in `index.html`).
- Pricing answer in the FAQ, and the "Fees and purchases" section of `terms.html` once pricing is set.
- Legal pages: fill in every highlighted `fill-in` (legal entity name, ABN, governing state/territory, overseas data locations), and check each `<!-- REVIEW: ... -->` comment in `privacy.html` and `terms.html`. Search for `fill-in` and `REVIEW` to find them all.
- Have both legal pages reviewed by an Australian lawyer before launch.
