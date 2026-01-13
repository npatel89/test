"""
Main game class for Tower Simulator
"""
import pygame
import sys


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
        self.font = pygame.font.Font(None, 48)
        
        print("Tower Simulator initialized!")
        print(f"Resolution: {self.WIDTH}x{self.HEIGHT}")
        print(f"FPS: {self.FPS}")

    def handle_events(self):
        """Handle user input and window events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

    def update(self):
        """Update game logic"""
        pass

    def draw(self):
        """Render the game"""
        # Sky blue background
        self.screen.fill((135, 206, 235))
        
        # Draw centered text
        text = self.font.render("TOWER SIMULATOR - Hello World!", True, (0, 0, 0))
        text_rect = text.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2))
        self.screen.blit(text, text_rect)
        
        # Draw subtitle
        small_font = pygame.font.Font(None, 24)
        subtitle = small_font.render("Press ESC to exit", True, (64, 64, 64))
        subtitle_rect = subtitle.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2 + 60))
        self.screen.blit(subtitle, subtitle_rect)
        
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
