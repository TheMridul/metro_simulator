from datetime import datetime
current_datetime = datetime.now()

# Frequency:
#   Off-peak hours: every 8 minutes
#   Peak hours (8–10 AM and 5–7 PM): every 4 minutes

def servicehours(start_hr=6, start_min=0, end_hr=23, end_min=0):
    
    now = datetime.now()
    start_time = now.replace(hour=start_hr, minute=start_min, second=0, microsecond=0)
    end_time = now.replace(hour=end_hr,minute=end_min)

    if now > start_time and now < end_time :
        return True
    return False

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

sourceLine = 0
count = 0
while sourceLine != "Blue" and sourceLine != "Magenta": 
    if count==0:
        count=1
        sourceLine = input("Enter the line ur on (Blue or Magenta): ")
    elif count!=0:
        sourceLine = input("Enter valid line (Blue or Magenta): ")
if sourceLine == "Blue" :
    for stations in stationsBlue:
        print(stations)
if sourceLine== "Magenta" :
    for stations in stationsMagenta:
        print(stations)

sourceStation= input("Enter the station ur on using ID: ")

# modeSelector= input("Enter Mode, \n 'A' for Metro Timings, \n 'B' for Trip Plannar: ")