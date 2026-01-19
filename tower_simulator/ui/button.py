"""
UI Button class for tower simulator
"""
import pygame
from dataclasses import dataclass


@dataclass
class Button:
    """Represents a clickable button in the UI"""
    x: int
    y: int
    width: int
    height: int
    text: str
    color: tuple  # RGB
    text_color: tuple = (255, 255, 255)
    
    def contains_point(self, px: int, py: int) -> bool:
        """Check if point (px, py) is within button bounds"""
        return (self.x <= px <= self.x + self.width and 
                self.y <= py <= self.y + self.height)
    
    def draw(self, surface: pygame.Surface, font: pygame.font.Font):
        """Draw the button on the given surface"""
        # Draw button rectangle
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))
        
        # Draw button border
        pygame.draw.rect(surface, (0, 0, 0), (self.x, self.y, self.width, self.height), 2)
        
        # Draw text
        text_surface = font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
        surface.blit(text_surface, text_rect)
