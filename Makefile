.ONESHELL:

SHELL  = /bin/bash
PYTHON = /usr/bin/python3

PYTHON_VERSION = 3.12.3


-include .env
export


define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
    match = re.match(r'^([a-zA-Z_-]+):.*?## (.*?)(?: - (.*))?$$', line)
    if match:
        target, params, help = match.groups()
        target = target.ljust(21)
        params = params.ljust(55)
        print("  %s %s %s" % (target, params, help or ""))
endef
export PRINT_HELP_PYSCRIPT


MAKEFLAGS += --silent


help:
	@echo "Usage: make <command> <parameters>"
	@echo "Options:"

	@$(PYTHON) -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)


version:  ## Read or update api version - Parameters: update-to=[0-9].[0-9].[0-9]
	@poetry version $(if $(update-to), $(update-to), -s)

build: stop  ## Build dockerized images, run tests and code convention
	@docker-compose build
	@docker-compose -f compose.yml -f compose.development.yml build

	@$(MAKE) database

	@$(MAKE) tests dockerized=true
	@$(MAKE) code-convention dockerized=true

dependencies:  ## Resolve dependencies for local development
	@poetry --version &> /dev/null || (pip3 install poetry && false) && \
		poetry config virtualenvs.in-project true

	@poetry config virtualenvs.in-project true
	@poetry env use $(shell pyenv which python)

	@poetry lock
	@poetry install

tests: -B  ## Run tests - Parameters: dockerized=true, verbose=true
	POETRY_RUN=""
	DOCKER_COMPOSE=""

	@if [ "$(dockerized)" = "true" ]; then
		DOCKER_COMPOSE="docker-compose -f compose.yml -f compose.development.yml run -e APP_ENVIRONMENT=tests --rm runner"
	else
		POETRY_RUN="poetry run"
	fi

	APP_ENVIRONMENT=tests $$DOCKER_COMPOSE $$POETRY_RUN pytest $(if $(filter "$(verbose)", "true"),-sxvv,)

tests-debug: -B  ## Run debuggable tests - Parameters: dockerized=true, verbose=true
	POETRY_RUN=""
	DOCKER_COMPOSE=""

	@if [ "$(dockerized)" = "true" ]; then
		DOCKER_COMPOSE="docker-compose -f compose.yml -f compose.development.yml run -e APP_ENVIRONMENT=tests --service-ports --rm runner"
	else
		POETRY_RUN="poetry run"
	fi

	echo "==== Ready to attach to port 5789..."

	APP_ENVIRONMENT=tests PYDEVD_DISABLE_FILE_VALIDATION=true $$DOCKER_COMPOSE $$POETRY_RUN python \
		-m debugpy --listen ${APP_HOST}:5678 --wait-for-client -m pytest $(if $(filter "$(verbose)", "true"),-sxvv,)

code-convention:  ## Run dockerized code convention - Parameters: dockerized=true, fix-imports=true, github=true
	POETRY_RUN=""
	DOCKER_COMPOSE=""

	@if [ "$(dockerized)" = "true" ]; then
		DOCKER_COMPOSE="docker-compose -f compose.yml -f compose.development.yml run --rm runner"
	else
		POETRY_RUN="poetry run"
	fi

	$$DOCKER_COMPOSE $$POETRY_RUN ruff check . $(if $(filter "$(github)", "true"),--output-format github,)
	$$DOCKER_COMPOSE $$POETRY_RUN isort $(if $(filter "$(fix-imports)", "true"),,--check) . -q

coverage:  ## Run dockerized tests and write reports - Parameters: dockerized=true
	POETRY_RUN=""
	DOCKER_COMPOSE=""

	@if [ "$(dockerized)" = "true" ]; then
		DOCKER_COMPOSE="docker-compose -f compose.yml -f compose.development.yml run -e APP_ENVIRONMENT=tests --rm runner"
	else
		POETRY_RUN="poetry run"
	fi

	APP_ENVIRONMENT=tests $$DOCKER_COMPOSE $$POETRY_RUN pytest --cov-report=html:tests/reports

database:  ## Run dockerized mongodb database - Parameters: seed=true
	@docker-compose up mongodb --wait

	@sleep 5
	@docker-compose run --rm mongodb-init > /dev/null 2>&1 || true

	@if [ "$(seed)" = "true" ]; then
		$(MAKE) database-seeds
	fi

database-seeds:  ## Run seeds on dockerized mongodb database - Parameters: dockerized=true
	POETRY_RUN=""

	@if [ "$(dockerized)" = "true" ]; then
		DOCKER_COMPOSE="docker-compose -f compose.yml -f compose.development.yml run --rm runner"
	else
		POETRY_RUN="poetry run"
	fi

	$$DOCKER_COMPOSE $$POETRY_RUN python seeds/main.py > /dev/null 2>&1 || true

database-seeds-debug:  ## Run debuggable seeds on dockerized mongodb database - Parameters: dockerized=true
	POETRY_RUN=""
	DOCKER_COMPOSE=""

	@if [ "$(dockerized)" = "true" ]; then
		DOCKER_COMPOSE="docker-compose -f compose.yml -f compose.development.yml run --service-ports --rm runner"
	else
		POETRY_RUN="poetry run"
	fi

	echo "==== Ready to attach to port 5789..."

	PYDEVD_DISABLE_FILE_VALIDATION=true $$DOCKER_COMPOSE $$POETRY_RUN python -m debugpy --listen ${APP_HOST}:5678 --wait-for-client seeds/main.py

run:  ## Run dockerized api
	@docker-compose up api

run-debug:  ## Run debuggable dockerized api
	@COMPOSE_DEVELOPMENT_COMMAND="python -m debugpy --listen ${APP_HOST}:5678 -m uvicorn api.main:app --host ${APP_HOST} --port ${APP_HOST_PORT} --reload" \
		docker-compose -f compose.yml -f compose.development.yml up api

run-terminal:  ## Run debuggable dockerized api terminal - Parameters: environment=staging|production
	RUNNER="run --rm runner"

	@if [ "$(environment)" = "staging" ]; then
		docker-compose -f compose.yml -f compose.development.yml $$RUNNER
	elif [ "$(environment)" = "production" ]; then
		docker-compose $$RUNNER
	else
		echo "==== Environment not found."
	fi

monitoring:  ## Run dockerized monitoring
	@docker-compose up -d prometheus grafana --wait

stop:  ## Stop all dockerized services
	@docker-compose down --volumes

secrets:  ## Encrypt or decrypt k8s secrets - Parameters: action=encrypt|decrypt, environment=staging|production
	@if [ "$(action)" = "encrypt" ]; then
		SECRETS_PATH=".k8s/$(environment)/secrets"
		SECRETS_PUBLIC_KEY="$$(cat $$SECRETS_PATH/.sops.yml | awk "/age:/" | sed "s/.*: *//" | xargs -d "\r")"

		sops -e -i --encrypted-regex "^(data|stringData)$$" -a $$SECRETS_PUBLIC_KEY \
			$$SECRETS_PATH/.secrets.yml

		echo "==== Ok"

	elif [ "$(action)" = "decrypt" ]; then
		SECRETS_KEY="$$(kubectl get secret sops-age --namespace argocd -o yaml | awk "/sops-age.txt:/" | sed "s/.*: *//" | base64 -d)"

		SOPS_AGE_KEY=$$SECRETS_KEY sops -d -i .k8s/$(environment)/secrets/.secrets.yml && \
			echo "==== Ok"

	else
		echo "==== Action not found."
	fi

github-tag:  ## Manage github tags - Parameters: action=create|delete, tag=[0-9].[0-9].[0-9]-staging|[0-9].[0-9].[0-9]
	@if [ "$(action)" = "create" ]; then
		git tag $(tag) && git push origin $(tag)
	elif [ "$(action)" = "delete" ]; then
		git tag -d $(tag) && git push origin :refs/tags/$(tag)
	else
		echo "==== Action not found"
	fi


%:
	@:
