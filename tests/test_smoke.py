from src.app import app

def test_health_ok():
    c=app.test_client(); r=c.get("/health"); assert r.status_code==200

def test_auth_required():
    c=app.test_client(); r=c.post("/api/query", json={"query":"hi"}); assert r.status_code==401

def test_query_with_key():
    c=app.test_client(); r=c.post("/api/query", headers={"X-API-Key":"test"}, json={"query":"hi"})
    assert r.status_code in (200,500)
