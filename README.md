# MemoryCare website

Static marketing site for MemoryCare. No build step: open `index.html` in a browser, or serve the folder:

```sh
python3 -m http.server 8000
```

## Files

- `index.html` — page content
- `styles.css` — design tokens (colors, type, spacing) at the top; light and dark themes
- `script.js` — mobile menu, "larger text" toggle, footer year
- `assets/` — put images, video and logos here

## Replacing placeholders

Every placeholder uses the `ph` class, so search `index.html` for `class="ph` to find them all.

| Placeholder | Suggested asset |
| --- | --- |
| Hero phone (`ph-phone`) | App home screen screenshot, 1170 × 2532 |
| Hero photo (`ph-photo`) | Lifestyle photo, 4:3 |
| Partner logos (`ph-logo`) | SVG/PNG logos, ~140 × 48 |
| Familiar faces phone (`ph-phone`) | App screenshot, 1170 × 2532 |
| Video (`ph-video`) | 16:9 `<video>` or YouTube/Vimeo embed |
| Caregiver dashboard (`ph-dashboard`) | Screenshot, 16:10 |
| Testimonial avatars (`ph-avatar`) | Square portraits |
| Store badges (`ph-badge`) | Official App Store / Google Play badges |
| Logo (`brand-mark`) and `assets/favicon.svg` | Final logo |

Swap a placeholder `<div>` for an `<img>` that keeps the same size class, e.g.:

```html
<img class="ph-phone" src="assets/home-screen.png" alt="MemoryCare home screen showing today's date and next reminder">
```

Placeholder copy to update: testimonials, pricing FAQ, partner logos, privacy/terms links, and the contact email (`hello@example.com`).
