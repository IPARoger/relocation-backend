# M1 Map Trust — QA screenshots

Capture after M1-C (popup overlay discovery + city readability).

## Files to capture

| File | Scene |
|------|--------|
| `popup_overlay_discovery.png` | City popup open → "View overlays here" expanded → condition list visible |
| `popup_overlay_run.png` | After tapping one condition (e.g. Venus in 7th) → overlay on map |
| `cities_medium_zoom_before_ref.png` | Reference: uniform bubbles at z6–7 (pre-M1-C commit) if available |
| `cities_medium_zoom_after.png` | z6–7: tiered markers, capped count, major labels only |

## Playwright waits (M1-B)

```javascript
await page.waitForFunction(() =>
  document.documentElement.getAttribute("data-overlay-final") === "true"
);
```

Do not screenshot during `data-overlay-phase="settling"`.
## M1-D chrome captures

| File | Scene |
|------|--------|
| `explore_save_disk.png` | Explore mode — save disk bottom-right |
| `explore_menu_save.png` | Hamburger open — Save investigation item |
| `pin_pinned_state.png` | Pin button showing Pinned + blue state |
| `history_back_replay.png` | After Back — ghost matches replayed plan |
