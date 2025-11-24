"""
Final fix: Add interchange check to Magenta → Blue Branch case as well
"""

with open("metro_simulator.py", "r", encoding="utf-8") as f:
    content = f.read()

# Fix Magenta → Blue Branch direction calculation
old_magenta_branch = '''        elif sourceLine == "Magenta" and endLine == "Blue Branch":
            # Magenta -- Blue -- Branch
            t_jpw, _ = calcTravelTime(linesDict["Magenta"], sourceStation, "Janak Puri West")
            t_blue_jpw, _ = calcTravelTime(linesDict["Blue"], "Janak Puri West", "Yamuna Bank")
            
            t_bot, _ = calcTravelTime(linesDict["Magenta"], sourceStation, "Botanical Garden")
            t_blue_bot, _ = calcTravelTime(linesDict["Blue"], "Botanical Garden", "Yamuna Bank")
            
            # Remaining path from Yamuna Bank is same, so just compare to Yamuna Bank
            if (t_jpw + t_blue_jpw) <= (t_bot + t_blue_bot):
                reqStation = "Janak Puri West"
            else:
                reqStation = "Botanical Garden"'''

new_magenta_branch = '''        elif sourceLine == "Magenta" and endLine == "Blue Branch":
            # Magenta -- Blue -- Branch
            # If already at an interchange, use the other one
            if sourceStation == "Janak Puri West":
                reqStation = "Botanical Garden"
            elif sourceStation == "Botanical Garden":
                reqStation = "Janak Puri West"
            else:
                t_jpw, _ = calcTravelTime(linesDict["Magenta"], sourceStation, "Janak Puri West")
                t_blue_jpw, _ = calcTravelTime(linesDict["Blue"], "Janak Puri West", "Yamuna Bank")
                
                t_bot, _ = calcTravelTime(linesDict["Magenta"], sourceStation, "Botanical Garden")
                t_blue_bot, _ = calcTravelTime(linesDict["Blue"], "Botanical Garden", "Yamuna Bank")
                
                # Remaining path from Yamuna Bank is same, so just compare to Yamuna Bank
                if (t_jpw + t_blue_jpw) <= (t_bot + t_blue_bot):
                    reqStation = "Janak Puri West"
                else:
                    reqStation = "Botanical Garden"'''

if old_magenta_branch in content:
    content = content.replace(old_magenta_branch, new_magenta_branch)
    
    with open("metro_simulator.py", "w", encoding="utf-8") as f:
        f.write(content)
    
    print("✅ Fixed Magenta → Blue Branch direction calculation!")
else:
    print("❌ Pattern not found")
