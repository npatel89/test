# Tower Simulator - Test Cases & Coverage

## Overview
This document outlines all test cases, edge cases, and testing strategy for Tower Simulator.

---

## Phase 1: Camera System Tests
**File:** `tests/test_camera.py`

### ✅ Implemented Tests

#### TestCameraInitialization
1. **test_camera_starts_centered_horizontally**
   - Verifies: Camera X position = (grid_width - screen_width) / 2
   - Expected: X = 860
   - Status: ✅ PASS

2. **test_camera_starts_at_basement_level**
   - Verifies: Camera Y position = GRID_MIN_LEVEL * PIXELS_PER_LEVEL
   - Expected: Y = -160 (Level -5)
   - Status: ✅ PASS

3. **test_camera_bounds_are_correct**
   - Verifies: Grid bounds are properly calculated
   - Expected: grid_width=3000, grid_min_y=-160, grid_max_y=3488
   - Status: ✅ PASS

4. **test_camera_can_view_level_zero**
   - Verifies: Lobby floor (Level 0) is visible on screen in lower half
   - Expected: screen_y between 360-720
   - Status: ✅ PASS

#### TestCameraScrolling
5. **test_camera_respects_left_boundary**
   - Verifies: Camera clamps at X=0 when scrolling left
   - Status: ✅ PASS

6. **test_camera_respects_bottom_boundary**
   - Verifies: Camera clamps at max height when scrolling down from basement
   - Status: ✅ PASS

---

## Phase 2: Edge Cases & TODO Tests

### Camera System - Additional Edge Cases
- [ ] **Scroll right boundary** - Camera should not scroll past grid_width
  - Test: Scroll right (D key) 1000x from starting position, should clamp at max_x
  - Expected: x = grid_width - screen_width = 1720

- [ ] **Scroll up boundary** - Camera should not scroll past top level
  - Test: Scroll up (W key) 10000x, should clamp at grid_max_y - screen_height
  - Expected: y = 3488 - 720 = 2768

- [ ] **Coordinate conversion accuracy**
  - Test: world_to_screen() and screen_to_world() are inverse operations
  - For random points, screen_to_world(world_to_screen(x,y)) == (x,y)

- [ ] **World to screen at screen corners**
  - Top-left corner visible: basement level at top, leftmost segment
  - Bottom-right corner visible: levels at bottom, rightmost segment
  - Test coordinate conversion at extremes

- [ ] **Camera movement from static position**
  - Hold W key: camera should move smoothly upward
  - Hold S key: camera should move smoothly downward
  - Hold A key: camera should move smoothly leftward
  - Hold D key: camera should move smoothly rightward

### Placement Validator System - Edge Cases
- [ ] **Basement only items validation**
  - Metro Station: only levels -5 to -1
  - Stairs, Escalator, Elevator Shaft: only in basement
  - Test: Place on each level, should fail on non-basement levels

- [ ] **Lobby connectivity validation**
  - Lobby: only Level 0
  - Test: Can place Lobby at Level 0
  - Test: Cannot place Lobby at other levels
  - Test: Lobby must be continuously connected (no floating segments)

- [ ] **Level restrictions across all 19 entity types**
  - For each ENTITY_DATA, test placement at min_level and max_level
  - Test placement above max_level (should fail)
  - Test placement below min_level (should fail)

- [ ] **Grid boundary violations**
  - Segment < 0 or >= 375 (should fail)
  - Level < -5 or > 109 (should fail)
  - Multi-segment rooms crossing boundaries

- [ ] **Overlap detection**
  - Place room A
  - Try to place room B at same location (should fail)
  - Try to place room B overlapping partially (should fail)
  - Place room B adjacent to A (should succeed)

- [ ] **Surface placement validation**
  - Cannot place on air (empty level)
  - Can only place on ground (Level -6 below) or other rooms
  - Test: Place room at Level 1, place room at Level 2 on top

- [ ] **Multi-segment rooms**
  - Room spanning 5 segments placement
  - Room crossing grid boundary (segment 371-376)
  - Overlaps with other rooms at different segments

### Game Logic - Building Placement Edge Cases
- [ ] **Fund validation**
  - Place room with exact funds (should succeed)
  - Place room with insufficient funds (should fail)
  - Place expensive room with limited funds (should fail)
  - Multiple placements depleting funds progressively

- [ ] **Room cost calculation**
  - Single-segment items (fixed cost)
  - Multi-segment items (cost * segment count)
  - Verify final funds = initial - cost

- [ ] **Entity creation validation**
  - Room entity has correct type
  - Room entity is at correct coordinate
  - Room entity appears in game.rooms list
  - Room entity renders correctly

- [ ] **Game state consistency after placement**
  - Validator updated with new room
  - Ghost room preview updated
  - Status bar shows correct remaining funds
  - Console logs placement correctly

### Coordinate System - Edge Cases
- [ ] **Coordinate validation**
  - Valid: segment 0-374, level -5 to 109
  - Invalid: negative segment
  - Invalid: segment >= 375
  - Invalid: level < -5
  - Invalid: level > 109

- [ ] **Pixel conversion accuracy**
  - Coordinate(0, 0) → (0, 0) pixels
  - Coordinate(375, 109) → (3000, 3488) pixels
  - Coordinate(1, 1) → (8, 32) pixels
  - Basement Coordinate(0, -5) → (0, -160) pixels

- [ ] **Basement floor coloring**
  - All basement floors (levels -5 to -1) have brown color
  - Level 0 and above can have other colors
  - Basement rooms render with correct color

### UI System - Edge Cases
- [ ] **Ghost room preview**
  - Follows mouse cursor correctly
  - Shows green when placement is valid
  - Shows red when placement is invalid
  - Updates based on current selected tool

- [ ] **Toolbox selection**
  - Can select between 4 tools (Office, Condo, Lobby, Elevator)
  - Selected tool highlighted in yellow
  - Ghost room matches selected tool

- [ ] **Status bar updates**
  - Funds decrease after placing room
  - Funds update on screen immediately
  - Population updates after placement
  - Rating updates based on placements

### Game Rendering - Edge Cases
- [ ] **Room rendering at all levels**
  - Basement rooms visible
  - Level 0-50 rooms visible
  - Top-level rooms visible
  - Rooms at camera boundaries render correctly

- [ ] **Multi-segment room rendering**
  - Room label renders at correct position
  - Room spans correct number of segments visually
  - Multi-segment rooms don't clip incorrectly

- [ ] **Visual glitches**
  - No flickering when scrolling
  - No rendering artifacts at screen edges
  - Basement color (brown) renders correctly
  - Level 0 (green) renders correctly

---

## Test Execution Strategy

### Quick Test Run (All Unit Tests)
```powershell
.\venv312\Scripts\python.exe -m unittest discover tests/ -v
```

### Run Specific Test File
```powershell
.\venv312\Scripts\python.exe -m unittest tests.test_camera -v
```

### Run Specific Test Class
```powershell
.\venv312\Scripts\python.exe -m unittest tests.test_camera.TestCameraInitialization -v
```

### Run Specific Test Method
```powershell
.\venv312\Scripts\python.exe -m unittest tests.test_camera.TestCameraInitialization.test_camera_starts_centered_horizontally -v
```

---

## Coverage Tracking

### Phase 1: Foundation (Steps 1-3)
- ✅ Coordinate System: Basic validation
- ✅ Grid System: Dimensions correct
- ⏳ Basement System: Rendering verified manually

### Phase 2: Entity Registry (Step 4)
- ⏳ Constants.py: 19 entity types loaded
- ⏳ Entity placement rules: Not yet tested

### Phase 3: UI & Construction (Steps 5-7)
- ✅ Camera: Initialization and boundaries
- ⏳ Camera: Scrolling mechanics
- ⏳ Placement Validator: All 6 checks
- ⏳ Building Action: Fund deduction
- ⏳ Ghost Room: Visual feedback

### Phase 4: Time & Economics (Steps 8-9)
- ⏳ TimeManager: Annual cycle
- ⏳ Revenue: Income collection
- ⏳ Maintenance: Cost deduction

### Phase 5: Elevator & NPC (Steps 10-12)
- ⏳ Elevator Logic: Dispatch algorithm
- ⏳ NPC Pathing: Stairs/escalators
- ⏳ NPC Behavior: State machine

---

## Known Issues Found by Tests
1. ⚠️ Camera world_to_screen conversion initially incorrect - FIXED
2. ⚠️ Level 0 position on screen - Test expectations updated
3. 🔴 **CRITICAL: Constants.py Missing Data** 
   - 18/19 entities missing `placement_level_min` and `placement_level_max`
   - 1/19 entities (elevator_shaft) missing `cost`
   - Basement items named with underscores (metro_station, elevator_shaft) not matching hardcoded strings (Metro, Elevator Shaft)
4. 🔴 **PlacementValidator._is_within_bounds() broken for negative levels**
   - Checks `0 <= coordinate.level` but levels go to -5
   - Causes valid basement placements to fail

---

## Next Priority Tests
1. **Placement Validator** - Test all 6 validation checks
2. **Building Action** - Test fund deduction and room creation
3. **Entity Types** - Test placement rules for each of 19 types
4. **Multi-segment Rooms** - Test complex placement scenarios
5. **Game State Consistency** - Verify game updates correctly after each action

