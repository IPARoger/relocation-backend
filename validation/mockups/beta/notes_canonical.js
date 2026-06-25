/**
 * H7-1 — shared Notes renderer (Profile, Relocated, Comparison, Notes Library).
 * Visual authority: validation/mockups/beta/comparison_notes_slot.html
 * Safe to import from app_shell.html and comparison_v5_route.js only.
 */
(function (global) {
  "use strict";

  const NOTES_CANONICAL = true;
  const HINT_DEFAULT = "Optional \u00b7 same record as Profile notebook \u00b7 pops out for long entries";
  const LIST_SVG = "<svg width=\"15\" height=\"15\" viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"1.7\" stroke-linecap=\"round\" aria-hidden=\"true\"><line x1=\"9\" y1=\"6\" x2=\"20\" y2=\"6\"/><line x1=\"9\" y1=\"12\" x2=\"20\" y2=\"12\"/><line x1=\"9\" y1=\"18\" x2=\"20\" y2=\"18\"/><circle cx=\"4.5\" cy=\"6\" r=\"1.3\" fill=\"currentColor\" stroke=\"none\"/><circle cx=\"4.5\" cy=\"12\" r=\"1.3\" fill=\"currentColor\" stroke=\"none\"/><circle cx=\"4.5\" cy=\"18\" r=\"1.3\" fill=\"currentColor\" stroke=\"none\"/></svg>";
  const MIC_SVG = "<svg width=\"16\" height=\"16\" viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"1.6\" stroke-linecap=\"round\" stroke-linejoin=\"round\" aria-hidden=\"true\"><rect x=\"9\" y=\"2\" width=\"6\" height=\"11\" rx=\"3\"/><path d=\"M5 10a7 7 0 0 0 14 0\"/><line x1=\"12\" y1=\"19\" x2=\"12\" y2=\"22\"/><line x1=\"8.5\" y1=\"22\" x2=\"15.5\" y2=\"22\"/></svg>";
  const FAB_SVG = "<svg width=\"18\" height=\"18\" viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"1.6\" stroke-linecap=\"round\" stroke-linejoin=\"round\" aria-hidden=\"true\"><path d=\"M4 4h16v13l-4 4H4z\"/><line x1=\"8\" y1=\"9\" x2=\"16\" y2=\"9\"/><line x1=\"8\" y1=\"13\" x2=\"13\" y2=\"13\"/></svg>";

  function esc(text, escapeHtml) {
    return escapeHtml ? escapeHtml(text) : String(text == null ? "" : text);
  }

  function renderToolbarHtml(opts) {
    const cfg = opts || {};
    const disabled = cfg.toolsDisabled !== false;
    const tab = disabled ? ' tabindex="-1" aria-disabled="true"' : "";
    return `<div class="notes-toolbar" aria-label="Formatting tools${disabled ? " (visual only)" : ""}">
      <button type="button" class="notes-tool" title="Bold"${tab}><b>B</b></button>
      <button type="button" class="notes-tool" title="Italic"${tab}><i>I</i></button>
      <button type="button" class="notes-tool" title="Underline"${tab}><u>U</u></button>
      <button type="button" class="notes-tool" title="Bullet list"${tab}>${LIST_SVG}</button>
      <button type="button" class="notes-tool mic" title="Voice note"${tab}>${MIC_SVG}</button>
    </div>`;
  }

  function renderSaveFootHtml(opts, escapeHtml) {
    const cfg = opts || {};
    if (!cfg.showSave) {
      return cfg.saveSlot
        ? `<div class="note-foot" data-notes-save-slot="${esc(cfg.saveSlot, escapeHtml)}" hidden></div>`
        : "";
    }
    const msgId = cfg.msgId ? ` id="${esc(cfg.msgId, escapeHtml)}"` : "";
    const action = esc(cfg.saveAction || "save-chart-note", escapeHtml);
    const label = esc(cfg.saveLabel || "Save Note", escapeHtml);
    const saveClass = cfg.saveClass ? ` class="${esc(cfg.saveClass, escapeHtml)}"` : ' class="primary"';
    return `<div class="note-foot">
        <button type="button"${saveClass} data-action="${action}">${label}</button>
        <span${msgId} class="meta" style="min-height:1.2em;"></span>
      </div>`;
  }

  function renderComposerHtml(config, escapeHtml) {
    const cfg = config || {};
    const textareaId = cfg.textareaId ? ` id="${esc(cfg.textareaId, escapeHtml)}"` : "";
    const extraAttrs = cfg.textareaAttrs || "";
    const textareaClass = cfg.textareaClass || "note-ta";
    const disabled = cfg.disabled ? " disabled" : "";
    const rows = cfg.rows ? ` rows="${cfg.rows}"` : "";
    const body = cfg.body != null ? String(cfg.body) : "";
    const placeholder = esc(cfg.placeholder || "Write or dictate a note\u2026", escapeHtml);
    const hintText = cfg.hint != null ? cfg.hint : (cfg.hintText != null ? cfg.hintText : HINT_DEFAULT);
    const hint = cfg.showHint === false
      ? ""
      : `<p class="note-hint">${esc(hintText, escapeHtml)}</p>`;
    const toolbar = renderToolbarHtml(cfg);
    const editor = `<textarea${textareaId} class="${textareaClass}" placeholder="${placeholder}"${rows}${disabled}${extraAttrs}>${esc(body, escapeHtml)}</textarea>`;
    const foot = renderSaveFootHtml(cfg, escapeHtml);
    if (cfg.toolbarPosition === "below") {
      return `${editor}${toolbar}${hint}${foot}`;
    }
    return `${toolbar}${editor}${hint}${foot}`;
  }

  function renderCardHtml(config, escapeHtml) {
    const cfg = config || {};
    const scopeAttr = cfg.scope ? ` data-notes-scope="${esc(cfg.scope, escapeHtml)}"` : "";
    const popoutDisabled = cfg.popoutDisabled !== false;
    const popoutAttrs = popoutDisabled ? ' tabindex="-1" aria-disabled="true"' : "";
    return `<div class="notes-card notes-slot notes-canonical"${scopeAttr}>
      <div class="card-head"><h3 class="ch-title">Notes</h3><button type="button" class="notes-popout" title="Pop out"${popoutAttrs}>\u2922</button></div>
      ${renderComposerHtml(cfg, escapeHtml)}
    </div>`;
  }

  function renderRailHtml(cs, escapeHtml) {
    const composer = cs
      ? renderComposerHtml({
          textareaId: "rm-cmp-note",
          body: cs.notes || "",
          placeholder: "General comparison notes\u2026",
          rows: 7,
          textareaAttrs: ' data-cmp-mount="notes-input" data-cmp-role="notes-input"',
          showSave: true,
          saveAction: "save-comparison-note",
          saveLabel: "Save",
          saveClass: "notes-save",
          msgId: "rm-cmp-note-msg",
          toolsDisabled: true,
        }, escapeHtml)
      : renderComposerHtml({
          placeholder: "Build or select a comparison to add notes.",
          rows: 7,
          disabled: true,
          hintText: "Notes attach to a built comparison set.",
          showSave: false,
          toolsDisabled: true,
        }, escapeHtml);
    return `<aside class="comparison-notes-rail notes-canonical" id="cmp-notes-rail" data-cmp-mount="notes-rail" data-cmp-role="notes-rail" data-cmp-notes-layout="floating">
      <button type="button" id="notes-fab" title="Open notes" data-action="cmp-notes-show" data-cmp-role="notes-fab">${FAB_SVG}</button>
      <div class="general-notes-section">
        <div class="general-notes-head">
          <button type="button" class="gn-collapse" title="Hide notes" data-action="cmp-notes-hide" data-cmp-role="notes-collapse">\u25be</button>
          <div class="general-notes-label">Notes</div>
        </div>
        ${composer}
      </div>
    </aside>`;
  }

  function renderRailShellInnerHtml(notesEsc) {
    const composer = renderComposerHtml({
      textareaId: "rm-cmp-note",
      body: notesEsc || "",
      placeholder: "General comparison notes\u2026",
      rows: 7,
      textareaAttrs: ' data-cmp-mount="notes-input" data-cmp-role="notes-input"',
      showSave: true,
      saveAction: "save-comparison-note",
      saveLabel: "Save",
      saveClass: "notes-save",
      msgId: "rm-cmp-note-msg",
      toolsDisabled: true,
    }, function (t) { return t; });
    return `<div class="general-notes-section">
        <div class="general-notes-head"><button type="button" class="gn-collapse" title="Hide notes" data-action="cmp-notes-hide" data-cmp-role="notes-collapse">\u25be</button><div class="general-notes-label">Notes</div></div>
        ${composer}
      </div>`;
  }

  function renderLibraryEditorHtml(item, escapeHtml) {
    if (!item) {
      return "";
    }
    return `<div class="notes-library-composer notes-canonical" data-notes-scope="library">
      <div class="nl-editor-head">
        <strong>${esc(item.title, escapeHtml)}</strong>
        <div class="meta">${esc(item.noteType, escapeHtml)} \u00b7 ${esc(item.relatedName, escapeHtml)}</div>
      </div>
      ${renderComposerHtml({
        textareaId: "rm-notes-lib-body",
        body: item.body || "",
        rows: 14,
        showSave: true,
        saveAction: "save-notes-library-note",
        saveLabel: "Save",
        hintText: "Edits sync to the workflow note for this record.",
        toolsDisabled: true,
      }, escapeHtml)}
    </div>`;
  }

  global.NotesCanonical = {
    CANONICAL: NOTES_CANONICAL,
    HINT_DEFAULT: HINT_DEFAULT,
    renderToolbarHtml: renderToolbarHtml,
    renderSaveFootHtml: renderSaveFootHtml,
    renderComposerHtml: renderComposerHtml,
    renderCardHtml: renderCardHtml,
    renderRailHtml: renderRailHtml,
    renderRailShellInnerHtml: renderRailShellInnerHtml,
    renderLibraryEditorHtml: renderLibraryEditorHtml,
  };
})(typeof window !== "undefined" ? window : globalThis);
