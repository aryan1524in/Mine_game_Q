import pygame
import random
import sys
import time
from pygame.locals import *

# Initialize pygame
pygame.init()

# Constants
WINDOW_SIZE = 500
GRID_SIZE = 5
CELL_SIZE = 80
MARGIN = 20
BUTTON_HEIGHT = 50
BUTTON_WIDTH = 150
BUTTON_MARGIN = 10

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Game settings
MINE_COUNT = 5
MINE_VALUE = -10
SAFE_MIN_VALUE = 1
SAFE_MAX_VALUE = 5

class MinesGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE + BUTTON_HEIGHT + BUTTON_MARGIN * 2))
        pygame.display.set_caption('Mines Game')
        self.font = pygame.font.SysFont('Arial', 24)
        self.small_font = pygame.font.SysFont('Arial', 18)
        
        self.reset_game()
    
    def reset_game(self):
        # Game state
        self.grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.revealed = [[False for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.game_over = False
        self.score = 0
        
        # Place mines and values
        self.place_mines()
        self.place_values()
    
    def place_mines(self):
        # Place MINE_COUNT mines randomly
        mines_placed = 0
        while mines_placed < MINE_COUNT:
            x = random.randint(0, GRID_SIZE - 1)
            y = random.randint(0, GRID_SIZE - 1)
            if self.grid[y][x] != MINE_VALUE:
                self.grid[y][x] = MINE_VALUE
                mines_placed += 1
    
    def place_values(self):
        # Place random values in non-mine cells
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                if self.grid[y][x] != MINE_VALUE:
                    self.grid[y][x] = random.randint(SAFE_MIN_VALUE, SAFE_MAX_VALUE)
    
    def reveal_cell(self, x, y):
        if not self.revealed[y][x] and not self.game_over:
            self.revealed[y][x] = True
            
            if self.grid[y][x] == MINE_VALUE:
                self.game_over = True
                return False
            else:
                self.score += self.grid[y][x]
                return True
        return None
    
    def cash_out(self):
        if not self.game_over:
            self.save_score()
            self.game_over = True
            return True
        return False
    
    def save_score(self):
        # Save score to a file with timestamp
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        with open("mines_scores.txt", "a") as f:
            f.write(f"{timestamp}: {self.score}\n")
    
    def draw(self):
        self.screen.fill(WHITE)
        
        # Draw grid
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                rect = pygame.Rect(
                    MARGIN + x * (CELL_SIZE + MARGIN),
                    MARGIN + y * (CELL_SIZE + MARGIN),
                    CELL_SIZE,
                    CELL_SIZE
                )
                
                if self.revealed[y][x]:
                    if self.grid[y][x] == MINE_VALUE:
                        # Draw mine
                        pygame.draw.rect(self.screen, RED, rect)
                        text = self.font.render("MINE", True, WHITE)
                    else:
                        # Draw value
                        pygame.draw.rect(self.screen, GREEN, rect)
                        text = self.font.render(str(self.grid[y][x]), True, BLACK)
                    
                    text_rect = text.get_rect(center=rect.center)
                    self.screen.blit(text, text_rect)
                else:
                    # Draw unrevealed cell
                    pygame.draw.rect(self.screen, GRAY, rect)
                
                # Draw cell border
                pygame.draw.rect(self.screen, BLACK, rect, 2)
        
        # Draw cash out button
        button_rect = pygame.Rect(
            (WINDOW_SIZE - BUTTON_WIDTH) // 2,
            WINDOW_SIZE - BUTTON_HEIGHT - BUTTON_MARGIN,
            BUTTON_WIDTH,
            BUTTON_HEIGHT
        )
        pygame.draw.rect(self.screen, BLUE, button_rect)
        pygame.draw.rect(self.screen, BLACK, button_rect, 2)
        
        button_text = self.font.render("CASH OUT", True, WHITE)
        button_text_rect = button_text.get_rect(center=button_rect.center)
        self.screen.blit(button_text, button_text_rect)
        
        # Draw score
        score_text = self.font.render(f"Score: {self.score}", True, BLACK)
        self.screen.blit(score_text, (MARGIN, WINDOW_SIZE - BUTTON_HEIGHT - BUTTON_MARGIN))
        
        # Draw game over message if applicable
        if self.game_over:
            overlay = pygame.Surface((WINDOW_SIZE, WINDOW_SIZE))
            overlay.set_alpha(150)
            overlay.fill(BLACK)
            self.screen.blit(overlay, (0, 0))
            
            if self.score > 0:
                message = f"Game Over! Final Score: {self.score}"
            else:
                message = "Game Over! You hit a mine!"
                
            game_over_text = self.font.render(message, True, WHITE)
            game_over_rect = game_over_text.get_rect(center=(WINDOW_SIZE // 2, WINDOW_SIZE // 2))
            self.screen.blit(game_over_text, game_over_rect)
            
            restart_text = self.small_font.render("Press R to restart", True, WHITE)
            restart_rect = restart_text.get_rect(center=(WINDOW_SIZE // 2, WINDOW_SIZE // 2 + 40))
            self.screen.blit(restart_text, restart_rect)
    
    def run(self):
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                
                elif event.type == KEYDOWN:
                    if event.key == K_r and self.game_over:
                        self.reset_game()
                
                elif event.type == MOUSEBUTTONDOWN and event.button == 1:  # Left click
                    x, y = event.pos
                    
                    # Check if click is on the grid
                    grid_x = (x - MARGIN) // (CELL_SIZE + MARGIN)
                    grid_y = (y - MARGIN) // (CELL_SIZE + MARGIN)
                    
                    if 0 <= grid_x < GRID_SIZE and 0 <= grid_y < GRID_SIZE:
                        self.reveal_cell(grid_x, grid_y)
                    
                    # Check if click is on cash out button
                    button_rect = pygame.Rect(
                        (WINDOW_SIZE - BUTTON_WIDTH) // 2,
                        WINDOW_SIZE - BUTTON_HEIGHT - BUTTON_MARGIN,
                        BUTTON_WIDTH,
                        BUTTON_HEIGHT
                    )
                    
                    if button_rect.collidepoint(event.pos):
                        self.cash_out()
            
            self.draw()
            pygame.display.flip()
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = MinesGame()
    game.run()
