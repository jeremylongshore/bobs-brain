#!/usr/bin/env python3
"""
Populate Neo4j Aura with comprehensive repair data
"""

import hashlib
import random
from datetime import datetime

from neo4j import GraphDatabase

# Neo4j Aura credentials
uri = "neo4j+s://d3653283.databases.neo4j.io"
user = "neo4j"
password = "q9eazAmPqXsv0KSnnjiX6Q-UvXXPKIUCZbkC7P5VOAE"

print("Connecting to Neo4j Aura...")
driver = GraphDatabase.driver(uri, auth=(user, password))

# Comprehensive repair data
equipment_data = {
    "Bobcat S740": {
        "type": "Skid Steer",
        "hp": 74,
        "common_problems": [
            (
                "Hydraulic System",
                "Low pressure, fluid leaks, cylinder failure",
                "Check hydraulic fluid levels, inspect hoses for leaks, test pressure relief valve",
            ),
            (
                "Engine",
                "Won't start, overheating, low power",
                "Check fuel system, clean air filter, inspect cooling system",
            ),
            (
                "Electrical",
                "Dead battery, display malfunction",
                "Test battery voltage, check alternator, inspect wiring harness",
            ),
            (
                "DEF/DPF System",
                "Clogging, sensor issues, regen cycles",
                "Clean DPF filter, check DEF quality, run forced regeneration",
            ),
            (
                "Drive System",
                "Track tension, drive motor issues",
                "Adjust track tension, check drive chains, inspect sprockets",
            ),
        ],
        "error_codes": ["E-1001", "E-2345", "H-3456", "T-4567", "S-1234"],
    },
    "Bobcat T770": {
        "type": "Compact Track Loader",
        "hp": 92,
        "common_problems": [
            (
                "Track System",
                "Track coming off, uneven wear",
                "Check track tension, inspect idlers and rollers, align tracks",
            ),
            (
                "Hydraulic Controls",
                "Jerky operation, slow response",
                "Check hydraulic fluid temperature, clean filters, calibrate controls",
            ),
            ("Engine", "Excessive smoke, rough idle", "Check injectors, clean EGR valve, replace fuel filters"),
            ("Cooling System", "Overheating under load", "Clean radiator, check coolant levels, test thermostat"),
            ("Electrical", "Error codes, sensor failures", "Scan for codes, check sensor connections, update software"),
        ],
        "error_codes": ["T-2001", "H-5678", "E-3456", "C-1234", "S-5678"],
    },
    "Caterpillar 320": {
        "type": "Excavator",
        "hp": 165,
        "common_problems": [
            (
                "Hydraulic System",
                "Boom drift, slow operation",
                "Check main relief valve, inspect boom cylinder seals, test pilot pressure",
            ),
            (
                "Undercarriage",
                "Track tension, sprocket wear",
                "Adjust track tension, inspect track chains, check sprocket teeth",
            ),
            (
                "Engine",
                "High fuel consumption, black smoke",
                "Clean fuel injectors, check turbocharger, replace air filter",
            ),
            (
                "Swing System",
                "Swing brake issues, jerky swing",
                "Adjust swing brake, check swing motor, inspect swing bearing",
            ),
            ("Electrical", "ECM errors, display issues", "Update ECM software, check ground connections, test sensors"),
        ],
        "error_codes": ["C-3001", "H-7890", "E-4567", "S-2345", "U-1234"],
    },
    "John Deere 310": {
        "type": "Backhoe Loader",
        "hp": 100,
        "common_problems": [
            (
                "Transmission",
                "Gear slipping, hard shifting",
                "Check transmission fluid, adjust clutch, inspect synchros",
            ),
            ("Loader Arms", "Slow lift, bucket drift", "Check loader valve, inspect cylinder seals, test relief valve"),
            (
                "Backhoe",
                "Boom drift, weak digging force",
                "Inspect boom cylinder, check pump pressure, test main relief",
            ),
            ("Brakes", "Spongy pedal, uneven braking", "Bleed brake system, check brake pads, inspect master cylinder"),
            (
                "Steering",
                "Hard steering, wandering",
                "Check power steering pump, inspect steering cylinder, align front end",
            ),
        ],
        "error_codes": ["J-4001", "T-8901", "H-2345", "B-3456", "S-6789"],
    },
    "Kubota KX040": {
        "type": "Mini Excavator",
        "hp": 40,
        "common_problems": [
            (
                "Hydraulic System",
                "Slow operation, overheating",
                "Check hydraulic oil level, clean oil cooler, replace filters",
            ),
            ("Tracks", "Rubber track damage, detracking", "Inspect track tension, check for debris, examine sprockets"),
            ("Engine", "Hard starting, white smoke", "Check glow plugs, test compression, inspect fuel system"),
            ("Boom/Arm", "Jerky movement, drift", "Check control valve, inspect cylinder seals, adjust cushion valves"),
            ("Cooling", "Overheating, coolant loss", "Clean radiator fins, check water pump, pressure test system"),
        ],
        "error_codes": ["K-5001", "H-1234", "E-5678", "T-3456", "C-7890"],
    },
}

repair_procedures = [
    "Drain and replace hydraulic fluid",
    "Replace hydraulic filter",
    "Check and adjust track tension",
    "Clean or replace air filter",
    "Test battery and charging system",
    "Inspect and replace worn hoses",
    "Calibrate hydraulic controls",
    "Clean radiator and cooling fins",
    "Check and replace fuel filters",
    "Perform diagnostic scan",
    "Inspect drive chains and sprockets",
    "Test hydraulic pump pressure",
    "Replace worn seals and O-rings",
    "Clean DPF filter",
    "Check DEF system operation",
]

parts_catalog = [
    ("Hydraulic Filter", "HF-12345", 45.99),
    ("Air Filter", "AF-67890", 32.50),
    ("Fuel Filter", "FF-11111", 28.75),
    ("Hydraulic Hose", "HH-22222", 89.99),
    ("Track Pad", "TP-33333", 125.00),
    ("Seal Kit", "SK-44444", 156.50),
    ("Battery", "BT-55555", 189.99),
    ("Alternator", "AL-66666", 425.00),
    ("Starter Motor", "SM-77777", 385.00),
    ("Control Valve", "CV-88888", 1250.00),
]

print("\nPopulating Neo4j with repair data...")

with driver.session() as session:
    # 1. Create Equipment nodes
    print("\n1. Creating equipment nodes...")
    for equipment_name, details in equipment_data.items():
        session.run(
            """
            MERGE (e:Equipment {name: $name})
            SET e.type = $type,
                e.horsepower = $hp,
                e.last_updated = datetime()
        """,
            name=equipment_name,
            type=details["type"],
            hp=details["hp"],
        )
        print(f"  ✅ Created: {equipment_name}")

    # 2. Create Problem nodes and relationships
    print("\n2. Creating problem nodes...")
    problem_count = 0
    for equipment_name, details in equipment_data.items():
        for problem_type, symptoms, solution in details["common_problems"]:
            problem_id = hashlib.md5(f"{equipment_name}{problem_type}".encode()).hexdigest()[:8]

            session.run(
                """
                MERGE (p:Problem {id: $id})
                SET p.type = $problem_type,
                    p.symptoms = $symptoms,
                    p.solution = $solution,
                    p.created_at = datetime()

                WITH p
                MATCH (e:Equipment {name: $equipment})
                MERGE (e)-[:HAS_PROBLEM]->(p)
            """,
                id=problem_id,
                problem_type=problem_type,
                symptoms=symptoms,
                solution=solution,
                equipment=equipment_name,
            )
            problem_count += 1
    print(f"  ✅ Created {problem_count} problem nodes")

    # 3. Create Error Code nodes
    print("\n3. Creating error code nodes...")
    error_count = 0
    for equipment_name, details in equipment_data.items():
        for error_code in details["error_codes"]:
            session.run(
                """
                MERGE (ec:ErrorCode {code: $code})
                SET ec.last_seen = datetime()

                WITH ec
                MATCH (e:Equipment {name: $equipment})
                MERGE (e)-[:THROWS_ERROR]->(ec)
            """,
                code=error_code,
                equipment=equipment_name,
            )
            error_count += 1
    print(f"  ✅ Created {error_count} error code nodes")

    # 4. Create Repair Procedure nodes
    print("\n4. Creating repair procedure nodes...")
    for procedure in repair_procedures:
        procedure_id = hashlib.md5(procedure.encode()).hexdigest()[:8]

        session.run(
            """
            MERGE (r:RepairProcedure {id: $id})
            SET r.description = $description,
                r.estimated_time = $time,
                r.difficulty = $difficulty
        """,
            id=procedure_id,
            description=procedure,
            time=random.randint(30, 240),  # 30 min to 4 hours
            difficulty=random.choice(["Easy", "Medium", "Hard"]),
        )
    print(f"  ✅ Created {len(repair_procedures)} repair procedures")

    # 5. Create Part nodes
    print("\n5. Creating parts catalog...")
    for part_name, part_number, price in parts_catalog:
        session.run(
            """
            MERGE (p:Part {part_number: $part_number})
            SET p.name = $name,
                p.price = $price,
                p.in_stock = $in_stock
        """,
            part_number=part_number,
            name=part_name,
            price=price,
            in_stock=random.choice([True, True, True, False]),
        )  # 75% in stock
    print(f"  ✅ Created {len(parts_catalog)} parts")

    # 6. Create Solution patterns
    print("\n6. Creating solution patterns...")
    solution_patterns = [
        ("Hydraulic issues", "Check fluid → Test pressure → Replace filter → Inspect hoses"),
        ("Engine problems", "Check fuel → Test battery → Scan codes → Inspect filters"),
        ("Electrical faults", "Test battery → Check fuses → Scan ECM → Inspect grounds"),
        ("Track/Tire issues", "Check tension → Inspect wear → Align → Replace if needed"),
        ("Overheating", "Check coolant → Clean radiator → Test thermostat → Inspect pump"),
    ]

    for pattern_name, steps in solution_patterns:
        pattern_id = hashlib.md5(pattern_name.encode()).hexdigest()[:8]

        session.run(
            """
            MERGE (sp:SolutionPattern {id: $id})
            SET sp.name = $name,
                sp.steps = $steps,
                sp.success_rate = $success_rate
        """,
            id=pattern_id,
            name=pattern_name,
            steps=steps,
            success_rate=random.randint(75, 95),
        )
    print(f"  ✅ Created {len(solution_patterns)} solution patterns")

    # 7. Create Diagnostic Cases (simulated history)
    print("\n7. Creating diagnostic case history...")
    case_count = 0
    for i in range(50):  # Create 50 diagnostic cases
        equipment = random.choice(list(equipment_data.keys()))
        problem = random.choice(equipment_data[equipment]["common_problems"])
        error_code = random.choice(equipment_data[equipment]["error_codes"])

        case_id = f"CASE-{i+1000}"

        session.run(
            """
            CREATE (dc:DiagnosticCase {
                id: $case_id,
                date: datetime(),
                equipment: $equipment,
                problem: $problem,
                error_code: $error_code,
                resolved: $resolved,
                resolution_time: $time,
                technician: $tech
            })

            WITH dc
            MATCH (e:Equipment {name: $equipment})
            CREATE (e)-[:HAD_CASE]->(dc)

            WITH dc
            MATCH (ec:ErrorCode {code: $error_code})
            CREATE (dc)-[:SHOWED_ERROR]->(ec)
        """,
            case_id=case_id,
            equipment=equipment,
            problem=problem[0],
            error_code=error_code,
            resolved=random.choice([True, True, True, False]),  # 75% resolved
            time=random.randint(60, 480),  # 1-8 hours
            tech=random.choice(["Tech A", "Tech B", "Tech C", "Jeremy"]),
        )
        case_count += 1
    print(f"  ✅ Created {case_count} diagnostic cases")

    # Get statistics
    result = session.run(
        """
        MATCH (n)
        RETURN
            COUNT(DISTINCT CASE WHEN 'Equipment' IN labels(n) THEN n END) as equipment,
            COUNT(DISTINCT CASE WHEN 'Problem' IN labels(n) THEN n END) as problems,
            COUNT(DISTINCT CASE WHEN 'ErrorCode' IN labels(n) THEN n END) as error_codes,
            COUNT(DISTINCT CASE WHEN 'RepairProcedure' IN labels(n) THEN n END) as procedures,
            COUNT(DISTINCT CASE WHEN 'Part' IN labels(n) THEN n END) as parts,
            COUNT(DISTINCT CASE WHEN 'DiagnosticCase' IN labels(n) THEN n END) as cases,
            COUNT(DISTINCT CASE WHEN 'SolutionPattern' IN labels(n) THEN n END) as patterns
    """
    )

    stats = result.single()

    print("\n" + "=" * 50)
    print("✅ NEO4J POPULATED WITH REPAIR DATA")
    print("=" * 50)
    print(f"Equipment types: {stats['equipment']}")
    print(f"Common problems: {stats['problems']}")
    print(f"Error codes: {stats['error_codes']}")
    print(f"Repair procedures: {stats['procedures']}")
    print(f"Parts catalog: {stats['parts']}")
    print(f"Diagnostic cases: {stats['cases']}")
    print(f"Solution patterns: {stats['patterns']}")
    print("=" * 50)

    # Total nodes
    total_result = session.run("MATCH (n) RETURN count(n) as total")
    total = total_result.single()["total"]
    print(f"\nTOTAL NODES IN NEO4J: {total}")

driver.close()
print("\n✅ Neo4j Aura now contains comprehensive repair data!")
