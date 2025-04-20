import pygame  # For initializing Pygame and handling the game window
import sys  # For handling system exit
import numpy as np  # For working with the board as a NumPy array
from renderer import Renderer  # Importing the Renderer class for visual representation
from logger import Logger  # Importing the Logger class to log moves
from minimax_ai import AI  # Importing the AI class to handle AI's logic
from humanPlayer import HumanPlayer  # Importing the HumanPlayer class to handle human player's moves
from aiPlayer import AIPlayer  # Importing the AIPlayer class for AI-controlled moves

class TicTacToe:
    def __init__(self):
        """Initialize the game with the chosen board size and necessary components."""
        self.board_size = self.get_board_size()  # Prompt the user to select the board size (3x3 or 5x5)
        self.square_size = 600 // self.board_size  # Dynamically adjust square size for rendering
        self.board = np.zeros((self.board_size, self.board_size), dtype=int)  # Initialize the board based on size
        
        # Initialize the AI with the correct board size (ensure it's an integer)
        self.ai = AI(self.board_size)  # Correctly passing the integer board size
        
        self.game_over = False  # This initializes the game_over attribute
        self.current_player_idx = 0  # This initializes the current player index
        
        # Initialize Renderer with the chosen board size
        self.renderer = Renderer(600, 600, self.board_size, self.board_size, {
            'WHITE': (255, 255, 255),
            'BLACK': (0, 0, 0),
            'RED': (250, 0, 0),
            'GREEN': (0, 255, 0),
        })

        # Initialize Logger
        self.logger = Logger()
        self.logger._set_board_size(self.board_size)  # Set the board size in the logger
        
        # Players: Human (symbol 1) and AI (symbol 2)
        self.players = [HumanPlayer(1), AIPlayer(2, self.board_size, self.logger)]  # Pass board_size and logger to AIPlayer

    def get_board_size(self):
        """Prompt the user to select the board size (3x3 or 5x5)."""
        while True:
            try:
                size = int(input("Choose board size: Enter 3 for 3x3 or 5 for 5x5: "))
                if size in [3, 5]:
                    return size
                else:
                    print("Invalid choice. Please enter 3 or 5.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")

    def play(self):
        """Main game loop where the game runs continuously until a player wins or a draw occurs."""
        while True:
            # Loop through all events in the Pygame window
            for event in pygame.event.get():
                # If the user closes the window, exit the game
                if event.type == pygame.QUIT:
                    sys.exit()

                # Check if 'r' key is pressed to restart the game
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    self.renderer._restart_game()  # Clear visual elements on the screen
                    self.board = np.zeros((self.board_size, self.board_size))  # Reset the board state
                    self.game_over = False  # Reset the game over flag
                    self.current_player_idx = 0  # Reset to the first player
                    self.logger._restart_round()  # Inform logger about the round restart
                    print("Game restarted!")

                # Only allow gameplay if the game is not over
                if not self.game_over:
                    current_player = self.players[self.current_player_idx]

                    # If it's the human player's turn
                    if isinstance(current_player, HumanPlayer):
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            mouseX, mouseY = event.pos
                            col = mouseX // self.square_size
                            row = mouseY // self.square_size

                            if self.board[row][col] == 0:
                                self.board[row][col] = current_player.symbol
                                position = row * self.board_size + col + 1
                                self.logger._log_move(position, current_player.symbol)

                                # Check for a win
                                if self.ai._check_win(self.board):
                                    print(f"Player {current_player.symbol} (Human) wins!")
                                    self.game_over = True
                                elif self.ai._is_board_full(self.board):
                                    print("It's a draw!")
                                    self.game_over = True
                                else:
                                    self.switch_player()

                    # If it's the AI player's turn
                    elif isinstance(current_player, AIPlayer):
                        move_made = current_player._make_move(self.board, self.logger, self.renderer)
                        if move_made:
                            # Check for a win
                            if self.ai._check_win(self.board):
                                print(f"Player {current_player.symbol} (AI) wins!")
                                self.game_over = True
                            elif self.ai._is_board_full(self.board):
                                print("It's a draw!")
                                self.game_over = True
                            else:
                                self.switch_player()

            # Render updates
            self.renderer.screen.fill(self.renderer.colors['BLACK'])
            self.renderer._draw_grid()
            self.renderer._draw_figures(self.board)
            pygame.display.update()

    def switch_player(self):
        """Switch between human and AI players."""
        self.current_player_idx = 1 - self.current_player_idx

# Main entry point for the game
if __name__ == "__main__":
    pygame.init()
    game = TicTacToe()
    game.play()
