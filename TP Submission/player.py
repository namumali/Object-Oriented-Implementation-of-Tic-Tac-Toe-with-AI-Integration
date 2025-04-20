class Player:
    """
    Interface declaring the basic functionality for a TicTacToe player.
    """
    def __init__(self, symbol):
        """
        Initializes a player with a given symbol ('X' or 'O').
        Args:
            symbol (int): 1 for 'X' (human), 2 for 'O' (AI).
        """
        self.symbol = symbol

    def _make_move(self, board, logger, renderer):
        """
        Abstract method for making a move.
        Args:
            board (list): The TicTacToe board.
            logger (Logger): The Logger instance.
            renderer (Renderer): The Renderer instance for display of the game window.
        """
        raise NotImplementedError("This method should be implemented by subclasses of human and AI player.")
