#!/bin/bash
set -euo pipefail

docker build . -f docker/Dockerfile.BuildJekyll --build-arg gid=${SUDO_GID} --build-arg gname=$(getent group $SUDO_GID | cut -d: -f1) --build-arg uid=${SUDO_UID} --build-arg uname=${SUDO_USER} "$@"

