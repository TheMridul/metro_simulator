from datetime import datetime,timedelta

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
                # spliting to get req. data
                if "|" in line and len(line) > 0 and line[0].isalnum():
                    columns = line.split("|")
                    if len(columns) >= 4:
                        s_id = columns[0].strip()
                        stationName = columns[1].strip()
                        
                        # time calc
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
# print(stationBlueBranch)

# inputs
def stationSelectoffset():
    print("Select Line ")
    print("1. Blue Line (Dwarka Sec 21 - Noida Elec. City)")
    print("2. Blue Branch (Yamuna Bank - Vaishali)")
    print("3. Magenta Line (Janak Puri West - Botanical Garden)")
    
    while True:
        choice = input("Enter Choice (1-3): ").strip()
        if choice == "1":
            choice = "Blue"
            activeLine = stationBlueMain
            break
        elif choice == "2":
            choice = "Blue Branch"
            activeLine = stationBlueBranch
            break
        elif choice == "3":
            choice = "Magenta"
            activeLine = stationMagenta
            break
        print("Invalid choice. Try again.")

    startStation = activeLine[0]["name"]
    endStation = activeLine[-1]["name"]
    
    print(f" Select Direction ")
    print(f"1. Down: {startStation} -> {endStation}")
    print(f"2. Up:   {endStation} -> {startStation}")
    
    direction = input("Enter Direction (1 or 2): ").strip()
    
    print(f" Stations on this Line ")
    for s in activeLine:
        print(f"{s["id"]}: {s["name"]}")
    
    targetID = input("Enter your Station ID (e.g., 1b): ").strip().lower()
    # index of the selected station
    reqIndex = -1
    for idx, s in enumerate(activeLine):
        if s["id"].lower() == targetID:
            reqIndex = idx
            break
    if reqIndex == -1:
        return None, None, None
    # Time Offset
    cumuSec = 0
    # Down
    if direction == "1":  
        # Add time of all previous stations upto current
        for i in range(1, reqIndex + 1):
            cumuSec += activeLine[i]["time"]
    else: 
        # Up
        for i in range(reqIndex + 1, len(activeLine)):
            cumuSec += activeLine[i]["time"]
            
    return activeLine[reqIndex]["name"], cumuSec, choice, direction

#  timing logic 

def calcTimings(offsetSec):
    now = datetime.now()
    
    # service hours
    serviceStart = now.replace(hour=6, minute=0, second=0, microsecond=0)
    serviceEnd = now.replace(hour=23, minute=0, second=0, microsecond=0)
    
    # offset adjusting
    firstArrival = serviceStart + timedelta(seconds=offsetSec)
    lastArrival = serviceEnd + timedelta(seconds=offsetSec)
    
    if now > lastArrival:
        return ["No service available"]
        
    def getFreq(time):
        h = time.hour
        if (8 <= h < 10) or (17 <= h < 19):
            return 4 
        else:
            return 8

    # next metro afterr first arrival using changing frequencies
    if now <= firstArrival:
        nextMetro = firstArrival
    else:
        cur = firstArrival
        while cur <= now:
            cur += timedelta(minutes=getFreq(cur))
        nextMetro = cur

    # next 3 metros
    timings = []
    for _ in range(3):
        if nextMetro > lastArrival:
            timings.append("End of Service")
            break
        timings.append(nextMetro.strftime("%H:%M"))
        nextMetro += timedelta(minutes=getFreq(nextMetro))
    return timings

def modeSelector():
    mode= input("Enter 1 for Metro Timings, 2 for Trip Planner: ").strip()
    if mode in ["1", "2"]:
        return mode
    else:
        print("Invalid choice. Try again.")

def tripPlanner():
    sourceStation, sourceOffset, sourceLine, sourcedirection = stationSelectoffset()
    endStation, endOffset, endLine, enddirection = stationSelectoffset()
    nextMetroTimings=calcTimings(sourceOffset)

    if sourceLine == endLine and sourcedirection == enddirection:
        diff=endOffset-sourceOffset
        print("Journey Plan")
        print(f"Start from {sourceStation} on {sourceLine} line.")
        print(f"Next metro at {nextMetroTimings[0]}")
        arrival_time = datetime.strptime(nextMetroTimings[0], "%H:%M") + timedelta(seconds=diff)
        print(f"Arrive at {endStation} at {arrival_time.strftime('%H:%M')}")
        print(f"Total time: {diff // 60} min {diff % 60} sec")
    else:
        print("Trip cannot be planned between different lines.")

if modeSelector() == "1":
    stationName, stationOffset, stationLine, direction = stationSelectoffset()
    if stationName:
        print(f"Station: {stationName} on {stationLine} line.")
        # print(f"{stationOffset // 60} min {stationOffset % 60} sec")

        timings = calcTimings(stationOffset)
        if "Service" in timings[0]:
            print(timings[0])
        else:
            print(f"Next metro at {timings[0]}")
            if len(timings) > 1:
                print(f"Subsequent metros at {", ".join(timings[1:])}")
    else:
        print("Station not found.")
else:
    tripPlanner()