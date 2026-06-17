// @ts-check
const { test, expect } = require('@playwright/test');
const { mintSession } = require('./session.cjs');

const BASE = (process.env.BASE_URL || 'http://127.0.0.1:8004').replace(/\/$/, '');

test('saved-searches read route returns JSON 200 or 404', async ({ request }) => {
  let session;
  try {
    session = mintSession();
  } catch (err) {
    test.skip(true, `Could not mint Supabase session: ${err.message}`);
  }

  if (!session.profile_id) {
    test.skip(true, 'No profile_id available from staging account; cannot call /saved-searches/{profile_id}');
  }

  const resp = await request.get(`${BASE}/saved-searches/${session.profile_id}`, {
    headers: {
      Authorization: `Bearer ${session.access_token}`,
    },
  });

  const status = resp.status();
  expect([200, 404].includes(status), `expected 200 or 404, got ${status}`).toBe(true);

  const contentType = resp.headers()['content-type'] || '';
  const bodyText = await resp.text();
  let parsed;
  try {
    parsed = JSON.parse(bodyText);
  } catch (err) {
    throw new Error(`response is not valid JSON: ${err.message}; body=${bodyText.slice(0, 200)}`);
  }

  if (status === 200) {
    expect(Array.isArray(parsed), '200 response should be JSON array').toBe(true);
  } else {
    expect(typeof parsed === 'object' && parsed !== null, '404 response should be JSON object').toBe(true);
  }
});
