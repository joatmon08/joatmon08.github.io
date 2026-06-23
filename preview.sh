#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

PORT="${PORT:-4000}"
LIVERELOAD_PORT="${LIVERELOAD_PORT:-35729}"
IMAGE="jekyll/jekyll:4"
CONTAINER="joatmon08-jekyll-preview"

# Stop a previous preview container if still running
docker rm -f "${CONTAINER}" >/dev/null 2>&1 || true

echo "Starting Jekyll preview at http://localhost:${PORT}"
echo "LiveReload on port ${LIVERELOAD_PORT} (browser should refresh after each rebuild)"
echo "Press Ctrl+C to stop."
echo

# :delegated improves macOS bind-mount sync; --force_polling watches file changes
docker run --rm -it \
  --name "${CONTAINER}" \
  --volume "${PWD}:/srv/jekyll:delegated" \
  --publish "${PORT}:4000" \
  --publish "${LIVERELOAD_PORT}:${LIVERELOAD_PORT}" \
  "${IMAGE}" \
  jekyll serve \
    --host 0.0.0.0 \
    --force_polling \
    --livereload \
    --livereload-port "${LIVERELOAD_PORT}"
