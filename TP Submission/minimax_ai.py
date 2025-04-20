class AI:
    """AI logic for Tic-Tac-Toe, implementing the minimax algorithm with optimizations."""
    
    def __init__(self, board_size):
        """
        Initializes the AI with the given board size.
        
        Args:
            board_size (int): Size of the board (either 3 for 3x3 or 5 for 5x5).
        """
        if not isinstance(board_size, int):
            raise ValueError(f"board_size must be an integer, but got {type(board_size)}.")
        self.board_size = board_size
        self.depth_limit = 3 if board_size == 3 else 4  # Depth limit for faster AI moves
        self.max_depth = 5  # Max depth for iterative deepening

    def _update_board_size(self, new_size):
        """Updates the board size for the AI."""
        if not isinstance(new_size, int):
            raise ValueError(f"new_size must be an integer, but got {type(new_size)}.")
        self.board_size = new_size
        self.depth_limit = 3 if new_size == 3 else 4

    def _best_move(self, board):
        """Finds the best move for the AI using iterative deepening."""
        best_move = None
        best_score = -float('inf')
        
        for depth in range(1, self.max_depth + 1):  # Iterative deepening
            move, score = self._iterative_deepening(board, depth)
            if score > best_score:
                best_score = score
                best_move = move
        
        return best_move

    def _iterative_deepening(self, board, depth):
        """Perform the minimax search up to the specified depth."""
        best_move = None
        best_score = -float('inf')
        
        for row in range(self.board_size):
            for col in range(self.board_size):
                if board[row][col] == 0:  # Only consider empty spots
                    board[row][col] = 2  # AI's move
                    score = self._minimax(board, 0, False, -float('inf'), float('inf'), depth)
                    board[row][col] = 0  # Reset the spot
                    if score > best_score:
                        best_score = score
                        best_move = (row, col)
        
        return best_move, best_score

    def _minimax(self, board, depth, is_maximizing, alpha, beta, max_depth):
        """Minimax algorithm with alpha-beta pruning."""
        if depth >= max_depth:
            return self._evaluate_board(board)  # Use heuristic evaluation
        
        # Check for terminal conditions (win, loss, draw)
        winner = self._check_win(board)
        if winner == 2:  # AI wins
            return 10 - depth
        elif winner == 1:  # Human wins
            return depth - 10
        elif self._is_board_full(board):  # Draw
            return 0

        if is_maximizing:  # AI's turn
            best_score = -float('inf')
            for row in range(self.board_size):
                for col in range(self.board_size):
                    if board[row][col] == 0:
                        board[row][col] = 2  # AI's move
                        score = self._minimax(board, depth + 1, False, alpha, beta, max_depth)
                        board[row][col] = 0  # Reset the spot
                        best_score = max(score, best_score)
                        alpha = max(alpha, score)
                        if beta <= alpha:
                            break  # Prune the branch
            return best_score
        else:  # Human's turn
            best_score = float('inf')
            for row in range(self.board_size):
                for col in range(self.board_size):
                    if board[row][col] == 0:
                        board[row][col] = 1  # Human's move
                        score = self._minimax(board, depth + 1, True, alpha, beta, max_depth)
                        board[row][col] = 0  # Reset the spot
                        best_score = min(score, best_score)
                        beta = min(beta, score)
                        if beta <= alpha:
                            break  # Prune the branch
            return best_score

    def _evaluate_board(self, board):
        """Heuristic evaluation function to speed up the decision-making process."""
        score = 0
        # Check for immediate threats or opportunities (e.g., 2 in a row, 1 in a row)
        for row in range(self.board_size):
            for col in range(self.board_size):
                if board[row][col] == 2:  # AI's piece
                    score += 1
                elif board[row][col] == 1:  # Human's piece
                    score -= 1
        return score

    def _check_win(self, board):
        """Checks if there is a winner on the board."""
        for row in range(self.board_size):
            if all(board[row][col] == 2 for col in range(self.board_size)):  # AI wins
                return 2
            if all(board[row][col] == 1 for col in range(self.board_size)):  # Human wins
                return 1
        
        for col in range(self.board_size):
            if all(board[row][col] == 2 for row in range(self.board_size)):  # AI wins
                return 2
            if all(board[row][col] == 1 for row in range(self.board_size)):  # Human wins
                return 1
        
        if all(board[i][i] == 2 for i in range(self.board_size)):  # AI wins
            return 2
        if all(board[i][i] == 1 for i in range(self.board_size)):  # Human wins
            return 1
        
        if all(board[i][self.board_size - 1 - i] == 2 for i in range(self.board_size)):  # AI wins
            return 2
        if all(board[i][self.board_size - 1 - i] == 1 for i in range(self.board_size)):  # Human wins
            return 1
        
        return 0  # No winner yet

    def _is_board_full(self, board):
        """Checks if the board is full."""
        return all(board[row][col] != 0 for row in range(self.board_size) for col in range(self.board_size))
