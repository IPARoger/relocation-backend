/**
 * supabase_client.js — shared Supabase client initialization.
 *
 * Fetches public config (URL + anon key) from the backend at /config/supabase,
 * then initializes @supabase/supabase-js via CDN UMD build.
 *
 * Exposes two globals:
 *   window.SupabaseClient  — the initialized Supabase client instance (once ready)
 *   window.SupabaseReady   — a Promise<SupabaseClient> that resolves when the client
 *                            is initialized, or rejects on config/load failure.
 *
 * Usage in any page script:
 *   const client = await window.SupabaseReady;
 *   const { data: { session } } = await client.auth.getSession();
 *
 * Requirements:
 *   - This script must be loaded before any script that calls window.SupabaseReady.
 *   - No CDN <script> tag for supabase-js is needed in HTML; this file loads it
 *     dynamically if not already present on the page.
 *   - The backend must be running and serving /config/supabase.
 *
 * Not in scope: auth UI, session guards, profile logic, map changes.
 */
(function () {
  "use strict";

  var SUPABASE_CDN =
    "https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2/dist/umd/supabase.js";
  var CONFIG_ENDPOINT = "/config/supabase";

  /** Load a script tag dynamically. Returns a Promise. */
  function loadScript(src) {
    return new Promise(function (resolve, reject) {
      if (
        document.querySelector('script[src="' + src + '"]') ||
        (window.supabase && window.supabase.createClient)
      ) {
        resolve();
        return;
      }
      var script = document.createElement("script");
      script.src = src;
      script.onload = resolve;
      script.onerror = function () {
        reject(new Error("Failed to load Supabase CDN: " + src));
      };
      document.head.appendChild(script);
    });
  }

  /** Fetch public config from the backend. Returns Promise<{url, anonKey}>. */
  function fetchConfig() {
    return fetch(CONFIG_ENDPOINT)
      .then(function (res) {
        if (!res.ok) {
          throw new Error(
            "Supabase config endpoint returned HTTP " + res.status
          );
        }
        return res.json();
      })
      .then(function (cfg) {
        if (!cfg.url || !cfg.anonKey) {
          throw new Error(
            "Supabase config missing url or anonKey. Check server .env."
          );
        }
        return cfg;
      });
  }

  var ready = fetchConfig()
    .then(function (cfg) {
      return loadScript(SUPABASE_CDN).then(function () {
        return cfg;
      });
    })
    .then(function (cfg) {
      if (!window.supabase || !window.supabase.createClient) {
        throw new Error(
          "supabase.createClient not found after CDN load."
        );
      }
      var client = window.supabase.createClient(cfg.url, cfg.anonKey);
      window.SupabaseClient = client;
      return client;
    });

  window.SupabaseReady = ready;

  ready.catch(function (err) {
    console.error("[SupabaseClient] initialization failed:", err);
  });
})();
