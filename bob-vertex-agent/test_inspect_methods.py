#!/usr/bin/env python3
"""
Inspect ReasoningEngine object to find available methods.
"""
import os

os.environ["GOOGLE_CLOUD_PROJECT"] = "bobs-brain"
os.environ["GOOGLE_CLOUD_LOCATION"] = "us-central1"

import vertexai
from vertexai.preview import reasoning_engines

vertexai.init(
    project=os.environ["GOOGLE_CLOUD_PROJECT"],
    location=os.environ["GOOGLE_CLOUD_LOCATION"]
)

AGENT_ENGINE_ID = "5828234061910376448"
remote_agent = reasoning_engines.ReasoningEngine(AGENT_ENGINE_ID)

print("=" * 80)
print("ReasoningEngine Object Methods")
print("=" * 80)

# Get all attributes
all_attrs = dir(remote_agent)

# Filter to public methods
public_methods = [attr for attr in all_attrs if not attr.startswith('_') and callable(getattr(remote_agent, attr))]

print("\nPublic Methods:")
for method in sorted(public_methods):
    print(f"  - {method}")

# Check for query-related methods
print("\n" + "=" * 80)
print("Query-Related Methods:")
print("=" * 80)
query_methods = [m for m in public_methods if 'query' in m.lower()]
for method in query_methods:
    print(f"  - {method}")

# Check the _gca_resource attribute (internal API)
print("\n" + "=" * 80)
print("Internal API Methods (_gca_resource):")
print("=" * 80)
if hasattr(remote_agent, '_gca_resource'):
    gca_methods = [attr for attr in dir(remote_agent._gca_resource) if not attr.startswith('_')]
    for method in sorted(gca_methods):
        print(f"  - {method}")

# Try to inspect the API operations
print("\n" + "=" * 80)
print("Available Operations:")
print("=" * 80)
if hasattr(remote_agent, '_gca_resource') and hasattr(remote_agent._gca_resource, 'resource_name'):
    print(f"Resource name: {remote_agent._gca_resource.resource_name}")
if hasattr(remote_agent, 'operation_schemas'):
    print(f"Operation schemas: {remote_agent.operation_schemas()}")
