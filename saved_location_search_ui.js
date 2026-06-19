/**
 * saved_location_search_ui.js — reusable Family B search input + results panel.
 */
(function () {
  "use strict";

  var STYLE_ID = "rm-saved-loc-search-styles";

  function injectStyles() {
    if (document.getElementById(STYLE_ID)) return;
    var style = document.createElement("style");
    style.id = STYLE_ID;
    style.textContent = [
      ".rm-sls-wrap { position: relative; width: 100%; }",
      ".rm-sls-input {",
      "  width: 100%; box-sizing: border-box;",
      "  background: #fff; border: 1px solid #cbd5e1; color: #0f172a;",
      "  padding: 8px 10px; border-radius: 6px; font-size: 0.95rem;",
      "}",
      ".rm-sls-input:focus { border-color: #6366f1; outline: none; }",
      ".rm-sls-panel {",
      "  position: absolute; left: 0; right: 0; top: calc(100% + 2px); z-index: 1200;",
      "  background: #fff; border: 1px solid #cbd5e1; border-radius: 6px;",
      "  max-height: 260px; overflow-y: auto; box-shadow: 0 8px 24px rgba(15,23,42,0.12);",
      "}",
      ".rm-sls-section-title {",
      "  padding: 6px 10px; font-size: 0.72rem; font-weight: 600;",
      "  text-transform: uppercase; letter-spacing: 0.04em; color: #64748b;",
      "  background: #f8fafc; border-bottom: 1px solid #e2e8f0;",
      "}",
      ".rm-sls-item {",
      "  padding: 8px 10px; cursor: pointer; font-size: 0.9rem;",
      "  border-bottom: 1px solid #f1f5f9; display: flex; justify-content: space-between; gap: 8px;",
      "}",
      ".rm-sls-item:hover, .rm-sls-item.is-active { background: #eef2ff; }",
      ".rm-sls-item-meta { font-size: 0.75rem; color: #64748b; white-space: nowrap; }",
      ".rm-sls-empty { padding: 10px; font-size: 0.85rem; color: #64748b; }",
      ".rm-sls-status { font-size: 0.78rem; color: #64748b; margin-top: 4px; min-height: 1.1em; }",
      ".rm-sls-status.is-error { color: #b91c1c; }",
      "#panel .rm-sls-input { background: #fff; }",
      "#panel .rm-sls-panel { background: #fff; }",
    ].join("\n");
    document.head.appendChild(style);
  }

  function esc(s) {
    return String(s || "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function sourceBadge(source) {
    if (source === "favorite") return "Favorite";
    if (source === "custom") return "Saved";
    return "Location";
  }

  function mount(options) {
    injectStyles();
    options = options || {};
    var root = options.root;
    if (!root) throw new Error("RMSavedLocationSearchUI.mount requires root");

    var inputId = options.inputId || ("rm-sls-input-" + Math.random().toString(36).slice(2, 8));
    var getProfileId = options.getProfileId || function () { return options.profileId || null; };
    var onSelect = options.onSelect || function () {};
    var formatSourceBadge = options.formatSourceBadge || sourceBadge;
    var placeholder = options.placeholder || (window.RMSavedLocationSearch && window.RMSavedLocationSearch.PLACEHOLDER) || "Search locations or favorites";
    var inputLabel = options.inputLabel || "Search locations or favorites";

    root.innerHTML = [
      '<div class="rm-sls-wrap" data-rm-saved-loc-search>',
      '  <label class="sr-only" for="' + esc(inputId) + '">' + esc(inputLabel) + '</label>',
      '  <input type="text" class="rm-sls-input" id="' + esc(inputId) + '"',
      '         data-rm-saved-loc-input placeholder="' + esc(placeholder) + '" autocomplete="off" />',
      '  <div class="rm-sls-panel" data-rm-saved-loc-panel hidden></div>',
      '  <div class="rm-sls-status" data-rm-saved-loc-status aria-live="polite"></div>',
      "</div>",
    ].join("\n");

    var input = root.querySelector("[data-rm-saved-loc-input]");
    var panel = root.querySelector("[data-rm-saved-loc-panel]");
    var status = root.querySelector("[data-rm-saved-loc-status]");
    var timer = null;
    var activeIdx = -1;
    var lastPayload = null;
    var searchSeq = 0;
    var destroyed = false;
    var onDocPointer = null;

    function setStatus(msg, isError) {
      if (!status) return;
      status.textContent = msg || "";
      status.className = "rm-sls-status" + (isError ? " is-error" : "");
    }

    function hidePanel() {
      if (panel) panel.hidden = true;
      activeIdx = -1;
    }

    function showPanel() {
      if (panel) panel.hidden = false;
    }

    function payloadHasItems(payload) {
      var sections = (payload && payload.sections) || [];
      for (var i = 0; i < sections.length; i++) {
        if ((sections[i].items || []).length) return true;
      }
      return Boolean(payload && (payload.items || []).length);
    }

    function renderPayload(payload) {
      lastPayload = payload;
      if (!panel) return;
      panel.innerHTML = "";
      var sections = (payload && payload.sections) || [];
      var any = false;
      sections.forEach(function (section) {
        var items = section.items || [];
        if (!items.length) return;
        any = true;
        var title = document.createElement("div");
        title.className = "rm-sls-section-title";
        title.textContent = section.title || "Results";
        panel.appendChild(title);
        items.forEach(function (item, idx) {
          var row = document.createElement("div");
          row.className = "rm-sls-item";
          row.setAttribute("data-rm-saved-loc-item", "1");
          row.setAttribute("data-place-id", item.place_id || "");
          row.setAttribute("data-index", String(idx));
          row.innerHTML = '<span>' + esc(item.display_name || item.label) + '</span>'
            + '<span class="rm-sls-item-meta">' + esc(formatSourceBadge(item.source)) + '</span>';
          row.addEventListener("mousedown", function (ev) {
            ev.preventDefault();
            pickItem(item).catch(function (err) {
              setStatus(err && err.message ? err.message : "Selection failed.", true);
            });
          });
          panel.appendChild(row);
        });
      });
      if (!any) {
        var empty = document.createElement("div");
        empty.className = "rm-sls-empty";
        var mode = payload && payload.mode;
        if (mode === "typing") {
          empty.textContent = "Type at least 2 characters to search locations or favorites.";
        } else if (mode === "starter") {
          empty.textContent = "No saved favorites yet. Type to search locations.";
        } else if (mode === "results") {
          empty.textContent = "No matching locations or favorites.";
        } else {
          empty.textContent = "No results.";
        }
        panel.appendChild(empty);
      }
      showPanel();
    }

    async function runSearch() {
      if (destroyed) return;
      var svc = window.RMSavedLocationSearch;
      if (!svc || typeof svc.search !== "function") {
        setStatus("Saved location search unavailable.", true);
        return;
      }
      var profileId = getProfileId();
      if (!profileId) {
        setStatus("Select a profile first.", true);
        hidePanel();
        return;
      }
      var qAtStart = String(input.value || "").trim();
      var seq = ++searchSeq;
      if (qAtStart.length >= 2) setStatus("Searching locations…");
      else setStatus("");
      try {
        var payload = await svc.search(profileId, input.value, options.searchOptions || {});
        if (destroyed || seq !== searchSeq) return;
        if (String(input.value || "").trim() !== qAtStart) return;
        if (payload && payload.mode === "results" && !payloadHasItems(payload)
            && lastPayload && lastPayload.query === qAtStart && payloadHasItems(lastPayload)) {
          return;
        }
        if (payload && payload.mode === "results") {
          var n = (payload.items || []).length;
          setStatus(n ? "" : "No matching locations or favorites.");
        } else {
          setStatus("");
        }
        renderPayload(payload);
      } catch (err) {
        if (destroyed || seq !== searchSeq) return;
        setStatus(err && err.message ? err.message : "Search failed.", true);
        hidePanel();
      }
    }

    async function pickItem(item) {
      if (item && item.source === "teaching" && item.teaching_query) {
        setStatus("Looking up location…");
        try {
          var searchSvc = window.RMSavedLocationSearch;
          if (!searchSvc || typeof searchSvc.search !== "function") {
            setStatus("Saved location search unavailable.", true);
            return;
          }
          var profileId = getProfileId();
          var resolved = await searchSvc.search(profileId, item.teaching_query, Object.assign({}, options.searchOptions || {}, { includeTeaching: false, limit: 8 }));
          var hits = (resolved && resolved.items) || [];
          var hit = hits.find(function (h) { return h.source === "geonames"; }) || hits[0];
          if (!hit || !hit.place_id) {
            setStatus("Could not resolve that location.", true);
            return;
          }
          item = hit;
        } catch (err) {
          setStatus(err && err.message ? err.message : "Lookup failed.", true);
          return;
        }
      }
      hidePanel();
      input.value = item.display_name || item.label || "";
      setStatus("");
      onSelect(item);
    }

    function scheduleSearch() {
      clearTimeout(timer);
      timer = setTimeout(runSearch, options.debounceMs || 250);
    }

    input.addEventListener("focus", function () {
      var q = String(input.value || "").trim();
      if (lastPayload && lastPayload.query === q && payloadHasItems(lastPayload)) {
        renderPayload(lastPayload);
        return;
      }
      scheduleSearch();
    });

    input.addEventListener("input", function () {
      setStatus("");
      scheduleSearch();
    });

    input.addEventListener("keydown", function (ev) {
      if (ev.key === "Escape") {
        hidePanel();
        return;
      }
      if (ev.key === "Enter") {
        ev.preventDefault();
        var items = (lastPayload && lastPayload.items) || [];
        if (items.length) pickItem(items[Math.max(0, activeIdx)]).catch(function () {});
        return;
      }
      if (ev.key === "ArrowDown" || ev.key === "ArrowUp") {
        var rows = panel ? panel.querySelectorAll("[data-rm-saved-loc-item]") : [];
        if (!rows.length) return;
        ev.preventDefault();
        if (ev.key === "ArrowDown") activeIdx = Math.min(rows.length - 1, activeIdx + 1);
        else activeIdx = Math.max(0, activeIdx - 1);
        rows.forEach(function (row, i) {
          row.classList.toggle("is-active", i === activeIdx);
        });
      }
    });

    onDocPointer = function (ev) {
      if (destroyed) return;
      if (!root.contains(ev.target)) hidePanel();
    };
    document.addEventListener("mousedown", onDocPointer);

    return {
      input: input,
      refresh: runSearch,
      destroy: function () {
        destroyed = true;
        clearTimeout(timer);
        if (onDocPointer) document.removeEventListener("mousedown", onDocPointer);
        onDocPointer = null;
        root.innerHTML = "";
      },
      clear: function () {
        input.value = "";
        hidePanel();
        setStatus("");
      },
    };
  }

  window.RMSavedLocationSearchUI = {
    mount: mount,
  };
})();
