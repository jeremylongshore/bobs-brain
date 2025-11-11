from my_agent.tools import get_current_time_tool

def test_time_tool_name():
    assert get_current_time_tool().name == "get_current_time"
