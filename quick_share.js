/**
 * QUICK-SHARE-MVP — shared create + clipboard helpers (map + app shell).
 */
(function (global) {
  "use strict";

  function buildQuickShareUrl(quickShareId) {
    const id = String(quickShareId || "").trim();
    if (!id) return "";
    const path = "/map_CURRENT.html?quickShare=" + encodeURIComponent(id);
    if (global.location && global.location.origin) {
      return global.location.origin + path;
    }
    return path;
  }

  async function copyTextToClipboard(text) {
    const value = String(text || "");
    if (!value) throw new Error("Nothing to copy");
    if (global.navigator && global.navigator.clipboard && global.navigator.clipboard.writeText) {
      await global.navigator.clipboard.writeText(value);
      return;
    }
    const ta = global.document.createElement("textarea");
    ta.value = value;
    ta.setAttribute("readonly", "");
    ta.style.position = "fixed";
    ta.style.left = "-9999px";
    global.document.body.appendChild(ta);
    ta.select();
    const ok = global.document.execCommand("copy");
    global.document.body.removeChild(ta);
    if (!ok) throw new Error("Clipboard unavailable");
  }

  async function createQuickShare(payload, token) {
    if (!token) throw new Error("Session unavailable. Reload and try again.");
    const resp = await fetch("/quick-share/create", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + token,
      },
      body: JSON.stringify(payload || {}),
    });
    let body = {};
    try { body = await resp.json(); } catch (e) { /* non-JSON */ }
    if (!resp.ok) {
      const detail = body && body.detail;
      const msg = (detail && (detail.message || detail.error)) ||
        (typeof detail === "string" ? detail : null) ||
        ("HTTP " + resp.status);
      throw new Error(msg);
    }
    return body;
  }

  async function createAndCopyQuickShare(payload, token) {
    const created = await createQuickShare(payload, token);
    const url = buildQuickShareUrl(created.quick_share_id);
    await copyTextToClipboard(url);
    return { created, url };
  }

  function renderChartFactsReadOnlyHtml(chartFacts, placeLabel) {
    if (!chartFacts || typeof chartFacts !== "object") return "";
    const planets = chartFacts.planets || {};
    const angles = chartFacts.angles || {};
    const planetRows = Object.keys(planets).sort().map((name) => {
      const p = planets[name] || {};
      const house = p.house != null ? "H" + p.house : "—";
      const sign = p.sign || "—";
      const near = p.near_cusp ? " · near cusp" : "";
      return "<tr><td>" + name + "</td><td>" + sign + "</td><td>" + house + near + "</td></tr>";
    }).join("");
    const angleRows = ["ASC", "MC", "DSC", "IC"].filter((k) => angles[k]).map((k) => {
      const a = angles[k] || {};
      return "<tr><td>" + k + "</td><td colspan=\"2\">" + (a.sign || "—") + "</td></tr>";
    }).join("");
    const title = placeLabel ? ("Chart at " + placeLabel) : "Relocated chart snapshot";
    return (
      "<div class=\"rm-qs-chart-facts panel\">" +
      "<h4 style=\"margin:0 0 8px;\">" + title + "</h4>" +
      "<p class=\"meta\" style=\"margin:0 0 8px;\">Frozen chart facts from the share snapshot. Read-only.</p>" +
      (angleRows ? "<table class=\"simple\"><tr><th>Angle</th><th colspan=\"2\">Sign</th></tr>" + angleRows + "</table>" : "") +
      (planetRows ? "<table class=\"simple\" style=\"margin-top:8px;\"><tr><th>Planet</th><th>Sign</th><th>House</th></tr>" + planetRows + "</table>" : "") +
      "</div>"
    );
  }

  global.RMQuickShare = {
    buildQuickShareUrl,
    copyTextToClipboard,
    createQuickShare,
    createAndCopyQuickShare,
    renderChartFactsReadOnlyHtml,
  };
})(typeof window !== "undefined" ? window : globalThis);
