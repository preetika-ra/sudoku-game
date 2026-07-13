"""Sudoku solver using backtracking algorithm."""

from typing import Optional, List


class SudokuSolver:
    """Solves Sudoku puzzles using backtracking."""

    def __init__(self, board: List[List[int]]) -> None:
        """Initialize solver with a board copy."""
        self.board = [row[:] for row in board]
        self.solution = None

    def solve(self) -> Optional[List[List[int]]]:
        """Solve the Sudoku puzzle and return solution or None if unsolvable."""
        board_copy = [row[:] for row in self.board]
        if self._backtrack(board_copy):
            return board_copy
        return None

    def count_solutions(self, limit: int = 2) -> int:
        """Count number of solutions up to limit (stops early for efficiency)."""
        board_copy = [row[:] for row in self.board]
        count = [0]

        def backtrack(board: List[List[int]]) -> None:
            """Helper for counting solutions with early termination."""
            if count[0] > limit:
                return

            # Find next empty cell
            for row in range(9):
                for col in range(9):
                    if board[row][col] == 0:
                        for num in range(1, 10):
                            if self._is_valid(board, row, col, num):
                                board[row][col] = num
                                backtrack(board)
                                board[row][col] = 0
                        return

            # No empty cells found, puzzle is solved
            count[0] += 1

        backtrack(board_copy)
        return count[0]

    def _backtrack(self, board: List[List[int]]) -> bool:
        """Backtrack to solve puzzle."""
        # Find next empty cell
        for row in range(9):
            for col in range(9):
                if board[row][col] == 0:
                    for num in range(1, 10):
                        if self._is_valid(board, row, col, num):
                            board[row][col] = num
                            if self._backtrack(board):
                                return True
                            board[row][col] = 0
                    return False
        return True

    def _is_valid(self, board: List[List[int]], row: int, col: int,
                  num: int) -> bool:
        """Check if placing num at (row, col) is valid."""
        # Check row
        if num in board[row]:
            return False

        # Check column
        if num in [board[i][col] for i in range(9)]:
            return False

        # Check 3x3 box
        box_row, box_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(box_row, box_row + 3):
            for j in range(box_col, box_col + 3):
                if board[i][j] == num:
                    return False

        return True

    def get_conflicts(self, row: int, col: int, num: int) -> List[tuple]:
        """Get all cells that conflict with placing num at (row, col)."""
        conflicts = []
        if num == 0:
            return conflicts

        # Check row conflicts
        for c in range(9):
            if c != col and self.board[row][c] == num:
                conflicts.append((row, c))

        # Check column conflicts
        for r in range(9):
            if r != row and self.board[r][col] == num:
                conflicts.append((r, col))

        # Check 3x3 box conflicts
        box_row, box_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(box_row, box_row + 3):
            for j in range(box_col, box_col + 3):
                if (i != row or j != col) and self.board[i][j] == num:
                    conflicts.append((i, j))

        return conflicts
