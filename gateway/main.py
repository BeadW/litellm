"""Gateway entrypoint.

Reuses the existing FastAPI app from `litellm.proxy.proxy_server` and trims its
route table to just the LLM data-plane surface. The trim is purely additive —
no existing module is modified, the full app continues to work via the legacy
entrypoint (`litellm.proxy.proxy_server:app`).

Run with:
    uvicorn gateway.main:app --host 0.0.0.0 --port 4000
"""

from fastapi.routing import Mount

from litellm.proxy.proxy_server import app

from gateway.routes.allowlist import GATEWAY_EXACT_PATHS, GATEWAY_PATH_PREFIXES


def _is_gateway_route(route) -> bool:
    """Keep the route on the gateway if its path is in the LLM data-plane surface."""
    path = getattr(route, "path", None)
    if path is None:
        return False
    if isinstance(route, Mount):
        # Gateway never serves the static UI or its asset bundles.
        return False
    if path in GATEWAY_EXACT_PATHS:
        return True
    return any(path.startswith(prefix) for prefix in GATEWAY_PATH_PREFIXES)


app.router.routes = [r for r in app.router.routes if _is_gateway_route(r)]
