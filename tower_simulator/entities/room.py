"""
Base Room Entity class
"""
from dataclasses import dataclass
from tower_simulator.world.coordinate import Coordinate, Grid


@dataclass
class RoomEntity:
    """Represents a room or building in the tower"""
    
    # Basic properties
    coordinate: Coordinate  # Top-left position
    width: int  # Width in segments
    height: int  # Height in levels (usually 1 for most rooms)
    room_type: str  # Type: 'lobby', 'office', 'condo', etc.
    
    # Financial
    cost: int
    
    # Display
    color: tuple  # RGB tuple for rendering
    
    def __post_init__(self):
        """Validate room data after initialization"""
        if not self.coordinate.is_valid():
            raise ValueError(f"Invalid coordinate: {self.coordinate}")
        
        if self.width <= 0 or self.height <= 0:
            raise ValueError("Room must have positive width and height")
    
    def get_pixel_bounds(self) -> tuple[int, int, int, int]:
        """Get room bounds in pixels as (x, y, width_px, height_px)"""
        x, y = self.coordinate.to_pixels()
        width_px = self.width * Grid.PIXELS_PER_SEGMENT
        height_px = self.height * Grid.PIXELS_PER_LEVEL
        return x, y, width_px, height_px
    
    def get_segments(self) -> tuple[int, int]:
        """Get segment range (start, end)"""
        start = self.coordinate.segment
        end = start + self.width
        return start, end
    
    def get_levels(self) -> tuple[int, int]:
        """Get level range (start, end)"""
        start = self.coordinate.level
        end = start + self.height
        return start, end
    
    def overlaps_with(self, other: 'RoomEntity') -> bool:
        """Check if this room overlaps with another room"""
        self_x_start, self_x_end = self.get_segments()
        self_y_start, self_y_end = self.get_levels()
        
        other_x_start, other_x_end = other.get_segments()
        other_y_start, other_y_end = other.get_levels()
        
        # Check for no overlap (easier to check than overlap)
        if self_x_end <= other_x_start or other_x_end <= self_x_start:
            return False
        if self_y_end <= other_y_start or other_y_end <= self_y_start:
            return False
        
        return True
    
    def can_place(self, other_rooms: list['RoomEntity']) -> bool:
        """Check if this room can be placed without overlapping others"""
        for room in other_rooms:
            if self.overlaps_with(room):
                return False
        return True
    
    def __repr__(self) -> str:
        return f"RoomEntity({self.room_type} at {self.coordinate}, {self.width}x{self.height})"
