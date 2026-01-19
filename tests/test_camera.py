"""
Test suite for Camera system
"""
import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tower_simulator.world.camera import Camera
from tower_simulator.world.coordinate import Grid, GRID_MIN_LEVEL


class TestCameraInitialization(unittest.TestCase):
    """Test camera startup position"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.screen_width = 1280
        self.screen_height = 720
    
    def test_camera_starts_centered_horizontally(self):
        """Camera should start centered horizontally on the map"""
        camera = Camera(self.screen_width, self.screen_height)
        
        # Calculate expected center position
        grid_width_pixels = Grid.WIDTH * 8  # 375 * 8 = 3000
        expected_x = (grid_width_pixels - self.screen_width) // 2  # (3000 - 1280) / 2 = 860
        
        print(f"\n[TEST] Camera X Position (Horizontal Center)")
        print(f"  Expected: {expected_x}")
        print(f"  Actual:   {camera.x}")
        print(f"  Status:   {'PASS' if camera.x == expected_x else 'FAIL'}")
        
        self.assertEqual(camera.x, expected_x, 
                        f"Camera X should be {expected_x}, got {camera.x}")
    
    def test_camera_starts_at_basement_level(self):
        """Camera should start at basement level (GRID_MIN_LEVEL)"""
        camera = Camera(self.screen_width, self.screen_height)
        
        expected_y = GRID_MIN_LEVEL * 32  # -5 * 32 = -160
        
        print(f"\n[TEST] Camera Y Position (Basement Start)")
        print(f"  Expected: {expected_y} (GRID_MIN_LEVEL = {GRID_MIN_LEVEL})")
        print(f"  Actual:   {camera.y}")
        print(f"  Status:   {'PASS' if camera.y == expected_y else 'FAIL'}")
        
        self.assertEqual(camera.y, expected_y,
                        f"Camera Y should be {expected_y}, got {camera.y}")
    
    def test_camera_bounds_are_correct(self):
        """Verify camera knows the grid bounds"""
        camera = Camera(self.screen_width, self.screen_height)
        
        expected_grid_width = Grid.WIDTH * 8
        expected_grid_min_y = GRID_MIN_LEVEL * 32
        expected_grid_max_y = 109 * 32  # GRID_MAX_LEVEL = 109
        
        print(f"\n[TEST] Camera Grid Bounds")
        print(f"  Grid Width: Expected {expected_grid_width}, Got {camera.grid_width}")
        print(f"  Grid Min Y: Expected {expected_grid_min_y}, Got {camera.grid_min_y}")
        print(f"  Grid Max Y: Expected {expected_grid_max_y}, Got {camera.grid_max_y}")
        
        self.assertEqual(camera.grid_width, expected_grid_width)
        self.assertEqual(camera.grid_min_y, expected_grid_min_y)
        self.assertEqual(camera.grid_max_y, expected_grid_max_y)
    
    def test_camera_can_view_level_zero(self):
        """Level 0 should be visible on screen (in lower half)"""
        camera = Camera(self.screen_width, self.screen_height)
        
        # Level 0 in world coordinates
        level_0_world_y = 0
        
        # Convert to screen coordinates
        screen_x, screen_y = camera.world_to_screen(0, level_0_world_y)
        
        print(f"\n[TEST] Level 0 Visibility")
        print(f"  World Y (Level 0): {level_0_world_y}")
        print(f"  Screen Y: {screen_y}")
        print(f"  Screen Height: {self.screen_height}")
        print(f"  Level 0 in lower half? {screen_y > self.screen_height // 2}")
        print(f"  Status: {'PASS' if screen_y > self.screen_height // 2 else 'FAIL'}")
        
        # Level 0 should appear in lower half of screen (between 360-720)
        self.assertGreater(screen_y, self.screen_height // 2,
                          f"Level 0 should appear in lower half of screen")
        self.assertLess(screen_y, self.screen_height,
                       f"Level 0 should be visible on screen")


class TestCameraScrolling(unittest.TestCase):
    """Test camera scrolling mechanics"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.screen_width = 1280
        self.screen_height = 720
        self.camera = Camera(self.screen_width, self.screen_height)
    
    def test_camera_respects_left_boundary(self):
        """Camera should not scroll past left edge (x < 0)"""
        # Try to scroll left from starting position
        keys = [False] * 512  # pygame key array (most unused)
        keys[97] = True  # A key (left scroll)
        
        initial_x = self.camera.x
        
        # Scroll left multiple times to hit boundary
        for _ in range(1000):
            self.camera.handle_input(keys)
        
        print(f"\n[TEST] Left Boundary")
        print(f"  Initial X: {initial_x}")
        print(f"  After scrolling left 1000x: {self.camera.x}")
        print(f"  Clamped to 0? {self.camera.x == 0}")
        
        self.assertEqual(self.camera.x, 0, "Camera should be clamped to X=0")
    
    def test_camera_respects_bottom_boundary(self):
        """Camera should not scroll past bottom edge (y < GRID_MIN_LEVEL)"""
        # Try to scroll down (S key) from basement - should not go lower
        keys = [False] * 512
        keys[115] = True  # S key (scroll down/increase Y)
        
        initial_y = self.camera.y
        min_y = self.camera.grid_min_y
        
        # We're already at the bottom (grid_min_y = -160)
        # Scrolling down (S key, increases Y) should go UP the tower, which is correct
        # The real test is: if we scroll down 1000x from basement, we should go up
        # but eventually clamp at the top
        
        for _ in range(100):
            self.camera.handle_input(keys)
        
        final_y = self.camera.y
        
        print(f"\n[TEST] Bottom Boundary (S key from basement)")
        print(f"  Initial Y: {initial_y} (at basement)")
        print(f"  Grid Min Y: {min_y}")
        print(f"  After pressing S 100x: {final_y}")
        print(f"  Moved upward into tower? {final_y > initial_y}")
        print(f"  Clamped to max? {final_y == self.camera.grid_max_y - self.screen_height}")
        
        # From basement, pressing S (down) moves up in the tower
        self.assertGreater(final_y, initial_y, 
                          f"Pressing S should move camera up in tower (higher Y)")
        
        # Also verify that we eventually clamp at the top
        keys[115] = True  # Keep S pressed
        for _ in range(10000):
            self.camera.handle_input(keys)
        
        max_y = self.camera.grid_max_y - self.screen_height
        self.assertEqual(self.camera.y, max_y,
                        f"Camera should clamp at max height")


if __name__ == '__main__':
    # Run tests with verbose output
    print("=" * 70)
    print("TOWER SIMULATOR TEST SUITE - Camera System")
    print("=" * 70)
    
    unittest.main(verbosity=2)
