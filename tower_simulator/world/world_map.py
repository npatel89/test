"""
World Map class for managing the tower grid
"""
from tower_simulator.world.coordinate import Coordinate, Grid


class WorldMap:
    """Manages the 375x110 grid of the tower"""

    def __init__(self):
        """Initialize the world map"""
        self.width = Grid.WIDTH
        self.height = Grid.HEIGHT
        
        # Initialize grid - each cell can hold a room or be empty
        # Using a 2D list where grid[level][segment] represents a cell
        self.grid = [[None for _ in range(self.width)] for _ in range(self.height)]
        
        # Track populated cells for efficient rendering
        self.occupied_cells = set()

    def place_room(self, coordinate: Coordinate, room_data: dict) -> bool:
        """Place a room at the given coordinate"""
        if not coordinate.is_valid():
            return False
        
        # Check if cell is already occupied
        if self.grid[coordinate.level][coordinate.segment] is not None:
            return False
        
        # Place the room
        self.grid[coordinate.level][coordinate.segment] = room_data
        self.occupied_cells.add((coordinate.segment, coordinate.level))
        return True

    def get_room(self, coordinate: Coordinate) -> dict | None:
        """Get room data at coordinate"""
        if not coordinate.is_valid():
            return None
        
        return self.grid[coordinate.level][coordinate.segment]

    def remove_room(self, coordinate: Coordinate) -> bool:
        """Remove a room at the given coordinate"""
        if not coordinate.is_valid():
            return False
        
        if self.grid[coordinate.level][coordinate.segment] is None:
            return False
        
        self.grid[coordinate.level][coordinate.segment] = None
        self.occupied_cells.discard((coordinate.segment, coordinate.level))
        return True

    def is_occupied(self, coordinate: Coordinate) -> bool:
        """Check if a cell is occupied"""
        if not coordinate.is_valid():
            return False
        
        return self.grid[coordinate.level][coordinate.segment] is not None

    def get_occupied_cells(self) -> set:
        """Get all occupied cell coordinates"""
        return self.occupied_cells.copy()

    def clear(self):
        """Clear all rooms from the map"""
        self.grid = [[None for _ in range(self.width)] for _ in range(self.height)]
        self.occupied_cells.clear()
