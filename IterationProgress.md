# Tower Simulator - Iteration Progress

## Phase 1: Foundation & The Spatial Grid
- [x] **Step 1: Environment & Skeleton** - Environment setup, basic window, MyGame class
  - Status: COMPLETE ✓
  - Completed:
    - Python 3.14.2 initially verified, then downgraded to Python 3.12.10 (stable with Pygame)
    - Virtual environment created (venv312)
    - Project directory structure initialized
    - pygame==2.6.1 successfully installed
    - main.py entry point created
    - game.py with TowerSimulatorGame class created
    - Hello World window displays with 1280x720 resolution at 60 FPS
    - Window can be closed with ESC key
- [ ] **Step 2: The 375-Segment Grid** - Coordinate system, WorldMap class, camera controls
  - Status: NOT STARTED
- [ ] **Step 3: Empty Ground & Lobby B1** - Ground rendering, auto-lobby, grid overlay, construction mode
  - Status: NOT STARTED

## Phase 2: Entity Data & Registry
- [ ] **Step 4: The Static Data Registry** - constants.py with ENTITY_DATA
  - Status: NOT STARTED

## Phase 3: UI & Construction Engine
- [ ] **Step 5: The Tool Window (HUD)** - Toolbox and World Details bar
  - Status: NOT STARTED
- [ ] **Step 6: Placement & Validation Logic** - Ghost room, can_place() function
  - Status: NOT STARTED
- [ ] **Step 7: The Building Action** - Click to place, fund deduction
  - Status: NOT STARTED

## Phase 4: Time & Economics Simulation
- [ ] **Step 8: The 12-Day Annual Clock** - TimeManager class
  - Status: NOT STARTED
- [ ] **Step 9: Revenue & Maintenance Triggers** - Financial loop
  - Status: NOT STARTED

## Phase 5: The Elevator & NPC Engine (Advanced)
- [ ] **Step 10: The Sim Behavioral State Machine** - Sim class with stress modeling
  - Status: NOT STARTED
- [ ] **Step 11: SCAN Elevator Dispatching** - ElevatorShaft and Car logic
  - Status: NOT STARTED
- [ ] **Step 12: Pathfinding (Stair/Escalator Logic)** - Graph-based pathfinder
  - Status: NOT STARTED

---

## Notes & Decisions
- **Python Version**: 3.12.10 (stable with Pygame)
- **Game Engine**: Pygame 2.6.1 (CPU-based, simpler to work with)
- **Target Resolution**: 1280x720
- **Window Title**: Tower Simulator
- **Virtual Environment**: venv312
- **To Run Game**: `c:\dev\v2\venv312\Scripts\python.exe main.py`
