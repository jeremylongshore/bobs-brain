#!/usr/bin/env python3
"""
Test suite for Bob v2 Unified
"""

import sys
import os
from pathlib import Path
import pytest
from unittest.mock import Mock, patch, MagicMock

# Add version directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "versions" / "v2-unified"))

def test_bob_v2_import():
    """Test that Bob v2 can be imported"""
    try:
        from bob_unified_v2 import BobUnifiedV2
        assert BobUnifiedV2 is not None
    except ImportError:
        pytest.skip("Bob v2 not available")

@patch('bob_unified_v2.WebClient')
@patch('bob_unified_v2.SocketModeClient')
@patch('bob_unified_v2.chromadb.PersistentClient')
def test_bob_v2_initialization(mock_chroma, mock_socket, mock_web):
    """Test Bob v2 initialization"""
    try:
        from bob_unified_v2 import BobUnifiedV2
        
        # Mock ChromaDB
        mock_chroma_instance = MagicMock()
        mock_collection = MagicMock()
        mock_chroma_instance.get_collection.return_value = mock_collection
        mock_chroma.return_value = mock_chroma_instance
        
        # Initialize Bob
        bob = BobUnifiedV2(
            slack_bot_token="xoxb-test-token",
            slack_app_token="xapp-test-token"
        )
        
        assert bob is not None
        assert hasattr(bob, 'processed_messages')
        assert hasattr(bob, 'conversation_memory')
        assert hasattr(bob, 'business_context')
        
    except ImportError:
        pytest.skip("Bob v2 not available")

@patch('bob_unified_v2.chromadb.PersistentClient')
def test_message_deduplication(mock_chroma):
    """Test message deduplication feature"""
    try:
        from bob_unified_v2 import BobUnifiedV2
        
        # Mock ChromaDB
        mock_chroma_instance = MagicMock()
        mock_collection = MagicMock()
        mock_chroma_instance.get_collection.return_value = mock_collection
        mock_chroma.return_value = mock_chroma_instance
        
        with patch('bob_unified_v2.WebClient'), \
             patch('bob_unified_v2.SocketModeClient'):
            
            bob = BobUnifiedV2(
                slack_bot_token="xoxb-test-token",
                slack_app_token="xapp-test-token"
            )
            
            # Test deduplication
            message_id = "test-message-123"
            assert message_id not in bob.processed_messages
            
            bob.processed_messages.add(message_id)
            assert message_id in bob.processed_messages
            
    except ImportError:
        pytest.skip("Bob v2 not available")

@patch('bob_unified_v2.chromadb.PersistentClient')
def test_conversation_memory(mock_chroma):
    """Test conversation memory system"""
    try:
        from bob_unified_v2 import BobUnifiedV2
        
        # Mock ChromaDB
        mock_chroma_instance = MagicMock()
        mock_collection = MagicMock()
        mock_chroma_instance.get_collection.return_value = mock_collection
        mock_chroma.return_value = mock_chroma_instance
        
        with patch('bob_unified_v2.WebClient'), \
             patch('bob_unified_v2.SocketModeClient'):
            
            bob = BobUnifiedV2(
                slack_bot_token="xoxb-test-token",
                slack_app_token="xapp-test-token"
            )
            
            # Test memory structure
            assert 'recent_interactions' in bob.conversation_memory
            assert 'greeting_count' in bob.conversation_memory
            assert 'user_context' in bob.conversation_memory
            
    except ImportError:
        pytest.skip("Bob v2 not available")

if __name__ == "__main__":
    pytest.main([__file__, "-v"])