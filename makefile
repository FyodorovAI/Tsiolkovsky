.PHONY: all

all: helm-build helm-deploy

helm-build: 
	./scripts/push-helm.sh

helm-deploy:
	./scripts/deploy-helm.sh