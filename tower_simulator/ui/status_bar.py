"""
Status bar UI for world details and information
"""
import pygame
from datetime import datetime


class StatusBar:
    """Top status bar showing funds, population, time, and ratings"""
    
    def __init__(self, screen_width: int, height: int = 50):
        """Initialize the status bar"""
        self.screen_width = screen_width
        self.height = height
        self.background_color = (100, 100, 100)
        self.text_color = (255, 255, 255)
        
        # Game state references (will be set by game)
        self.funds = 0
        self.population = 0
        self.rating = 1
        self.time_hour = 5
        self.time_minute = 0

    def update(self, funds: int, population: int, rating: int, hour: int = 5, minute: int = 0):
        """Update status bar values"""
        self.funds = funds
        self.population = population
        self.rating = rating
        self.time_hour = hour
        self.time_minute = minute

    def _format_time(self) -> str:
        """Format time as HH:MM AM/PM"""
        period = "AM" if self.time_hour < 12 else "PM"
        display_hour = self.time_hour if self.time_hour <= 12 else self.time_hour - 12
        if display_hour == 0:
            display_hour = 12
        return f"{display_hour:02d}:{self.time_minute:02d} {period}"

    def draw(self, surface: pygame.Surface):
        """Draw the status bar"""
        # Draw background
        pygame.draw.rect(surface, self.background_color, (0, 0, self.screen_width, self.height))
        pygame.draw.line(surface, (200, 200, 200), (0, self.height - 1), (self.screen_width, self.height - 1), 2)
        
        # Prepare text
        font = pygame.font.Font(None, 20)
        time_str = self._format_time()
        rating_str = '★' * self.rating
        
        status_text = f"Funds: ${self.funds:,}  |  Population: {self.population}  |  Rating: {rating_str}  |  Time: {time_str}"
        
        # Draw text
        text_surface = font.render(status_text, True, self.text_color)
        text_rect = text_surface.get_rect(center=(self.screen_width // 2, self.height // 2))
        surface.blit(text_surface, text_rect)

    def get_height(self) -> int:
        """Get the height of the status bar"""
        return self.height
