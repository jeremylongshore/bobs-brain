from src.circle_of_life import CircleOfLife

def test_dedupe_and_cooldown():
    col = CircleOfLife(llm_call=lambda p: [{"pattern":"p","action":"a","confidence":0.9}])
    r1 = col.run_once([{"type":"t","v":1},{"type":"t","v":1}])
    r2 = col.run_once([{"type":"t","v":2}])
    assert r1["ran"] is True and r1["batch"] == 1
    assert r2["ran"] is False
