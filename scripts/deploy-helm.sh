#!/bin/bash
set -e -o pipefail

# Set the chart repository URL
CHART_REPO="oci://ghcr.io/fyodorovai/tsiolkovsky-helm"

# Set the release name
RELEASE_NAME="tsiolkovsky-helm"

# Set the namespace
NAMESPACE="fyodorov"

# Install the Helm chart
kubectl config use-context do-ams3-fyodorov-ai-cluster
kubectl create namespace $NAMESPACE || true
helm install $RELEASE_NAME $CHART_REPO --namespace $NAMESPACE || \
helm upgrade $RELEASE_NAME $CHART_REPO --namespace $NAMESPACE
