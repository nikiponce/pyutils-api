PYTHON_VERSION=3.8.10
SERVICE_NAME=pyutils
HOST_UID=$(shell id -u)
HOST_GID=$(shell id -g)
DOCKER_COMPOSE=PYTHON_VERSION=$(PYTHON_VERSION) docker-compose

.PHONY: help
help: Makefile
	@echo "Lista de comandos disponibles para gestionar el contenedor del servicio $(SERVICE_NAME):"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-10s\033[0m %s\n", $$1, $$2}'

build: ## up and build
	@$(DOCKER_COMPOSE) -f docker-compose.dev.yaml  up --build
up: ## up 
	@$(DOCKER_COMPOSE) -f docker-compose.dev.yaml up

sh: ## sh 
	@$(DOCKER_COMPOSE) run $(SERVICE_NAME) sh

.PHONY: pip
pip: ## Agrega paquetes con pnpm dentro del contenedor, e.g., make add vue-router@next axios
	@$(DOCKER_COMPOSE) run --rm $(SERVICE_NAME) pip install $(filter-out $@,$(MAKECMDGOALS))