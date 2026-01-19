"""
Ghost room - preview of room being placed
"""
import pygame
from tower_simulator.entities.room import RoomEntity
from tower_simulator.world.coordinate import Coordinate, Grid, GRID_MIN_LEVEL, GRID_MAX_LEVEL


class GhostRoom:
    """Preview of a room being placed (follows mouse cursor)"""
    
    def __init__(self, room_type: str, width: int, height: int = 1):
        """Initialize ghost room"""
        self.room_type = room_type
        self.width = width
        self.height = height
        self.coordinate = Coordinate(0, 0)
        self.can_place = False
        self.color_valid = (100, 200, 100, 100)  # Green with alpha
        self.color_invalid = (200, 100, 100, 100)  # Red with alpha

    def update_position(self, world_x: int, world_y: int):
        """Update ghost room position based on mouse position in world coordinates"""
        # Snap to grid
        segment = world_x // Grid.PIXELS_PER_SEGMENT
        level = world_y // Grid.PIXELS_PER_LEVEL
        
        # Clamp to grid bounds
        segment = max(0, min(segment, Grid.WIDTH - self.width))
        level = max(GRID_MIN_LEVEL, min(level, GRID_MAX_LEVEL - self.height))
        
        self.coordinate = Coordinate(segment, level)

    def set_validity(self, valid: bool):
        """Set whether the ghost room can be placed"""
        self.can_place = valid

    def draw(self, surface: pygame.Surface, camera):
        """Draw the ghost room preview"""
        # Get pixel bounds in world space
        world_x, world_y, width_px, height_px = self.get_pixel_bounds()
        
        # Convert to screen coordinates
        screen_x, screen_y = camera.world_to_screen(world_x, world_y)
        
        # Create semi-transparent surface for the ghost room
        ghost_surface = pygame.Surface((width_px, height_px))
        color = self.color_valid if self.can_place else self.color_invalid
        ghost_surface.fill(color[:3])
        ghost_surface.set_alpha(100)
        
        # Draw the ghost room
        surface.blit(ghost_surface, (screen_x, screen_y))
        
        # Draw border (solid, not transparent)
        border_color = (0, 150, 0) if self.can_place else (150, 0, 0)
        pygame.draw.rect(
            surface,
            border_color,
            (screen_x, screen_y, width_px, height_px),
            2
        )
        
        # Draw label
        label_font = pygame.font.Font(None, 14)
        label = label_font.render(self.room_type.upper(), True, (0, 0, 0))
        label_rect = label.get_rect(center=(screen_x + width_px // 2, screen_y + height_px // 2))
        surface.blit(label, label_rect)

    def get_pixel_bounds(self) -> tuple[int, int, int, int]:
        """Get bounds in pixels (x, y, width, height)"""
        x, y = self.coordinate.to_pixels()
        width_px = self.width * Grid.PIXELS_PER_SEGMENT
        height_px = self.height * Grid.PIXELS_PER_LEVEL
        return x, y, width_px, height_px

    def create_room_entity(self, room_class, **kwargs) -> RoomEntity:
        """Create actual room entity from ghost room"""
        return room_class(self.coordinate, width=self.width, **kwargs)
