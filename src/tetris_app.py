import pygame
from constants import WIDTH, HEIGHT, GRID_SIZE, BLACK, SCORE_FILE
from tetris_board import TetrisBoard
from button import Button

class TetrisApp:
    """
    A Tetris game application class that manages game initialization, the game loop,
    user interactions, and transitioning between game states such as the main menu,
    game over, and playing states.
    """

    def __init__(self):
        """Initialize the Tetris game application."""
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Tetris Game")
        self.clock = pygame.time.Clock()
        self.running = True
        self.game = TetrisBoard(WIDTH // GRID_SIZE, HEIGHT // GRID_SIZE)
        self.fall_time = 0
        self.fall_speed = 100  # milliseconds
        self.highest_score = self.load_score()
        self.restart_button = Button(WIDTH - 110, 10, 100, 40, "Restart", (117, 113, 94))
        self.back_menu_button = Button(WIDTH - 270, 10, 150, 40, "Main Menu", (117, 113, 94))
        self.start_button = Button(WIDTH // 2 - 50, HEIGHT // 2, 100, 50, "Start", (0, 128, 0))
        self.show_menu = True
    
    def load_score(self):
        """Load the highest score from a file."""
        try:
            with open(SCORE_FILE, 'r') as file:
                return int(file.read())
        except FileNotFoundError:
            return 0
    
    def save_score(self):
        """Save the highest score to a file."""
        try:
            with open(SCORE_FILE, 'w') as file:
                file.write(str(max(self.game.score, self.highest_score)))
        except FileNotFoundError:
            pass
    
    def run(self):
        """Run the main game loop."""
        while self.running:
            if self.show_menu:
                self.main_menu()
            else:
                self.clock.tick(60)
                self.handle_events()
                self.update_game_state()
                self.draw()

    def handle_events(self):
        """Handle user input and system events."""
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.restart_button.is_over(mouse_pos) and not self.show_menu:
                    self.reset_game()
                elif self.back_menu_button.is_over(mouse_pos) and not self.show_menu:
                    self.show_menu = True  # Return to the main menu
                elif self.start_button.is_over(mouse_pos) and self.show_menu:
                    self.reset_game()

            elif event.type == pygame.KEYDOWN and not self.show_menu:
                self.handle_keydown(event)
    
    def handle_keydown(self, event):
        """Handle keyboard events for game controls."""
        if event.key == pygame.K_LEFT:
            self.game.move(-1, 0)
        elif event.key == pygame.K_RIGHT:
            self.game.move(1, 0)
        elif event.key == pygame.K_DOWN:
            self.game.move(0, 1)
        elif event.key == pygame.K_UP:
            self.game.rotate()

    def update_game_state(self):
        """Update the game state, including falling pieces and game over checks."""
        if not self.show_menu:
            self.fall_time += self.clock.get_rawtime()
            if self.fall_time > self.fall_speed:
                self.fall_time = 0
                self.game.update()

    def draw(self):
        """Draw the current game state to the screen."""
        self.screen.fill(BLACK)
        self.game.draw(self.screen)
        self.draw_score()
        if not self.show_menu:
            self.restart_button.draw(self.screen)
            self.back_menu_button.draw(self.screen)
        if self.game.game_over:
            self.draw_game_over()
            pygame.display.update()
            pygame.time.wait(2000)  # Wait for 2 seconds before showing the main menu
            self.show_menu = True
        pygame.display.update()

    def draw_score(self):
        """Draw the current score on the screen."""
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.game.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))

    def draw_game_over(self):
        """Display the game over message."""
        font = pygame.font.Font(None, 48)
        game_over_text = font.render("Game Over", True, (255, 0, 0))
        text_rect = game_over_text.get_rect(center=(WIDTH / 2, HEIGHT / 2))
        self.screen.blit(game_over_text, text_rect)

    def main_menu(self):
        """
        Display the main menu of the game. This includes the start button and the highest score.
        """
        self.screen.fill(BLACK)
        self.start_button.draw(self.screen)

        # Display the highest score in the main menu
        font = pygame.font.Font(None, 36)
        highest_score_text = font.render(f"Highest Score: {self.highest_score}", True, (255, 255, 255))
        score_text_rect = highest_score_text.get_rect(center=(WIDTH / 2, HEIGHT / 2 - 100))
        self.screen.blit(highest_score_text, score_text_rect)
        
        pygame.display.update()
        
        # Handle events in the main menu
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if self.start_button.is_over(mouse_pos):
                    self.reset_game()

    def reset_game(self):
        """
        Reset the game to its initial state. This is used for starting a new game from the main menu or restarting the game.
        """
        self.game = TetrisBoard(WIDTH // GRID_SIZE, HEIGHT // GRID_SIZE)
        self.fall_time = 0
        self.show_menu = False
        self.fall_speed = 100


