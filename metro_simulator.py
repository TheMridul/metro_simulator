from datetime import datetime,timedelta
TRANSFER_TIME = 240  # 4 minutes in seconds
SERVICE_START_HOUR = 6
SERVICE_END_HOUR = 23
now= datetime.now()
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
    
    direction = None
    if ask_direction:
        print(f" Select Direction ")
        print(f"1. Down: {startStation} -> {endStation}")
        print(f"2. Up:   {endStation} -> {startStation}")
        
        direction = input("Enter Direction (1 or 2): ").strip()
    
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
    if direction == "1":  
        # Add time of all previous stations upto current
        for i in range(1, reqIndex + 1):
            cumuSec += activeLine[i]["time"]
    else: 
        # Up
        for i in range(reqIndex + 1, len(activeLine)):
            cumuSec += activeLine[i]["time"]
    return cumuSec

#  timing logic 
def calcTimings(offsetSec, start_time=now):
    
    # service hours
    serviceStart = now.replace(hour=SERVICE_START_HOUR, minute=0, second=0, microsecond=0)
    serviceEnd = now.replace(hour=SERVICE_END_HOUR, minute=0, second=0, microsecond=0)
    
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
        return total_time, "down"
    else: 
        for i in range(end_idx + 1, start_idx + 1):
            total_time += line_data[i]["time"]
        return total_time, "up"

def customTime():
    print("\nSelect Time Option:")
    print("1. Current Time")
    print("2. Custom Time")
    choice = input("Enter Choice (1 or 2): ").strip()
    
    if choice == "2":
        time_str = input("Enter time (HH:MM): ").strip()
        try:
            # custom time, assuming current date
            t = datetime.strptime(time_str, "%H:%M").time()
            now = datetime.now()
            return now.replace(hour=t.hour, minute=t.minute, second=0, microsecond=0)
        except ValueError:
            print("Invalid time format. Using current time.")
            return datetime.now()
    return datetime.now()

# mode selection
def modeSelector():
    mode= input("Enter 1 for Metro Timings, 2 for Trip Planner: ").strip()
    if mode in ["1", "2"]:
        return mode
    else:
        print("Invalid choice. Defaulting to Metro Timings.")
        return "1"

def tripPlanner():
    print("Trip Planner ")
    print("Disclaimer: Transfer time at interchanges are approximated to 4 minutes.\n If source or destination is interchange station, please select lines accordingly.")
    # Get Time
    start_time = customTime()
    # Source
    activeLineS, reqIndexs, sourceLine, _ = stationSelect(ask_direction=False)
    if reqIndexs == -1: return
    sourceStation = activeLineS[reqIndexs]["name"]
    
    # Destination
    activeLineE, reqIndexE, endLine, _ = stationSelect(ask_direction=False)
    if reqIndexE == -1: return
    endStation = activeLineE[reqIndexE]["name"]
    
    # Map line names to data
    linesDict = {
        "Blue": stationBlueMain,
        "Blue Branch": stationBlueBranch,
        "Magenta": stationMagenta
    }

    #Direction for Source Line
    reqStation = endStation 
    
    if sourceLine != endLine:
        if sourceLine == "Blue Branch":
            reqStation = "Yamuna Bank"
        elif sourceLine == "Blue" and endLine == "Blue Branch":
            reqStation = "Yamuna Bank"
        elif (sourceLine == "Blue" and endLine == "Magenta") or (sourceLine == "Magenta" and endLine == "Blue"):
            # Comparing JPW(janakpuri west) vs Botanical
            t_jpw, _ = calcTravelTime(linesDict[sourceLine], sourceStation, "Janak Puri West")
            t_jpw2, _ = calcTravelTime(linesDict[endLine], "Janak Puri West", endStation)
            
            t_bot, _ = calcTravelTime(linesDict[sourceLine], sourceStation, "Botanical Garden")
            t_bot2, _ = calcTravelTime(linesDict[endLine], "Botanical Garden", endStation)
            
            if (t_jpw + t_jpw2) <= (t_bot + t_bot2):
                reqStation = "Janak Puri West"
            else:
                reqStation = "Botanical Garden"
        elif sourceLine == "Magenta" and endLine == "Blue Branch":
            # Magenta -- Blue -- Branch
            t_jpw, _ = calcTravelTime(linesDict["Magenta"], sourceStation, "Janak Puri West")
            t_blue_jpw, _ = calcTravelTime(linesDict["Blue"], "Janak Puri West", "Yamuna Bank")
            
            t_bot, _ = calcTravelTime(linesDict["Magenta"], sourceStation, "Botanical Garden")
            t_blue_bot, _ = calcTravelTime(linesDict["Blue"], "Botanical Garden", "Yamuna Bank")
            
            # Remaining path from Yamuna Bank is same, so just compare to Yamuna Bank
            if (t_jpw + t_blue_jpw) <= (t_bot + t_blue_bot):
                reqStation = "Janak Puri West"
            else:
                reqStation = "Botanical Garden"

    # Get direction to target
    _, dir_str = calcTravelTime(linesDict[sourceLine], sourceStation, reqStation)
    sourceDirection = "1" if dir_str == "Down" else "2"
    
    sourceOffset = calcOffset(activeLineS, reqIndexs, sourceDirection)
    nextMetroTimings = calcTimings(sourceOffset, start_time)

    print("\nJourney Plan")
    print(f"Start from {sourceStation} ({sourceLine})")
    print(f"Next metro at {nextMetroTimings[0]}")

    totalDuration = 0
    
    if sourceLine == endLine:
        duration, _ = calcTravelTime(linesDict[sourceLine], sourceStation, endStation)
        totalDuration = duration
        print(f"Direct trip on {sourceLine} line.")
        
    elif (sourceLine == "Blue" and endLine == "Blue Branch") or (sourceLine == "Blue Branch" and endLine == "Blue"):
        # Transfer at Yamuna Bank
        interchange = "Yamuna Bank"
        t1, _ = calcTravelTime(linesDict[sourceLine], sourceStation, interchange)
        t2, _ = calcTravelTime(linesDict[endLine], interchange, endStation)
        totalDuration = t1 + t2 + TRANSFER_TIME
        print(f"Take {sourceLine} to {interchange}")
        print(f"Change to {endLine} (Wait 4 mins)")
        print(f"Take {endLine} to {endStation}")

    elif (sourceLine == "Blue" and endLine == "Magenta") or (sourceLine == "Magenta" and endLine == "Blue"):
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
            totalDuration = dist_b + TRANSFER_TIME
            
        print(f"Take {sourceLine} to {interchange}")
        print(f"Change to {endLine} (Wait 4 mins)")
        print(f"Take {endLine} to {endStation}")

    elif (sourceLine == "Magenta" and endLine == "Blue Branch") or (sourceLine == "Blue Branch" and endLine == "Magenta"):
        if sourceLine == "Magenta":
            m_station = sourceStation
            b_station = endStation
            m_line = linesDict["Magenta"]
            bb_line = linesDict["Blue Branch"]
            
            t1_a, _ = calcTravelTime(m_line, m_station, "Janak Puri West")
            t2_a, _ = calcTravelTime(linesDict["Blue"], "Janak Puri West", "Yamuna Bank")
            t3_a, _ = calcTravelTime(bb_line, "Yamuna Bank", b_station)
            total_a = t1_a + t2_a + t3_a
            
            t1_b, _ = calcTravelTime(m_line, m_station, "Botanical Garden")
            t2_b, _ = calcTravelTime(linesDict["Blue"], "Botanical Garden", "Yamuna Bank")
            t3_b, _ = calcTravelTime(bb_line, "Yamuna Bank", b_station)
            total_b = t1_b + t2_b + t3_b
            
            if total_a <= total_b:
                int1 = "Janak Puri West"
                totalDuration = total_a + (TRANSFER_TIME * 2)
            else:
                int1 = "Botanical Garden"
                totalDuration = total_b + (TRANSFER_TIME * 2)
            
            print(f"Take Magenta to {int1}")
            print(f"Change to Blue Line (Wait 4 mins)")
            print(f"Take Blue Line to Yamuna Bank")
            print(f"Change to Blue Branch (Wait 4 mins)")
            print(f"Take Blue Branch to {endStation}")
        # Branch to Magenta
        else: 
            b_station = sourceStation
            m_station = endStation
            bb_line = linesDict["Blue Branch"]
            m_line = linesDict["Magenta"]
            
            t1, _ = calcTravelTime(bb_line, b_station, "Yamuna Bank")
            
            t2_a, _ = calcTravelTime(linesDict["Blue"], "Yamuna Bank", "Janak Puri West")
            t3_a, _ = calcTravelTime(m_line, "Janak Puri West", m_station)
            total_a = t1 + t2_a + t3_a
            
            t2_b, _ = calcTravelTime(linesDict["Blue"], "Yamuna Bank", "Botanical Garden")
            t3_b, _ = calcTravelTime(m_line, "Botanical Garden", m_station)
            total_b = t1 + t2_b + t3_b
            
            if total_a <= total_b:
                int2 = "Janak Puri West"
                totalDuration = total_a + (TRANSFER_TIME * 2)
            else:
                int2 = "Botanical Garden"
                totalDuration = total_b + (TRANSFER_TIME * 2)
                
            print(f"Take Blue Branch to Yamuna Bank")
            print(f"Change to Blue Line (Wait 4 mins)")
            print(f"Take Blue Line to {int2}")
            print(f"Change to Magenta Line (Wait 4 mins)")
            print(f"Take Magenta to {endStation}")

    else:
        print("Trip cannot be planned.")

    if nextMetroTimings[0] == "No service available" or nextMetroTimings[0] == "End of Service":
        print(f"Arrive at {endStation}: {nextMetroTimings[0]}")
    else:
        # formatting time
        nm_time = datetime.strptime(nextMetroTimings[0], "%H:%M").time()
        nm_dt = start_time.replace(hour=nm_time.hour, minute=nm_time.minute, second=0, microsecond=0)
        
        arrival_time = nm_dt + timedelta(seconds=totalDuration)
        print(f"Arrive at {endStation} at {arrival_time.strftime('%H:%M')}")
        print(f"Total time: {totalDuration // 60} min {totalDuration % 60} sec")


selected_mode = modeSelector()
if selected_mode == "1":
    activeLine, reqIndex, stationLine, direction = stationSelect()
    if reqIndex != -1:
        stationName = activeLine[reqIndex]["name"]
        stationOffset = calcOffset(activeLine, reqIndex, direction)
        
        print(f"Station: {stationName} on {stationLine} line.")
        # print(f"{stationOffset // 60} min {stationOffset % 60} sec")
        start_time = customTime()
        timings = calcTimings(stationOffset, start_time)
        
        if "Service" in timings[0]:
            print(timings[0])
        else:
            print(f"Next metro at {timings[0]}")
            if len(timings) > 1:
                print("Subsequent metros at " + ", ".join(timings[1:]))
    else:
        print("Station not found.")
else:
    tripPlanner()