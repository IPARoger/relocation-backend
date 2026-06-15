/**
 * auth_guard.js — session guard for protected pages.
 *
 * Waits for window.SupabaseReady, then checks for an active Supabase session.
 * If no session is found, redirects to /auth.html immediately — before any
 * page rendering or data fetching can proceed.
 *
 * Also exposes window.logout() for use by any page UI.
 *
 * Requirements:
 *   - supabase_client.js must be loaded before this script.
 *   - Include both scripts in the <head>, before any application scripts.
 *
 * Usage:
 *   <script src="/supabase_client.js"></script>
 *   <script src="/auth_guard.js"></script>
 *
 * Then from any button or link:
 *   onclick="window.logout()"
 */
(function () {
  "use strict";

  var AUTH_URL = "/auth.html";

  /**
   * logout() — sign out and redirect to auth screen.
   * Exposed as window.logout() for use from any page element.
   */
  window.logout = function logout() {
    window.SupabaseReady.then(function (client) {
      return client.auth.signOut();
    }).then(function () {
      window.location.href = AUTH_URL;
    }).catch(function () {
      // If signOut fails (e.g. already expired), still redirect.
      window.location.href = AUTH_URL;
    });
  };

  /**
   * requireAuth() — check session and redirect if unauthenticated.
   * Runs immediately on script load.
   */
  window.SupabaseReady.then(function (client) {
    return client.auth.getSession();
  }).then(function (result) {
    if (!result || !result.data || !result.data.session) {
      window.location.href = AUTH_URL;
    }
    // Session present — continue normally. No action needed.
  }).catch(function (err) {
    // Config load failed or CDN unavailable. Redirect to auth as a safe fallback.
    console.error("[auth_guard] session check failed:", err);
    window.location.href = AUTH_URL;
  });

})();
