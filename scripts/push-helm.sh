#!/bin/bash

set -e -o pipefail

echo 'Logging into ghcr.io'
# export $(cat .env); helm registry login ghcr.io -u $GITHUB_ACTOR --password-stdin $GITHUB_TOKEN
echo 'Packaging helm chart'
helm package ./helm
echo 'Pushing helm chart'
helm push ./tsiolkovsky-helm-*.tgz oci://ghcr.io/fyodorovai