# UI container — Next.js static export served by `serve`.
#
# The dashboard uses `output: "export"` (see ui/litellm-dashboard/next.config.mjs)
# so the build produces a folder of static HTML/JS in `out/`. We serve it on
# port 3000. The proxy_server used to mount the same files at `/_next/` AND
# `<assetPrefix>/_next/`; we replicate that by symlinking the asset-prefix path
# at build time so existing HTML asset URLs resolve.

FROM node:20-alpine AS builder

WORKDIR /app

COPY ui/litellm-dashboard/package.json ui/litellm-dashboard/package-lock.json ./
RUN npm ci

COPY ui/litellm-dashboard/ ./
RUN npm run build && \
    cp -r out/_next out/litellm-asset-prefix && \
    mv out/litellm-asset-prefix out/litellm-asset-prefix-tmp && \
    mkdir out/litellm-asset-prefix && \
    mv out/litellm-asset-prefix-tmp out/litellm-asset-prefix/_next

# ---------- Runtime ----------
FROM node:20-alpine AS runtime

WORKDIR /app

RUN npm install -g serve@14.2.4

COPY --from=builder /app/out ./out

EXPOSE 3000/tcp

# `-s` rewrites unknown paths to index.html (SPA fallback).
# `--no-clipboard` keeps the container quiet on startup.
CMD ["serve", "-s", "out", "-l", "3000", "--no-clipboard"]
