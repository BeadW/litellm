"""Path allowlist for the gateway component.

The gateway exposes the LLM data-plane surface: chat/completions, embeddings,
audio, batches, files, fine-tuning, rerank, ocr, rag, video, search, image,
responses, vector stores, passthrough providers, realtime websockets, and
operational endpoints (/health, /metrics).

Any path not listed here is dropped from the gateway process so management/UI
endpoints don't ride on the same pods.
"""

GATEWAY_PATH_PREFIXES: tuple[str, ...] = (
    # OpenAI-compatible surface
    "/v1/",
    "/v2/",
    "/openai/",
    "/chat/",
    "/completions",
    "/embeddings",
    "/moderations",
    "/audio/",
    "/images/",
    "/files",
    "/batches",
    "/fine_tuning/",
    "/fine-tuning/",
    "/responses",
    "/threads",
    "/assistants",
    "/vector_stores",
    "/messages",
    # LiteLLM-native LLM surface
    "/rerank",
    "/ocr",
    "/rag/",
    "/video/",
    "/search",
    "/containers",
    # Provider passthrough
    "/anthropic/",
    "/azure/",
    "/aws/",
    "/bedrock/",
    "/cohere/",
    "/gemini/",
    "/google/",
    "/vertex_ai/",
    "/vertex-ai/",
    "/assemblyai/",
    "/eu.assemblyai/",
    "/langfuse/",
    "/vllm/",
    "/mistral/",
    "/groq/",
    "/voyage/",
    # Realtime / streaming
    "/realtime",
    # Health & ops
    "/health",
    "/metrics",
    "/test",
)

GATEWAY_EXACT_PATHS: frozenset[str] = frozenset(
    {
        "/",
        "/routes",
        "/openapi.json",
        "/docs",
        "/docs/oauth2-redirect",
        "/redoc",
    }
)
