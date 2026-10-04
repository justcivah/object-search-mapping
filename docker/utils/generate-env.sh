#!/usr/bin/env bash
# generate the .env file read by docker compose
set -euo pipefail
cd "$(dirname "$0")/.."

HOST_UID="$(id -u)"
HOST_GID="$(id -g)"

# gid of the group that owns the gpu render device in /dev/dri
# try the group name first, then fall back to the owner of the device
RENDER_GID="$(getent group render | cut -d: -f3 || true)"
if [ -z "$RENDER_GID" ] && [ -e /dev/dri/renderD128 ]; then
    RENDER_GID="$(stat -c '%g' /dev/dri/renderD128)"
fi
if [ -z "$RENDER_GID" ]; then
    echo "Error: unable to determine the gid of the render group" >&2
    echo "Check that /dev/dri exists and try again" >&2
    exit 1
fi

if [ -f .env ]; then
    echo "Overwriting existing .env file"
fi

# .env file creation
cat > .env <<EOF
HOST_UID=${HOST_UID}
HOST_GID=${HOST_GID}
RENDER_GID=${RENDER_GID}
CONTAINER_USER=ros
EOF

echo ".env generated in $(pwd):"
cat .env
