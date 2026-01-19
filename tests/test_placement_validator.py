"""
Test suite for Placement Validator system
"""
import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tower_simulator.systems.placement_validator import PlacementValidator
from tower_simulator.world.coordinate import Coordinate, Grid, GRID_MIN_LEVEL, GRID_MAX_LEVEL
from tower_simulator.entities.room import RoomEntity
from tower_simulator.constants import ENTITY_DATA


class TestPlacementValidatorBasics(unittest.TestCase):
    """Test basic placement validator initialization"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Initialize validator with empty room list for testing
        self.rooms = []
        self.validator = PlacementValidator(existing_rooms=self.rooms)
    
    def get_room_dimensions(self, room_type: str) -> tuple[int, int]:
        """Get width and height for a room type"""
        data = ENTITY_DATA.get(room_type, {})
        width = data.get("width", 1)
        height = data.get("height", 1)
        return width, height
    
    def test_validator_knows_grid_bounds(self):
        """Validator should know the grid boundaries"""
        print(f"\n[TEST] Grid Bounds Knowledge")
        print(f"  Grid Width: {Grid.WIDTH} segments")
        print(f"  Grid Min Level: {GRID_MIN_LEVEL}")
        print(f"  Grid Max Level: {GRID_MAX_LEVEL}")
        
        self.assertEqual(Grid.WIDTH, 375)
        self.assertEqual(GRID_MIN_LEVEL, -5)
        self.assertEqual(GRID_MAX_LEVEL, 109)


class TestPlacementValidatorBoundaryChecks(unittest.TestCase):
    """Test grid boundary validation"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.rooms = []
        self.validator = PlacementValidator(existing_rooms=self.rooms)
    
    def get_room_dimensions(self, room_type: str) -> tuple[int, int]:
        """Get width and height for a room type"""
        data = ENTITY_DATA.get(room_type, {})
        width = data.get("width", 1)
        height = data.get("height", 1)
        return width, height
    
    def test_cannot_place_before_grid_left_boundary(self):
        """Cannot place room at segment < 0"""
        width, height = self.get_room_dimensions("condo")
        can_place, reason = self.validator.can_place("condo", Coordinate(-1, 0), width, height)
        
        print(f"\n[TEST] Left Boundary (Segment < 0)")
        print(f"  Placement at segment -1: {can_place}")
        print(f"  Reason: {reason}")
        print(f"  Status: {'✅ PASS' if not can_place else '❌ FAIL'}")
        
        self.assertFalse(can_place, f"Should not allow segment < 0: {reason}")
    
    def test_cannot_place_after_grid_right_boundary(self):
        """Cannot place room at segment >= 375"""
        width, height = self.get_room_dimensions("condo")
        can_place, reason = self.validator.can_place("condo", Coordinate(375, 0), width, height)
        
        print(f"\n[TEST] Right Boundary (Segment >= 375)")
        print(f"  Placement at segment 375: {can_place}")
        print(f"  Reason: {reason}")
        print(f"  Status: {'✅ PASS' if not can_place else '❌ FAIL'}")
        
        self.assertFalse(can_place, f"Should not allow segment >= 375: {reason}")
    
    def test_cannot_place_below_basement(self):
        """Cannot place room below level -5"""
        width, height = self.get_room_dimensions("condo")
        can_place, reason = self.validator.can_place("condo", Coordinate(100, -6), width, height)
        
        print(f"\n[TEST] Below Basement (Level < -5)")
        print(f"  Placement at level -6: {can_place}")
        print(f"  Reason: {reason}")
        print(f"  Status: {'✅ PASS' if not can_place else '❌ FAIL'}")
        
        self.assertFalse(can_place, f"Should not allow level < -5: {reason}")
    
    def test_cannot_place_above_max_level(self):
        """Cannot place room above level 109"""
        width, height = self.get_room_dimensions("condo")
        can_place, reason = self.validator.can_place("condo", Coordinate(100, 110), width, height)
        
        print(f"\n[TEST] Above Max Level (Level > 109)")
        print(f"  Placement at level 110: {can_place}")
        print(f"  Reason: {reason}")
        print(f"  Status: {'✅ PASS' if not can_place else '❌ FAIL'}")
        
        self.assertFalse(can_place, f"Should not allow level > 109: {reason}")
    
    def test_can_place_at_valid_boundaries(self):
        """Can place rooms at valid boundary coordinates"""
        print(f"\n[TEST] Valid Boundaries")
        
        # Basement levels don't need support
        width, height = self.get_room_dimensions("stairs")
        result3, _ = self.validator.can_place("stairs", Coordinate(100, -5), width, height)
        print(f"  Basement Level -5: {result3}")
        self.assertTrue(result3, "Should allow basement level -5")
        
        # Lobby level is always valid (use fixed width for testing)
        lobby_w, lobby_h = 2, 1  # Lobby has variable width, so specify fixed for test
        result5, _ = self.validator.can_place("lobby", Coordinate(100, 0), lobby_w, lobby_h)
        print(f"  Level 0 (Lobby): {result5}")
        self.assertTrue(result5, "Should allow Level 0 for Lobby")


class TestPlacementValidatorBasementRestrictions(unittest.TestCase):
    """Test basement-only item placement restrictions"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.rooms = []
        self.validator = PlacementValidator(existing_rooms=self.rooms)
    
    def get_room_dimensions(self, room_type: str) -> tuple[int, int]:
        """Get width and height for a room type"""
        data = ENTITY_DATA.get(room_type, {})
        width = data.get("width", 1)
        height = data.get("height", 1)
        return width, height
    
    def test_metro_only_in_basement(self):
        """Metro Station can only be placed in basement (-5 to -1)"""
        print(f"\n[TEST] Metro Station Basement Restriction")
        width, height = self.get_room_dimensions("metro_station")
        
        # Should succeed in basement
        result_basement, _ = self.validator.can_place("metro_station", Coordinate(100, -3), width, height)
        print(f"  Level -3 (basement): {result_basement}")
        self.assertTrue(result_basement, "Metro should be placeable in basement")
        
        # Should fail at Level 0
        result_level0, reason = self.validator.can_place("metro_station", Coordinate(100, 0), width, height)
        print(f"  Level 0 (lobby): {result_level0} - {reason}")
        self.assertFalse(result_level0, "Metro should not be placeable at Level 0")
        
        # Should fail at Level 1
        result_above, reason = self.validator.can_place("metro_station", Coordinate(100, 1), width, height)
        print(f"  Level 1: {result_above} - {reason}")
        self.assertFalse(result_above, "Metro should not be placeable above basement")
    
    def test_non_basement_items_fail_in_basement(self):
        """Regular items (condo, office) should not be placeable in basement"""
        print(f"\n[TEST] Non-Basement Items in Basement")
        width, height = self.get_room_dimensions("condo")
        
        result_condo, reason = self.validator.can_place("condo", Coordinate(100, -2), width, height)
        print(f"  Condo at level -2: {result_condo} - {reason}")
        self.assertFalse(result_condo, f"Condo should not be placeable in basement: {reason}")


class TestPlacementValidatorLevelRestrictions(unittest.TestCase):
    """Test level-specific placement restrictions"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.rooms = []
        self.validator = PlacementValidator(existing_rooms=self.rooms)
    
    def get_room_dimensions(self, room_type: str) -> tuple[int, int]:
        """Get width and height for a room type"""
        data = ENTITY_DATA.get(room_type, {})
        width = data.get("width", 1)
        height = data.get("height", 1)
        return width, height
    
    def test_lobby_only_at_level_0(self):
        """Lobby can only be placed at Level 0"""
        print(f"\n[TEST] Lobby Level Restriction")
        # Lobby has variable width, use fixed width for testing
        width, height = 2, 1
        
        # Should succeed at Level 0
        result_level0, _ = self.validator.can_place("lobby", Coordinate(100, 0), width, height)
        print(f"  Level 0: {result_level0}")
        self.assertTrue(result_level0, "Lobby should be placeable at Level 0")
        
        # Should fail at Level 1
        result_above, reason = self.validator.can_place("lobby", Coordinate(100, 1), width, height)
        print(f"  Level 1: {result_above} - {reason}")
        self.assertFalse(result_above, f"Lobby should not be placeable above Level 0: {reason}")


class TestEntityTypeData(unittest.TestCase):
    """Test that entity type data is properly configured"""
    
    def test_all_entity_types_have_dimensions(self):
        """All entity types should have width and height defined"""
        print(f"\n[TEST] Entity Type Dimensions")
        
        missing = []
        for entity_type in ENTITY_DATA:
            data = ENTITY_DATA[entity_type]
            if "width" not in data or "height" not in data:
                missing.append(entity_type)
        
        print(f"  Total entity types: {len(ENTITY_DATA)}")
        print(f"  Missing dimensions: {missing}")
        self.assertEqual(len(missing), 0, f"All types need dimensions. Missing: {missing}")
    
    def test_all_entity_types_have_level_restrictions(self):
        """All entity types should have placement level restrictions"""
        print(f"\n[TEST] Entity Type Level Restrictions")
        
        missing = []
        for entity_type in ENTITY_DATA:
            data = ENTITY_DATA[entity_type]
            if "placement_level_min" not in data or "placement_level_max" not in data:
                missing.append(entity_type)
        
        print(f"  Total entity types: {len(ENTITY_DATA)}")
        print(f"  Missing level restrictions: {missing}")
        self.assertEqual(len(missing), 0, f"All types need level restrictions. Missing: {missing}")


if __name__ == '__main__':
    print("=" * 70)
    print("TOWER SIMULATOR TEST SUITE - Placement Validator System")
    print("=" * 70)
    
    unittest.main(verbosity=2)
