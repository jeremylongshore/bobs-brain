#!/usr/bin/env python3
"""
Load sample data into BigQuery for Bob's Brain Circle of Life
"""

import json

from google.cloud import bigquery


def load_sample_data():
    """Load sample knowledge data into BigQuery"""

    client = bigquery.Client(project="bobs-house-ai")

    print("Loading sample data into BigQuery...")

    # Load repair manuals data
    manual_data = [
        {
            "content": "Brake pad replacement: Remove wheel, remove caliper bolts, slide out old pads, install new pads with brake grease. Typical cost $150-300 for front pads.",
            "source": "Haynes Manual - Honda Civic 2015-2020",
            "vehicle_type": "car",
        },
        {
            "content": "Oil change procedure: Drain old oil via drain plug, replace oil filter, add new oil. Use 5W-30 synthetic. Typical cost $40-80.",
            "source": "OEM Service Manual",
            "vehicle_type": "car",
        },
        {
            "content": "Boat engine winterization: Change oil, add fuel stabilizer, fog cylinders, drain water systems. Critical for preventing freeze damage.",
            "source": "Marine Mechanic Handbook",
            "vehicle_type": "boat",
        },
        {
            "content": "Motorcycle chain maintenance: Clean with kerosene, lubricate with chain lube, adjust tension to 1-1.5 inches of play.",
            "source": "Motorcycle Service Guide",
            "vehicle_type": "motorcycle",
        },
        {
            "content": "Bobcat S740 specifications: 3.4L Tier 4 diesel engine, 74.3 HP, 3,000 lbs operating capacity, $73,675 list price",
            "source": "Bobcat Dealer Manual",
            "vehicle_type": "equipment",
        },
    ]

    table_id = "bobs-house-ai.knowledge_base.repair_manuals"
    errors = client.insert_rows_json(table_id, manual_data)
    if errors:
        print(f"Errors inserting manual data: {errors}")
    else:
        print(f"✅ Loaded {len(manual_data)} repair manual entries")

    # Load forum posts data
    forum_data = [
        {
            "question": "Why are my brakes squealing?",
            "answer": "Usually worn brake pads. The wear indicator is metal-on-metal contact. Get them checked ASAP before damage to rotors.",
            "upvotes": 45,
            "source": "r/MechanicAdvice",
            "vehicle_type": "car",
        },
        {
            "question": "How often should I change my boat engine oil?",
            "answer": "Every 100 hours of operation or annually, whichever comes first. Marine engines work harder than car engines.",
            "upvotes": 23,
            "source": "BoatUS Forum",
            "vehicle_type": "boat",
        },
        {
            "question": "Best oil for motorcycle engine?",
            "answer": "Use motorcycle-specific oil. Car oil has friction modifiers that can make your clutch slip. Rotella T6 is popular.",
            "upvotes": 67,
            "source": "r/motorcycles",
            "vehicle_type": "motorcycle",
        },
        {
            "question": "What maintenance does a Bobcat S740 need?",
            "answer": "Regular maintenance includes hydraulic fluid changes every 1000 hours, engine oil every 500 hours, and daily greasing of pivot points.",
            "upvotes": 12,
            "source": "Heavy Equipment Forum",
            "vehicle_type": "equipment",
        },
    ]

    forum_table_id = "bobs-house-ai.knowledge_base.forum_posts"
    errors = client.insert_rows_json(forum_table_id, forum_data)
    if errors:
        print(f"Errors inserting forum data: {errors}")
    else:
        print(f"✅ Loaded {len(forum_data)} forum posts")

    # Load repair quotes data
    quotes_data = [
        {
            "repair_type": "brake_replacement",
            "vehicle_type": "car",
            "quoted_price": 450.0,
            "fair_price": 300.0,
            "shop_name": "Quick Lube Plus",
            "location": "Houston",
        },
        {
            "repair_type": "brake_replacement",
            "vehicle_type": "car",
            "quoted_price": 280.0,
            "fair_price": 300.0,
            "shop_name": "Honest Al's",
            "location": "Houston",
        },
        {
            "repair_type": "oil_change",
            "vehicle_type": "car",
            "quoted_price": 85.0,
            "fair_price": 50.0,
            "shop_name": "Fancy Motors",
            "location": "Dallas",
        },
        {
            "repair_type": "oil_change",
            "vehicle_type": "car",
            "quoted_price": 45.0,
            "fair_price": 50.0,
            "shop_name": "Bob's Garage",
            "location": "Austin",
        },
        {
            "repair_type": "engine_tune",
            "vehicle_type": "boat",
            "quoted_price": 850.0,
            "fair_price": 600.0,
            "shop_name": "Marina Masters",
            "location": "Lake Travis",
        },
        {
            "repair_type": "chain_replacement",
            "vehicle_type": "motorcycle",
            "quoted_price": 120.0,
            "fair_price": 80.0,
            "shop_name": "Biker's Paradise",
            "location": "Austin",
        },
        {
            "repair_type": "hydraulic_service",
            "vehicle_type": "equipment",
            "quoted_price": 1200.0,
            "fair_price": 900.0,
            "shop_name": "Heavy Equipment Services",
            "location": "Houston",
        },
    ]

    quotes_table_id = "bobs-house-ai.scraped_data.repair_quotes"
    errors = client.insert_rows_json(quotes_table_id, quotes_data)
    if errors:
        print(f"Errors inserting quotes data: {errors}")
    else:
        print(f"✅ Loaded {len(quotes_data)} repair quotes")

    print("\n🎯 Sample data loaded successfully!")
    print("BigQuery now contains:")
    print(f"  - {len(manual_data)} repair manual entries")
    print(f"  - {len(forum_data)} forum posts")
    print(f"  - {len(quotes_data)} repair quotes")
    print("\nBob's Brain can now query this knowledge!")


if __name__ == "__main__":
    load_sample_data()
