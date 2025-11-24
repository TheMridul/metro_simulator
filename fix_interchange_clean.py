"""
Complete fix for the interchange direction logic.
This manually writes the corrected section to fix the bug.
"""

with open("metro_simulator.py", "r", encoding="utf-8") as f:
    content = f.read()

# Define the corrected Blue/Magenta interchange logic
old_logic = '''        elif (sourceLine == "Blue" and endLine == "Magenta") or (sourceLine == "Magenta" and endLine == "Blue"):
            # Comparing JPW(janakpuri west) vs Botanical
            t_jpw, _ = calcTravelTime(linesDict[sourceLine], sourceStation, "Janak Puri West")
            t_jpw2, _ = calcTravelTime(linesDict[endLine], "Janak Puri West", endStation)
            
            t_bot, _ = calcTravelTime(linesDict[sourceLine], sourceStation, "Botanical Garden")
            t_bot2, _ = calcTravelTime(linesDict[endLine], "Botanical Garden", endStation)
            
            if (t_jpw + t_jpw2) <= (t_bot + t_bot2):
                reqStation = "Janak Puri West"
            else:
                reqStation = "Botanical Garden"'''

new_logic = '''        elif (sourceLine == "Blue" and endLine == "Magenta") or (sourceLine == "Magenta" and endLine == "Blue"):
            # If already at an interchange, use the other one
            if sourceStation == "Janak Puri West":
                reqStation = "Botanical Garden"
            elif sourceStation == "Botanical Garden":
                reqStation = "Janak Puri West"
            else:
                # Comparing JPW(janakpuri west) vs Botanical
                t_jpw, _ = calcTravelTime(linesDict[sourceLine], sourceStation, "Janak Puri West")
                t_jpw2, _ = calcTravelTime(linesDict[endLine], "Janak Puri West", endStation)
                
                t_bot, _ = calcTravelTime(linesDict[sourceLine], sourceStation, "Botanical Garden")
                t_bot2, _ = calcTravelTime(linesDict[endLine], "Botanical Garden", endStation)
                
                if (t_jpw + t_jpw2) <= (t_bot + t_bot2):
                    reqStation = "Janak Puri West"
                else:
                    reqStation = "Botanical Garden"'''

# Replace
if old_logic in content:
    content = content.replace(old_logic, new_logic)
    
    with open("metro_simulator.py", "w", encoding="utf-8") as f:
        f.write(content)
    
    print("✅ Successfully fixed the interchange logic!")
    print("Added check to prevent selecting an interchange you're already at.")
else:
    print("❌ Could not find the exact pattern to replace.")
    print("The file may have already been modified.")
