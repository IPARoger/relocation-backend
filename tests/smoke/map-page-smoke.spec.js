// @ts-check
const { test, expect } = require('@playwright/test');
const { mintSession } = require('./session.cjs');

const BASE = process.env.BASE_URL || 'http://127.0.0.1:8004';

test('map page smoke: leaflet, /profiles, engine-birth, no JS errors', async ({ page }) => {
  let session;
  try {
    session = mintSession();
  } catch (err) {
    test.skip(true, `Could not mint Supabase session: ${err.message}`);
  }

  const consoleErrors = [];
  const profilesStatuses = [];
  const engineBirthStatuses = [];

  page.on('pageerror', (err) => consoleErrors.push(`pageerror: ${err.message}`));
  page.on('console', (msg) => {
    if (msg.type() === 'error') consoleErrors.push(`console.error: ${msg.text()}`);
  });
  page.on('response', (resp) => {
    const url = resp.url();
    if (url.includes('/profiles') && !url.match(/\/profiles\/[^/?]+/)) {
      profilesStatuses.push(resp.status());
    }
    if (url.includes('/supabase/chart-records/') && url.includes('/engine-birth')) {
      engineBirthStatuses.push(resp.status());
    }
  });

  await page.addInitScript(({ storageKey, storageVal }) => {
    try {
      window.localStorage.setItem(storageKey, storageVal);
    } catch (_) {
      /* ignore */
    }
  }, { storageKey: session.storage_key, storageVal: session.storage_val });

  const profileQuery = session.profile_id
    ? `&chartRecordId=${encodeURIComponent(session.profile_id)}`
    : '';
  const url = `${BASE}/map_CURRENT.html?skipOnboarding=1&bust=${Date.now()}${profileQuery}`;

  const response = await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 45000 });
  expect(response, 'navigation response').toBeTruthy();

  await page.waitForSelector('#map, .leaflet-container', { timeout: 30000 });
  const mapPresent = (await page.locator('#map').count()) > 0
    || (await page.locator('.leaflet-container').count()) > 0;
  expect(mapPresent, 'Leaflet map container present').toBe(true);

  await page.waitForTimeout(5000);

  if (profilesStatuses.length === 0) {
    test.info().annotations.push({ type: 'profiles', description: 'No /profiles network call observed' });
  } else {
    expect(profilesStatuses.some((s) => s === 200), `/profiles returned 200 (saw: ${profilesStatuses.join(',')})`).toBe(true);
  }

  if (!session.profile_id) {
    test.info().annotations.push({ type: 'engine-birth', description: 'SKIP: no profile_id from mint_session' });
  } else if (engineBirthStatuses.length === 0) {
    test.info().annotations.push({ type: 'engine-birth', description: 'No engine-birth network call observed within wait window' });
  } else {
    expect(engineBirthStatuses.some((s) => s === 200), `engine-birth returned 200 (saw: ${engineBirthStatuses.join(',')})`).toBe(true);
  }

  const benign404 = consoleErrors.filter(
    (e) => e.includes('404') && e.includes('Failed to load resource'),
  );
  const actionable = consoleErrors.filter((e) => !benign404.includes(e));
  expect(actionable, `unhandled JS errors: ${actionable.join(' | ')}`).toEqual([]);
});
