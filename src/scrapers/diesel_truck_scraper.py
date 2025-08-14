#!/usr/bin/env python3
"""
Diesel Truck Focused Scraper
Targets: Ford Powerstroke, Ram Cummins, Chevy/GMC Duramax
"""

print("🚛 DIESEL TRUCK FOCUSED SCRAPER")
print("=" * 60)
print()

# HIGH-VALUE YOUTUBE SEARCHES FOR DIESEL TRUCKS
youtube_searches = {
    "ford_powerstroke": [
        "6.7 Powerstroke common problems",
        "6.7 Powerstroke P0299 turbo underboost",
        "6.7 Powerstroke CP4 pump failure",
        "6.7 Powerstroke death wobble fix",
        "6.0 Powerstroke bulletproof",
        "6.0 Powerstroke EGR delete",
        "6.0 Powerstroke head gasket",
        "6.4 Powerstroke DPF delete",
        "7.3 Powerstroke IPR valve",
        "7.3 Powerstroke HPOP",
        "Ford F250 P132B turbo boost control",
        "Ford F350 P0087 fuel rail pressure",
        "Powerstroke DEF problems",
        "Powerstroke injector replacement",
        "Powerstroke FICM repair",
    ],
    "ram_cummins": [
        "6.7 Cummins grid heater delete",
        "6.7 Cummins DPF delete",
        "6.7 Cummins P0191 fuel rail pressure sensor",
        "6.7 Cummins turbo actuator",
        "6.7 Cummins EGR cooler",
        "5.9 Cummins VP44 injection pump",
        "5.9 Cummins P0216 timing",
        "5.9 Cummins lift pump",
        "5.9 Cummins killer dowel pin",
        "5.9 Cummins 53 block crack",
        "Ram 2500 P2262 turbo boost pressure",
        "Ram 3500 U0101 TCM communication",
        "Cummins ISB common rail problems",
        "Cummins exhaust brake install",
        "Cummins APPS sensor",
    ],
    "gm_duramax": [
        "LML Duramax DEF problems",
        "LML Duramax P0191 fuel rail pressure",
        "LML Duramax ninth injector",
        "LBZ Duramax water pump",
        "LBZ Duramax head gasket",
        "LB7 Duramax injector replacement",
        "LB7 Duramax injector harness",
        "LLY Duramax overheating",
        "LLY Duramax turbo vane position sensor",
        "L5P Duramax MAP sensor",
        "Duramax P0087 low fuel rail pressure",
        "Duramax P0093 large fuel leak",
        "Duramax glow plug controller",
        "Duramax transfer case pump rub",
        "Duramax Allison transmission limp mode",
    ],
}

# HIGH-VALUE REDDIT COMMUNITIES
reddit_communities = {
    "ford": ["r/FordDiesels", "r/Powerstroke", "r/FordTrucks"],
    "ram": ["r/Cummins", "r/ram_trucks", "r/DodgeRam"],
    "gm": ["r/Duramax", "r/ChevyTrucks", "r/GMC"],
}

# COMMON ERROR CODES BY BRAND
error_codes = {
    "ford_powerstroke": {
        "P0299": "Turbo underboost",
        "P0087": "Fuel rail pressure too low",
        "P132B": "Turbo boost control A performance",
        "P2291": "Injector control pressure too low",
        "P0261": "Cylinder 1 injector circuit low",
        "P0401": "EGR flow insufficient",
        "P2263": "Turbo boost system performance",
        "P0470": "Exhaust pressure sensor malfunction",
        "P0671-P0678": "Glow plug circuit codes",
    },
    "ram_cummins": {
        "P0191": "Fuel rail pressure sensor range",
        "P2262": "Turbo boost pressure not detected",
        "P0216": "Injection timing control",
        "P0336": "Crankshaft position sensor",
        "U0101": "Lost communication with TCM",
        "P0121": "APPS sensor range/performance",
        "P2509": "ECM power input signal intermittent",
        "P0606": "ECM processor fault",
        "P0483": "Cooling fan rationality check",
    },
    "gm_duramax": {
        "P0087": "Fuel rail pressure too low",
        "P0093": "Large fuel leak detected",
        "P0191": "Fuel rail pressure sensor",
        "P1093": "Fuel rail pressure low during acceleration",
        "P0101": "MAF sensor range/performance",
        "P2563": "Turbo vane position sensor",
        "P0671-P0678": "Glow plug circuit codes",
        "U0100": "Lost communication with ECM",
        "P0700": "Transmission control system",
    },
}

# COMMON PARTS & COSTS
parts_database = {
    "ford_powerstroke": {
        "CP4 Pump": "$3000-4500",
        "Turbo": "$2000-3500",
        "EGR Cooler": "$800-1500",
        "Injectors (set)": "$3000-4000",
        "FICM": "$800-1200",
        "HPOP (7.3)": "$800-1200",
        "Head Gaskets (6.0)": "$3500-5000",
        "Oil Cooler": "$250-500",
    },
    "ram_cummins": {
        "VP44 Pump (5.9)": "$1200-1800",
        "CP3 Pump": "$1500-2500",
        "Grid Heater": "$150-300",
        "Turbo Actuator": "$400-800",
        "Injectors (set)": "$2500-3500",
        "Lift Pump": "$400-800",
        "EGR Valve": "$300-500",
        "DPF Filter": "$2000-3000",
    },
    "gm_duramax": {
        "Injectors (LB7)": "$2500-3500",
        "CP3 Pump": "$1500-2500",
        "Water Pump": "$150-300",
        "Turbo": "$2000-3000",
        "DEF Tank": "$800-1200",
        "Ninth Injector": "$300-500",
        "Transfer Case Pump": "$600-900",
        "Glow Plugs (set)": "$200-400",
    },
}

print("🎯 TARGET DIESEL TRUCKS:")
print()
print("FORD POWERSTROKE:")
print("  • 6.0L (2003-2007) - Head gaskets, EGR, oil cooler")
print("  • 6.4L (2008-2010) - DPF issues, fuel dilution")
print("  • 6.7L (2011+) - CP4 pump, turbo, DEF system")
print("  • 7.3L (1994-2003) - HPOP, IPR, injectors")
print()
print("RAM CUMMINS:")
print("  • 5.9L 12V (1989-1998) - Killer dowel pin, lift pump")
print("  • 5.9L 24V (1998-2007) - VP44/CP3 pump, injectors")
print("  • 6.7L (2007+) - DPF/DEF, grid heater, turbo actuator")
print()
print("CHEVY/GMC DURAMAX:")
print("  • LB7 (2001-2004) - Injector failure endemic")
print("  • LLY (2004-2006) - Overheating, head gaskets")
print("  • LBZ (2006-2007) - Most reliable, water pump")
print("  • LML (2011-2016) - DEF system, ninth injector")
print("  • L5P (2017+) - Most powerful, DEF issues")
print()
print("-" * 60)
print()
print("📺 YOUTUBE CHANNELS FOR DIESEL TRUCKS:")
print()
print("MUST WATCH:")
print("  • PowerStroke Tech Talk")
print("  • Diesel Tech Ron (Cummins expert)")
print("  • Duramax Tuner")
print("  • Thoroughbred Diesel")
print("  • Blessed Performance")
print()
print("DIAGNOSTIC EXPERTS:")
print("  • Ford Boss Me")
print("  • Diesel Diagnostics")
print("  • Motor City Mechanic")
print()
print("-" * 60)
print()
print("💰 TYPICAL REPAIR COSTS:")
for brand, parts in parts_database.items():
    print(f"\n{brand.upper().replace('_', ' ')}:")
    for part, cost in list(parts.items())[:4]:
        print(f"  • {part}: {cost}")
print()
print("-" * 60)
print()
print("🔍 WHAT TO SCRAPE:")
print()
print("1. ERROR CODE SOLUTIONS")
print("   P0087 (fuel pressure) - All three brands")
print("   P0299 (turbo) - Common on Powerstroke")
print("   P0191 (rail pressure sensor) - Cummins/Duramax")
print()
print("2. COMMON FAILURES BY YEAR/ENGINE")
print("   6.0 Powerstroke head gaskets")
print("   LB7 Duramax injectors")
print("   5.9 Cummins VP44 pump")
print()
print("3. COST COMPARISONS")
print("   OEM vs aftermarket parts")
print("   Shop vs DIY labor time")
print("   Delete kit pricing")
print()
print("Ready to scrape these specific diesel truck models!")
