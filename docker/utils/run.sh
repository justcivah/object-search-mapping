#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

if [ ! -f .env ]; then
    ./utils/generate-env.sh
fi

# x11 cookie used by the container to draw windows on the host display
# on wayland XAUTHORITY points to a temporary file that changes at every login,
# so it is resolved here at every start instead of being stored in .env
XAUTH_FILE="${XAUTHORITY:-$HOME/.Xauthority}"
if [ -f "$XAUTH_FILE" ]; then
    export XAUTH_FILE
else
    unset XAUTH_FILE
    # no cookie available: fall back to allowing local connections, if xhost is installed
    if command -v xhost > /dev/null; then
        xhost +local:docker
    else
        echo "Warning: no Xauthority file and no xhost, GUI apps may fail to open" >&2
    fi
fi

docker compose up -d
echo "Container started. Open a terminal using the script terminal.sh"
