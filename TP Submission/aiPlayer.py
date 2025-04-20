from player import Player
from minimax_ai import AI  # Importing the AI class that implements the minimax algorithm

class AIPlayer(Player):
    """
    Class representing an AI player in the game. This class extends the base Player interface 
    and provides a specific implementation for making an AI move based on the minimax algorithm.
    """

    def __init__(self, symbol, board_size, logger):
        """
        Initializes the AI player with the given symbol and board size.
        
        Args:
            symbol (int): The symbol of the AI player (1 or 2).
            board_size (int): Size of the Tic-Tac-Toe board (e.g., 3 for 3x3 or 5 for 5x5).
        """
        super().__init__(symbol)  # Initialize the base Player class
        self.board_size = board_size  # Store the board size for AI logic

    def _make_move(self, board, logger, renderer):
        """
        Handles the AI's move by calculating the best possible move using the minimax algorithm.
        The move is then logged and applied to the board.

        Args:
            board (list): The current Tic-Tac-Toe board (3x3 grid or larger).
            logger (Logger): An instance of the Logger class to log the moves.
            renderer (Renderer): An instance of the Renderer class (not used here, but passed for consistency).
        
        Returns:
            move (tuple or None): A tuple representing the row and column of the AI's move (if made), 
                                   or None if no valid move is made.
        """
        ai_helper = AI(self.board_size)  # Creating an instance of the AI helper class, which will compute the best move.
        move = ai_helper._best_move(board)  # Getting the best move from the AI helper.

        if move:  # If the AI has a valid move
            row, col = move
            board[row][col] = self.symbol  # Apply the AI's symbol to the board.
            
            # Log the move: The position calculation is now dynamic based on board size
            position = row * len(board) + col + 1  # Adjusting for dynamic board size
            logger._log_move(position, self.symbol)  # Log the move to the file

        return move  # Return the move that was made (row, col)
