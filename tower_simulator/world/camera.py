"""
Camera system for viewport management
"""
import pygame
from tower_simulator.world.coordinate import Grid, GRID_MIN_LEVEL, GRID_MAX_LEVEL, PIXELS_PER_LEVEL, PIXELS_PER_SEGMENT


class Camera:
    """Manages the viewport and scrolling"""

    def __init__(self, screen_width: int, screen_height: int):
        """Initialize camera with screen dimensions"""
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Grid bounds in pixels
        # X: 0 to (375 * 8) = 3000 pixels
        # Y: (-5 * 32) to (109 * 32) = -160 to 3488 pixels
        self.grid_width = Grid.WIDTH * PIXELS_PER_SEGMENT
        self.grid_min_y = GRID_MIN_LEVEL * PIXELS_PER_LEVEL  # -160 for level -5
        self.grid_max_y = GRID_MAX_LEVEL * PIXELS_PER_LEVEL  # 3488 for level 109
        
        # Scroll speed in pixels per frame
        self.scroll_speed = 16
        
        # Initialize camera: centered horizontally, starting at basement (bottom) vertically
        # Center horizontally
        total_grid_width = self.grid_width
        center_x = (total_grid_width - screen_width) // 2
        
        # Start at basement level (bottom of tower)
        # This shows level 0 near the bottom and basement levels visible
        start_y = self.grid_min_y
        
        self.x = max(0, center_x)
        self.y = start_y
        
        # Clamp camera to grid bounds
        self._clamp()

    def _clamp(self):
        """Ensure camera doesn't scroll past grid boundaries"""
        # Clamp X
        if self.x < 0:
            self.x = 0
        if self.x + self.screen_width > self.grid_width:
            self.x = max(0, self.grid_width - self.screen_width)
        
        # Clamp Y (now allows negative values for basement levels)
        if self.y < self.grid_min_y:
            self.y = self.grid_min_y
        if self.y + self.screen_height > self.grid_max_y:
            self.y = max(self.grid_min_y, self.grid_max_y - self.screen_height)

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
        # Invert Y: world_y increases upward, screen_y increases downward
        # Camera looks from (self.x, self.y) at top-left of view
        # Level 0 = 0 pixels, higher levels = higher pixel values
        # But on screen, top is 0 and bottom is 720
        # So: screen_y = (camera_bottom - world_y) = (self.y + screen_height) - world_y
        screen_y = (self.y + self.screen_height) - world_y
        return screen_x, screen_y

    def screen_to_world(self, screen_x: int, screen_y: int) -> tuple[int, int]:
        """Convert screen coordinates to world coordinates"""
        world_x = screen_x + self.x
        # Invert Y back: world_y = (self.y + screen_height) - screen_y
        world_y = (self.y + self.screen_height) - screen_y
        return world_x, world_y

    def get_bounds(self) -> tuple[int, int, int, int]:
        """Get camera bounds as (x, y, width, height)"""
        return self.x, self.y, self.screen_width, self.screen_height

    def reset(self):
        """Reset camera to origin"""
        self.x = 0
        self.y = 0
        self._clamp()
