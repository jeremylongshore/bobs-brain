from my_agent.agent import create_runner

def test_runner_constructs():
    r = create_runner()
    assert r is not None
