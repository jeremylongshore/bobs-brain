.PHONY: dev test smoke
dev:
	adk api_server
test:
	pytest -q
smoke:
	bash scripts/smoke_test.sh
