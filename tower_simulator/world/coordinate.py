"""
Coordinate system and grid utilities for Tower Simulator
"""
from dataclasses import dataclass


# Grid constants
GRID_WIDTH = 375  # segments
GRID_HEIGHT = 110  # levels (floors)
PIXELS_PER_SEGMENT = 8
PIXELS_PER_LEVEL = 32


@dataclass
class Coordinate:
    """Represents a coordinate in the grid (segment, level)"""
    segment: int  # 0-374 (horizontal)
    level: int    # 0-109 (vertical, 0 is bottom, 109 is top)

    def to_pixels(self) -> tuple[int, int]:
        """Convert grid coordinate to pixel coordinates"""
        pixel_x = self.segment * PIXELS_PER_SEGMENT
        pixel_y = self.level * PIXELS_PER_LEVEL
        return pixel_x, pixel_y

    def is_valid(self) -> bool:
        """Check if coordinate is within grid bounds"""
        return 0 <= self.segment < GRID_WIDTH and 0 <= self.level < GRID_HEIGHT

    def __repr__(self) -> str:
        return f"Coordinate(seg={self.segment}, level={self.level})"


class Grid:
    """Manages the grid system"""

    WIDTH = GRID_WIDTH
    HEIGHT = GRID_HEIGHT
    PIXELS_PER_SEGMENT = PIXELS_PER_SEGMENT
    PIXELS_PER_LEVEL = PIXELS_PER_LEVEL

    @staticmethod
    def pixel_to_coordinate(pixel_x: int, pixel_y: int) -> Coordinate:
        """Convert pixel coordinates to grid coordinate"""
        segment = pixel_x // PIXELS_PER_SEGMENT
        level = pixel_y // PIXELS_PER_LEVEL
        return Coordinate(segment, level)

    @staticmethod
    def get_grid_size_pixels() -> tuple[int, int]:
        """Get total grid size in pixels"""
        width_pixels = GRID_WIDTH * PIXELS_PER_SEGMENT
        height_pixels = GRID_HEIGHT * PIXELS_PER_LEVEL
        return width_pixels, height_pixels
