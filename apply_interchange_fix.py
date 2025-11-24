"""
Script to fix the fragile interchange direction logic in metro_simulator.py
Adds checks to prevent selecting an interchange you're already at.
"""

# Read the file
with open("metro_simulator.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

# Find and replace the problematic section (lines 241-252 in original)
# We need to add a check for when sourceStation is already at an interchange

new_lines = []
i = 0
while i < len(lines):
    line = lines[i]
    
    # Check if we're at the start of the Blue/Magenta interchange logic
    if 'elif (sourceLine == "Blue" and endLine == "Magenta") or (sourceLine == "Magenta" and endLine == "Blue"):' in line:
        # Add the line with the condition
        new_lines.append(line)
        i += 1
        
        # Add the fix: check if already at an interchange
        new_lines.append('            # If already at an interchange, use the other one\n')
        new_lines.append('            if sourceStation == "Janak Puri West":\n')
        new_lines.append('                reqStation = "Botanical Garden"\n')
        new_lines.append('            elif sourceStation == "Botanical Garden":\n')
        new_lines.append('                reqStation = "Janak Puri West"\n')
        new_lines.append('            else:\n')
        
        # Now add the original logic with extra indentation
        while i < len(lines) and 'elif sourceLine == "Magenta" and endLine == "Blue Branch":' not in lines[i]:
            # Add extra indentation to existing lines
            if lines[i].strip() and not lines[i].strip().startswith('#'):
                new_lines.append('    ' + lines[i])
            else:
                new_lines.append(lines[i])
            i += 1
        continue
    
    new_lines.append(line)
    i += 1

# Write back
with open("metro_simulator.py", "w", encoding="utf-8") as f:
    f.writelines(new_lines)

print("✅ Fixed the interchange logic!")
print("Added check to prevent selecting an interchange you're already at.")
