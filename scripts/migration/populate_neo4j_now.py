#!/usr/bin/env python3
"""
Populate Neo4j with real equipment and diesel truck data
So you can see it in the Neo4j console!
"""

from neo4j import GraphDatabase
import os
from datetime import datetime
import json

# Neo4j connection
NEO4J_URI = os.getenv("NEO4J_URI", "neo4j+s://d3653283.databases.neo4j.io")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "q9eazAmPqXsv0KSnnjiX6Q-UvXXPKIUCZbkC7P5VOAE")

class Neo4jPopulator:
    def __init__(self):
        self.driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
        print(f"🔗 Connected to Neo4j at: {NEO4J_URI}")
        
    def close(self):
        self.driver.close()
    
    def clear_database(self):
        """Clear existing data (optional)"""
        with self.driver.session() as session:
            session.run("MATCH (n) DETACH DELETE n")
            print("🧹 Cleared existing data")
    
    def populate_equipment(self):
        """Add equipment nodes"""
        print("\n🚜 Adding Equipment Nodes...")
        
        equipment = [
            # Bobcat
            {"brand": "Bobcat", "model": "S740", "type": "Skid Steer", "year": 2020, "engine": "Kubota V3800"},
            {"brand": "Bobcat", "model": "T770", "type": "Track Loader", "year": 2021, "engine": "Kubota V3800"},
            {"brand": "Bobcat", "model": "MT85", "type": "Mini Track Loader", "year": 2019, "engine": "Kubota D1803"},
            
            # Ford Trucks
            {"brand": "Ford", "model": "F-250", "type": "Diesel Truck", "year": 2015, "engine": "6.7L Powerstroke"},
            {"brand": "Ford", "model": "F-350", "type": "Diesel Truck", "year": 2005, "engine": "6.0L Powerstroke"},
            {"brand": "Ford", "model": "F-450", "type": "Diesel Truck", "year": 2003, "engine": "7.3L Powerstroke"},
            
            # Ram Trucks
            {"brand": "Ram", "model": "2500", "type": "Diesel Truck", "year": 2018, "engine": "6.7L Cummins"},
            {"brand": "Ram", "model": "3500", "type": "Diesel Truck", "year": 2001, "engine": "5.9L Cummins"},
            
            # Chevy/GMC
            {"brand": "GMC", "model": "Sierra 2500HD", "type": "Diesel Truck", "year": 2003, "engine": "LB7 Duramax"},
            {"brand": "Chevy", "model": "Silverado 3500", "type": "Diesel Truck", "year": 2011, "engine": "LML Duramax"},
        ]
        
        with self.driver.session() as session:
            for eq in equipment:
                result = session.run("""
                    CREATE (e:Equipment {
                        brand: $brand,
                        model: $model,
                        type: $type,
                        year: $year,
                        engine: $engine,
                        full_name: $brand + ' ' + $model
                    })
                    RETURN e.full_name as name
                """, **eq)
                print(f"  ✅ Added: {result.single()['name']}")
    
    def populate_error_codes(self):
        """Add error code nodes with descriptions"""
        print("\n⚠️  Adding Error Codes...")
        
        error_codes = [
            # Common Powerstroke codes
            {"code": "P0087", "description": "Fuel rail pressure too low", "severity": "Critical"},
            {"code": "P0088", "description": "Fuel rail pressure too high", "severity": "Critical"},
            {"code": "P0299", "description": "Turbo underboost", "severity": "High"},
            {"code": "P0401", "description": "EGR flow insufficient", "severity": "Medium"},
            
            # Cummins codes
            {"code": "P0191", "description": "Fuel rail pressure sensor range", "severity": "High"},
            {"code": "P0216", "description": "Injection timing control", "severity": "Critical"},
            {"code": "P2262", "description": "Turbo boost pressure not detected", "severity": "High"},
            
            # Duramax codes
            {"code": "P0093", "description": "Large fuel leak detected", "severity": "Critical"},
            {"code": "P0201", "description": "Injector 1 circuit malfunction", "severity": "High"},
            {"code": "P1093", "description": "Fuel rail pressure low during acceleration", "severity": "High"},
            {"code": "P21DD", "description": "DEF tank heater control", "severity": "Medium"},
            
            # Bobcat specific
            {"code": "9809-31", "description": "Hydraulic pressure sensor fault", "severity": "High"},
            {"code": "523615-31", "description": "High pressure fuel pump", "severity": "Critical"},
        ]
        
        with self.driver.session() as session:
            for code in error_codes:
                result = session.run("""
                    CREATE (c:ErrorCode {
                        code: $code,
                        description: $description,
                        severity: $severity
                    })
                    RETURN c.code as code
                """, **code)
                print(f"  ✅ Added: {result.single()['code']} - {code['description']}")
    
    def populate_parts(self):
        """Add part nodes with prices"""
        print("\n🔧 Adding Parts...")
        
        parts = [
            # Powerstroke parts
            {"number": "BC3Z-9A543-B", "name": "CP4.2 Fuel Pump", "brand": "Ford", "price": 3800},
            {"number": "BC3Z-9H529-B", "name": "Fuel Injector Set", "brand": "Ford", "price": 3200},
            {"number": "3C3Z-6A642-CA", "name": "Oil Cooler", "brand": "Ford", "price": 245},
            
            # Cummins parts
            {"number": "0-470-506-040", "name": "VP44 Injection Pump", "brand": "Bosch", "price": 1400},
            {"number": "5297640", "name": "Fuel Rail Pressure Sensor", "brand": "Cummins", "price": 165},
            
            # Duramax parts
            {"number": "97188463", "name": "LB7 Injector", "brand": "AC Delco", "price": 280},
            {"number": "23379348", "name": "DEF Tank Assembly", "brand": "GM", "price": 950},
            
            # Bobcat parts
            {"number": "7023037", "name": "Hydraulic Filter", "brand": "Bobcat", "price": 85},
            {"number": "6661248", "name": "Hydraulic Filter Premium", "brand": "Bobcat", "price": 125},
            {"number": "7256775", "name": "High Pressure Fuel Pump", "brand": "Bobcat", "price": 2800},
        ]
        
        with self.driver.session() as session:
            for part in parts:
                result = session.run("""
                    CREATE (p:Part {
                        number: $number,
                        name: $name,
                        brand: $brand,
                        price: $price
                    })
                    RETURN p.number as number
                """, **part)
                print(f"  ✅ Added: {result.single()['number']} - {part['name']} (${part['price']})")
    
    def populate_problems(self):
        """Add common problem nodes"""
        print("\n❌ Adding Common Problems...")
        
        problems = [
            {"name": "Won't Start", "category": "Engine"},
            {"name": "CP4 Pump Failure", "category": "Fuel System"},
            {"name": "Turbo Underboost", "category": "Turbo"},
            {"name": "DEF System Fault", "category": "Emissions"},
            {"name": "Injector Failure", "category": "Fuel System"},
            {"name": "Head Gasket Blown", "category": "Engine"},
            {"name": "Hydraulic Leak", "category": "Hydraulics"},
            {"name": "No Hydraulic Pressure", "category": "Hydraulics"},
            {"name": "EGR Cooler Failure", "category": "Emissions"},
            {"name": "DPF Clogged", "category": "Emissions"},
        ]
        
        with self.driver.session() as session:
            for problem in problems:
                result = session.run("""
                    CREATE (p:Problem {
                        name: $name,
                        category: $category
                    })
                    RETURN p.name as name
                """, **problem)
                print(f"  ✅ Added: {result.single()['name']}")
    
    def create_relationships(self):
        """Create relationships between nodes"""
        print("\n🔗 Creating Relationships...")
        
        with self.driver.session() as session:
            # Link error codes to equipment
            relationships = [
                # Powerstroke codes
                ("6.7L Powerstroke", "P0087", "THROWS_CODE"),
                ("6.7L Powerstroke", "P0088", "THROWS_CODE"),
                ("6.0L Powerstroke", "P0299", "THROWS_CODE"),
                
                # Cummins codes
                ("6.7L Cummins", "P0191", "THROWS_CODE"),
                ("5.9L Cummins", "P0216", "THROWS_CODE"),
                
                # Duramax codes
                ("LB7 Duramax", "P0093", "THROWS_CODE"),
                ("LB7 Duramax", "P0201", "THROWS_CODE"),
                ("LML Duramax", "P21DD", "THROWS_CODE"),
                
                # Bobcat codes
                ("Kubota V3800", "9809-31", "THROWS_CODE"),
            ]
            
            for engine, code, rel_type in relationships:
                session.run(f"""
                    MATCH (e:Equipment) WHERE e.engine CONTAINS $engine
                    MATCH (c:ErrorCode {{code: $code}})
                    CREATE (e)-[:{rel_type}]->(c)
                """, engine=engine, code=code)
            print("  ✅ Linked error codes to equipment")
            
            # Link parts to problems
            part_fixes = [
                ("BC3Z-9A543-B", "CP4 Pump Failure", "FIXES"),
                ("BC3Z-9H529-B", "Injector Failure", "FIXES"),
                ("0-470-506-040", "Won't Start", "FIXES"),
                ("7023037", "Hydraulic Leak", "FIXES"),
            ]
            
            for part_num, problem_name, rel_type in part_fixes:
                session.run(f"""
                    MATCH (part:Part {{number: $part_num}})
                    MATCH (prob:Problem {{name: $problem_name}})
                    CREATE (part)-[:{rel_type}]->(prob)
                """, part_num=part_num, problem_name=problem_name)
            print("  ✅ Linked parts to problems they fix")
            
            # Link problems to error codes
            problem_codes = [
                ("CP4 Pump Failure", "P0087", "CAUSES"),
                ("Turbo Underboost", "P0299", "CAUSES"),
                ("DEF System Fault", "P21DD", "CAUSES"),
                ("Injector Failure", "P0201", "CAUSES"),
            ]
            
            for problem, code, rel_type in problem_codes:
                session.run(f"""
                    MATCH (p:Problem {{name: $problem}})
                    MATCH (c:ErrorCode {{code: $code}})
                    CREATE (p)-[:{rel_type}]->(c)
                """, problem=problem, code=code)
            print("  ✅ Linked problems to error codes")
    
    def add_repair_cases(self):
        """Add some real repair cases"""
        print("\n🔧 Adding Repair Cases...")
        
        cases = [
            {
                "id": "CASE001",
                "equipment": "Ford F-250",
                "problem": "CP4 Pump Failure",
                "cost": 8500,
                "duration_hours": 12,
                "outcome": "Replaced with CP3 conversion"
            },
            {
                "id": "CASE002",
                "equipment": "GMC Sierra 2500HD",
                "problem": "Injector Failure",
                "cost": 2600,
                "duration_hours": 10,
                "outcome": "Replaced all 8 injectors"
            },
            {
                "id": "CASE003",
                "equipment": "Bobcat S740",
                "problem": "No Hydraulic Pressure",
                "cost": 650,
                "duration_hours": 3,
                "outcome": "Replaced hydraulic filter and fluid"
            }
        ]
        
        with self.driver.session() as session:
            for case in cases:
                session.run("""
                    CREATE (r:RepairCase {
                        id: $id,
                        equipment: $equipment,
                        problem: $problem,
                        cost: $cost,
                        duration_hours: $duration_hours,
                        outcome: $outcome,
                        date: datetime()
                    })
                """, **case)
                print(f"  ✅ Added case: {case['id']} - {case['equipment']} - ${case['cost']}")
    
    def show_statistics(self):
        """Show what's in the database"""
        print("\n📊 DATABASE STATISTICS:")
        
        with self.driver.session() as session:
            # Count nodes
            result = session.run("""
                MATCH (n)
                RETURN labels(n)[0] as label, count(n) as count
                ORDER BY count DESC
            """)
            
            print("\nNode counts:")
            for record in result:
                print(f"  • {record['label']}: {record['count']}")
            
            # Count relationships
            result = session.run("""
                MATCH ()-[r]->()
                RETURN type(r) as type, count(r) as count
            """)
            
            print("\nRelationship counts:")
            for record in result:
                print(f"  • {record['type']}: {record['count']}")
            
            # Sample query
            print("\n🔍 Sample Query - Equipment with P0087 error:")
            result = session.run("""
                MATCH (e:Equipment)-[:THROWS_CODE]->(c:ErrorCode {code: 'P0087'})
                RETURN e.full_name as equipment, e.engine as engine
            """)
            for record in result:
                print(f"  • {record['equipment']} ({record['engine']})")

def main():
    print("🚀 POPULATING NEO4J WITH EQUIPMENT DATA")
    print("=" * 60)
    
    populator = Neo4jPopulator()
    
    try:
        # Clear and repopulate (comment out if you want to keep existing data)
        # populator.clear_database()
        
        # Add all data
        populator.populate_equipment()
        populator.populate_error_codes()
        populator.populate_parts()
        populator.populate_problems()
        populator.create_relationships()
        populator.add_repair_cases()
        
        # Show what we added
        populator.show_statistics()
        
        print("\n" + "=" * 60)
        print("✅ NEO4J POPULATED SUCCESSFULLY!")
        print("\n🎯 TO VIEW IN NEO4J:")
        print("1. Go to: https://console.neo4j.io")
        print("2. Open your database")
        print("3. Run this query to see everything:")
        print("   MATCH (n) RETURN n LIMIT 100")
        print("\n📊 Or try these specific queries:")
        print("   MATCH (e:Equipment) RETURN e")
        print("   MATCH (c:ErrorCode) RETURN c")
        print("   MATCH (p:Part) WHERE p.price > 1000 RETURN p")
        print("   MATCH path = (e:Equipment)-[:THROWS_CODE]->(c:ErrorCode) RETURN path")
        
    finally:
        populator.close()

if __name__ == "__main__":
    main()