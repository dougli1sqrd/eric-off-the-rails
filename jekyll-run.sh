#!/bin/bash
set -euo pipefail

docker run -it --rm --init -v ./static:/srv/jekyll $1 bundle exec jekyll build -w --future

