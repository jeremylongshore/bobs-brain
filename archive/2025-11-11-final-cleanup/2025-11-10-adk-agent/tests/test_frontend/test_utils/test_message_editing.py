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

from unittest.mock import MagicMock

import pytest

from frontend.utils.message_editing import MessageEditing


@pytest.fixture
def mock_streamlit() -> MagicMock:
    """Create a mock streamlit object with required session state"""
    st = MagicMock()
    st.session_state = MagicMock()

    # Configure session_state getitem to return values
    def getitem(key: str) -> str:
        if key == "session_id":
            return "test-123"
        if key == "edit_box_0":
            return "Edited message"
        if key == "edit_box_1":
            return "Edited message 2"
        raise KeyError(key)

    st.session_state.__getitem__.side_effect = getitem

    st.session_state.session_id = "test-123"
    st.session_state.user_chats = {"test-123": {"messages": []}}
    return st


def test_edit_message_human(mock_streamlit: MagicMock) -> None:
    """Test editing a human message"""
    mock_streamlit.session_state.user_chats["test-123"]["messages"] = [
        {"type": "human", "content": "Original message"},
        {"type": "ai", "content": "Response message"},
    ]

    MessageEditing.edit_message(mock_streamlit, 0, "human")

    assert mock_streamlit.session_state.modified_prompt == "Edited message"
    assert len(mock_streamlit.session_state.user_chats["test-123"]["messages"]) == 0


def test_edit_message_ai(mock_streamlit: MagicMock) -> None:
    """Test editing an AI message"""
    mock_streamlit.session_state.user_chats["test-123"]["messages"] = [
        {"type": "human", "content": "Original message"},
        {"type": "ai", "content": "Original AI response"},
    ]

    MessageEditing.edit_message(mock_streamlit, 1, "ai")

    messages = mock_streamlit.session_state.user_chats["test-123"]["messages"]
    assert len(messages) == 2
    assert messages[0]["content"] == "Original message"
    assert messages[1]["content"] == "Edited message 2"


def test_refresh_message(mock_streamlit: MagicMock) -> None:
    """Test refreshing a message"""
    mock_streamlit.session_state.user_chats["test-123"]["messages"] = [
        {"type": "human", "content": "Message 1"},
        {"type": "ai", "content": "Message 2"},
        {"type": "human", "content": "Message 3"},
    ]

    MessageEditing.refresh_message(mock_streamlit, 1, "Refreshed content")

    messages = mock_streamlit.session_state.user_chats["test-123"]["messages"]
    assert mock_streamlit.session_state.modified_prompt == "Refreshed content"
    assert len(messages) == 1
    assert messages[0]["content"] == "Message 1"


def test_delete_message(mock_streamlit: MagicMock) -> None:
    """Test deleting a message"""
    mock_streamlit.session_state.user_chats["test-123"]["messages"] = [
        {"type": "human", "content": "Message 1"},
        {"type": "ai", "content": "Message 2"},
        {"type": "human", "content": "Message 3"},
    ]

    MessageEditing.delete_message(mock_streamlit, 1)

    messages = mock_streamlit.session_state.user_chats["test-123"]["messages"]
    assert len(messages) == 1
    assert messages[0]["content"] == "Message 1"
