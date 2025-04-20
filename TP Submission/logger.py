import os

class Logger:
    """Handles the logging of moves to a file."""

    def __init__(self):
        """Initializes the Logger object with an empty move log and sets the first round number."""
        self.move_log = []  # List to store the moves made during the game
        self.round_number = 1  # Initialize round number as 1
        self.new_round_started = True  # Always start with the first round header
        self.board_size = None  # Initially set to None, to be updated dynamically
        self._set_round_number()

    def _set_round_number(self):
        """Sets the round number by checking how many rounds are already logged in the file."""
        if os.path.exists("tictactoe.txt"):
            with open("tictactoe.txt", "r") as file:
                # Count how many rounds are already logged by looking for the "Round" keyword
                round_count = sum(1 for line in file if "Round" in line)
                self.round_number = round_count + 1  # Increment round number based on existing rounds

    def _log_move(self, position, player):
        """Logs the current move to a file in vertical format."""
        move = f"{'X' if player == 1 else 'O'}:{position}"
        self.move_log.append(move)

        # Open the file "tictactoe.txt" in append mode to log the moves
        with open("tictactoe.txt", "a") as file:
            # Write round header only if this is the first move of the new round
            if self.new_round_started:
                if self.board_size is not None:  # Check if board_size has been set
                    file.write(f"\nRound {self.round_number} (Board Size: {self.board_size}x{self.board_size}):\nX\tO\n")
                    self.new_round_started = False  # Reset the flag after writing header
                else:
                    raise ValueError("Board size is not set before logging the move.")

            # Log the current move
            if player == 1:  # Player 1 is 'X'
                file.write(f"{move}\t\n")
            else:  # Player 2 is 'O'
                file.write(f"\t{move}\n")

    def _set_board_size(self, size):
        """Sets the board size for logging purposes."""
        if size not in [3, 5]:  # Assuming valid sizes are only 3 and 5
            raise ValueError("Invalid board size. Only 3x3 or 5x5 boards are supported.")
        self.board_size = size  # Dynamically set the board size

    def _restart_round(self):
        """Restarts the round and prepares for a new round."""
        self.round_number += 1  # Increment round number
        self.move_log.clear()  # Clear the move log
        self.new_round_started = True  # Mark that a new round has started
