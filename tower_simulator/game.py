"""
Main game class for Tower Simulator
"""
import pygame
import sys
from tower_simulator.world.world_map import WorldMap
from tower_simulator.world.camera import Camera
from tower_simulator.world.coordinate import Grid, Coordinate
from tower_simulator.entities.room import RoomEntity
from tower_simulator.entities.rooms.lobby import Lobby
from tower_simulator.constants import INITIAL_FUNDS, ENTITY_DATA
from tower_simulator.ui.toolbox import Toolbox
from tower_simulator.ui.status_bar import StatusBar
from tower_simulator.ui.ghost_room import GhostRoom
from tower_simulator.systems.placement_validator import PlacementValidator


class TowerSimulatorGame:
    """Main game class"""

    def __init__(self):
        """Initialize the game"""
        pygame.init()
        
        self.WIDTH = 1280
        self.HEIGHT = 720
        self.FPS = 60
        
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Tower Simulator")
        
        self.clock = pygame.time.Clock()
        self.running = True
        self.font = pygame.font.Font(None, 24)
        self.title_font = pygame.font.Font(None, 48)
        
        # Initialize world
        self.world_map = WorldMap()
        self.camera = Camera(self.WIDTH, self.HEIGHT)
        
        # Track rooms
        self.rooms = []
        
        # Game state
        self.funds = INITIAL_FUNDS
        self.population = 0
        self.star_rating = 1
        
        # UI elements
        self.toolbox = Toolbox()
        self.status_bar = StatusBar(self.WIDTH)
        
        # Placement system
        self.validator = PlacementValidator(self.rooms)
        self.ghost_room = None
        self.selected_tool = None
        
        # Create default lobby at level 1
        self._initialize_default_layout()
        
        # Grid display toggle
        self.show_grid = True
        
        print("Tower Simulator initialized!")
        print(f"Resolution: {self.WIDTH}x{self.HEIGHT}")
        print(f"Grid: {Grid.WIDTH} segments x {Grid.HEIGHT} levels")
        print(f"Pixel size: {Grid.PIXELS_PER_SEGMENT}px per segment, {Grid.PIXELS_PER_LEVEL}px per level")
        print("Controls: WASD to scroll, G to toggle grid, ESC to exit")

    def _initialize_default_layout(self):
        """Initialize the default tower layout with basement floors and ground lobby floor"""
        # Create basement floors (levels -5 to -1) - brown color
        basement_color = (139, 90, 43)  # Brown
        for level in range(-5, 0):  # -5 to -1
            basement_floor = RoomEntity(
                coordinate=Coordinate(0, level),
                width=Grid.WIDTH,
                height=1,
                room_type=f'basement_floor_level_{level}',
                cost=0,
                color=basement_color
            )
            self.rooms.append(basement_floor)
        
        # Note: Level 0 is reserved for LOBBY placement
        # No default ground entity - level 0 is for player-placed lobby segments
        
        # Update validator with all rooms
        self.validator.update_rooms(self.rooms)

    def _create_ghost_room(self, tool_id: str):
        """Create a ghost room preview for the selected tool"""
        # Get tool dimensions from entity data
        entity_info = ENTITY_DATA.get(tool_id)
        if not entity_info:
            return
        
        width = entity_info.get('width', 1)
        if width is None:
            width = 4  # Default for variable-width items like lobby
        
        height = entity_info.get('height', 1)
        if height is None:
            height = 1  # Default for variable-height items like elevators
        
        self.ghost_room = GhostRoom(tool_id, width, height)
        self.selected_tool = tool_id

    def _place_room(self):
        """
        Place the current ghost room if valid.
        Handles fund deduction, entity creation, and game state updates.
        """
        # Validation checks
        if not self.ghost_room:
            return
        
        # Perform a final, logged validation check before placing
        can_place_final, reason = self.validator.can_place(
            self.ghost_room.room_type,
            self.ghost_room.coordinate,
            self.ghost_room.width,
            self.ghost_room.height,
            log_attempt=True  # Enable logging for this specific attempt
        )
        
        if not can_place_final:
            print(f"❌ Cannot place {self.ghost_room.room_type} at {self.ghost_room.coordinate} - Reason: {reason}")
            # The ghost room is already red, so just returning is enough
            return
        
        # Get room type and entity data
        room_type = self.ghost_room.room_type
        entity_data = ENTITY_DATA.get(room_type)
        
        if not entity_data:
            print(f"❌ Unknown room type: {room_type}")
            return
        
        # Calculate cost
        cost = self._calculate_room_cost(room_type, entity_data)
        
        # Check if player has enough funds
        if self.funds < cost:
            print(f"❌ Insufficient funds! Cost: ${cost:,}, Available: ${self.funds:,}")
            return
        
        # Create the actual room entity
        new_room = self._create_room_entity(room_type, entity_data)
        
        if not new_room:
            print(f"❌ Failed to create room entity for {room_type}")
            return
        
        # Deduct funds
        self.funds -= cost
        print(f"✅ Placed {room_type.upper()} at {new_room.coordinate}")
        print(f"   Cost: ${cost:,} | Remaining funds: ${self.funds:,}")
        
        # Add room to game world
        self.rooms.append(new_room)
        
        # Update validator with new room list
        self.validator.update_rooms(self.rooms)
        
        # Clear ghost room and selection
        self.ghost_room = None
        self.selected_tool = None

    def _calculate_room_cost(self, room_type: str, entity_data: dict) -> int:
        """
        Calculate the cost to place a room.
        Some items have per-segment costs (lobby), others have fixed costs.
        """
        # Items with per-segment cost
        if room_type == 'lobby':
            return entity_data.get('cost_per_segment', 500) * self.ghost_room.width
        
        if room_type == 'elevator_shaft':
            # Cost: shaft cost + per-car cost
            shaft_cost = entity_data.get('cost_per_shaft', 200000)
            car_cost = entity_data.get('cost_per_car', 80000)
            default_cars = entity_data.get('cars_per_shaft_default', 1)
            return shaft_cost + (car_cost * default_cars)
        
        # Standard fixed cost
        return entity_data.get('cost', 0)

    def _create_room_entity(self, room_type: str, entity_data: dict) -> RoomEntity:
        """
        Create the appropriate room entity based on type.
        Uses factory pattern for different room types.
        """
        try:
            # Lobby - special handling
            if room_type == 'lobby':
                return Lobby(
                    coordinate=self.ghost_room.coordinate,
                    width=self.ghost_room.width
                )
            
            # Standard room entity
            color = entity_data.get('color', (200, 200, 200))
            cost = self._calculate_room_cost(room_type, entity_data)
            
            return RoomEntity(
                coordinate=self.ghost_room.coordinate,
                width=self.ghost_room.width,
                height=self.ghost_room.height,
                room_type=room_type,
                cost=cost,
                color=color
            )
        
        except Exception as e:
            print(f"Error creating room entity: {e}")
            return None

    def _update_ghost_room_position(self):
        """Update ghost room position based on current mouse position"""
        if not self.ghost_room:
            return
        
        # Get mouse position
        mouse_x, mouse_y = pygame.mouse.get_pos()
        
        # Convert to world coordinates
        world_x, world_y = self.camera.screen_to_world(mouse_x, mouse_y)
        
        # Update ghost room position
        self.ghost_room.update_position(world_x, world_y)
        
        # Validate placement
        can_place, reason = self.validator.can_place(
            self.ghost_room.room_type,
            self.ghost_room.coordinate,
            self.ghost_room.width,
            self.ghost_room.height
        )
        self.ghost_room.set_validity(can_place)

    def handle_events(self):
        """Handle user input and window events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_g:
                    self.show_grid = not self.show_grid
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    selected = self.toolbox.handle_click(mouse_x, mouse_y)
                    if selected:
                        self._create_ghost_room(selected)
                    elif self.ghost_room:
                        self._place_room()

    def update(self):
        """Update game logic"""
        keys = pygame.key.get_pressed()
        self.camera.handle_input(keys)
        self._update_ghost_room_position()

    def draw_grid(self):
        """Draw the grid overlay"""
        grid_color = (200, 200, 200)
        bright_grid_color = (220, 220, 220)
        
        # Draw vertical lines (segments)
        for seg in range(Grid.WIDTH + 1):
            world_x = seg * Grid.PIXELS_PER_SEGMENT
            screen_x, _ = self.camera.world_to_screen(world_x, 0)
            
            if 0 <= screen_x <= self.WIDTH:
                # Every 10th line is brighter
                color = bright_grid_color if seg % 10 == 0 else grid_color
                pygame.draw.line(self.screen, color, (screen_x, 0), (screen_x, self.HEIGHT), 1)
        
        # Draw horizontal lines (levels)
        for level in range(Grid.HEIGHT + 1):
            world_y = level * Grid.PIXELS_PER_LEVEL
            _, screen_y = self.camera.world_to_screen(0, world_y)
            
            if 0 <= screen_y <= self.HEIGHT:
                # Every 10th line is brighter
                color = bright_grid_color if level % 10 == 0 else grid_color
                pygame.draw.line(self.screen, color, (0, screen_y), (self.WIDTH, screen_y), 1)

    def draw_ground(self):
        """
        DEPRECATED: Level 0 is now reserved for LOBBY placement.
        Basement floors are created as room entities and drawn via draw_rooms().
        This method is kept for reference but no longer called.
        """
        pass

    def draw_rooms(self):
        """Draw all room entities"""
        for room in self.rooms:
            self.draw_room(room)

    def draw_room(self, room):
        """Draw a single room"""
        # Get room pixel bounds in world space
        world_x, world_y, width_px, height_px = room.get_pixel_bounds()
        
        # Convert to screen coordinates
        screen_x, screen_y = self.camera.world_to_screen(world_x, world_y)
        
        # Draw room rectangle
        pygame.draw.rect(
            self.screen,
            room.color,
            (screen_x, screen_y, width_px, height_px)
        )
        
        # Draw room border
        pygame.draw.rect(
            self.screen,
            (0, 0, 0),  # Black border
            (screen_x, screen_y, width_px, height_px),
            2
        )
        
        # Draw room label
        label_font = pygame.font.Font(None, 16)
        label = label_font.render(room.room_type.upper(), True, (255, 255, 255))
        label_rect = label.get_rect(center=(screen_x + width_px // 2, screen_y + height_px // 2))
        self.screen.blit(label, label_rect)


    def draw(self):
        """Render the game"""
        # Sky blue background
        self.screen.fill((135, 206, 235))
        
        # Draw all rooms (including basement floors)
        self.draw_rooms()
        
        # Draw ghost room if active
        if self.ghost_room:
            self.ghost_room.draw(self.screen, self.camera)
        
        # Draw grid if enabled
        if self.show_grid:
            self.draw_grid()
        
        # Draw UI (on top)
        self.status_bar.update(self.funds, self.population, self.star_rating)
        self.status_bar.draw(self.screen)
        
        self.toolbox.draw(self.screen, self.font)
        
        pygame.display.flip()

    def run(self):
        """Main game loop"""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(self.FPS)
        
        pygame.quit()
        sys.exit()


def main():
    """Create and run the application"""
    game = TowerSimulatorGame()
    game.run()


if __name__ == "__main__":
    main()
