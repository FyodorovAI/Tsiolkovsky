.PHONY: all

all: helm-build helm-deploy

helm-build: 
	./scripts/push-helm.sh

helm-deploy:
	. ./src/.env && \
	helm upgrade --install tsiolkovsky ./helm --namespace fyodorov --create-namespace \
	--set env.SUPABASE_PROJECT_URL=$${SUPABASE_PROJECT_URL} \
	--set env.SUPABASE_API_KEY=$${SUPABASE_API_KEY} \
	--set env.JWT_SECRET=$${JWT_SECRET}

docker-build:
	./scripts/docker-push.sh