VERSION := $(shell poetry version --no-ansi | tr -cd ".0-9")
HASH := $(shell git rev-parse --short HEAD)


black:
	poetry run isort tanser tests
	poetry run black tanser tests

build:
	docker build -t pavkazzz/tanser:$(VERSION)-$(HASH) .

upload: build
	docker push pavkazzz/tanser:$(VERSION)-$(HASH)

develop:
	pip install poetry==1.0.*
	poetry install

run:
	poetry run uvicorn tanser.__main__:app --reload