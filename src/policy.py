from typing import Any, Dict


def guard_request(path: str, body: Dict[str, Any]) -> None:
    # basic examples; expand as needed
    if path.startswith("/api/query"):
        if (
            not isinstance(body.get("query", ""), str)
            or len(body["query"]) == 0
        ):
            raise ValueError("Invalid query")
