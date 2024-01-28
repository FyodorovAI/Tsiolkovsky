#!/bin/bash

set -e -o pipefail

docker build . -t ghcr.io/fyodorovai/tsiolkovsky
docker login ghcr.io -u $GITHUB_ACTOR --password-stdin
docker push ghcr.io/fyodorovai/tsiolkovsky