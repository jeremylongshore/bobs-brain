from src.app import app

def test_config_and_backends():
    c=app.test_client()
    assert c.get("/config").status_code==200
    assert c.get("/health/backends").status_code==200