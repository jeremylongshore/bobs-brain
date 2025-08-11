#!/usr/bin/env python3
"""
Add Bobcat S740 knowledge to Bob's memory system
"""

import asyncio
import os
import sys

sys.path.append("src")

from bob_brain_v5 import BobBrainV5


async def add_bobcat_knowledge():
    """Add comprehensive Bobcat S740 knowledge"""

    print("🚜 Adding Bobcat S740 knowledge to Bob's Brain...")

    # Initialize Bob
    bob = BobBrainV5()

    # Knowledge entries about Bobcat S740
    knowledge_entries = [
        {
            "topic": "Bobcat S740 specifications",
            "content": "The Bobcat S740 skid-steer loader has a 3.4L Tier 4 diesel engine producing 74.3 horsepower, rated operating capacity of 3,000 lbs, tipping load capacity of 8,794 lbs, and operating weight of 8,794 lbs. Standard hydraulic flow is 23 GPM (30 GPM high flow) at 3,500 PSI pressure.",
        },
        {
            "topic": "Bobcat S740 dimensions",
            "content": "Bobcat S740 dimensions: Width 72.1 inches, Length 141.6 inches with standard bucket, Height 81.3 inches with operator cab. Lift capacity at 35% tipping load is 2,170 lbs, at 50% is 3,100 lbs.",
        },
        {
            "topic": "Bobcat S740 features",
            "content": "The Bobcat S740 features SJC joystick controls, heated air-ride seats, optional automatic climate control, reversible cooling fan, cast-steel lift arms for strength, and one-sided serviceability with belt-drive system for reduced maintenance.",
        },
        {
            "topic": "Bobcat S740 maintenance",
            "content": "Bobcat S740 maintenance includes estimated monthly costs of $200, large swing-open tailgate for service access, no chain adjustments needed (welded axle tubes), self-priming fuel system, and Tier 4 compliance without DPF regeneration reducing downtime.",
        },
        {
            "topic": "Bobcat S740 pricing",
            "content": "The Bobcat S740 Skid Steer Loader has a list price of approximately $73,675. Monthly fuel costs are estimated at $1,000. It's designed for heavy-duty applications with industry-leading breakout forces.",
        },
        {
            "topic": "Bobcat S740 hydraulics",
            "content": "Bobcat S740 hydraulic system: Standard flow 23 GPM (47 HP), High flow 30 GPM (62.3 HP), 3,500 PSI pressure. Features vertical lift path ideal for loading trucks and working at height. Belt-drive system allows engine to run slower for reduced noise.",
        },
    ]

    # Add each knowledge entry as a conversation
    for i, entry in enumerate(knowledge_entries):
        user_message = f"Tell me about {entry['topic']}"
        bot_response = entry["content"]

        print(f"Adding knowledge {i+1}/{len(knowledge_entries)}: {entry['topic']}")

        # Store in memory system
        await bob.remember_conversation(user_message, bot_response, user="system_knowledge")

        print(f"✅ Added: {entry['topic']}")

    print(f"\n🎯 Successfully added {len(knowledge_entries)} Bobcat S740 knowledge entries to Bob's Brain!")
    print("Bob can now answer questions about Bobcat S740 specifications, features, and maintenance.")

    return True


if __name__ == "__main__":
    asyncio.run(add_bobcat_knowledge())
