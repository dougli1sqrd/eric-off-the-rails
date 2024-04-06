#!/bin/bash
set -euo pipefail

docker run -it --rm -v ./static:/srv/jekyll jekyll /bin/bash -c "bundle exec jekyll build -w"

