"""
Test A2A AgentCard - Hard Mode (R7)

Tests AgentCard creation and SPIFFE ID inclusion.
"""

import os
import pytest
from unittest.mock import patch


@pytest.fixture
def mock_env():
    """Mock environment variables for testing"""
    with patch.dict(os.environ, {
        # Required by agent.py
        "PROJECT_ID": "test-project",
        "LOCATION": "us-central1",
        "AGENT_ENGINE_ID": "test-engine-id",
        "AGENT_SPIFFE_ID": "spiffe://test.intent.solutions/agent/bobs-brain/test/us-central1/0.6.0",
        # Required by a2a_card.py
        "APP_NAME": "bobs-brain-test",
        "APP_VERSION": "0.6.0-test",
        "PUBLIC_URL": "https://test.example.com"
    }):
        yield


def test_get_agent_card(mock_env):
    """Test AgentCard creation"""
    from agents.bob.a2a_card import get_agent_card

    card = get_agent_card()

    assert card is not None
    assert card.name == "bobs-brain-test"
    assert card.version == "0.6.0-test"
    assert card.url == "https://test.example.com"
    assert "Bob's Brain" in card.description


def test_agent_card_spiffe_id(mock_env):
    """Test SPIFFE ID is included in AgentCard description (R7)"""
    from agents.bob.a2a_card import get_agent_card

    card = get_agent_card()

    # R7: SPIFFE ID must be in description
    assert "spiffe://test.intent.solutions/agent/bobs-brain/test/us-central1/0.6.0" in card.description


def test_get_agent_card_dict(mock_env):
    """Test AgentCard dict serialization"""
    from agents.bob.a2a_card import get_agent_card_dict

    card_dict = get_agent_card_dict()

    assert isinstance(card_dict, dict)
    assert "name" in card_dict
    assert "description" in card_dict
    assert "url" in card_dict
    assert "version" in card_dict
    assert "skills" in card_dict
    assert "spiffe_id" in card_dict  # R7: Explicit SPIFFE field


def test_agent_card_dict_spiffe_field(mock_env):
    """Test SPIFFE ID is in dict (R7)"""
    from agents.bob.a2a_card import get_agent_card_dict

    card_dict = get_agent_card_dict()

    assert card_dict["spiffe_id"] == "spiffe://test.intent.solutions/agent/bobs-brain/test/us-central1/0.6.0"


def test_agent_card_skills_array(mock_env):
    """Test AgentCard has skills array"""
    from agents.bob.a2a_card import get_agent_card

    card = get_agent_card()

    assert hasattr(card, "skills")
    assert isinstance(card.skills, list)


def test_agent_card_required_fields():
    """Test AgentCard has all required A2A protocol fields"""
    with patch.dict(os.environ, {
        "PROJECT_ID": "test-project",
        "LOCATION": "us-central1",
        "AGENT_ENGINE_ID": "test-engine-id",
        "AGENT_SPIFFE_ID": "spiffe://test.intent.solutions/agent/bobs-brain/test/us-central1/0.6.0",
        "APP_NAME": "test-agent",
        "APP_VERSION": "1.0.0",
        "PUBLIC_URL": "https://test.com"
    }):
        from agents.bob.a2a_card import get_agent_card

        card = get_agent_card()

        # All required A2A fields must be present
        assert hasattr(card, "name")
        assert hasattr(card, "description")
        assert hasattr(card, "url")
        assert hasattr(card, "version")
        assert hasattr(card, "capabilities")
        assert hasattr(card, "default_input_modes")
        assert hasattr(card, "default_output_modes")
        assert hasattr(card, "skills")

        # Verify types
        assert isinstance(card.default_input_modes, list)
        assert isinstance(card.default_output_modes, list)
        assert "text" in card.default_input_modes
        assert "text" in card.default_output_modes
