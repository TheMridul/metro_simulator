from datetime import datetime,timedelta
now = datetime.now()
timeNow=now.strftime("%H:%M")

time6AM=now.replace(hour=6,minute=0,second=0,microsecond=0)
time8AM=now.replace(hour=8,minute=0,microsecond=0,second=0)
time10AM=now.replace(hour=10,minute=0,microsecond=0,second=0)
time5PM=now.replace(hour=17,minute=0,microsecond=0,second=0)
time7PM=now.replace(hour=19,minute=0,microsecond=0,second=0)
time11PM=now.replace(hour=23,minute=0,microsecond=0,second=0)

def read_section(filename, start_marker, end_marker):
    stations=[]
    inSection = False 
    
    with open(filename, 'r') as file:
        for line in file:
            if start_marker in line:
                inSection = True
            
            if end_marker in line:
                inSection = False
                break 
            
            if inSection:
                colunms= line.split('|') 
                if len(colunms)>1:
                    target_part = colunms[0] + "|" + colunms[1]
                    stations.append(target_part)
    return stations

stationsBlue= read_section("metro_data.txt", "BLUE LINE STATIONS", "[END BLUE]")
stationsMagenta= read_section("metro_data.txt", "MAGENTA LINE STATIONS", "[END MAGENTA]")

def stationSelector():
    valid_lines = ["blue", "magenta"]
    while True:
        line = input("Enter the line (Blue or Magenta): ").strip().lower()
        if line in valid_lines:
            break
        print("Invalid line. Please enter 'Blue' or 'Magenta'.")
    if line.lower() == "blue":
        for station in stationsBlue:
            print(station)
    if line.lower() == "magenta":
        for station in stationsMagenta:
            print(station)
    station = input("Enter Station using Ids:")
    return station

def metroTimings(now):
    tempTimings = []
    timings=[]
    if time6AM<=now<time8AM:
        time = time6AM
        while time < time8AM:
            tempTimings.append(time)
            time += timedelta(minutes=8)
        for time in tempTimings:
            if time>=now:
                timings.append(time)
        finalTimings = [t.strftime("%H:%M") for t in timings]
        return finalTimings
    
    elif time8AM<=now<time10AM:
        time = time8AM
        while time < time10AM:
            tempTimings.append(time)
            time += timedelta(minutes=4)
        for time in tempTimings:
            if time>=now:
                timings.append(time)
        finalTimings = [t.strftime("%H:%M") for t in timings]
        return finalTimings
    
    elif time10AM<=now<time5PM:
        if time10AM<=now<=time5PM:
            time = time6AM
        while time < time5PM:
            tempTimings.append(time)
            time += timedelta(minutes=8)
        for time in tempTimings:
            if time>=now:
                timings.append(time)
        finalTimings = [t.strftime("%H:%M") for t in timings]
        return finalTimings
    
    elif time5PM<=now<time7PM:
        if time5PM<=now<=time7PM:
            time = time5PM
        while time < time7PM:
            tempTimings.append(time)
            time += timedelta(minutes=4)
        for time in tempTimings:
            if time >= now:
                timings.append(time)
        finalTimings = [t.strftime("%H:%M") for t in timings]
        return finalTimings
    
    elif time5PM<=now<time7PM:
        if time5PM<=now<=time7PM:
            time = time5PM
        while time < time7PM:
            tempTimings.append(time)
            time += timedelta(minutes=4)
        for time in tempTimings:
            if time>=now:
                timings.append(time)
        finalTimings = [t.strftime("%H:%M") for t in timings]
        return finalTimings
    else:
        return "No service available"


def modeSelector(now,sourceStation):
    mode= input("Enter Mode, \n 'A' for Metro Timings, \n 'B' for Trip Plannar:")
    if mode.lower()=="a":
        return metroTimings(now)
    elif mode.lower() == "b":
        return "under development"

sourceStation= stationSelector()
print(modeSelector(now,sourceStation))