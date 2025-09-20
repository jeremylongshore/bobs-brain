"""Test the Circle of Life learning system"""

import time

from src.circle_of_life import CircleOfLife, content_hash


def test_content_hash_deterministic():
    """Test that content hash is deterministic"""
    data = {"test": "data", "number": 42}
    hash1 = content_hash(data)
    hash2 = content_hash(data)
    assert hash1 == hash2
    assert len(hash1) == 64  # SHA-256 hex string


def test_content_hash_different():
    """Test that different content produces different hashes"""
    data1 = {"test": "data1"}
    data2 = {"test": "data2"}
    assert content_hash(data1) != content_hash(data2)


def test_dedupe_and_batch():
    """Test deduplication and batching"""
    col = CircleOfLife(neo4j_driver=None, bq_client=None, llm_call=lambda x: [])

    # Duplicate events should be deduped
    events = [{"a": 1}, {"a": 1}, {"b": 2}]
    batch = col.ingest(events)
    assert len(batch) == 2  # Duplicates removed


def test_batch_size_limit():
    """Test that batch size is limited by environment variable"""
    col = CircleOfLife(neo4j_driver=None, bq_client=None, llm_call=lambda x: [])

    # Create more events than batch size
    events = [{"id": i} for i in range(100)]
    batch = col.ingest(events)

    # Should be limited by BATCH_SIZE (default 50)
    assert len(batch) <= 50


def test_run_once_cooldown():
    """Test cooldown mechanism"""
    col = CircleOfLife(neo4j_driver=None, bq_client=None, llm_call=lambda x: [{"pattern": "test", "confidence": 0.9}])

    # First run should work
    result1 = col.run_once([{"test": 1}])
    assert result1["ran"] is True

    # Second run immediately should be blocked by cooldown
    result2 = col.run_once([{"test": 2}])
    assert result2["ran"] is False
    assert result2["reason"] == "cooldown"


def test_confidence_filtering():
    """Test that low confidence insights are filtered"""
    high_conf_insight = {"pattern": "high", "confidence": 0.9}
    low_conf_insight = {"pattern": "low", "confidence": 0.3}

    def mock_llm(payload):
        return [high_conf_insight, low_conf_insight]

    col = CircleOfLife(neo4j_driver=None, bq_client=None, llm_call=mock_llm)

    # Run with cooldown override
    col._last_run = 0  # Reset cooldown
    result = col.run_once([{"test": 1}])

    assert result["ran"] is True
    assert result["insights_generated"] == 2
    assert result["high_confidence_insights"] == 1  # Only high confidence counted


def test_analysis_grouping():
    """Test event analysis and grouping"""
    col = CircleOfLife(neo4j_driver=None, bq_client=None, llm_call=lambda x: [])

    events = [
        {"type": "message", "user_id": "user1"},
        {"type": "message", "user_id": "user2"},
        {"type": "correction", "user_id": "user1"},
    ]

    analysis = col.analyze(events)

    assert analysis["total_events"] == 3
    assert analysis["event_types"]["message"] == 2
    assert analysis["event_types"]["correction"] == 1
    assert analysis["users"]["user1"] == 2
    assert analysis["users"]["user2"] == 1


def test_mock_llm_fallback():
    """Test mock LLM when no real LLM configured"""
    col = CircleOfLife(neo4j_driver=None, bq_client=None, llm_call=None)

    analysis = {"test": "data"}
    insights = col.generate_insights(analysis)

    assert len(insights) == 1
    assert insights[0]["pattern"] == "mock_pattern"
    assert insights[0]["confidence"] == 0.9


def test_empty_events_handling():
    """Test handling of empty events list"""
    col = CircleOfLife(neo4j_driver=None, bq_client=None, llm_call=lambda x: [])

    col._last_run = 0  # Reset cooldown
    result = col.run_once([])

    assert result["ran"] is False
    assert result["reason"] == "no_new_events"


def test_hash_cleanup():
    """Test that processed hashes are cleaned up to prevent memory growth"""
    col = CircleOfLife(neo4j_driver=None, bq_client=None, llm_call=lambda x: [])

    # Fill up processed hashes beyond cleanup threshold
    for i in range(600):  # More than BATCH_SIZE * 10
        col.ingest([{"id": i}])

    # Should trigger cleanup
    assert len(col._processed_hashes) < 600
