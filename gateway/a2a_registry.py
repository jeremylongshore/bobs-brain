"""
A2A Peer Registry

Manages a registry of known Agent-to-Agent (A2A) peers that can be discovered
and communicated with. Currently file-backed, designed to migrate to Firestore.
"""
import os
import json
from typing import List, Dict, Any

REG_PATH = os.getenv("A2A_REGISTRY_PATH", "a2a/peers.json")


def load_peers() -> List[Dict[str, Any]]:
    """
    Load peer agents from registry file.

    Returns:
        List of AgentCard dictionaries representing known peers.
        Returns empty list if registry file doesn't exist.

    Example peer format:
        {
            "name": "Engineering Agent",
            "version": "1.0.0",
            "description": "Handles engineering tasks",
            "skills": ["code_review", "testing"],
            "endpoint": "https://eng-agent.example.com",
            "card_url": "https://eng-agent.example.com/card"
        }
    """
    if not os.path.exists(REG_PATH):
        return []

    try:
        with open(REG_PATH, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        # Log error but return empty list to avoid breaking service
        print(f"Warning: Failed to load A2A registry from {REG_PATH}: {e}")
        return []


def add_peer(peer: Dict[str, Any]) -> bool:
    """
    Add a new peer to the registry (future: validation + Firestore).

    Args:
        peer: AgentCard dictionary

    Returns:
        True if peer was added successfully
    """
    peers = load_peers()

    # Check if peer already exists (by endpoint)
    endpoint = peer.get("endpoint")
    if endpoint and any(p.get("endpoint") == endpoint for p in peers):
        return False

    peers.append(peer)

    try:
        os.makedirs(os.path.dirname(REG_PATH), exist_ok=True)
        with open(REG_PATH, "w") as f:
            json.dump(peers, f, indent=2)
        return True
    except IOError as e:
        print(f"Error: Failed to write A2A registry to {REG_PATH}: {e}")
        return False


def remove_peer(endpoint: str) -> bool:
    """
    Remove a peer from the registry by endpoint.

    Args:
        endpoint: Peer endpoint URL

    Returns:
        True if peer was found and removed
    """
    peers = load_peers()
    original_count = len(peers)

    peers = [p for p in peers if p.get("endpoint") != endpoint]

    if len(peers) == original_count:
        return False

    try:
        with open(REG_PATH, "w") as f:
            json.dump(peers, f, indent=2)
        return True
    except IOError as e:
        print(f"Error: Failed to write A2A registry to {REG_PATH}: {e}")
        return False


def get_peer_by_name(name: str) -> Dict[str, Any] | None:
    """
    Find a peer by name.

    Args:
        name: Peer agent name

    Returns:
        AgentCard dictionary or None if not found
    """
    peers = load_peers()
    for peer in peers:
        if peer.get("name") == name:
            return peer
    return None
