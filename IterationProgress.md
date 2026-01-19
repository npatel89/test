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
- [x] **Step 2: The 375-Segment Grid** - Coordinate system, WorldMap class, camera controls
  - Status: COMPLETE ✓
  - Completed:
    - Created world/coordinate.py with Coordinate and Grid utilities
    - Grid dimensions: 375 segments (horizontal) × 110 levels (vertical)
    - Pixel scaling: 8 pixels per segment, 32 pixels per level
    - Created world/world_map.py with WorldMap class
    - Room placement, removal, and tracking system
    - Created world/camera.py with Camera system
    - WASD scrolling implemented (W=up, A=left, S=down, D=right)
    - Screen-to-world coordinate conversion
    - Grid overlay rendering with subtle gradient
    - HUD showing camera position and grid info
    - Grid toggle with G key

- [x] **Step 3: Empty Ground & Lobby B1** - Ground rendering, auto-lobby, grid overlay, construction mode
  - Status: COMPLETE ✓
  - Completed:
    - Created entities/room.py with RoomEntity base class
    - Room overlap detection and validation
    - Created entities/rooms/lobby.py with Lobby class
    - Default 4-segment wide lobby, costs 500/segment
    - Lobby auto-placed at level 1 (center of grid)
    - Ground rendering (brown rectangle at level 0)
    - Room rendering system with borders and labels
    - Room storage and tracking in game
    - Game initializes with default ground and lobby

## Phase 2: Entity Data & Registry
- [x] **Step 4: The Static Data Registry** - constants.py with ENTITY_DATA
  - Status: COMPLETE ✓
  - Completed:
    - Created tower_simulator/constants.py with comprehensive ENTITY_DATA registry
    - 19 entity types defined (Condo, Office, Hotel, FastFood, Restaurant, Cinema, etc.)
    - Complete facility specifications: cost, width, capacity, income types, maintenance
    - Game parameters: initial funds ($2M), grid size, population targets
    - Work schedules: office hours, lunch times, condo sales windows, hotel check times
    - Elevator dispatch parameters: SCAN algorithm, shaft/car limits
    - Stress and satisfaction thresholds
    - Full documentation and notes on game mechanics
    - All data matches TechnicalDoc specifications

## Phase 3: UI & Construction Engine
- [x] **Step 5: The Tool Window (HUD)** - Toolbox and World Details bar
  - Status: COMPLETE ✓
  - Completed:
    - Created ui/button.py with Button class for UI elements
    - Created ui/toolbox.py with Toolbox panel
    - Toolbox displays 4 tools: Office, Condo, Lobby, Elevator
    - Tools have distinct colors matching their entity type
    - Selected tool is highlighted with yellow border
    - Created ui/status_bar.py with StatusBar
    - Status bar shows: Funds, Population, Star Rating, Current Time
    - Status bar positioned at top of screen
    - Toolbox positioned on left side
    - Mouse click handling for tool selection
    - UI integrated into game rendering pipeline
- [x] **Step 6: Placement & Validation Logic** - Ghost room, can_place() function
  - Status: COMPLETE ✓
  - Completed:
    - Created ui/ghost_room.py with GhostRoom class
    - Ghost room follows mouse cursor in world coordinates
    - Grid snapping (8-pixel segments, 32-pixel levels)
    - Validation indicators: green border (valid), red border (invalid)
    - Created systems/placement_validator.py with PlacementValidator
    - Placement rules implemented:
      - Offices/Condos cannot be placed below level 1
      - Rooms snap to grid automatically
      - No room overlaps allowed
      - Rooms must be placed on valid surfaces (ground or other rooms)
      - Special rules for Lobby (level 1 only), Cathedral (level 100), Metro (B1-B3)
    - Ghost room creation on tool selection
    - Real-time position updates as mouse moves
    - Validation feedback with visual indicators
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
- **Coordinate System**: Y-axis inverted (ground at bottom, higher levels at top)
- **Initial Funds**: $2,000,000
- **Starting Rating**: 1 Star
- **Starting Population**: 0 Sims
