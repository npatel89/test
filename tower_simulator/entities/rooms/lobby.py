"""
Lobby room type
"""
from tower_simulator.entities.room import RoomEntity
from tower_simulator.world.coordinate import Coordinate


class Lobby(RoomEntity):
    """Lobby room - Entry point for the tower"""
    
    # Class constants
    COST_PER_SEGMENT = 500
    DEFAULT_WIDTH = 4  # segments
    HEIGHT = 1  # Always 1 level
    COLOR = (150, 100, 50)  # Brown color
    ROOM_TYPE = 'lobby'
    
    def __init__(self, coordinate: Coordinate, width: int = DEFAULT_WIDTH):
        """Create a lobby at the given coordinate"""
        cost = width * self.COST_PER_SEGMENT
        
        super().__init__(
            coordinate=coordinate,
            width=width,
            height=self.HEIGHT,
            room_type=self.ROOM_TYPE,
            cost=cost,
            color=self.COLOR
        )
    
    @staticmethod
    def create_default() -> 'Lobby':
        """Create a default lobby at level 1, centered"""
        # Center the 4-segment lobby on the 375-segment wide grid
        center_segment = (375 - Lobby.DEFAULT_WIDTH) // 2
        coordinate = Coordinate(segment=center_segment, level=1)
        return Lobby(coordinate, width=Lobby.DEFAULT_WIDTH)
