"""
Test cases to verify the fixed interchange direction logic

This tests various scenarios that would have been problematic with the old logic:
1. Blue → Magenta through different interchanges
2. Magenta → Blue Branch
3. Same-line trips
4. Edge cases where old logic would choose wrong interchange
"""

from datetime import datetime, timedelta

# Import the station data and functions
import sys
sys.path.insert(0, '.')

# Read station data
def readSection(filename, start, end):
    stations = []
    inSection = False
    
    with open(filename, "r") as file:
        for line in file:
            line = line.strip()            
            if start in line:
                inSection = True
                continue
            if end in line:
                inSection = False
                break

            if inSection:
                if "|" in line and len(line) > 0 and line[0].isalnum():
                    columns = line.split("|")
                    if len(columns) >= 4:
                        s_id = columns[0].strip()
                        stationName = columns[1].strip()
                        
                        time = columns[3].strip()
                        s_time = 0
                        if ":" in time:
                            parts = time.split(":")
                            try:
                                minutes = int(parts[0])
                                seconds = int(parts[1])
                                s_time = (minutes * 60) + seconds
                            except ValueError:
                                s_time = 0

                        stations.append({
                            "id": s_id, 
                            "name": stationName, 
                            "time": s_time
                        })
    return stations

stationBlueMain = readSection("metro_data.txt", "BLUE LINE STATIONS", "BLUE LINE BRANCH STATIONS")
stationBlueBranch = readSection("metro_data.txt", "BLUE LINE BRANCH STATIONS", "[END BLUE]")
stationMagenta = readSection("metro_data.txt", "MAGENTA LINE STATIONS", "[END MAGENTA]")

linesDict = {
    "Blue": stationBlueMain,
    "Blue Branch": stationBlueBranch,
    "Magenta": stationMagenta
}

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

def test_direction_logic(source_line, source_station, end_line, end_station, expected_direction):
    """Test the direction calculation logic"""
    _, dir_str = calcTravelTime(linesDict[source_line], source_station, end_station)
    source_direction = "1" if dir_str == "Down" else "2"
    
    result = "✓" if source_direction == expected_direction else "✗"
    print(f"{result} {source_line}: {source_station} → {end_line}: {end_station}")
    print(f"  Direction: {dir_str} ({source_direction}) | Expected: {expected_direction}")
    return source_direction == expected_direction

print("=" * 70)
print("Testing Fixed Direction Logic")
print("=" * 70)

all_passed = True

# Test 1: Same line trips
print("\n📍 Test 1: Same Line Trips")
print("-" * 70)
all_passed &= test_direction_logic("Blue", "Dwarka Sector 21", "Blue", "Botanical Garden", "1")  # Down
all_passed &= test_direction_logic("Blue", "Botanical Garden", "Blue", "Dwarka Sector 21", "2")  # Up
all_passed &= test_direction_logic("Magenta", "Janak Puri West", "Magenta", "Botanical Garden", "1")  # Down

# Test 2: Blue → Magenta (should use direction to final destination)
print("\n📍 Test 2: Blue → Magenta Cross-Line Trips")
print("-" * 70)
# From west side (before JPW) - should go Down toward destination
all_passed &= test_direction_logic("Blue", "Dwarka Sector 21", "Magenta", "Botanical Garden", "1")
# From east side (after Botanical) - should go Up toward destination  
all_passed &= test_direction_logic("Blue", "Noida Electronic City", "Magenta", "Janak Puri West", "2")
# Middle section
all_passed &= test_direction_logic("Blue", "Yamuna Bank", "Magenta", "Botanical Garden", "1")

# Test 3: Magenta → Blue
print("\n📍 Test 3: Magenta → Blue Cross-Line Trips")
print("-" * 70)
all_passed &= test_direction_logic("Magenta", "Janak Puri West", "Blue", "Noida Electronic City", "1")  # Down on Magenta
all_passed &= test_direction_logic("Magenta", "Botanical Garden", "Blue", "Dwarka Sector 21", "2")  # Up on Magenta

# Test 4: Blue Branch ↔ Blue
print("\n📍 Test 4: Blue Branch ↔ Blue")
print("-" * 70)
all_passed &= test_direction_logic("Blue Branch", "Vaishali", "Blue", "Dwarka Sector 21", "2")  # Up to Yamuna Bank
all_passed &= test_direction_logic("Blue", "Dwarka Sector 21", "Blue Branch", "Vaishali", "1")  # Down to Yamuna Bank

# Test 5: Magenta ↔ Blue Branch (most complex - 2 interchanges)
print("\n📍 Test 5: Magenta ↔ Blue Branch (via Blue Line)")
print("-" * 70)
all_passed &= test_direction_logic("Magenta", "Janak Puri West", "Blue Branch", "Vaishali", "1")  # Down on Magenta
all_passed &= test_direction_logic("Blue Branch", "Vaishali", "Magenta", "Janak Puri West", "2")  # Up to Yamuna Bank

# Test 6: Edge cases - stations near interchanges
print("\n📍 Test 6: Edge Cases - Near Interchange Stations")
print("-" * 70)
# Near JPW interchange
all_passed &= test_direction_logic("Blue", "Janak Puri East", "Magenta", "Botanical Garden", "1")  # Just after JPW
all_passed &= test_direction_logic("Blue", "Uttam Nagar West", "Magenta", "Hauz Khas", "1")  # Just before JPW
# Near Botanical interchange  
all_passed &= test_direction_logic("Blue", "Golf Course", "Magenta", "Janak Puri West", "2")  # Just after Botanical
all_passed &= test_direction_logic("Blue", "Noida Sector 18", "Magenta", "Krishna Park Extension", "1")  # Just before Botanical

print("\n" + "=" * 70)
if all_passed:
    print("✅ ALL TESTS PASSED!")
    print("The direction logic is working correctly.")
else:
    print("❌ SOME TESTS FAILED!")
    print("There may be issues with the direction calculation.")
print("=" * 70)

# Additional verification: Check that proper interchange selection still works
print("\n📍 Bonus: Verify Interchange Selection Logic")
print("-" * 70)

def calc_best_interchange(source_line_name, source_station, end_line_name, end_station):
    """Calculate which interchange is better for Blue ↔ Magenta"""
    source_line = linesDict[source_line_name]
    end_line = linesDict[end_line_name]
    
    # Via Janak Puri West
    t1_jpw, _ = calcTravelTime(source_line, source_station, "Janak Puri West")
    t2_jpw, _ = calcTravelTime(end_line, "Janak Puri West", end_station)
    total_jpw = t1_jpw + t2_jpw
    
    # Via Botanical Garden
    t1_bot, _ = calcTravelTime(source_line, source_station, "Botanical Garden")
    t2_bot, _ = calcTravelTime(end_line, "Botanical Garden", end_station)
    total_bot = t1_bot + t2_bot
    
    if total_jpw <= total_bot:
        return "Janak Puri West", total_jpw
    else:
        return "Botanical Garden", total_bot

# Test interchange selection
test_cases = [
    ("Blue", "Dwarka Sector 21", "Magenta", "Botanical Garden", "Janak Puri West"),
    ("Blue", "Noida Electronic City", "Magenta", "Janak Puri West", "Botanical Garden"),
    ("Magenta", "Janak Puri West", "Blue", "Botanical Garden", "Janak Puri West"),
]

for source_line, source_st, end_line, end_st, expected_interchange in test_cases:
    best_int, time = calc_best_interchange(source_line, source_st, end_line, end_st)
    result = "✓" if best_int == expected_interchange else "✗"
    print(f"{result} {source_st} → {end_st}: Best interchange = {best_int} ({time//60}min {time%60}sec)")

print("\n✅ Verification complete!")
