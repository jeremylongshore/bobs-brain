.PHONY: dev test smoke
dev:
	uvicorn main:app --reload --host 0.0.0.0 --port ${PORT:-8080}
test:
	pytest -q
smoke:
	bash scripts/smoke_test.sh
