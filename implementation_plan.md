# Implementation Plan for Metro Simulator Fixes

## Goal
Apply the recommended fixes identified in the bug report:
1. Fix UnicodeEncodeError in `test_direction_logic.py`.
2. Correct service‑end time calculation in `calcTimings`.
3. Unify direction representation – make `calcTravelTime` return numeric codes (`"1"` for Down, `"2"` for Up) and update all callers.
4. Improve interchange selection logic to avoid choosing an interchange that lies behind the current station.
5. Remove duplicate import and `readSection` definitions in `metro_simulator.py`.
6. Adjust any dependent code (e.g., `tripPlanner`, tests) to use the new direction codes.

## Files to Modify
- `metro_simulator.py`
- `test_direction_logic.py`

## Detailed Changes
### metro_simulator.py
- Delete the duplicated block of imports and `readSection` (lines 47‑53).
- In `calcTimings`, change `lastArrival = serviceEnd + timedelta(seconds=offsetSec)` to `lastArrival = serviceEnd - timedelta(seconds=offsetSec)`.
- Update `calcTravelTime` to return numeric direction codes:
  ```python
  if start_idx < end_idx:
      return total_time, "1"  # Down
  else:
      return total_time, "2"  # Up
  ```
- Remove the translation `sourceDirection = "1" if dir_str == "Down" else "2"` and use `sourceDirection = dir_str` directly.
- Refactor the interchange selection block (around lines 236‑260) to filter candidates based on travel direction and the index of the current station. Only consider interchanges that are ahead when traveling Down (`"1"`) or behind when traveling Up (`"2"`). If no viable candidate remains, fall back to the original shortest‑time logic.
- Ensure any other references to direction strings (`"Down"`/`"Up"`) are updated to use the numeric codes.

### test_direction_logic.py
- Replace the emoji in the print statement on line 106:
  ```python
  print("\nTest 1: Same Line Trips")
  ```
- Adjust any assertions that rely on the old string directions; they already compare numeric codes after the change, so no further modifications are needed.

## Verification Plan
1. Run `test_direction_logic.py` – it should now pass without Unicode errors.
2. Run `test_offset_fix.py` – should still pass.
3. Run `test_interchange_bug.py` – output should indicate that the interchange selection no longer picks a backward interchange.
4. Manually execute `metro_simulator.py` and request a trip near the service end (e.g., 22:50) to verify that the last arrival is correctly handled.
5. Inspect the console output for direction codes to ensure they are numeric.

## Risks & Mitigations
- Changing `calcTravelTime` return values may break any external scripts that expect the old strings. Mitigation: all internal callers are updated; the repository is self‑contained.
- Interchange selection logic becomes more complex; we keep the original shortest‑time fallback as a safety net.
- Removing duplicate code must be done carefully to keep one valid definition.

**User Review Required**: Please confirm the plan or suggest adjustments before we proceed with the implementation.
