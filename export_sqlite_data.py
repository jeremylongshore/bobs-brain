#!/usr/bin/env python3
"""
Export SQLite database data for migration
"""

import json
import sqlite3
import os
from langchain_community.utilities import SQLDatabase

def export_sqlite_data():
    """Export data from Bob's SQLite databases"""

    print("🗃️  Exporting SQLite database data...")

    # Database paths
    databases = {
        "bob_memory": "/home/jeremylongshore/.bob_brain/bob_memory.db",
        "automation": "/home/jeremylongshore/.bob_brain/automation.db",
        "smart_insights": "/home/jeremylongshore/.bob_brain/smart_insights.db"
    }

    exported_data = {}

    for db_name, db_path in databases.items():
        if not os.path.exists(db_path):
            print(f"⚠️  Database not found: {db_path}")
            continue

        print(f"📂 Exporting {db_name} database...")

        try:
            # Connect directly with sqlite3
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            # Get all tables
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()

            db_data = {
                "database": db_name,
                "path": db_path,
                "tables": {}
            }

            for table in tables:
                table_name = table[0]

                # Get table schema
                cursor.execute(f"PRAGMA table_info({table_name})")
                schema = cursor.fetchall()

                # Get table data
                cursor.execute(f"SELECT * FROM {table_name}")
                rows = cursor.fetchall()

                # Get column names
                column_names = [col[1] for col in schema]

                # Convert rows to dict format
                table_data = []
                for row in rows:
                    row_dict = dict(zip(column_names, row))
                    table_data.append(row_dict)

                db_data["tables"][table_name] = {
                    "schema": schema,
                    "column_names": column_names,
                    "data": table_data,
                    "row_count": len(table_data)
                }

                print(f"   📊 Table '{table_name}': {len(table_data)} rows")

            conn.close()

            # Save to JSON
            export_path = f"/home/jeremylongshore/bob_brain_backup/{db_name}_export.json"
            with open(export_path, "w") as f:
                json.dump(db_data, f, indent=2, default=str)

            print(f"✅ Exported {db_name} to: {export_path}")
            exported_data[db_name] = db_data

        except Exception as e:
            print(f"❌ Error exporting {db_name}: {e}")
            continue

    return exported_data

if __name__ == "__main__":
    export_sqlite_data()
