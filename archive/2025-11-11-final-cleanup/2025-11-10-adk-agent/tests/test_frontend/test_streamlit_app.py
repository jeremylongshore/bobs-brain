# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import Any
from unittest.mock import MagicMock, patch

import pytest

from frontend.streamlit_app import (
    display_chat_message,
    display_message_buttons,
    display_messages,
    display_tool_output,
    display_user_input,
)


@pytest.fixture
def st_mock() -> Any:
    """Fixture providing a MockStreamlit instance"""

    class MockStreamlit:
        class SessionState(dict):
            def __init__(self, messages: list[dict[str, Any]] | None = None) -> None:
                super().__init__()
                self.user_chats: dict[str, dict[str, list[dict[str, Any]]]] = {
                    "test_session": {"messages": messages or []}
                }
                self["session_id"] = "test_session"
                self["user_id"] = "test_user"
                self["run_id"] = "dummy"

        def __init__(self, messages: list[dict[str, Any]] | None = None) -> None:
            self.session_state = self.SessionState(messages)
            self.markdown_calls: list[tuple[str, bool]] = []
            self.button_calls: list[tuple[str, str | None, str | None, Any | None]] = []
            self.expander_calls: list[tuple[str | None, bool | None]] = []
            self.error_calls: list[str] = []

        def chat_message(self, _: str) -> MagicMock:
            return MagicMock()

        def columns(self, widths: list[int]) -> list[MagicMock]:
            return [MagicMock() for _ in widths]

        def markdown(self, text: str, unsafe_allow_html: bool = False) -> None:
            self.markdown_calls.append((text, unsafe_allow_html))

        def button(
            self,
            label: str,
            key: str | None = None,
            type: str | None = None,
            on_click: Any | None = None,
        ) -> bool:
            self.button_calls.append((label, key, type, on_click))
            if key:
                self.session_state[key] = False
            return False

        def expander(
            self, label: str | None = None, expanded: bool | None = None
        ) -> MagicMock:
            mock = MagicMock()
            mock.markdown = MagicMock()
            self.expander_calls.append((label, expanded))
            return mock

        def text_area(
            self,
            label: str,
            value: str,
            key: str | None = None,
            on_change: Any | None = None,
        ) -> str:
            return value

        def error(self, message: str) -> None:
            self.error_calls.append(message)

        def write(self, *args: Any, **kwargs: Any) -> None:
            self.markdown_calls.append((str(args[0]), False))

    return MockStreamlit()


def test_display_chat_message(st_mock: Any) -> None:
    """Test displaying a single chat message"""
    message = {"type": "human", "content": "test message"}

    with patch("frontend.streamlit_app.st", st_mock):
        display_chat_message(message, 0)

    assert len(st_mock.markdown_calls) > 0


def test_display_message_buttons(st_mock: Any) -> None:
    """Test displaying message control buttons"""
    message = {"type": "human", "content": "test message"}
    cols = st_mock.columns([2, 2, 94])

    with patch("frontend.streamlit_app.st", st_mock):
        display_message_buttons(message, 0, cols[0], cols[1], cols[2])

    assert all(
        key in st_mock.session_state for key in ["0_edit", "0_refresh", "0_delete"]
    )


def test_display_tool_output(st_mock: Any) -> None:
    """Test displaying tool call input/output"""
    tool_input = {"name": "test_tool", "args": {"arg1": "value1"}}
    tool_output = {"content": "test output"}

    with patch("frontend.streamlit_app.st", st_mock):
        display_tool_output(tool_input, tool_output)

    assert len(st_mock.expander_calls) == 1
    assert st_mock.expander_calls[0] == ("Tool Calls:", False)


def test_display_user_input(st_mock: Any) -> None:
    """Test displaying user input"""
    parts = [{"type": "text", "text": "test input"}]

    with patch("frontend.streamlit_app.st", st_mock):
        display_user_input(parts)

    assert len(st_mock.markdown_calls) == 1
    assert st_mock.markdown_calls[0] == ("test input", True)


def test_display_messages(st_mock: Any) -> None:
    """Test displaying all messages in chat"""
    messages = [
        {"type": "human", "content": "test question"},
        {"type": "ai", "content": "test response"},
        {
            "type": "ai",
            "tool_calls": [
                {"id": "test_id", "name": "test_tool", "args": {"arg1": "value1"}}
            ],
            "content": "",
        },
        {"type": "tool", "tool_call_id": "test_id", "content": "tool output"},
    ]
    st_mock.session_state.user_chats["test_session"]["messages"] = messages

    with patch("frontend.streamlit_app.st", st_mock):
        display_messages()

        assert len(st_mock.markdown_calls) >= 2
        assert len(st_mock.expander_calls) == 1
        assert st_mock.expander_calls[0] == ("Tool Calls:", False)

        with pytest.raises(ValueError):
            messages.append({"type": "invalid_type"})
            display_messages()
