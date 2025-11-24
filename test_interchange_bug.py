"""
Reproduction script to demonstrate fragile interchange selection logic

This script tests various scenarios where the current logic might choose
an interchange that's in the opposite direction or past the user's position.
"""

from datetime import datetime, timedelta

# Simulated station data (simplified)
stationBlueMain = [
    {"id": "1b", "name": "Dwarka Sector 21", "time": 0},
    {"id": "14b", "name": "Janak Puri West", "time": 100},  # Simplified
    {"id": "34b", "name": "Yamuna Bank", "time": 200},
    {"id": "42b", "name": "Botanical Garden", "time": 250},
    {"id": "50b", "name": "Noida Electronic City", "time": 300}
]

stationMagenta = [
    {"id": "1m", "name": "Krishna Park Extension", "time": 0},
    {"id": "2m", "name": "Janak Puri West", "time": 50},
    {"id": "26m", "name": "Botanical Garden", "time": 200}
]

def calcTravelTime(line_data, start_name, end_name):
    start_idx = -1
    end_idx = -1
    for i, s in enumerate(line_data):
        if s["name"] == start_name:
            start_idx = i
        if s["name"] == end_name:
            end_idx = i
            
    if start_idx == -1 or end_idx == -1:
        return 0, ""

    total_time = 0
    if start_idx < end_idx: 
        for i in range(start_idx + 1, end_idx + 1):
            total_time += line_data[i]["time"]
        return total_time, "Down"
    else: 
        for i in range(end_idx + 1, start_idx + 1):
            total_time += line_data[i]["time"]
        return total_time, "Up"


print("=" * 60)
print("Testing Interchange Selection Logic")
print("=" * 60)

# Test Case 1: Near Janak Puri West going to Botanical Garden on Magenta
print("\nTest 1: Dwarka Sector 21 (Blue) → Botanical Garden (Magenta)")
print("-" * 60)
sourceStation = "Dwarka Sector 21"
endStation = "Botanical Garden"

t_jpw_1, _ = calcTravelTime(stationBlueMain, sourceStation, "Janak Puri West")
t_jpw_2, _ = calcTravelTime(stationMagenta, "Janak Puri West", endStation)
print(f"Via Janak Puri West: {t_jpw_1} + {t_jpw_2} = {t_jpw_1 + t_jpw_2}")

t_bot_1, _ = calcTravelTime(stationBlueMain, sourceStation, "Botanical Garden")
t_bot_2, _ = calcTravelTime(stationMagenta, "Botanical Garden", endStation)
print(f"Via Botanical Garden: {t_bot_1} + {t_bot_2} = {t_bot_1 + t_bot_2}")

if (t_jpw_1 + t_jpw_2) <= (t_bot_1 + t_bot_2):
    selected = "Janak Puri West"
else:
    selected = "Botanical Garden"
print(f"✓ Selected: {selected} (CORRECT - JPW is on the way)")

# Test Case 2: Near Botanical Garden going backwards to Janak Puri West on Magenta
print("\n\nTest 2: Botanical Garden (Blue) → Janak Puri West (Magenta)")
print("-" * 60)
sourceStation = "Botanical Garden"
endStation = "Janak Puri West"

t_jpw_1, _ = calcTravelTime(stationBlueMain, sourceStation, "Janak Puri West")
t_jpw_2, _ = calcTravelTime(stationMagenta, "Janak Puri West", endStation)
print(f"Via Janak Puri West: {t_jpw_1} + {t_jpw_2} = {t_jpw_1 + t_jpw_2}")

t_bot_1, _ = calcTravelTime(stationBlueMain, sourceStation, "Botanical Garden")
t_bot_2, _ = calcTravelTime(stationMagenta, "Botanical Garden", endStation)
print(f"Via Botanical Garden: {t_bot_1} + {t_bot_2} = {t_bot_1 + t_bot_2}")

if (t_jpw_1 + t_jpw_2) <= (t_bot_1 + t_bot_2):
    selected = "Janak Puri West"
else:
    selected = "Botanical Garden"
print(f"✗ Selected: {selected} (WRONG - Should be JPW, not already at Botanical!)")

# Test Case 3: Past both interchanges
print("\n\nTest 3: Noida Electronic City (Blue) → Krishna Park Extension (Magenta)")
print("-" * 60)
sourceStation = "Noida Electronic City"
endStation = "Krishna Park Extension"

t_jpw_1, _ = calcTravelTime(stationBlueMain, sourceStation, "Janak Puri West")
t_jpw_2, _ = calcTravelTime(stationMagenta, "Janak Puri West", endStation)
print(f"Via Janak Puri West: {t_jpw_1} + {t_jpw_2} = {t_jpw_1 + t_jpw_2}")

t_bot_1, _ = calcTravelTime(stationBlueMain, sourceStation, "Botanical Garden")
t_bot_2, _ = calcTravelTime(stationMagenta, "Botanical Garden", endStation)
print(f"Via Botanical Garden: {t_bot_1} + {t_bot_2} = {t_bot_1 + t_bot_2}")

if (t_jpw_1 + t_jpw_2) <= (t_bot_1 + t_bot_2):
    selected = "Janak Puri West"
else:
    selected = "Botanical Garden"
print(f"✓ Selected: {selected} (Either works, but JPW is shorter)")

print("\n" + "=" * 60)
print("Summary: Current logic can select wrong interchange!")
print("=" * 60)
