# READMEbonus.md — Bonus Fare & Time Features (Detailed)

## 1. Overview
This document describes all bonus features added on top of the base Delhi Metro Simulator. These additions extend the simulator to support real DMRC-style fare computation and flexible time inputs.

---

## 2. Bonus Feature Set

### 2.1 Distance‑Based Fare Calculation
The simulator implements full DMRC fare slabs:

- 0–2 km → ₹11  
- 2–5 km → ₹21  
- 5–12 km → ₹32  
- 12–21 km → ₹43  
- 21–32 km → ₹54  
- Above 32 km → ₹64  

These slabs are implemented in `calculateFare(distance)`.

### 2.2 Automatic Distance Extraction
Distances are pulled directly from **metro_data.txt** instead of hard-coded values.  
The engine uses the `Distance (km)` column to compute:

- Distance between two stations  
- Segment distances for multi-line routes  
- Total journey distance  

### 2.3 Multi‑Segment Distance Handling
For single, double, or direct transfers, each segment contributes its distance to the final cumulative value. Routes using Blue → Magenta → Blue Branch calculate total distance correctly across line boundaries.

### 2.4 Fare Integration in Trip Planner
At the end of `simulateJourney()`, the system computes:

```
Total Fare: Rs. <value>
```

Fare depends **only on total km**, not on time or interchange count.

---

## 3. Time Input Enhancements

### 3.1 Current Time Mode
User chooses *Current Time*, and the system reads from Python’s system clock.

### 3.2 Custom Time Mode
User can enter any HH:MM input.  
Validation includes:

- Format checking  
- Hour/minute range  
- Automatic fallback to current time on invalid input  

### 3.3 Auto‑Shift Before Service Hours
If a user enters a time before 06:00, the simulator auto-adjusts:

```
Start time → 06:00 + station offset
```

This ensures correctness with first‑metro rules.

### 3.4 Unified Time Logic
Both modes feed into the same timing engine, handling:

- First metro  
- Last metro  
- Peak vs off‑peak frequency  
- Dynamic interval selection (4 min / 8 min)

---

## 4. Differences From Main Assignment

The base assignment included:

- Timings logic  
- Route selection  
- Interchange handling  
- Peak/off‑peak logic  

The bonus adds:

1. A complete fare system  
2. Automatic trip distance calculation  
3. Flexible time-selection system  
4. Full integration into journey simulation  

These features were **not** part of the original scope.

---

## 5. Design Choices & Assumptions

### 5.1 Distance = Absolute Station Distance Difference  
Assumes the provided cumulative distances in `metro_data.txt` reflect line‑accurate measurements.

### 5.2 Transfer Distance = 0  
Transfers only add time, not distance, matching real-world fare systems.

### 5.3 No Fare Discounts Implemented  
Smart Card discounts and special rules excluded for simplicity.

### 5.4 Time Input Validation  
Robust checks ensure user inputs are valid, with fallbacks to current time to avoid crashes.

---

## 6. Summary
The bonus feature transforms the metro simulator into a fare-accurate, time-flexible trip calculator. The additions significantly improve realism and completeness while requiring minimal change to the core architecture.

