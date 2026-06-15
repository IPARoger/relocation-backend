/**
 * user_profile.js — authenticated user / account loader.
 *
 * Waits for window.SupabaseReady, resolves the authenticated session,
 * and loads the user's primary account row from Supabase.
 *
 * Uses:
 *   app_account_ids() RPC  — SECURITY DEFINER, returns account UUIDs for
 *                            the calling auth.uid() (bypasses RLS safely).
 *   accounts table         — direct SELECT scoped to the resolved account_id.
 *   account_memberships    — direct SELECT for role.
 *
 * Exposes:
 *   window.CurrentUser     — populated once load succeeds (see shape below).
 *   window.CurrentUserReady — Promise<CurrentUser> that resolves when done.
 *   window.initializeCurrentUser() — re-runnable init; returns the same Promise.
 *
 * window.CurrentUser shape:
 * {
 *   userId:      string   — auth.users.id
 *   accountId:   string   — accounts.id (primary personal account)
 *   accountName: string   — accounts.name
 *   accountType: string   — accounts.account_type
 *   role:        string   — account_memberships.role
 * }
 *
 * Requirements:
 *   supabase_client.js and auth_guard.js must be loaded before this script.
 *
 * Note on "professional_accounts":
 *   The project's database uses the table name "accounts" (Phase 1 migration).
 *   "Professional account" in product language maps to the accounts +
 *   account_memberships rows created automatically by the handle_new_user()
 *   trigger on signup. This file loads that record.
 */
(function () {
  "use strict";

  var _resolveReady;
  var _rejectReady;

  /** Promise<CurrentUser> — resolves when CurrentUser is populated. */
  var readyPromise = new Promise(function (resolve, reject) {
    _resolveReady = resolve;
    _rejectReady  = reject;
  });

  window.CurrentUserReady = readyPromise;

  /**
   * initializeCurrentUser() — main entry point.
   * Safe to call more than once; returns the same promise.
   */
  function initializeCurrentUser() {
    window.SupabaseReady.then(function (client) {
      return client.auth.getSession().then(function (result) {
        var session = result && result.data && result.data.session;
        if (!session) {
          throw new Error("[user_profile] No active session — auth_guard should have redirected.");
        }

        var userId = session.user.id;

        // 1. Resolve account IDs via SECURITY DEFINER RPC (RLS-safe).
        return client.rpc("app_account_ids").then(function (rpcResult) {
          if (rpcResult.error) {
            throw new Error("[user_profile] app_account_ids() failed: " + rpcResult.error.message);
          }

          var accountIds = rpcResult.data || [];

          // 2a. Happy path — account exists.
          if (accountIds.length > 0) {
            return loadAccount(client, userId, accountIds[0]);
          }

          // 2b. No account found — hard failure.
          //     The only approved bootstrap path is the handle_new_user()
          //     SECURITY DEFINER trigger (Phase 6). Creating an account from the
          //     anon key is impossible under Phase 5 RLS (memberships_insert requires
          //     an existing membership — bootstrap paradox). Attempting it would
          //     create orphaned accounts rows. Do not perform any database writes.
          throw new Error(
            "[user_profile] No account membership found for authenticated user. " +
            "handle_new_user() may be missing or the account is corrupted. " +
            "No database writes attempted. Ensure Phase 6 is applied to this project."
          );
        });
      });
    }).then(function (currentUser) {
      window.CurrentUser = currentUser;
      console.log("[user_profile] CurrentUser loaded:", currentUser);
      _resolveReady(currentUser);
    }).catch(function (err) {
      console.error("[user_profile] Failed to load CurrentUser:", err);
      window.CurrentUser = null;
      _rejectReady(err);
    });

    return readyPromise;
  }

  /**
   * loadAccount() — fetch the accounts row and role, return CurrentUser object.
   */
  function loadAccount(client, userId, accountId) {
    return client
      .from("accounts")
      .select("id, name, account_type")
      .eq("id", accountId)
      .single()
      .then(function (acctResult) {
        if (acctResult.error || !acctResult.data) {
          throw new Error(
            "[user_profile] Failed to load accounts row: " +
            (acctResult.error ? acctResult.error.message : "not found")
          );
        }
        var account = acctResult.data;

        return client
          .from("account_memberships")
          .select("role")
          .eq("account_id", accountId)
          .eq("user_id", userId)
          .single()
          .then(function (memResult) {
            return {
              userId:      userId,
              accountId:   account.id,
              accountName: account.name,
              accountType: account.account_type,
              role:        (memResult.data && memResult.data.role) || "owner",
            };
          });
      });
  }

  window.initializeCurrentUser = initializeCurrentUser;

  // Run immediately on load.
  initializeCurrentUser();

})();
