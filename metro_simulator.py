from datetime import datetime,timedelta

def readSection(filename, start_marker, end_marker):
    stations = []
    in_section = False
    
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()            
            if start_marker in line:
                in_section = True
                continue
            if end_marker in line:
                in_section = False
                break

            if in_section:
                # spliting to get req. data
                if "|" in line and len(line) > 0 and line[0].isalnum():
                    columns = line.split('|')
                    if len(columns) >= 4:
                        s_id = columns[0].strip()
                        stationName = columns[1].strip()
                        
                        # time calc
                        time = columns[3].strip()
                        s_time = 0
                        if ":" in time:
                            parts = time.split(':')
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

stations_blue_main = readSection("metro_data.txt", "BLUE LINE STATIONS", "BLUE LINE BRANCH STATIONS")
stations_blue_branch = readSection("metro_data.txt", "BLUE LINE BRANCH STATIONS", "[END BLUE]")
stations_magenta = readSection("metro_data.txt", "MAGENTA LINE STATIONS", "[END MAGENTA]")


# inputs
def get_user_selection():
    print("\n--- Select Line ---")
    print("1. Blue Line (Dwarka Sec 21 - Noida Elec. City)")
    print("2. Blue Branch (Yamuna Bank - Vaishali)")
    print("3. Magenta Line (Janak Puri West - Botanical Garden)")
    
    while True:
        choice = input("Enter Choice (1-3): ").strip()
        if choice == '1':
            active_line = stations_blue_main
            break
        elif choice == '2':
            active_line = stations_blue_branch
            break
        elif choice == '3':
            active_line = stations_magenta
            break
        print("Invalid choice. Try again.")

    start_station = active_line[0]['name']
    end_station = active_line[-1]['name']
    
    print(f"\n--- Select Direction ---")
    print(f"1. Down: {start_station} -> {end_station}")
    print(f"2. Up:   {end_station} -> {start_station}")
    
    direction = input("Enter Direction (1 or 2): ").strip()
    
    print(f"\n--- Stations on this Line ---")
    for s in active_line:
        print(f"{s['id']}: {s['name']}")
    
    target_id = input("Enter your Station ID (e.g., 1b): ").strip().lower()
    # Find the index of the selected station
    target_index = -1
    for idx, s in enumerate(active_line):
        if s['id'].lower() == target_id:
            target_index = idx
            break
    if target_index == -1:
        return None, None
    # Time Offset
    cumuSec = 0
    # Down
    if direction == '1':  
        # Add time of all previous stations up to current
        for i in range(1, target_index + 1):
            cumuSec += active_line[i]['time']
    else: 
        # Up
        for i in range(target_index + 1, len(active_line)):
            cumuSec += active_line[i]['time']
            
    return active_line[target_index]['name'], cumuSec

# --- 3. Timing Logic ---

def calculate_timings(offsetSec):
    now = datetime.now()
    
    # service hours
    service_start = now.replace(hour=6, minute=0, second=0, microsecond=0)
    service_end = now.replace(hour=23, minute=0, second=0, microsecond=0)
    
    # offset adjusting
    first_arrival = service_start + timedelta(seconds=offsetSec)
    last_arrival = service_end + timedelta(seconds=offsetSec)
    
    if now > last_arrival:
        return ["No service available"]
        
    if now < first_arrival:
        next_metro = first_arrival
    else:
        # freq for peak and off peak hrs
        hour = now.hour
        if (8 <= hour < 10) or (17 <= hour < 19):
            freq = 4
        else:
            freq = 8
            
        # Calc next metro
        time_diff = now - first_arrival
        minutes_passed = time_diff.total_seconds() / 60
        cycles = int(minutes_passed // freq)
        minutes_to_add = (cycles + 1) * freq
        
        next_metro = first_arrival + timedelta(minutes=minutes_to_add)

    # Generate next 3 metros
    timings = []
    for _ in range(3):
        if next_metro > last_arrival:
            timings.append("End of Service")
            break
        timings.append(next_metro.strftime("%H:%M"))
        
        # Advance to next train
        h = next_metro.hour
        next_freq = 4 if (8 <= h < 10) or (17 <= h < 19) else 8
        next_metro += timedelta(minutes=next_freq)
        
    return timings

stationName, stationOffset = get_user_selection()

if stationName:
    print(f"\nStation: {stationName}")
    print(f"Travel time from Line Origin: {stationOffset // 60} min {stationOffset % 60} sec")
    
    timings = calculate_timings(stationOffset)
    if "Service" in timings[0]:
        print(timings[0])
    else:
        print(f"Next metro at {timings[0]}")
        if len(timings) > 1:
            print(f"Subsequent metros at {', '.join(timings[1:])}")
else:
    print("Station not found.")