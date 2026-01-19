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
    - Grid dimensions: 375 segments (horizontal) × 115 levels (vertical)
    - **Basement levels: -5 to -1 (5 basement floors)**
    - **Lobby floor: Level 0**
    - **Main floors: 1 to 109**
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
  - Status: COMPLETE ✓ (UPDATED: Basement levels + Level 0 reserved for lobby)
  - Completed:
    - Created entities/room.py with RoomEntity base class
    - Room overlap detection and validation
    - Created entities/rooms/lobby.py with Lobby class
    - Default 4-segment wide lobby, costs 500/segment
    - **Lobby must be placed on Level 0 only (was previously level 1)**
    - **Lobby segments must be continuously connected (no gaps)**
    - Basement floors rendering (levels -5 to -1) in brown color (139, 90, 43)
    - Room rendering system with borders and labels
    - Room storage and tracking in game
    - Game initializes with basement floors (level 0 reserved for lobby, no default lobby)

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
    - **UPDATED: Grid height now 115 levels (-5 to 109) to support basements**
    - **UPDATED: Lobby placement restriction to Level 0 only**
    - **UPDATED: Metro station restriction to basement levels (-5 to -1)**

## Phase 2.5: Basement Floor Requirements Implementation
- [x] **Basement Floor System** - Support 5 basement levels with restrictions
  - Status: COMPLETE ✓
  - Completed:
    - Updated coordinate system to support negative levels (-5 to -1)
    - Grid height increased from 110 to 115 levels
    - Added GRID_MIN_LEVEL (-5) and GRID_MAX_LEVEL (109) constants
    - Created basement floor entities for levels -5 to -1 with brown color
    - Basement floors initialized in game startup
    - **Basement-only items restriction:**
      - ✓ Metro Station (allowed)
      - ✓ Stairs (allowed)
      - ✓ Escalator (allowed)
      - ✓ Elevator Shaft (allowed, spans multiple levels)
      - ✗ All other items blocked from basement
    - Service modules (housekeeping, security, medical) restricted to Level 0+
    - Level 0 reserved exclusively for Lobby placement
    - **Lobby connectivity validation:**
      - ✓ Lobby segments must be continuously connected (no gaps)
      - ✓ First lobby placement on Level 0 always valid
      - ✓ Subsequent lobby segments must touch existing lobby
    - Placement validator updated with 6 checks (was 4)
    - Ghost room bounds checking updated for negative levels
    - Game initialization updated (basement auto-created, no default lobby)

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
      - **UPDATED: Lobby restricted to Level 0, Metro to basement only**
      - **UPDATED: 6-check validation system (bounds, basement, level, overlaps, surface, connectivity)**
    - Ghost room creation on tool selection
    - Real-time position updates as mouse moves
    - Validation feedback with visual indicators
- [x] **Step 7: The Building Action** - Click to place, fund deduction
  - Status: COMPLETE ✓
  - Completed:
    - Implemented `_place_room()` method for actual room placement
    - Fund validation: checks player has sufficient funds before placing
    - Cost calculation: handles per-segment costs (lobby) and fixed costs
    - Room entity creation: factory pattern for different room types
    - Game state updates: adds room to list, updates validator, deducts funds
    - Placement feedback: console messages showing placement success and remaining funds
    - Clear selection: resets ghost room and selected tool after placement
    - **NEW: Lobby connectivity validation prevents disconnected segments**
    - **NEW: Cost calculation handles variable-width items (lobby: 500/segment)**
    - **NEW: Elevator shaft pricing (shaft + per-car costs)**

## Phase 3.5: Camera & Viewport Improvements
- [x] **Camera System Enhancements** - Proper scrolling and centering
  - Status: COMPLETE ✓
  - Completed:
    - **FIXED: Camera now allows negative Y values** to view basement levels
    - **FIXED: Camera scroll limits now respect grid boundaries correctly**
    - Camera starts centered horizontally on the map
    - Camera starts at basement level (y = GRID_MIN_LEVEL) vertically
    - Level 0 visible near bottom of screen for tower building
    - Smooth scrolling with WASD keys (16px/frame)
    - Proper pixel calculations for grid bounds
    - Basement floors (-5 to -1) fully viewable by scrolling down

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

## Foundation Ready for Phase 4
✅ **Core systems complete:**
- Game window and rendering pipeline
- Grid system with basement and main tower levels
- Room entity system with placement validation
- UI toolbox and status bar
- Building action (click to place, fund deduction)
- Camera system with proper scrolling and centering
- 19 entity types with complete specifications

✅ **What Phase 4 needs:**
- TimeManager: Track in-game days, quarters, and annual cycle
- Revenue system: Collect income from placed buildings
- Maintenance system: Deduct maintenance costs quarterly
- Population management: Track sims in residential/office buildings
- Rating system: Update star rating based on tower quality

---

## Key Implementation Files
| File | Purpose |
|------|---------|
| [main.py](main.py) | Entry point |
| [tower_simulator/game.py](tower_simulator/game.py) | Main game loop, rendering, input handling |
| [tower_simulator/constants.py](tower_simulator/constants.py) | Game data registry (19 entity types) |
| [tower_simulator/world/coordinate.py](tower_simulator/world/coordinate.py) | Coordinate system with basement support |
| [tower_simulator/world/camera.py](tower_simulator/world/camera.py) | Viewport management and scrolling |
| [tower_simulator/entities/room.py](tower_simulator/entities/room.py) | Room base class |
| [tower_simulator/entities/rooms/lobby.py](tower_simulator/entities/rooms/lobby.py) | Lobby entity |
| [tower_simulator/systems/placement_validator.py](tower_simulator/systems/placement_validator.py) | Placement validation rules |
| [tower_simulator/ui/toolbox.py](tower_simulator/ui/toolbox.py) | Tool selection UI |
| [tower_simulator/ui/ghost_room.py](tower_simulator/ui/ghost_room.py) | Building preview |
| [tower_simulator/ui/status_bar.py](tower_simulator/ui/status_bar.py) | HUD display |

---

## Notes & Decisions
- **Python Version**: 3.12.10 (stable with Pygame)
- **Game Engine**: Pygame 2.6.1 (CPU-based, simpler to work with)
- **Target Resolution**: 1280x720
- **Window Title**: Tower Simulator
- **Virtual Environment**: venv312
- **To Run Game**: `venv312\Scripts\python.exe main.py`
- **Coordinate System**: Y-axis inverted (basement at bottom, higher levels at top)
  - Level -5 to -1: Basement floors (brown)
  - Level 0: Lobby floor (empty, player-placed)
  - Level 1 to 109: Main tower floors
- **Initial Funds**: $2,000,000
- **Starting Rating**: 1 Star
- **Starting Population**: 0 Sims
- **Grid Size**: 375 segments (horizontal) × 115 levels (vertical: -5 to 109)
- **Grid Scale**: 8 pixels per segment, 32 pixels per level
- **Basement System**: 
  - 5 basement floors for underground structures
  - Only Metro Station, Stairs, Escalator, Elevator allowed
  - Basement color: Brown RGB(139, 90, 43)
- **Git Configuration**:
  - Remote: `develop` (GitHub: npatel89/test)
  - .gitignore: Excludes __pycache__, *.pyc, venv312, IDE files
  - .pyc files removed from tracking (Jan 18, 2026)
