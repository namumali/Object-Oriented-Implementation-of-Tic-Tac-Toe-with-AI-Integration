import pygame
import numpy as np

class Renderer:
    """Handles all rendering of the game elements."""
    
    def __init__(self, board_width, board_height, board_rows, board_cols, colors):
        """
        Initializes the Renderer object with game board dimensions, colors, and other properties.
        
        Args:
            board_width (int): The width of the game window.
            board_height (int): The height of the game window.
            board_rows (int): Number of rows on the Tic-Tac-Toe board.
            board_cols (int): Number of columns on the Tic-Tac-Toe board.
            colors (dict): A dictionary containing color mappings for different elements of the game.
        """
        self.board_width = board_width
        self.board_height = board_height
        self.board_rows = board_rows
        self.board_cols = board_cols
        self.colors = colors
        
        # Calculate the size of each square based on the board's dimensions
        self.square_size = min(self.board_width // self.board_cols, self.board_height // self.board_rows)
        
        # Define the radius for drawing the circle (for player X)
        self.circle_radius = self.square_size // 3
        
        # Define the width for drawing the circle and cross
        self.circle_width = 15
        self.cross_width = 25
        
        # Set up the Pygame window for rendering
        self.screen = pygame.display.set_mode((self.board_width, self.board_height))
        pygame.display.set_caption("AI-Based Tic Tac Toe")
        
        # Fill the screen with black color at the start
        self.screen.fill(self.colors['BLACK'])

    def _draw_grid(self):
        """
        Draws the grid lines for the Tic-Tac-Toe board.
        
        Horizontal and vertical lines separate the squares on the game board.
        """
        for i in range(1, self.board_rows):
            # Draw horizontal lines
            pygame.draw.line(
                self.screen, self.colors['WHITE'], 
                (0, self.square_size * i), 
                (self.board_width, self.square_size * i), 5
            )
        
        for i in range(1, self.board_cols):
            # Draw vertical lines
            pygame.draw.line(
                self.screen, self.colors['WHITE'], 
                (self.square_size * i, 0), 
                (self.square_size * i, self.board_height), 5
            )

    def _draw_figures(self, board):
        """
        Draws Xs (circles) and Os (crosses) on the game board.
        
        Args:
            board (ndarray): A 2D numpy array representing the Tic-Tac-Toe board.
        """
        for row in range(self.board_rows):
            for col in range(self.board_cols):
                # Draw a circle if the value is 1 (Human player - X)
                if board[row][col] == 1:
                    pygame.draw.circle(
                        self.screen, self.colors['WHITE'], 
                        (col * self.square_size + self.square_size // 2,
                         row * self.square_size + self.square_size // 2), 
                        self.circle_radius, self.circle_width
                    )
                # Draw a cross if the value is 2 (AI player - O)
                elif board[row][col] == 2:
                    pygame.draw.line(
                        self.screen, self.colors['WHITE'], 
                        (col * self.square_size + self.square_size // 4, 
                         row * self.square_size + self.square_size // 4), 
                        (col * self.square_size + 3 * self.square_size // 4, 
                         row * self.square_size + 3 * self.square_size // 4), 
                        self.cross_width
                    )
                    pygame.draw.line(
                        self.screen, self.colors['WHITE'], 
                        (col * self.square_size + self.square_size // 4, 
                         row * self.square_size + 3 * self.square_size // 4), 
                        (col * self.square_size + 3 * self.square_size // 4, 
                         row * self.square_size + self.square_size // 4), 
                         self.cross_width
                    )

    def _restart_game(self):
        """
        Restarts the game by resetting the board and clearing the screen.
        """
        self.screen.fill(self.colors['BLACK'])  # Clear the screen
        self._draw_grid()  # Redraw the grid

    def _update_dimensions(self, board_rows, board_cols):
        """
        Updates the board dimensions dynamically.
        
        Args:
            board_rows (int): Number of rows on the Tic-Tac-Toe board.
            board_cols (int): Number of columns on the Tic-Tac-Toe board.
        """
        self.board_rows = board_rows
        self.board_cols = board_cols
        self.square_size = min(self.board_width // self.board_cols, self.board_height // self.board_rows)
        self.circle_radius = self.square_size // 3
        self._restart_game()  # Clear and redraw the grid with updated dimensions
