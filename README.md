# MemoryCare website

Static marketing site for MemoryCare. No build step: open `index.html` in a browser, or serve the folder:

```sh
python3 -m http.server 8000
```

## Files

- `index.html`: home page
- `privacy.html`, `terms.html`: Privacy Policy and Terms of Use (Australian law)
- `styles.css`: colour, type and spacing tokens at the top; light and dark themes. Use only the `--s-*` spacing scale, and keep state changes instant (no transitions)
- `script.js`: entrance animations, waitlist form, mobile menu, "larger text" toggle, footer year
- `assets/screens/`: phone mockups cut from the App Store screenshots (600px wide WebP, transparent corners)
- `assets/badges/`: official App Store and Google Play badges (not shown until launch)
- `assets/favicon.svg`: green heart app icon
- `sitemap.xml`, `robots.txt`: for Google Search Console (update `<lastmod>` when a page changes; add new pages to the sitemap)
- `assets/og-image.png`: 1200 × 630 social link preview (Open Graph / X card), used by all pages

## Updating screenshots

Each file in `assets/screens/` is the full iPhone (bezel included) with a transparent background, so it sits on any section color. To swap one, export a new screen at the same name and size (600 × ~1258).

| File | Used in |
| --- | --- |
| `home.webp` | Opening (annotated home screen), link preview image |
| `tasks.webp`, `checkin.webp` | Features |
| `sos.webp`, `fall.webp` | Safety |
| `dashboard.webp`, `medications.webp`, `location.webp`, `insights.webp` | For families |
| `games.webp` | Brain games |

## Still to do

- Connect the waitlist to Kit (see below). Until then the form tells visitors it isn't connected yet.
- At launch: swap the "Join the waitlist" buttons back to the App Store and Google Play badges in `assets/badges/`, linked to the real store listings.
- Legal pages: check each `<!-- REVIEW: ... -->` comment in `privacy.html` and `terms.html` (search for `REVIEW`).
- Have both legal pages reviewed by an Australian lawyer before launch.

## Waitlist (Kit)

The "Join the waitlist" form at the bottom of `index.html` sends signups to [Kit](https://kit.com), which stores the list, sends the confirmation and launch-day emails, and handles unsubscribes.

1. In Kit, create a form: **Grow > Landing Pages & Forms > Create new > Form** (any template; the site uses its own design).
2. In the form's **Settings > Incentive**, turn on **Send incentive email** so people confirm their address (double opt-in).
3. Open **Publish > HTML** and find the number in `action="https://app.kit.com/forms/1234567/subscriptions"`.
4. In `index.html`, replace `KIT_FORM_ID` in the waitlist form's `action` with that number.
5. Push, then sign up with your own email to test. You should appear under **Grow > Subscribers**.

On launch day, email everyone from **Send > Broadcasts**, filtered to that form.
