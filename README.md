# Delhi Metro Simulator

A command-line simulation of Delhi Metro timings and route planning.

## Overview
A CLI tool that calculates next-metro timings and end-to-end trip planning across Blue, Blue Branch, and Magenta lines.

## Features
- **Next Metro Prediction**: Computes next metro arrival times for any station and direction.
- **Trip Planning**: Generates complete trip plans with optimized interchange routing.
- **Smart Routing**: Detects when source/destination exist on alternate lines and avoids unnecessary transfers.
- **Service Rules**: Handles operating windows and frequency variations (peak: 4 min, off-peak: 8 min).
- **Custom Time Input**: Accepts user-defined start times.
- **Auto-Correction**: Requests before 06:00 automatically return first metro at 06:00 + offset.
- **Menu-Driven Interface**: User-friendly CLI prompts for seamless interaction.
- **Custom time handling**: Users can specify custom start times for planning.

## Service Rules
- **Operating Hours**: 06:00 to 23:00.
- **First Metro**: Starts at 06:00 from both terminals of all lines.
- **Last Metro**: Departs at 23:00 from both terminals.
- **Frequencies**:
  - Peak hours (08:00–10:00, 17:00–19:00): 4 minutes.
  - Normal hours (06:00–23:00 except peak): 8 minutes.
- **Interchange**: Wait time depends on availability of next train on destination line.

## Fare Calculation (Bonus Feature)

## Data Source & Meta Data
Station datasets and timing data are loaded from `metro_data.txt`.
The file uses pipe-separated rows inside named line sections. Expected columns:

`ID | Station Name | Distance (km) | Travel Time from Previous (min:ss) | Interchange Line(s)`

Keep station names consistent across sections for interchanges; `Travel Time from Previous` must use `MM:SS` format.


## Internal Architecture
- **Station Parsing**: Loads data from `metro_data.txt`.
- **Offset Calculation**: Computes cumulative time from line origin based on distance (assuming 2 min/km).
- **Frequency Engine**: Applies peak/off-peak logic to determine arrival times.
- **Trip Planner**: Supports direct routes, single interchanges, and double interchanges.

## Station ID Format
- **Blue Line**: IDs end with 'b' (e.g., `1b` for Noida City Centre, `14b` for Rajiv Chowk).
- **Blue Branch**: IDs end with 'bb' (e.g., `1bb` for Vaishali).
- **Magenta Line**: IDs end with 'm' (e.g., `2m` for Janak Puri West).

## Usage
Run the script using Python:
```bash
python metro_simulator.py
```

### Step-by-Step Guide
1. **Select Mode**:
   - Enter `1` for **Metro Timings** (Next arrival at a specific station).
   - Enter `2` for **Trip Planner** (Route between two stations).

2. **Select Line**:
   - Choose from Blue Line (`1`), Blue Branch (`2`), or Magenta Line (`3`).

3. **Select Station**:
   - Enter the **Station ID** (e.g., `1b`, `14b`, `1m`) as listed on the screen.

4. **Select Direction** (Timings Mode only):
   - Choose `1` (Down) or `2` (Up) based on the displayed terminal stations.

5. **Select Time**:
   - Choose `1` for **Current Time**.
   - Choose `2` to enter a **Custom Time** (format `HH:MM`).

## Station ID Format
- Blue Line: IDs end with 'b' (e.g., `1b` for Noida City Centre, `14b` for Rajiv Chowk, `42b` for Dwarka Sector 21)
- Blue Branch: IDs end with 'bb' (e.g., `1bb` for Vaishali, `4bb` for Kaushambi)
- Magenta Line: IDs end with 'm' (e.g., `2m` for Janak Puri West, `26m` for Botanical Garden)

## Example Output
```
Journey Plan
Start Time: 11:15
Next metro from Dwarka Sector 21: 11:20
Board Blue at Dwarka Sector 21: 11:20
Arrive Dwarka Sector 10: 11:27

Total travel time: 12 min 23 sec
Total Fare: Rs. 20
```

## File Layout
```
metro_simulator.py
metro_data.txt
README.md
```

## Assumptions & Notes
- Travel times are cumulative seconds stored in `metro_data.txt` (Travel Time from Previous column).
- Interchange wait time is variable, determined by the next train's departure time on the destination line.
- Service runs 06:00–23:00; requests before 06:00 automatically use 06:00 as the start time.
- Peak-hour frequency (4 min) applies during 08:00–10:00 and 17:00–19:00; 8 min otherwise.
- The trip planner detects when source or destination stations exist on multiple lines and optimizes routing to avoid unnecessary transfers.
- Station names are case-sensitive; keep them consistent across sections in `metro_data.txt`.
