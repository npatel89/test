"""
Camera system for viewport management
"""
import pygame
from tower_simulator.world.coordinate import Grid


class Camera:
    """Manages the viewport and scrolling"""

    def __init__(self, screen_width: int, screen_height: int):
        """Initialize camera with screen dimensions"""
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Camera position (top-left corner in world pixels)
        self.x = 0
        self.y = 0
        
        # Get grid bounds
        self.grid_width, self.grid_height = Grid.get_grid_size_pixels()
        
        # Scroll speed in pixels per frame
        self.scroll_speed = 16
        
        # Clamp camera to grid bounds
        self._clamp()

    def _clamp(self):
        """Ensure camera doesn't scroll past grid boundaries"""
        # Clamp X
        if self.x < 0:
            self.x = 0
        if self.x + self.screen_width > self.grid_width:
            self.x = max(0, self.grid_width - self.screen_width)
        
        # Clamp Y
        if self.y < 0:
            self.y = 0
        if self.y + self.screen_height > self.grid_height:
            self.y = max(0, self.grid_height - self.screen_height)

    def handle_input(self, keys):
        """Handle camera movement from keyboard input"""
        # W - Pan up
        if keys[pygame.K_w]:
            self.y -= self.scroll_speed
        
        # S - Pan down
        if keys[pygame.K_s]:
            self.y += self.scroll_speed
        
        # A - Pan left
        if keys[pygame.K_a]:
            self.x -= self.scroll_speed
        
        # D - Pan right
        if keys[pygame.K_d]:
            self.x += self.scroll_speed
        
        self._clamp()

    def world_to_screen(self, world_x: int, world_y: int) -> tuple[int, int]:
        """Convert world coordinates to screen coordinates"""
        screen_x = world_x - self.x
        # Invert Y so higher levels appear higher on screen (level 0 at bottom)
        screen_y = self.screen_height - (world_y - self.y + Grid.PIXELS_PER_LEVEL)
        return screen_x, screen_y

    def screen_to_world(self, screen_x: int, screen_y: int) -> tuple[int, int]:
        """Convert screen coordinates to world coordinates"""
        world_x = screen_x + self.x
        # Invert Y back to world coordinates
        world_y = (self.screen_height - screen_y) + self.y - Grid.PIXELS_PER_LEVEL
        return world_x, world_y

    def get_bounds(self) -> tuple[int, int, int, int]:
        """Get camera bounds as (x, y, width, height)"""
        return self.x, self.y, self.screen_width, self.screen_height

    def reset(self):
        """Reset camera to origin"""
        self.x = 0
        self.y = 0
        self._clamp()
