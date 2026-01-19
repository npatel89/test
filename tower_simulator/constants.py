"""
Global game constants and entity data registry
"""

# ============================================================================
# ENTITY DATA REGISTRY
# ============================================================================
# Comprehensive data structure for all buildable facilities in the tower
# Reference: TechnicalDoc.txt sections on Entity Specifications

ENTITY_DATA = {
    # =========================================================================
    # RESIDENTIAL MODULES
    # =========================================================================
    'condo': {
        'name': 'Condominium',
        'type': 'residential',
        'width': 16,  # segments
        'height': 1,  # levels
        'cost': 80000,
        'color': (200, 150, 100),
        'capacity': 3,  # Sims per unit
        'sale_price': 150000,  # Base sale price
        'sale_price_max': 200000,
        'sale_price_min': 50000,
        'placement_level_min': 1,
        'placement_level_max': 109,
        'income_type': 'one_time',
        'maintenance': 0,
        'notes': 'One-time income on sale. High risk of abandonment if tower conditions worsen.'
    },
    
    # =========================================================================
    # CORPORATE MODULES
    # =========================================================================
    'office': {
        'name': 'Office',
        'type': 'corporate',
        'width': 9,  # segments
        'height': 1,  # levels
        'cost': 40000,
        'color': (100, 150, 200),
        'capacity': 6,  # Sims per unit
        'placement_level_min': 1,
        'placement_level_max': 109,
        'income_type': 'quarterly_rent',
        'income_min': 2000,
        'income_max': 15000,
        'income_default': 4000,
        'maintenance': 0,
        'notes': 'Stable income source. Most important for financial stability.'
    },
    
    # =========================================================================
    # HOSPITALITY MODULES
    # =========================================================================
    'hotel_single': {
        'name': 'Hotel Single Room',
        'type': 'hospitality',
        'width': 4,  # segments
        'height': 1,  # levels
        'cost': 20000,
        'color': (200, 100, 100),
        'capacity': 1,  # Sims per unit
        'rating_required': 2,
        'placement_level_min': 1,
        'placement_level_max': 109,
        'income_type': 'daily_occupancy',
        'income_min': 500,
        'income_max': 3000,
        'maintenance': 0,
        'notes': 'Requires housekeeping service. Check-out 6:30 AM - noon.'
    },
    
    'hotel_twin': {
        'name': 'Hotel Twin Room',
        'type': 'hospitality',
        'width': 8,  # segments
        'height': 1,  # levels
        'cost': 50000,
        'color': (200, 100, 100),
        'capacity': 2,  # Sims per unit
        'rating_required': 3,
        'placement_level_min': 1,
        'placement_level_max': 109,
        'income_type': 'daily_occupancy',
        'income_min': 800,
        'income_max': 4500,
        'maintenance': 0,
        'notes': 'Requires housekeeping service and good tower rating.'
    },
    
    'hotel_suite': {
        'name': 'Hotel Suite',
        'type': 'hospitality',
        'width': 12,  # segments
        'height': 1,  # levels
        'cost': 100000,
        'color': (200, 100, 100),
        'capacity': 2,  # Sims per unit
        'rating_required': 3,
        'placement_level_min': 1,
        'placement_level_max': 109,
        'income_type': 'daily_occupancy',
        'income_min': 1500,
        'income_max': 9000,
        'maintenance': 0,
        'notes': 'Luxury suite. Requires parking space nearby.'
    },
    
    # =========================================================================
    # COMMERCIAL MODULES
    # =========================================================================
    'fast_food': {
        'name': 'Fast Food',
        'type': 'commercial',
        'width': 16,  # segments
        'height': 1,  # levels
        'cost': 100000,
        'color': (255, 200, 100),
        'capacity': 50,  # Sims
        'placement_level_min': 1,
        'placement_level_max': 109,
        'income_type': 'daily_service',
        'income_red': -3000,
        'income_yellow': 2000,
        'income_blue': 5000,
        'maintenance': 0,
        'notes': 'Main lunch destination for office workers. 9 AM - 5 PM service.'
    },
    
    'restaurant': {
        'name': 'Restaurant',
        'type': 'commercial',
        'width': 24,  # segments
        'height': 1,  # levels
        'cost': 200000,
        'color': (200, 100, 50),
        'capacity': 100,  # Sims
        'placement_level_min': 1,
        'placement_level_max': 109,
        'income_type': 'daily_service',
        'income_red': -6000,
        'income_yellow': 4000,
        'income_blue': 10000,
        'maintenance': 0,
        'notes': 'Opens after 5 PM. Serves hotel guests and residents.'
    },
    
    'retail_shop': {
        'name': 'Retail Shop',
        'type': 'commercial',
        'width': 12,  # segments
        'height': 1,  # levels
        'cost': 100000,
        'color': (200, 180, 150),
        'capacity': 100,  # Sims
        'placement_level_min': 1,
        'placement_level_max': 109,
        'income_type': 'daily_rent',
        'income_min': 4000,
        'income_max': 20000,
        'maintenance': 0,
        'notes': 'Income based on rent price and customer count.'
    },
    
    # =========================================================================
    # ENTERTAINMENT MODULES
    # =========================================================================
    'cinema': {
        'name': 'Cinema',
        'type': 'entertainment',
        'width': 31,  # segments
        'height': 2,  # levels (2-floor building)
        'cost': 500000,
        'color': (100, 100, 200),
        'capacity': 120,  # Sims
        'placement_level_min': 1,
        'placement_level_max': 108,
        'income_type': 'daily_flat',
        'income_base': 10000,
        'maintenance': 0,
        'notes': 'Movie rotation required. New movie: $300k, Classic: $150k.'
    },
    
    # =========================================================================
    # SPECIALIZED FACILITIES
    # =========================================================================
    'cathedral': {
        'name': 'Cathedral',
        'type': 'landmark',
        'width': 20,  # segments (estimated)
        'height': 1,  # levels
        'cost': 3000000,
        'color': (150, 100, 200),
        'capacity': 0,  # No capacity
        'placement_level_min': 100,
        'placement_level_max': 100,
        'rating_required': 5,
        'income_type': 'none',
        'maintenance': 0,
        'notes': 'Required for TOWER rating. Placement on level 100 with 5-star rating.'
    },
    
    'metro_station': {
        'name': 'Metro Station',
        'type': 'transport',
        'width': 30,  # segments (estimated)
        'height': 3,  # Must be 3 levels
        'cost': 1000000,
        'color': (50, 150, 50),
        'capacity': 500,  # Sims injected at start of day
        'placement_level_min': -5,  # B1-B5 (basement levels)
        'placement_level_max': -1,
        'income_type': 'none',
        'maintenance': 100000,  # Quarterly
        'notes': 'Subterranean. Basement levels only (-5 to -1). Massive population booster. 3-level requirement.',
    },
    
    # =========================================================================
    # TRANSIT MODULES
    # =========================================================================
    'lobby': {
        'name': 'Lobby',
        'type': 'transit',
        'width': None,  # Variable 1-4 segments
        'height': 1,  # levels
        'cost_per_segment': 500,
        'color': (150, 100, 50),
        'capacity': None,  # Infinite
        'placement_level_min': 0,
        'placement_level_max': 0,
        'income_type': 'none',
        'maintenance_per_segment': 3,
        'notes': 'Entry point for Sims. Level 0 only. Must be continuously connected (no gaps).',
    },
    
    'elevator_shaft': {
        'name': 'Elevator Shaft',
        'type': 'transit',
        'width': 4,  # segments
        'height': None,  # Variable height
        'cost': 200000,
        'cost_per_shaft': 200000,
        'cost_per_car': 80000,
        'color': (100, 100, 100),
        'capacity': 8,  # Cars max per shaft
        'cars_per_shaft_default': 1,
        'placement_level_min': -5,
        'placement_level_max': 109,
        'income_type': 'none',
        'maintenance_per_car': 10000,  # Quarterly
        'max_shaft_count': 24,  # Hard limit
        'notes': 'Core of transportation. SCAN algorithm dispatch.'
    },
    
    'stairs': {
        'name': 'Stairs',
        'type': 'transit',
        'width': 8,  # segments
        'height': 2,  # levels (occupies 2 levels)
        'cost': 5000,
        'color': (180, 140, 100),
        'capacity': None,  # Infinite
        'stress_generation': 0,
        'placement_level_min': -5,
        'placement_level_max': -1,
        'income_type': 'none',
        'maintenance': 0,
        'notes': 'Generates no stress. Limited to 64 units per tower.'
    },
    
    'escalator': {
        'name': 'Escalator',
        'type': 'transit',
        'width': 8,  # segments
        'height': 2,  # levels
        'cost': 20000,
        'color': (200, 160, 100),
        'capacity': None,  # Infinite
        'stress_generation': 0,
        'preferred_range': 7,  # Levels (5 practical)
        'placement_level_min': -5,
        'placement_level_max': -1,
        'income_type': 'none',
        'maintenance': 0,
        'notes': 'Preferred for short trips. Max 64 units per tower.'
    },
    
    # =========================================================================
    # SERVICE MODULES
    # =========================================================================
    'housekeeping': {
        'name': 'Housekeeping Station',
        'type': 'service',
        'width': 10,  # segments
        'height': 1,  # levels
        'cost': 10000,
        'color': (150, 200, 150),
        'capacity': 6,  # Housekeepers per station
        'rooms_per_housekeeper': 19,
        'work_hours_end': 17,  # 5:00 PM
        'no_new_work_after': 16.5,  # 4:30 PM
        'placement_level_min': 1,
        'placement_level_max': 109,
        'income_type': 'none',
        'maintenance': 0,
        'notes': 'Required for hotel operations. Max 6 floors per service elevator.'
    },
    
    'security_station': {
        'name': 'Security Station',
        'type': 'service',
        'width': 10,  # segments
        'height': 1,  # levels
        'cost': 50000,
        'color': (150, 150, 150),
        'rating_required': 2,
        'placement_level_min': 1,
        'placement_level_max': 109,
        'income_type': 'none',
        'maintenance': 0,
        'notes': 'Handles bomb threats and other events.'
    },
    
    'medical_center': {
        'name': 'Medical Center',
        'type': 'service',
        'width': 15,  # segments
        'height': 1,  # levels
        'cost': 100000,
        'color': (255, 150, 150),
        'rating_required': 3,
        'placement_level_min': 1,
        'placement_level_max': 109,
        'income_type': 'none',
        'maintenance': 0,
        'notes': 'Required by 3+ star offices. Prevents worker dissatisfaction.'
    },
    
    'party_hall': {
        'name': 'Party Hall',
        'type': 'entertainment',
        'width': 16,  # segments
        'height': 1,  # levels
        'cost': 100000,
        'color': (200, 100, 200),
        'capacity': 200,  # Sims
        'placement_level_min': 1,
        'placement_level_max': 109,
        'income_type': 'daily_flat',
        'income_flat': 20000,
        'maintenance': 0,
        'notes': 'High-margin entertainment. Flat daily fee.'
    },
}

# ============================================================================
# GAME PARAMETERS & SETTINGS
# ============================================================================

# Financial
INITIAL_FUNDS = 2000000  # Starting cash
SIMULATION_SPEED = 0.5  # Real seconds per game minute

# Grid & World
GRID_WIDTH = 375
GRID_HEIGHT = 115  # -5 (basement) to 109 (top)
GRID_MIN_LEVEL = -5
GRID_MAX_LEVEL = 109
PIXELS_PER_SEGMENT = 8
PIXELS_PER_LEVEL = 32

# Population & Progression
POPULATION_TARGET_1_STAR = 0  # Starting point
POPULATION_TARGET_2_STARS = 300
POPULATION_TARGET_3_STARS = 1000
POPULATION_TARGET_4_STARS = 5000
POPULATION_TARGET_5_STARS = 10000
POPULATION_TARGET_TOWER = 15000

# Timing (12-day year cycle)
WEEKDAY_1 = 0
WEEKDAY_2 = 1
WEEKEND = 2

DAYS_PER_YEAR = 12
QUARTERS_PER_YEAR = 4
DAYS_PER_QUARTER = 3

# Work Hours
OFFICE_WORK_START = 9.0  # 9:00 AM
OFFICE_WORK_END = 17.0  # 5:00 PM
LUNCH_START = 12.0  # Noon
LUNCH_END = 13.0  # 1:00 PM
CONDO_SALES_START = 9.0  # 9:00 AM
CONDO_SALES_END = 13.0  # 1:00 PM

# Hotel Check Times
HOTEL_CHECKOUT_START = 6.5  # 6:30 AM
HOTEL_CHECKOUT_END = 12.0  # Noon
HOTEL_CHECKIN_START = 17.0  # 5:00 PM
HOTEL_CHECKIN_END = 23.0  # 11:00 PM

# Elevator Dispatch
SCAN_ALGORITHM_ENABLED = True
WAITING_CAR_RESPONSE_RANGE = (1, 5)  # Floors
STANDARD_FLOOR_DEPARTURE = (30, 60)  # Seconds
MAX_ELEVATOR_SHAFTS = 24
MAX_CARS_PER_SHAFT = 8

# Stress/Satisfaction
MAX_SIM_TRIPS = 4  # Maximum transit legs per destination
STRESS_LEVEL_PINK = 60  # Seconds
STRESS_LEVEL_RED = 120  # Seconds

# Notes
NOTES = {
    'sim_trips': 'A Sim can only handle 4 transit legs (elevator, stair, escalator) to reach destination',
    'escalator_limits': '64 escalators/stairs max per tower, limited to 5-7 level range',
    'metro_injection': 'Metro pumps large population at start of workday to B1-B3',
    'condo_glitch': 'Phantom Sims can appear in unsold condos during bomb threats',
}
