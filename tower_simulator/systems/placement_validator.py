"""
Placement validation logic for building placement rules
"""
import logging
from tower_simulator.world.coordinate import Coordinate, Grid
from tower_simulator.entities.room import RoomEntity

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class PlacementValidator:
    """Validates whether a room can be placed at a given location"""
    
    def __init__(self, existing_rooms: list[RoomEntity]):
        """Initialize validator with list of existing rooms"""
        self.existing_rooms = existing_rooms
        logging.info("PlacementValidator initialized with %d rooms.", len(existing_rooms))
        if any(r.room_type == 'lobby' for r in existing_rooms):
            self.log_lobby_locations()

    def can_place(self, room_type: str, coordinate: Coordinate, width: int, height: int = 1, log_attempt: bool = False) -> tuple[bool, str]:
        """
        Check if a room can be placed at the given location.
        
        Returns:
            (can_place: bool, reason: str) - True if valid, False with reason if invalid
        """
        if log_attempt:
            logging.info("="*50)
            logging.info("VALIDATION START: Placing '%s' at %s (width=%d, height=%d)", room_type, coordinate, width, height)
        
        # Check 1: Coordinate is within grid bounds
        if not self._is_within_bounds(coordinate, width, height):
            reason = "Room extends outside grid bounds"
            if log_attempt:
                logging.warning("VALIDATION FAILED: %s", reason)
            return False, reason
        
        # Check 2: Basement-specific restrictions
        if -5 <= coordinate.level <= -1:
            if not self._check_basement_allowed(room_type):
                reason = f"{room_type} cannot be placed in basement"
                if log_attempt:
                    logging.warning("VALIDATION FAILED: %s", reason)
                return False, reason
        
        # Check 3: Room type restrictions by level
        if not self._check_level_restrictions(room_type, coordinate, height):
            reason = f"{room_type} cannot be placed at this level"
            if log_attempt:
                logging.warning("VALIDATION FAILED: %s", reason)
            return False, reason
        
        # Check 4: No overlapping with existing rooms
        if not self._check_no_overlaps(coordinate, width, height):
            reason = "Room overlaps with existing building"
            if log_attempt:
                logging.warning("VALIDATION FAILED: %s", reason)
            return False, reason
        
        # Check 5: Room placement on valid surfaces
        if not self._check_valid_placement(coordinate, width, height, log_attempt=log_attempt):
            reason = "Room must be placed on valid surface (floor, ground, or lobby)"
            if log_attempt:
                logging.warning("VALIDATION FAILED: %s", reason)
            return False, reason
        
        # Check 6: Lobby connectivity (if placing lobby on level 0)
        if room_type == 'lobby' and coordinate.level == 0:
            if log_attempt:
                logging.info("Performing special validation for lobby connectivity...")
            if not self._check_lobby_connectivity(coordinate, width, log_attempt=log_attempt):
                reason = "Lobby segments must be connected (no gaps)"
                if log_attempt:
                    logging.warning("VALIDATION FAILED: %s", reason)
                return False, reason
        
        if log_attempt:
            logging.info("VALIDATION SUCCESS: '%s' can be placed at %s.", room_type, coordinate)
            logging.info("="*50)
        return True, "Valid placement"

    def _is_within_bounds(self, coordinate: Coordinate, width: int, height: int) -> bool:
        """Check if room fits within grid bounds"""
        from tower_simulator.world.coordinate import GRID_MIN_LEVEL, GRID_MAX_LEVEL
        
        seg_end = coordinate.segment + width
        level_end = coordinate.level + height
        
        return (0 <= coordinate.segment and seg_end <= Grid.WIDTH and
                GRID_MIN_LEVEL <= coordinate.level and level_end <= GRID_MAX_LEVEL + 1)

    def _check_level_restrictions(self, room_type: str, coordinate: Coordinate, height: int) -> bool:
        """Check placement restrictions based on room type and level"""
        # Residential (Condo) - Cannot be placed below level 1
        if room_type == 'condo':
            return coordinate.level >= 1
        
        # Corporate (Office) - Cannot be placed below level 1
        if room_type == 'office':
            return coordinate.level >= 1
        
        # Lobby - Can be placed on level 0 only
        if room_type == 'lobby':
            return coordinate.level == 0
        
        # Hotel - Cannot be placed below level 1
        if room_type.startswith('hotel_'):
            return coordinate.level >= 1
        
        # Commercial/Entertainment - Cannot be placed below level 1
        if room_type in ['fast_food', 'restaurant', 'retail_shop', 'cinema', 'party_hall']:
            return coordinate.level >= 1
        
        # Service modules - Can be placed anywhere except basement
        if room_type in ['housekeeping', 'security_station', 'medical_center']:
            return coordinate.level >= 0  # Level 0 and above only
        
        # Elevator - Can be placed at any level (vertical structure)
        if room_type == 'elevator_shaft':
            return True
        
        # Transit (stairs, escalator) - Can be placed in basement and above
        if room_type in ['stairs', 'escalator']:
            return True
        
        # Landmarks (Cathedral, Metro) - Specific placement rules
        if room_type == 'cathedral':
            return coordinate.level == 100  # Level 100 only
        
        if room_type == 'metro_station':
            return -5 <= coordinate.level <= -1  # Basement levels only
        
        # Default: allow placement
        return True

    def _check_basement_allowed(self, room_type: str) -> bool:
        """Check if room type is allowed in basement (-5 to -1)"""
        # Only these items allowed in basement
        allowed_in_basement = [
            'metro_station',  # Metro station occupies basement
            'stairs',         # Stairs for transport
            'escalator',      # Escalators for transport
            'elevator_shaft', # Elevators span multiple levels
        ]
        return room_type in allowed_in_basement

    def _check_no_overlaps(self, coordinate: Coordinate, width: int, height: int) -> bool:
        """Check that room doesn't overlap with existing rooms"""
        # Create temporary room for overlap checking
        test_room = RoomEntity(
            coordinate=coordinate,
            width=width,
            height=height,
            room_type='test',
            cost=0,
            color=(0, 0, 0)
        )
        
        # Check against all existing rooms
        for room in self.existing_rooms:
            if test_room.overlaps_with(room):
                return False
        
        return True

    def _check_valid_placement(self, coordinate: Coordinate, width: int, height: int, log_attempt: bool = False) -> bool:
        """
        Check that room is placed on a valid surface.
        Valid surfaces: Basement levels, Level 0 (lobby floor), or on top of existing rooms.
        This version correctly checks for a continuous foundation from multiple rooms.
        """
        # Basement levels (-5 to -1) don't need support - they're on bedrock
        if -5 <= coordinate.level <= -1:
            return True
        
        # Level 0 (lobby floor) is always valid for placement
        if coordinate.level == 0:
            return True
        
        # For all other levels, check for a continuous supporting structure from rooms below.
        level_below = coordinate.level - 1
        if log_attempt:
            logging.info("Checking for continuous supporting structure on level %d.", level_below)

        # 1. Find all segments on the level below that are covered by any room.
        supported_segments = set()
        for room in self.existing_rooms:
            # Check if the top of the room is on the level directly below our placement coordinate
            if room.coordinate.level + room.height == coordinate.level:
                for i in range(room.coordinate.segment, room.coordinate.segment + room.width):
                    supported_segments.add(i)

        # 2. Check if the new room's required segments are all supported by the foundation.
        required_segments = set(range(coordinate.segment, coordinate.segment + width))
        
        if required_segments.issubset(supported_segments):
            if log_attempt:
                logging.info("Found continuous support for segments %d to %d on level %d.", coordinate.segment, coordinate.segment + width - 1, level_below)
            return True
        else:
            if log_attempt:
                unsupported = sorted(list(required_segments - supported_segments))
                logging.warning("VALIDATION FAILED: No continuous foundation. Missing support for segments: %s", unsupported)
            return False

    def _check_lobby_connectivity(self, coordinate: Coordinate, width: int, log_attempt: bool = False) -> bool:
        """
        Check that lobby segments are connected (no gaps).
        Lobby must be continuous at level 0.
        """
        seg_start = coordinate.segment
        seg_end = coordinate.segment + width
        
        # Check if there's an existing lobby adjacent to this placement
        for room in self.existing_rooms:
            if room.room_type != 'lobby' or room.coordinate.level != 0:
                continue
            
            room_seg_start, room_seg_end = room.get_segments()
            
            # Check if new lobby touches existing lobby
            # Adjacent means: new segment overlaps or is directly next to existing
            if room_seg_end >= seg_start and room_seg_start <= seg_end:
                return True  # Connected
        
        # If no existing lobby, first placement is always valid
        has_any_lobby = any(r.room_type == 'lobby' and r.coordinate.level == 0 
                           for r in self.existing_rooms)
        if not has_any_lobby:
            if log_attempt:
                logging.info("No existing lobby found. This is the first lobby segment.")
            return True  # First lobby placement is valid
        
        if log_attempt:
            logging.warning("Proposed lobby at %s is not connected to any existing lobby segments.", coordinate)
            self.log_lobby_locations()
        return False  # No connection to existing lobby

    def update_rooms(self, rooms: list[RoomEntity]):
        """Update the list of existing rooms"""
        newly_added = [r for r in rooms if r not in self.existing_rooms]
        self.existing_rooms = rooms
        if newly_added:
            for room in newly_added:
                logging.info("ROOM PLACED: '%s' at %s (width=%d)", room.room_type, room.coordinate, room.width)
                if room.room_type == 'lobby':
                    self.log_lobby_locations()

    def log_lobby_locations(self):
        """Logs the coordinates and widths of all existing lobby segments."""
        lobby_locations = [f"Lobby at {r.coordinate} (width {r.width})" for r in self.existing_rooms if r.room_type == 'lobby']
        if lobby_locations:
            logging.info("Current lobby segments: %s", '; '.join(lobby_locations))
        else:
            logging.info("No lobby segments currently exist.")
