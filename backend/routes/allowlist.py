"""Path allowlist for the UI backend (control plane) component.

The backend exposes management/admin endpoints consumed by the UI: keys, users,
teams, orgs, customers, budgets, tags, workflows, model management, spend &
analytics, settings (router/cache/cost-tracking/fallbacks), SSO/onboarding,
audit logs, debug, enterprise admin, and UI bootstrap helpers (logo, favicon,
.well-known config).

Anything LLM data-plane is dropped — those run on the gateway component.
"""

BACKEND_PATH_PREFIXES: tuple[str, ...] = (
    # Identity / access
    "/key/",
    "/user/",
    "/team/",
    "/organization/",
    "/customer/",
    "/sso/",
    "/login",
    "/logout",
    "/token",
    "/onboarding/",
    "/audit",
    "/oauth/",
    # Models & routing config
    "/model/",
    "/model_group",
    "/model_access_group/",
    "/router_settings",
    "/fallbacks",
    "/cache_settings",
    "/cost_tracking",
    "/credentials",
    "/credential",
    # Budgets / tags / workflows / memory mgmt
    "/budget/",
    "/tag/",
    "/workflow/",
    "/memory/",
    "/mcp/",
    # Spend / analytics
    "/spend/",
    "/analytics/",
    "/global/",
    "/user_agent",
    "/daily/",
    # Caching admin
    "/cache/",
    "/caching/",
    # Callbacks / hooks
    "/callbacks",
    "/team_callback",
    # Enterprise admin
    "/enterprise/",
    # Debug / config
    "/debug/",
    "/config/",
    # UI bootstrap helpers (assets the dashboard fetches)
    "/get_logo_url",
    "/get_image",
    "/get_favicon",
    "/.well-known/",
    "/ui_discovery/",
    "/ui-config",
    "/sso_settings",
    # Health (k8s probes)
    "/health",
)

BACKEND_EXACT_PATHS: frozenset[str] = frozenset(
    {
        "/",
        "/routes",
        "/openapi.json",
        "/docs",
        "/docs/oauth2-redirect",
        "/redoc",
        "/fallback/login",
    }
)
