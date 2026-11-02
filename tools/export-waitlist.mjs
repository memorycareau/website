// Prints the website waitlist as CSV (email,signed_up), one row per unique
// email, oldest first. Needs a Firebase service account key; see README.md.
//
//   cd tools && npm install firebase-admin
//   GOOGLE_APPLICATION_CREDENTIALS=~/memorycare-key.json node export-waitlist.mjs > waitlist.csv

import { initializeApp, applicationDefault } from 'firebase-admin/app';
import { getFirestore } from 'firebase-admin/firestore';

initializeApp({ credential: applicationDefault() });

const snapshot = await getFirestore().collection('waitlist').orderBy('createdAt').get();
const seen = new Set();
const rows = ['email,signed_up'];

for (const doc of snapshot.docs) {
  const { email, createdAt } = doc.data();
  const address = String(email || '').trim().toLowerCase();
  if (!address || seen.has(address)) continue;
  seen.add(address);
  rows.push(`${address},${createdAt ? createdAt.toDate().toISOString() : ''}`);
}

console.log(rows.join('\n'));
console.error(`${seen.size} unique email addresses`);
