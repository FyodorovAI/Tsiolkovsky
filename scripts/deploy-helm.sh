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
if helm list -q | grep -q "^$RELEASE_NAME$"; then
    helm upgrade $RELEASE_NAME --namespace $NAMESPACE \
    --set env[0].value=$SUPABASE_PROJECT_URL \
    --set env[1].value=$SUPABASE_API_KEY \
    --set env[2].value=$JWT_SECRET
else
    helm install $RELEASE_NAME $CHART_REPO --namespace $NAMESPACE \
    --set env[0].name=supabaseProjectURL --set env[0].value=$SUPABASE_PROJECT_URL \
    --set env[1].name=supabaseAPIKey --set env[1].value=$SUPABASE_API_KEY \
    --set env[2].name=jwtSecret --set env[2].value=$JWT_SECRET
fi
