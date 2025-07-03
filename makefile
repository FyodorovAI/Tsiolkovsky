.PHONY: all

all: helm-build deploy-helm

helm-build: 
	./scripts/push-helm.sh

deploy-helm:
	make -C ./helm deploy-helm

docker-build:
	./scripts/docker-push.sh