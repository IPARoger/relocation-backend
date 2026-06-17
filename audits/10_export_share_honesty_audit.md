# AUDIT: 10_EXPORT_SHARE_HONESTY_AUDIT

Task: `10_EXPORT_SHARE_HONESTY_AUDIT`
Mode: read-only audit; documentation output only
Result: **VERIFIED**

## Files inspected

Allowed files only:

- `app_shell.html`
- `map_CURRENT.html`
- `audits/05_frontend_placeholder_honesty_audit.md`
- `results/05_frontend_placeholder_honesty_audit.md`

No production files were modified.

## Search summary

Searched for export/share/artifact terms:

- `export`
- `share`
- `png`
- `pdf`
- `example.com`
- `copy link`
- `artifact`
- `download`
- `viewport`

## 1. Is Export reachable from the UI?

Yes. Export is reachable in `app_shell.html` through multiple visible buttons:

- Chart Record page: `Export entry (Screen 6)`.
- In-shell map route action panel: `Export viewport (Screen 6)`.
- Chart screen: `Export chart`.
- Comparison screen: `Export comparison`.

All of these use `data-nav="export"`, which routes to `screenExport()`.

`map_CURRENT.html` does not appear to provide a visible Export / Share UI in the inspected search results. The only relevant `share` hit there is a code comment about a bare `chartRecordId` URL parameter as a direct share link; it is not user-facing export/share UI.

## 2. Does Export create a real PNG/PDF/share artifact?

No.

Current `screenExport()` in `app_shell.html` creates a local-looking readonly URL string using:

```text
https://example.com${buildLocationHash(...)}
```

It does not create, upload, persist, or share a real artifact.

The PNG control is disabled and explicitly labeled:

```text
Export map PNG (illustrative · placeholder)
```

No PDF export behavior was found in the allowed files. No download/share handler was found for a generated artifact.

## 3. Is there any visible `example.com` / fake share URL?

Yes.

`screenExport()` builds a readonly input value beginning with `https://example.com...`. This is visible to the user and can look like a real share link, but it is not backed by real share/export infrastructure.

This matches the prior task 05 finding that the export/share screen is reachable and shows an `https://example.com...` link that looks like a share artifact but is not real share/export wiring.

## 4. Is any export/share wording misleading?

Yes.

Misleading or over-strong wording:

- `Screen 6 — Export / Share` implies an export/share surface exists.
- `Export entry (Screen 6)` implies an exportable entry.
- `Export viewport (Screen 6)` implies viewport export.
- `Export chart` implies chart export.
- `Export comparison` implies comparison export.
- `Module: export-investigation-link` plus the readonly `https://example.com...` input implies a usable share/export link.
- Roadmap/onboarding copy says `Export chart records for client reports`, which is future-facing but not currently true as an implemented feature.

Honest wording already present:

- `Export map PNG (illustrative · placeholder)` is disabled and clearly labeled as placeholder.

## 5. Smallest honesty fix if needed

Smallest copy-only honesty fix:

1. Rename the screen title from `Screen 6 — Export / Share` to something like `Screen 6 — Export / Share (not wired yet)` or `Screen 6 — Export / Share placeholder`.
2. Replace/remove the visible `https://example.com...` readonly input. If retained, label it as a non-functional preview, e.g. `Deep-link preview only — not a share URL`.
3. Relabel entry buttons to avoid promising real export behavior, e.g. `Export placeholder (Screen 6)` or `Export / Share preview`.
4. Keep the disabled PNG button as-is or shorten it to `Map PNG export not available yet`.

No backend, map, schema, renderer, or artifact-generation work is needed for the honesty fix. The minimum fix is UI copy only in `app_shell.html`.

## Verification status

VERIFIED: Export/Share is reachable from shell UI, does not create a real PNG/PDF/share artifact, contains a visible fake `example.com` URL, and has misleading export/share wording. The smallest needed fix is a scoped copy/label honesty change in `app_shell.html`.

VERIFIED
