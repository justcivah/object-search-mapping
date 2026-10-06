#!/usr/bin/env bash
# generate the .env file read by docker compose
set -euo pipefail
cd "$(dirname "$0")/.."

# when launched with sudo use the ids of the real user, not root
HOST_UID="${SUDO_UID:-$(id -u)}"
HOST_GID="${SUDO_GID:-$(id -g)}"
if [ "$HOST_UID" -eq 0 ]; then
    echo "Error: run this script as your normal user, not as root" >&2
    exit 1
fi

# gid of the group owning a gpu device in /dev/dri
# the owner of the device is used first since the group name differs between distros
device_gid() {
    local pattern="$1" group="$2" dev
    for dev in /dev/dri/$pattern; do
        if [ -e "$dev" ]; then
            stat -c '%g' "$dev"
            return
        fi
    done
    getent group "$group" | cut -d: -f3 || true
}

RENDER_GID="$(device_gid 'renderD*' render)"
VIDEO_GID="$(device_gid 'card*' video)"
if [ -z "$RENDER_GID" ] || [ -z "$VIDEO_GID" ]; then
    echo "Error: unable to determine the gid of the render/video groups" >&2
    echo "Check that /dev/dri exists and try again" >&2
    exit 1
fi

if [ -f .env ]; then
    echo "Overwriting existing .env file"
fi

# .env file creation
cat > .env <<EOT
HOST_UID=${HOST_UID}
HOST_GID=${HOST_GID}
RENDER_GID=${RENDER_GID}
VIDEO_GID=${VIDEO_GID}
CONTAINER_USER=ros
EOT

echo ".env generated in $(pwd):"
cat .env
