.PHONY: unit-test
unit-test:
	pytest tests/unit --cov=kryptic_cypher --cov-report=term --cov-report=xml --cov-report=html
.PHONY: int-test
int-test:
	pytest tests/integration --cov=kryptic_cypher --cov-report=term --cov-report=xml --cov-report=html
.PHONY: all-test
all-test:
	pytest tests --cov=kryptic_cypher --cov-report=term --cov-report=xml --cov-report=html
.PHONY: docs
docs:
	pdoc ./kryptic_cypher
.PHONY: build-docs
build-docs:
	make cov-all
	pdoc ./kryptic_cypher -o ./docs
.PHONY: cov-all
cov-all:
	pytest tests --cov=kryptic_cypher --cov-report=html:docs/coverage --html=docs/coverage/report.html
.PHONY: render-cov
render-cov:
	python -m http.server -d htmlcov 8081
.PHONY: format
format:
	black .