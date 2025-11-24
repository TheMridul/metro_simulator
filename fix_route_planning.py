"""
Fix the route planning interchange logic too (lines 301-318)
"""

with open("metro_simulator.py", "r", encoding="utf-8") as f:
    content = f.read()

# Fix the route planning logic
old_route_logic = '''    elif (sourceLine == "Blue" and endLine == "Magenta") or (sourceLine == "Magenta" and endLine == "Blue"):
        # Transfer at Janak Puri West or Botanical Garden
        int1 = "Janak Puri West"
        t1_a, _ = calcTravelTime(linesDict[sourceLine], sourceStation, int1)
        t2_a, _ = calcTravelTime(linesDict[endLine], int1, endStation)
        dist_a = t1_a + t2_a
        
        int2 = "Botanical Garden"
        t1_b, _ = calcTravelTime(linesDict[sourceLine], sourceStation, int2)
        t2_b, _ = calcTravelTime(linesDict[endLine], int2, endStation)
        dist_b = t1_b + t2_b
        
        if dist_a <= dist_b:
            interchange = int1
            totalDuration = dist_a + TRANSFER_TIME
        else:
            interchange = int2
            totalDuration = dist_b + TRANSFER_TIME'''

new_route_logic = '''    elif (sourceLine == "Blue" and endLine == "Magenta") or (sourceLine == "Magenta" and endLine == "Blue"):
        # Transfer at Janak Puri West or Botanical Garden
        # If already at an interchange, use the other one
        if sourceStation == "Janak Puri West":
            interchange = "Botanical Garden"
            t1, _ = calcTravelTime(linesDict[sourceLine], sourceStation, interchange)
            t2, _ = calcTravelTime(linesDict[endLine], interchange, endStation)
            totalDuration = t1 + t2 + TRANSFER_TIME
        elif sourceStation == "Botanical Garden":
            interchange = "Janak Puri West"
            t1, _ = calcTravelTime(linesDict[sourceLine], sourceStation, interchange)
            t2, _ = calcTravelTime(linesDict[endLine], interchange, endStation)
            totalDuration = t1 + t2 + TRANSFER_TIME
        else:
            int1 = "Janak Puri West"
            t1_a, _ = calcTravelTime(linesDict[sourceLine], sourceStation, int1)
            t2_a, _ = calcTravelTime(linesDict[endLine], int1, endStation)
            dist_a = t1_a + t2_a
            
            int2 = "Botanical Garden"
            t1_b, _ = calcTravelTime(linesDict[sourceLine], sourceStation, int2)
            t2_b, _ = calcTravelTime(linesDict[endLine], int2, endStation)
            dist_b = t1_b + t2_b
            
            if dist_a <= dist_b:
                interchange = int1
                totalDuration = dist_a + TRANSFER_TIME
            else:
                interchange = int2
                totalDuration = dist_b + TRANSFER_TIME'''

if old_route_logic in content:
    content = content.replace(old_route_logic, new_route_logic)
    
    with open("metro_simulator.py", "w", encoding="utf-8") as f:
        f.write(content)
    
    print("✅ Successfully fixed the route planning interchange logic!")
else:
    print("❌ Could not find the pattern. File may already be modified.")
