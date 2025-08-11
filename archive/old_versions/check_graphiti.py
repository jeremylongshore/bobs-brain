#!/usr/bin/env python3
"""
Check the OFFICIAL Graphiti framework parameters
This verifies we're using the real framework, not an invention
"""

from graphiti_core import Graphiti
import inspect

print("=" * 60)
print("OFFICIAL GRAPHITI FRAMEWORK VERIFICATION")
print("=" * 60)
print()

# Get the actual constructor signature
sig = inspect.signature(Graphiti.__init__)

print("Package: graphiti-core")
print("Class: Graphiti")
print("GitHub: https://github.com/getzep/graphiti")
print()

print("CONSTRUCTOR PARAMETERS:")
print("-" * 40)

for name, param in sig.parameters.items():
    if name == 'self':
        continue
    
    # Get parameter info
    param_type = param.annotation if param.annotation != inspect.Parameter.empty else "Any"
    default = param.default
    
    if default == inspect.Parameter.empty:
        default_str = "REQUIRED"
    elif default is None:
        default_str = "None (optional)"
    else:
        default_str = f"{default}"
    
    print(f"  {name}:")
    print(f"    Default: {default_str}")
    print()

print("-" * 40)
print()

# Show correct usage
print("CORRECT INITIALIZATION:")
print("-" * 40)
print("""
from graphiti_core import Graphiti

# Basic usage (what we should use):
graphiti = Graphiti(
    uri="bolt://localhost:7687",  # Neo4j connection string
    user="neo4j",                 # Neo4j username
    password="your_password"       # Neo4j password
)

# The error we had:
# WRONG: Graphiti(neo4j_uri=..., neo4j_user=..., neo4j_password=...)
# RIGHT: Graphiti(uri=..., user=..., password=...)
""")

print("=" * 60)
print("This is the OFFICIAL framework from Zep (getzep/graphiti)")
print("NOT a Claude invention!")
print("=" * 60)