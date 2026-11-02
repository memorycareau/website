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
- `tools/export-waitlist.mjs`: exports the waitlist on launch day (see below)
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

- Add the waitlist security rules in Firebase (step 3 below), then push and test a signup.
- At launch: swap the "Join the waitlist" buttons back to the App Store and Google Play badges in `assets/badges/`, linked to the real store listings.
- Legal pages: check each `<!-- REVIEW: ... -->` comment in `privacy.html` and `terms.html` (search for `REVIEW`).
- Have both legal pages reviewed by an Australian lawyer before launch.

## Waitlist (Firebase)

The "Join the waitlist" form saves each signup to a `waitlist` collection in the app's Firestore database (Sydney, `australia-southeast1`). It's free on Firebase's Spark plan, which never bills. The website talks to Firestore's REST API directly, so it doesn't load the Firebase SDK.

### One-time setup

1. **Get the web config.** Firebase console > ⚙ **Project settings** > **General** > **Your apps**. If there's no web app (`</>` icon), click **Add app** > **Web**, name it "Website" and skip Firebase Hosting. From the config shown, copy `projectId` and `apiKey`.
2. **Paste them into `index.html`**, replacing `FIREBASE_PROJECT_ID` and `FIREBASE_WEB_API_KEY` on the waitlist form. The web API key is meant to be public; the security rules below are what protect the data.
3. **Add the security rules.** Firebase console > **Firestore Database** > **Rules**. Paste this block *inside* the existing `match /databases/{database}/documents { ... }`, next to the app's rules (don't replace them), then **Publish**:

   ```
   // Website waitlist: anyone can add themselves; nobody can read, change or delete entries
   match /waitlist/{entry} {
     allow create: if request.resource.data.keys().hasOnly(['email', 'createdAt', 'source'])
       && request.resource.data.email is string
       && request.resource.data.email.size() <= 254
       && request.resource.data.email.matches('^[^@ ]+@[^@ ]+[.][^@ ]+$')
       && request.resource.data.createdAt is timestamp
       && request.resource.data.source == 'website';
     allow read, update, delete: if false;
   }
   ```

   If the rules contain a catch-all such as `match /{document=**} { allow read, write: if request.auth != null; }`, every signed-in app user could read the waitlist. Narrow that rule to the app's own collections.
4. **Push and test.** Sign up on getmemorycare.app, then check **Firestore Database** > **Data** > `waitlist`. A new document with your email should appear.

### Unsubscribes

People unsubscribe by replying to any email. Within 5 working days (Spam Act), find their document in Firestore (filter `email` == their address) and delete it.

### Launch day

1. Firebase console > ⚙ **Project settings** > **Service accounts** > **Generate new private key**. Save the file **outside this folder** (for example `~/memorycare-key.json`) and never commit it.
2. Export the list (needs Node.js):

   ```sh
   cd tools
   npm install firebase-admin
   GOOGLE_APPLICATION_CREDENTIALS=~/memorycare-key.json node export-waitlist.mjs > ~/waitlist.csv
   ```

   This prints one row per unique email, oldest first.
3. Send the email from memorycareau@gmail.com with everyone in **Bcc**, never To or Cc. A personal Gmail account can send to about 500 recipients a day, so split bigger lists across days. Every email must say who it's from and end with: "To unsubscribe, just reply to this email."
4. Delete the key file when you're done, or remove it under **Service accounts**.
