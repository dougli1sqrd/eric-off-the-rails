#!/bin/bash
set -euo pipefail

docker build . -f docker/Dockerfile.BuildJekyll --build-arg gid=1000 --build-arg uid=1000 "$@"

