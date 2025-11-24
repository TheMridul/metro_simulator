# Bug Report for Metro Simulator Assignment

## Summary
This report documents the functional issues discovered in the **metro_simulator** project. The issues were identified by running the provided unit tests and manual inspection of the code base.

## Environment
- **OS**: Windows (user's system)
- **Python version**: 3.14 (as inferred from the environment path `C:\Python314`)
- **Project files**: `metro_simulator.py`, `metro_data.txt`, and several test scripts.

## Test Results
| Test Script | Status | Notes |
|-------------|--------|-------|
| `test_direction_logic.py` | **Failed** | UnicodeEncodeError caused by an emoji (`\U0001f4cd`) in a `print` statement. The test aborts before exercising the logic.
| `test_offset_fix.py` | **Passed** | Verifies that offset calculations work for a typical trip.
| `test_interchange_bug.py` | **Passed (logic check)** | The script prints a summary indicating that the current interchange selection logic can select the wrong interchange in certain scenarios. No assertion failure, but the output highlights a potential bug.

## Identified Bugs
1. **Unicode handling in test output**
   - **Location**: `test_direction_logic.py` (line 106).
   - **Issue**: `print("\n\U0001f4cd Test 1: Same Line Trips")` raises `UnicodeEncodeError` on Windows default code page (cp1252).
   - **Impact**: The test suite aborts, hiding potential failures in direction logic.

2. **Service‑end time calculation**
   - **Location**: `metro_simulator.py` – function `calcTimings` (lines 124‑127).
   - **Issue**: `lastArrival = serviceEnd + timedelta(seconds=offsetSec)` assumes the last metro arrives at the *service end* time plus the offset. This incorrectly pushes the last possible arrival beyond the actual service window (23:00). The correct calculation should subtract the offset: `lastArrival = serviceEnd - timedelta(seconds=offsetSec)`.
   - **Impact**: Users requesting trips near the end of service may receive a "No service available" message even though a metro could still be caught.

3. **Direction string mismatch**
   - **Location**: `calcTravelTime` returns direction strings `'Down'` and `'Up'`, while other parts of the code (e.g., `stationSelect` and `calcOffset`) expect `'1'` for Down and `'2'` for Up.
   - **Issue**: The mismatch forces callers to translate the direction manually (`sourceDirection = "1" if dir_str == "Down" else "2"`). This translation is error‑prone and was the source of a previously reported bug where the wrong direction was used for offset calculation.
   - **Impact**: Inconsistent direction handling can lead to incorrect offset computation and wrong next‑metro timings.

4. **Interchange selection logic can choose a sub‑optimal interchange**
   - **Location**: `tripPlanner` (lines around 236‑260).
   - **Issue**: The algorithm selects the interchange based on the *shortest total travel time* but does not consider the current position relative to the interchange. In scenarios where the traveler is already past the optimal interchange (e.g., starting at Botanical Garden and heading towards Janak Puri West), the logic may still select Botanical Garden as the interchange, resulting in a backward move.
   - **Impact**: Generates inefficient routes and confusing user instructions.

## Root Cause Analysis
- **Unicode error** stems from using an emoji literal in a `print` statement without ensuring the console encoding supports it. Windows consoles default to `cp1252`, which cannot encode many Unicode characters.
- **Service‑end calculation** incorrectly adds the offset to the service end time. Offsets represent travel time *from* the start of service to the target station, so they must be subtracted when determining the latest departure that still reaches the destination before service ends.
- **Direction mismatch** arises from mixing two representations (`'Down'/'Up'` vs `'1'/'2'`). The original design used numeric codes, but later refactoring introduced string literals without updating all callers.
- **Interchange logic** does not account for the direction of travel relative to the interchange. It only compares total travel times, ignoring whether the chosen interchange lies ahead of the current station.

## Recommendations
1. **Fix Unicode in tests**
   - Replace the emoji with a plain ASCII marker or use `print(u"\U0001f4cd Test 1…")` after setting `sys.stdout.reconfigure(encoding='utf-8')`.
   - Alternatively, guard the print with a try/except to ignore encoding errors.
2. **Correct `lastArrival` calculation**
   ```python
   # In calcTimings
   lastArrival = serviceEnd - timedelta(seconds=offsetSec)
   ```
   - Add unit tests that request a trip close to 23:00 to verify the fix.
3. **Unify direction representation**
   - Define constants, e.g., `DIR_DOWN = "1"`, `DIR_UP = "2"` and have `calcTravelTime` return these codes directly.
   - Update all callers to use the constants.
4. **Improve interchange selection**
   - Before comparing total travel times, check the relative index of the current station and each candidate interchange on the source line. Discard any interchange that lies *behind* the current position when traveling forward, and vice‑versa.
   - Add test cases covering:
     * Starting after both interchanges.
     * Starting exactly at an interchange.
     * Traveling in the opposite direction.
5. **Add regression tests**
   - Create a dedicated test suite for service‑end edge cases and direction handling.
   - Include tests for the new interchange selection algorithm.

## Conclusion
The metro simulator functions correctly for many typical scenarios, but the identified bugs affect edge‑case reliability and user experience. Implementing the recommended fixes will make the application robust, especially for trips near service boundaries and for routes requiring interchanges.

*Prepared by Antigravity – AI coding assistant*
