"""
Toolbox UI panel for building tools
"""
import pygame
from tower_simulator.ui.button import Button
from tower_simulator.constants import ENTITY_DATA


class Toolbox:
    """Left-side toolbox panel with building tools"""
    
    def __init__(self, x: int = 10, y: int = 60, button_width: int = 80, button_height: int = 40):
        """Initialize the toolbox"""
        self.x = x
        self.y = y
        self.button_width = button_width
        self.button_height = button_height
        self.button_spacing = 10
        
        # Panel properties
        self.panel_width = button_width + 20
        self.background_color = (200, 200, 200)
        self.border_color = (0, 0, 0)
        
        # Create buttons for basic tools
        self.buttons = {}
        self._create_buttons()
        
        # Track selected tool
        self.selected_tool = None

    def _create_buttons(self):
        """Create tool buttons"""
        tools = [
            ('office', 'Office', (100, 150, 200)),
            ('condo', 'Condo', (200, 150, 100)),
            ('lobby', 'Lobby', (150, 100, 50)),
            ('elevator_shaft', 'Elevator', (100, 100, 100)),
        ]
        
        for i, (tool_id, label, color) in enumerate(tools):
            btn_y = self.y + i * (self.button_height + self.button_spacing)
            self.buttons[tool_id] = Button(
                x=self.x + 10,
                y=btn_y,
                width=self.button_width,
                height=self.button_height,
                text=label,
                color=color
            )

    def get_panel_rect(self) -> pygame.Rect:
        """Get the bounds of the toolbox panel"""
        return pygame.Rect(self.x, self.y, self.panel_width, self._get_panel_height())

    def _get_panel_height(self) -> int:
        """Calculate panel height based on number of buttons"""
        num_buttons = len(self.buttons)
        return num_buttons * self.button_height + (num_buttons - 1) * self.button_spacing + 20

    def handle_click(self, mouse_x: int, mouse_y: int) -> str | None:
        """Handle mouse click, return selected tool or None"""
        for tool_id, button in self.buttons.items():
            if button.contains_point(mouse_x, mouse_y):
                self.selected_tool = tool_id
                return tool_id
        return None

    def draw(self, surface: pygame.Surface, font: pygame.font.Font):
        """Draw the toolbox panel"""
        # Draw background panel
        panel_rect = self.get_panel_rect()
        pygame.draw.rect(surface, self.background_color, panel_rect)
        pygame.draw.rect(surface, self.border_color, panel_rect, 2)
        
        # Draw title
        title_font = pygame.font.Font(None, 18)
        title = title_font.render("TOOLS", True, (0, 0, 0))
        surface.blit(title, (self.x + 15, self.y + 5))
        
        # Draw buttons
        button_font = pygame.font.Font(None, 14)
        for tool_id, button in self.buttons.items():
            # Highlight selected button
            if tool_id == self.selected_tool:
                pygame.draw.rect(surface, (255, 255, 0), (button.x - 2, button.y - 2, button.width + 4, button.height + 4), 3)
            
            button.draw(surface, button_font)
