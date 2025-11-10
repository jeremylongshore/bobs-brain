.PHONY: run fmt test
run:
    BB_API_KEY=test python -m flask --app src.core.app run --host 0.0.0.0 --port 8080
fmt:
    isort src && black src
test:
    BB_API_KEY=test pytest -q