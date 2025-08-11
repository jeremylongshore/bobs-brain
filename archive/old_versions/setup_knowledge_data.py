#!/usr/bin/env python3
"""
Setup sample knowledge data in BigQuery for testing the Circle of Life
"""

import json

from google.cloud import bigquery


def setup_bigquery_knowledge():
    """Create sample tables with knowledge data"""

    client = bigquery.Client(project="bobs-house-ai")

    # 1. Create repair manuals table with sample data
    print("Setting up repair_manuals table...")

    manuals_schema = [
        bigquery.SchemaField("content", "STRING"),
        bigquery.SchemaField("source", "STRING"),
        bigquery.SchemaField("vehicle_type", "STRING"),
        bigquery.SchemaField("tags", "STRING", mode="REPEATED"),
    ]

    table_id = "bobs-house-ai.knowledge_base.repair_manuals"
    table = bigquery.Table(table_id, schema=manuals_schema)
    table = client.create_table(table, exists_ok=True)

    # Sample repair manual data
    manual_data = [
        {
            "content": "Brake pad replacement: Remove wheel, remove caliper bolts, slide out old pads, install new pads with brake grease. Typical cost $150-300 for front pads.",
            "source": "Haynes Manual - Honda Civic 2015-2020",
            "vehicle_type": "car",
            "tags": ["brake", "pad", "replacement", "civic", "honda"],
        },
        {
            "content": "Oil change procedure: Drain old oil via drain plug, replace oil filter, add new oil. Use 5W-30 synthetic. Typical cost $40-80.",
            "source": "OEM Service Manual",
            "vehicle_type": "car",
            "tags": ["oil", "change", "maintenance", "filter"],
        },
        {
            "content": "Boat engine winterization: Change oil, add fuel stabilizer, fog cylinders, drain water systems. Critical for preventing freeze damage.",
            "source": "Marine Mechanic Handbook",
            "vehicle_type": "boat",
            "tags": ["boat", "winterization", "engine", "maintenance"],
        },
        {
            "content": "Motorcycle chain maintenance: Clean with kerosene, lubricate with chain lube, adjust tension to 1-1.5 inches of play.",
            "source": "Motorcycle Service Guide",
            "vehicle_type": "motorcycle",
            "tags": ["motorcycle", "chain", "maintenance", "lubrication"],
        },
    ]

    errors = client.insert_rows_json(table_id, manual_data)
    if errors:
        print(f"Errors inserting manual data: {errors}")
    else:
        print(f"✅ Inserted {len(manual_data)} repair manual entries")

    # 2. Create forum posts table with sample data
    print("Setting up forum_posts table...")

    forum_schema = [
        bigquery.SchemaField("question", "STRING"),
        bigquery.SchemaField("answer", "STRING"),
        bigquery.SchemaField("upvotes", "INTEGER"),
        bigquery.SchemaField("source", "STRING"),
        bigquery.SchemaField("vehicle_type", "STRING"),
    ]

    forum_table_id = "bobs-house-ai.knowledge_base.forum_posts"
    forum_table = bigquery.Table(forum_table_id, schema=forum_schema)
    forum_table = client.create_table(forum_table, exists_ok=True)

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
            "question": "Can I do brake work myself?",
            "answer": "Basic pad replacement yes, but if you're not confident, don't risk it. Brakes are safety critical. At minimum have your work inspected.",
            "upvotes": 89,
            "source": "DIY Mechanics Forum",
            "vehicle_type": "car",
        },
    ]

    errors = client.insert_rows_json(forum_table_id, forum_data)
    if errors:
        print(f"Errors inserting forum data: {errors}")
    else:
        print(f"✅ Inserted {len(forum_data)} forum posts")

    # 3. Update scraped_data table with better sample data
    print("Setting up repair quotes table...")

    quotes_table_id = "bobs-house-ai.scraped_data.repair_quotes"

    # Check if table exists, create if not
    try:
        table = client.get_table(quotes_table_id)
        print("Repair quotes table exists")
    except:
        quotes_schema = [
            bigquery.SchemaField("repair_type", "STRING"),
            bigquery.SchemaField("vehicle_type", "STRING"),
            bigquery.SchemaField("quoted_price", "FLOAT"),
            bigquery.SchemaField("fair_price", "FLOAT"),
            bigquery.SchemaField("shop_name", "STRING"),
            bigquery.SchemaField("location", "STRING"),
        ]

        table = bigquery.Table(quotes_table_id, schema=quotes_schema)
        table = client.create_table(table, exists_ok=True)
        print("Created repair quotes table")

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
    ]

    errors = client.insert_rows_json(quotes_table_id, quotes_data)
    if errors:
        print(f"Errors inserting quotes data: {errors}")
    else:
        print(f"✅ Inserted {len(quotes_data)} repair quotes")

    print("\n🎯 Knowledge base setup complete!")
    print("Tables created:")
    print("- knowledge_base.repair_manuals")
    print("- knowledge_base.forum_posts")
    print("- scraped_data.repair_quotes")


if __name__ == "__main__":
    setup_bigquery_knowledge()
