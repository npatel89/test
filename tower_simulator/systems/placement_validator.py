"""
Placement validation logic for building placement rules
"""
from tower_simulator.world.coordinate import Coordinate, Grid
from tower_simulator.entities.room import RoomEntity


class PlacementValidator:
    """Validates whether a room can be placed at a given location"""
    
    def __init__(self, existing_rooms: list[RoomEntity]):
        """Initialize validator with list of existing rooms"""
        self.existing_rooms = existing_rooms

    def can_place(self, room_type: str, coordinate: Coordinate, width: int, height: int = 1) -> tuple[bool, str]:
        """
        Check if a room can be placed at the given location.
        
        Returns:
            (can_place: bool, reason: str) - True if valid, False with reason if invalid
        """
        # Check 1: Coordinate is within grid bounds
        if not self._is_within_bounds(coordinate, width, height):
            return False, "Room extends outside grid bounds"
        
        # Check 2: Basement-specific restrictions
        if -5 <= coordinate.level <= -1:
            if not self._check_basement_allowed(room_type):
                return False, f"{room_type} cannot be placed in basement"
        
        # Check 3: Room type restrictions by level
        if not self._check_level_restrictions(room_type, coordinate, height):
            return False, f"{room_type} cannot be placed at this level"
        
        # Check 4: No overlapping with existing rooms
        if not self._check_no_overlaps(coordinate, width, height):
            return False, "Room overlaps with existing building"
        
        # Check 5: Room placement on valid surfaces
        if not self._check_valid_placement(coordinate, width, height):
            return False, "Room must be placed on valid surface (floor, ground, or lobby)"
        
        # Check 6: Lobby connectivity (if placing lobby on level 0)
        if room_type == 'lobby' and coordinate.level == 0:
            if not self._check_lobby_connectivity(coordinate, width):
                return False, "Lobby segments must be connected (no gaps)"
        
        return True, "Valid placement"

    def _is_within_bounds(self, coordinate: Coordinate, width: int, height: int) -> bool:
        """Check if room fits within grid bounds"""
        seg_end = coordinate.segment + width
        level_end = coordinate.level + height
        
        return (0 <= coordinate.segment and seg_end <= Grid.WIDTH and
                0 <= coordinate.level and level_end <= Grid.HEIGHT)

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

    def _check_valid_placement(self, coordinate: Coordinate, width: int, height: int) -> bool:
        """
        Check that room is placed on a valid surface.
        Valid surfaces: Ground (level 0), or on top of existing rooms
        """
        # Level 0 (lobby floor) is always valid
        if coordinate.level == 0:
            return True
        
        # Check if there's a room directly below this placement
        seg_start = coordinate.segment
        seg_end = coordinate.segment + width
        
        # A room below can be any width as long as it covers the segments
        for room in self.existing_rooms:
            room_seg_start, room_seg_end = room.get_segments()
            room_level_start, room_level_end = room.get_levels()
            
            # Check if room's top aligns with our placement's bottom
            if room_level_end == coordinate.level:
                # Check if it supports our placement
                if room_seg_start <= seg_start and seg_end <= room_seg_end:
                    return True
        
        return False

    def _check_lobby_connectivity(self, coordinate: Coordinate, width: int) -> bool:
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
            return True  # First lobby placement is valid
        
        return False  # No connection to existing lobby

    def update_rooms(self, rooms: list[RoomEntity]):
        """Update the list of existing rooms"""
        self.existing_rooms = rooms
