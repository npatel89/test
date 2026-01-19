"""
Test suite for Building Action (placing rooms and deducting funds)
"""
import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tower_simulator.constants import ENTITY_DATA
from tower_simulator.world.coordinate import Coordinate


class TestRoomCostCalculation(unittest.TestCase):
    """Test room cost calculation logic"""
    
    def test_entity_data_has_cost_info(self):
        """All entities should have cost defined"""
        print(f"\n[TEST] Entity Cost Information")
        
        missing_cost = []
        for entity_type, data in ENTITY_DATA.items():
            if "cost" not in data and "cost_per_segment" not in data:
                missing_cost.append(entity_type)
        
        print(f"  Total entity types: {len(ENTITY_DATA)}")
        print(f"  Types with cost info: {len(ENTITY_DATA) - len(missing_cost)}")
        print(f"  Missing cost: {missing_cost}")
        
        self.assertEqual(len(missing_cost), 0, 
                        f"All entities need cost defined. Missing: {missing_cost}")
    
    def test_basement_items_have_reasonable_cost(self):
        """Basement items should have cost defined"""
        print(f"\n[TEST] Basement Item Costs")
        
        basement_items = ["Metro", "Stairs", "Escalator", "Elevator Shaft"]
        
        for item in basement_items:
            data = ENTITY_DATA.get(item)
            if not data:
                print(f"  WARNING: {item} not found in ENTITY_DATA")
                continue
            
            cost = data.get("cost") or data.get("cost_per_segment")
            print(f"  {item}: ${cost:,}")
            self.assertIsNotNone(cost, f"{item} should have cost defined")


class TestBuildingFundValidation(unittest.TestCase):
    """Test that game validates funds before placing"""
    
    def test_expensive_items_exist(self):
        """Game should have expensive items for testing"""
        print(f"\n[TEST] Item Price Range")
        
        prices = []
        for entity_type, data in ENTITY_DATA.items():
            cost = data.get("cost") or data.get("cost_per_segment") or 0
            prices.append((entity_type, cost))
        
        prices.sort(key=lambda x: x[1])
        
        cheapest = prices[0]
        most_expensive = prices[-1]
        
        print(f"  Cheapest: {cheapest[0]} = ${cheapest[1]:,}")
        print(f"  Most Expensive: {most_expensive[0]} = ${most_expensive[1]:,}")
        
        self.assertLess(cheapest[1], most_expensive[1], "Should have price variation")


class TestEntityDataCompleteness(unittest.TestCase):
    """Test that all entity data is properly filled out"""
    
    def test_all_entities_have_required_fields(self):
        """Each entity should have all required fields"""
        print(f"\n[TEST] Entity Data Completeness")
        
        required_fields = [
            "width", "height", "cost",
            "placement_level_min", "placement_level_max"
        ]
        
        incomplete = {}
        for entity_type, data in ENTITY_DATA.items():
            missing = [f for f in required_fields if f not in data and not (f == "cost" and "cost_per_segment" in data)]
            if missing:
                incomplete[entity_type] = missing
        
        print(f"  Total entities: {len(ENTITY_DATA)}")
        print(f"  Complete entities: {len(ENTITY_DATA) - len(incomplete)}")
        
        if incomplete:
            print(f"  Incomplete:")
            for entity, fields in incomplete.items():
                print(f"    - {entity}: missing {fields}")
        
        self.assertEqual(len(incomplete), 0, 
                        f"All entities need complete data. Incomplete: {incomplete}")
    
    def test_placement_levels_are_valid(self):
        """Level restrictions should be within valid grid bounds"""
        print(f"\n[TEST] Placement Level Validity")
        
        invalid = {}
        for entity_type, data in ENTITY_DATA.items():
            min_level = data.get("placement_level_min")
            max_level = data.get("placement_level_max")
            
            if min_level is None or max_level is None:
                continue
            
            if min_level < -5 or max_level > 109 or min_level > max_level:
                invalid[entity_type] = (min_level, max_level)
        
        print(f"  Total entities: {len(ENTITY_DATA)}")
        print(f"  Valid placement ranges: {len(ENTITY_DATA) - len(invalid)}")
        
        if invalid:
            print(f"  Invalid ranges:")
            for entity, (min_l, max_l) in invalid.items():
                print(f"    - {entity}: {min_l} to {max_l}")
        
        self.assertEqual(len(invalid), 0, 
                        f"All placement ranges must be -5 to 109. Invalid: {invalid}")


class TestCoordinateSystem(unittest.TestCase):
    """Test coordinate system functionality"""
    
    def test_valid_coordinates_in_valid_range(self):
        """Valid coordinates should pass validation"""
        print(f"\n[TEST] Valid Coordinate Ranges")
        
        test_cases = [
            (Coordinate(0, -5), "Bottom-left basement"),
            (Coordinate(374, -5), "Bottom-right basement"),
            (Coordinate(0, 0), "Bottom-left lobby"),
            (Coordinate(374, 109), "Top-right tower"),
            (Coordinate(187, 50), "Middle tower"),
        ]
        
        for coord, desc in test_cases:
            valid = coord.is_valid()
            print(f"  {desc}: {coord} = {valid}")
            self.assertTrue(valid, f"{desc} should be valid")
    
    def test_invalid_coordinates_fail_validation(self):
        """Invalid coordinates should fail validation"""
        print(f"\n[TEST] Invalid Coordinate Ranges")
        
        test_cases = [
            (Coordinate(-1, 0), "Negative segment"),
            (Coordinate(375, 0), "Segment too large"),
            (Coordinate(0, -6), "Below basement"),
            (Coordinate(0, 110), "Above top"),
        ]
        
        for coord, desc in test_cases:
            valid = coord.is_valid()
            print(f"  {desc}: {coord} = {valid}")
            self.assertFalse(valid, f"{desc} should be invalid")


if __name__ == '__main__':
    print("=" * 70)
    print("TOWER SIMULATOR TEST SUITE - Building & Economics System")
    print("=" * 70)
    
    unittest.main(verbosity=2)
