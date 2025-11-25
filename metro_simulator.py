from datetime import datetime,timedelta
TRANSFER_TIME = 0  
SERVICE_START_HOUR = 6
SERVICE_END_HOUR = 23
# reading data from filr
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

# inputs
def stationSelect(ask_direction=True):
    print("Select Line ")
    print("1. Blue Line (Dwarka Sec 21 - Noida Elec. City)")
    print("2. Blue Branch (Yamuna Bank - Vaishali)")
    print("3. Magenta Line (Janak Puri West - Botanical Garden)")
    
    while True:
        try:
            choice = input("Enter Choice (1-3): ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nInput cancelled.")
            exit()

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
    
    direction = None
    if ask_direction:
        print(f" Select Direction ")
        print(f"1. Down: {startStation} -> {endStation}")
        print(f"2. Up:   {endStation} -> {startStation}")
        while True:
            direction = input("Enter Direction (1 or 2): ").strip()
            if direction in ("1", "2"):
                break
            print("Invalid input. Enter 1 or 2.")

    
    print(f" Stations on this Line ")
    for s in activeLine:
        print(f'{s["id"]}: {s["name"]}')
    
    targetID = input("Enter your Station ID (e.g., 1b): ").strip().lower()
    # index of the selected station
    reqIndex = -1
    for idx, s in enumerate(activeLine):
        if s["id"].lower() == targetID:
            reqIndex = idx
            break
    
    return activeLine, reqIndex, choice, direction

# offset calc
def calcOffset(activeLine, reqIndex, direction):
    if reqIndex == -1:
        return None
    # Time Offset
    cumuSec = 0
    # Down
    if str(direction) == "1":  # string or no.
        # Add time of all previous stations upto current
        for i in range(1, reqIndex + 1):
            cumuSec += activeLine[i]["time"]
    else: 
        # Up
        for i in range(reqIndex + 1, len(activeLine)):
            cumuSec += activeLine[i]["time"]
    return cumuSec

#  timing logic 
def calcTimings(offsetSec, startTime):
    
    # service hours
    serviceStart = startTime.replace(hour=SERVICE_START_HOUR, minute=0, second=0, microsecond=0)
    serviceEnd = startTime.replace(hour=SERVICE_END_HOUR, minute=0, second=0, microsecond=0)
    
    # offset adjusting
    firstArrival = serviceStart + timedelta(seconds=offsetSec)
    lastArrival = serviceEnd + timedelta(seconds=offsetSec)
    
    
    #the first metro at 06:00 + offset 
    if startTime < serviceStart:
        startTime = serviceStart

    if startTime > lastArrival:
        return ["No service available"]
        
    def getFreq(time):
        h = time.hour
        if (8 <= h < 10) or (17 <= h < 19):
            return 4 
        else:
            return 8

    # next metro afterr first arrival using changing frequencies
    if startTime <= firstArrival:
        nextMetro = firstArrival
    else:
        cur = firstArrival
        while cur <= startTime:
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
        return total_time, 1
    else: 
        for i in range(end_idx + 1, start_idx + 1):
            total_time += line_data[i]["time"]
        return total_time, 2

def customTime(now):
    print("\nSelect Time Option:")
    print("1. Current Time")
    print("2. Custom Time")
    try:
        choice = input("Enter Choice (1 or 2): ").strip()
    except:
        print("\nInvalid input. Using current time.")
        return now
        
    
    if choice == "2":
        time_str = input("Enter time (HH:MM): ").strip()
        try:
            # custom time, assuming current date
            t = datetime.strptime(time_str, "%H:%M").time()
            return now.replace(hour=t.hour, minute=t.minute, second=0, microsecond=0)
        except ValueError:
            print("Invalid time format. Using current time.")
            return now
    return now

# mode selection
def modeSelector():
    print()
    print("Welcome to Delhi Metro Simulator")
    print("Select Mode:")
    mode= input("Enter 1 for Metro Timings, 2 for Trip Planner: ").strip()
    if mode in ["1", "2"]:
        return mode
    else:
        print("Invalid choice. Defaulting to Metro Timings.")
        return "1"

def findRoute(sourceLine, sourceStation, endLine, endStation):
    linesDict = {
        "Blue": stationBlueMain,
        "Blue Branch": stationBlueBranch,
        "Magenta": stationMagenta
    }
    # same-named station on multiple lines
    is_direct = False
    if sourceLine != endLine:
        for s in linesDict[endLine]:
            if s["name"] == sourceStation:
                is_direct = True
                sourceLine = endLine
                break
    if is_direct:
        return [{"line": sourceLine, "start": sourceStation, "end": endStation}]

    # destination exists on the source line
    if sourceLine != endLine:
        for s in linesDict[sourceLine]:
            if s["name"] == endStation:
                # destination is on the source line -- give a direct segment
                return [{"line": sourceLine, "start": sourceStation, "end": endStation}]
    
    # Same Line
    if sourceLine == endLine:
        return [{"line": sourceLine, "start": sourceStation, "end": endStation}]
        
    #Direct Transfer
    # Blue - Blue Branch (Yamuna Bank)
    if (sourceLine == "Blue" and endLine == "Blue Branch") or (sourceLine == "Blue Branch" and endLine == "Blue"):
        return [
            {"line": sourceLine, "start": sourceStation, "end": "Yamuna Bank"},
            {"line": endLine, "start": "Yamuna Bank", "end": endStation}
        ]
        
    # Blue - Magenta (Janak Puri West or Botanical Garden)
    if (sourceLine == "Blue" and endLine == "Magenta") or (sourceLine == "Magenta" and endLine == "Blue"):
        # via Janak Puri West
        t1_a, _ = calcTravelTime(linesDict[sourceLine], sourceStation, "Janak Puri West")
        t2_a, _ = calcTravelTime(linesDict[endLine], "Janak Puri West", endStation)
        dist_a = t1_a + t2_a
        
        # via Botanical Garden
        t1_b, _ = calcTravelTime(linesDict[sourceLine], sourceStation, "Botanical Garden")
        t2_b, _ = calcTravelTime(linesDict[endLine], "Botanical Garden", endStation)
        dist_b = t1_b + t2_b
        
        interchange = "Janak Puri West" if dist_a <= dist_b else "Botanical Garden"
        
        return [
            {"line": sourceLine, "start": sourceStation, "end": interchange},
            {"line": endLine, "start": interchange, "end": endStation}
        ]

    # double transfer (Magenta - Blue Branch)
    if sourceLine == "Magenta" and endLine == "Blue Branch":
        # via Janak Puri West
        t1_a, _ = calcTravelTime(linesDict["Magenta"], sourceStation, "Janak Puri West")
        t2_a, _ = calcTravelTime(linesDict["Blue"], "Janak Puri West", "Yamuna Bank")
        
        # via Botanical Garden
        t1_b, _ = calcTravelTime(linesDict["Magenta"], sourceStation, "Botanical Garden")
        t2_b, _ = calcTravelTime(linesDict["Blue"], "Botanical Garden", "Yamuna Bank")
        
        interchange1 = "Janak Puri West" if (t1_a + t2_a) <= (t1_b + t2_b) else "Botanical Garden"
        
        return [
            {"line": "Magenta", "start": sourceStation, "end": interchange1},
            {"line": "Blue", "start": interchange1, "end": "Yamuna Bank"},
            {"line": "Blue Branch", "start": "Yamuna Bank", "end": endStation}
        ]
        
    if sourceLine == "Blue Branch" and endLine == "Magenta":
        # via Janak Puri West
        t2_a, _ = calcTravelTime(linesDict["Blue"], "Yamuna Bank", "Janak Puri West")
        t3_a, _ = calcTravelTime(linesDict["Magenta"], "Janak Puri West", endStation)
        
        # via Botanical Garden
        t2_b, _ = calcTravelTime(linesDict["Blue"], "Yamuna Bank", "Botanical Garden")
        t3_b, _ = calcTravelTime(linesDict["Magenta"], "Botanical Garden", endStation)
        
        interchange2 = "Janak Puri West" if (t2_a + t3_a) <= (t2_b + t3_b) else "Botanical Garden"
        
        return [
            {"line": "Blue Branch", "start": sourceStation, "end": "Yamuna Bank"},
            {"line": "Blue", "start": "Yamuna Bank", "end": interchange2},
            {"line": "Magenta", "start": interchange2, "end": endStation}
        ]

    return []

def simulateJourney(segments, startTime):
    linesDict = {
        "Blue": stationBlueMain,
        "Blue Branch": stationBlueBranch,
        "Magenta": stationMagenta
    }
    
    currentTime = startTime
    journeyStart = startTime
    print("\nJourney Plan")
    print(f"Start Time: {startTime.strftime('%H:%M')}")
    
    for i, seg in enumerate(segments):
        lineName = seg["line"]
        sourceStation = seg["start"]
        desStation = seg["end"]
        lineData = linesDict[lineName]
        
        # direction
        _, dirCode = calcTravelTime(lineData, sourceStation, desStation)
        directionStr = "1" if dirCode == 1 else "2"
        
        # start Index
        startIndex = -1
        for idx, s in enumerate(lineData):
            if s["name"] == sourceStation:
                startIndex = idx
                break
                
        # Offset calc
        offset = calcOffset(lineData, startIndex, directionStr)
        
        # next train departure
        if i > 0:
            currentTime += timedelta(seconds=TRANSFER_TIME)
            print(f"Transfer at {sourceStation} ... Ready at {currentTime.strftime('%H:%M')}")
            
        timings = calcTimings(offset, currentTime)
        
        if not timings or "service" in timings[0].lower() or "End of Service" in timings[0]:
            print(f"No service available on {lineName} from {sourceStation}")
            return
            
        # first timing to format 
        next_train_str = timings[0]
        next_train_time = datetime.strptime(next_train_str, "%H:%M").time()
        departureTime = currentTime.replace(hour=next_train_time.hour, minute=next_train_time.minute, second=0, microsecond=0)
        print(f"Next metro from {sourceStation}: {departureTime.strftime('%H:%M')}")
        print(f"Board {lineName} at {sourceStation}: {departureTime.strftime('%H:%M')}")
        
        s_idx = startIndex
        e_idx = -1
        for idx, s in enumerate(lineData):
            if s["name"] == desStation:
                e_idx = idx
                break
            # Down    
        if dirCode == 1:
            indices = range(s_idx, e_idx)
        else: # Up
            indices = range(s_idx, e_idx, -1)
            
        currentTrainTime = departureTime
        
        for idx in indices:
            if dirCode == 1:
                next_idx = idx + 1
                travel_time = lineData[next_idx]["time"]
                next_station_name = lineData[next_idx]["name"]
            else:
                next_idx = idx - 1
                travel_time = lineData[idx]["time"]
                next_station_name = lineData[next_idx]["name"]
            
            currentTrainTime += timedelta(seconds=travel_time)

            # ONLY print if it is the end station of the segment
            if next_station_name == desStation:
                print(f"Arrive {next_station_name}: {currentTrainTime.strftime('%H:%M')}")
            
        currentTime = currentTrainTime
    
    #total travel time
    totalSeconds = int((currentTime - journeyStart).total_seconds())
    minutes = totalSeconds // 60
    seconds = totalSeconds % 60
    print(f"\nTotal travel time: {minutes} min {seconds} sec")

def tripPlanner():
    print("Trip Planner ")
    print("Disclaimer: Transfer time at interchanges as wait for next train.")
    
    startTime = customTime(datetime.now())
    
    activeLineS, reqIndexs, sourceLine, _ = stationSelect(ask_direction=False)
    if reqIndexs == -1: return
    sourceStation = activeLineS[reqIndexs]["name"]
    
    activeLineE, reqIndexD, endLine, _ = stationSelect(ask_direction=False)
    if reqIndexD == -1: return
    endStation = activeLineE[reqIndexD]["name"]
    
    if sourceStation == endStation:
        print("Source and Destination are the same. Travel time is 0.")
        return

    segments = findRoute(sourceLine, sourceStation, endLine, endStation)
    
    if not segments:
        print("Could not find a route.")
        return
    simulateJourney(segments, startTime)

selected_mode = modeSelector()
if selected_mode == "1":
    activeLine, reqIndex, stationLine, direction = stationSelect()
    if reqIndex != -1:
        stationName = activeLine[reqIndex]["name"]
        stationOffset = calcOffset(activeLine, reqIndex, direction)
        
        print(f"Station: {stationName} on {stationLine} line")
        startTime = customTime(datetime.now())
        timings = calcTimings(stationOffset, startTime)
        
        if "service" in timings[0].lower():
            print(timings[0])
        else:
            print(f"Next metro at {timings[0]}")
            if len(timings) > 1:
                print("Subsequent metros at " + ", ".join(timings[1:]))
    else:
        print("Station not found.")
else:
    tripPlanner()