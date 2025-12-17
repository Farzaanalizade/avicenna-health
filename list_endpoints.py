#!/usr/bin/env python
"""
📋 List all available API endpoints
"""

import requests
import json

BASE_URL = "http://localhost:8000"

# Get OpenAPI schema
response = requests.get(f"{BASE_URL}/openapi.json")
openapi = response.json()

print("\n" + "="*70)
print("📋 Available API Endpoints")
print("="*70 + "\n")

paths = openapi.get("paths", {})
tags = {}

# Organize by tag
for path, methods in paths.items():
    for method, details in methods.items():
        if method.upper() == "PARAMETERS":
            continue
        tag = details.get("tags", ["Uncategorized"])[0]
        if tag not in tags:
            tags[tag] = []
        tags[tag].append(f"{method.upper():6} {path}")

# Print organized
for tag in sorted(tags.keys()):
    print(f"\n🏷️  {tag.upper()}")
    print("-" * 70)
    for endpoint in sorted(tags[tag]):
        print(f"  {endpoint}")

print("\n" + "="*70)
print(f"Total endpoints: {len(paths)}")
print("="*70 + "\n")
