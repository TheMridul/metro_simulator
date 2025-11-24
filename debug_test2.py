"""Debug: Check what's happening in test 2"""

# Simplified test
stationBlueMain_test = [{"name": "Dwarka Sector 21"}, {"name": "Botanical Garden"}, {"name": "Noida Electronic City"}]
stationMagenta_test = [{"name": "Krishna Park Extension"}, {"name": "Janak Puri West"}, {"name": "Botanical Garden"}]

sourceStation = "Botanical Garden"
endStation = "Janak Puri West"
sourceLine = "Blue"
endLine = "Magenta"

print(f"Source: {sourceStation} on {sourceLine}")
print(f"Destination: {endStation} on {endLine}")
print(f"Check: sourceStation == 'Botanical Garden': {sourceStation == 'Botanical Garden'}")
print(f"This SHOULD select Janak Puri West as the interchange")
