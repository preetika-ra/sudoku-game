"""Sudoku puzzle board model."""

from typing import List, Set, Tuple, Optional
from sudoku.solver import SudokuSolver


class SudokuBoard:
    """Represents a Sudoku board state and logic."""

    def __init__(self, puzzle: List[List[int]], solution: List[List[int]]) -> None:
        """Initialize board with puzzle and solution.

        Args:
            puzzle: 9x9 grid with clues (0 = empty)
            solution: 9x9 grid with complete solution
        """
        self.puzzle = [row[:] for row in puzzle]
        self.board = [row[:] for row in puzzle]
        self.solution = [row[:] for row in solution]
        self.initial_cells = self._get_initial_cells()

    def _get_initial_cells(self) -> Set[Tuple[int, int]]:
        """Get set of initially filled cell coordinates."""
        return {(r, c) for r in range(9) for c in range(9)
                if self.puzzle[r][c] != 0}

    def set_cell(self, row: int, col: int, num: int) -> bool:
        """Set cell value. Return False if cell is locked (initial)."""
        if (row, col) in self.initial_cells:
            return False
        self.board[row][col] = num
        return True

    def get_cell(self, row: int, col: int) -> int:
        """Get cell value."""
        return self.board[row][col]

    def is_locked(self, row: int, col: int) -> bool:
        """Check if cell is locked (initial clue)."""
        return (row, col) in self.initial_cells

    def get_conflicts(self, row: int, col: int) -> Set[Tuple[int, int]]:
        """Get all cells that conflict with current cell value."""
        conflicts: Set[Tuple[int, int]] = set()
        num = self.board[row][col]

        if num == 0:
            return conflicts

        # Check row
        for c in range(9):
            if c != col and self.board[row][c] == num:
                conflicts.add((row, c))
        conflicts.add((row, col))

        # Check column
        for r in range(9):
            if r != row and self.board[r][col] == num:
                conflicts.add((r, col))
        conflicts.add((row, col))

        # Check 3x3 box
        box_row, box_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(box_row, box_row + 3):
            for j in range(box_col, box_col + 3):
                if (i != row or j != col) and self.board[i][j] == num:
                    conflicts.add((i, j))
        conflicts.add((row, col))

        return conflicts

    def get_errors(self) -> Set[Tuple[int, int]]:
        """Get all cells with wrong values (differ from solution)."""
        errors: Set[Tuple[int, int]] = set()
        for r in range(9):
            for c in range(9):
                if self.board[r][c] != 0 and self.board[r][c] != self.solution[r][c]:
                    errors.add((r, c))
        return errors

    def is_complete(self) -> bool:
        """Check if board is completely filled."""
        return all(self.board[r][c] != 0 for r in range(9) for c in range(9))

    def is_valid(self) -> bool:
        """Check if current board state is valid (no conflicts)."""
        for r in range(9):
            for c in range(9):
                if self.board[r][c] != 0:
                    if len(self.get_conflicts(r, c)) > 1:
                        return False
        return True

    def is_solved(self) -> bool:
        """Check if board is correctly solved."""
        if not self.is_complete():
            return False
        return all(self.board[r][c] == self.solution[r][c]
                   for r in range(9) for c in range(9))

    def clear_cell(self, row: int, col: int) -> bool:
        """Clear cell. Return False if cell is locked."""
        if (row, col) in self.initial_cells:
            return False
        self.board[row][col] = 0
        return True

    def get_candidates(self, row: int, col: int) -> Set[int]:
        """Get valid candidates for a cell."""
        if self.board[row][col] != 0 or (row, col) in self.initial_cells:
            return set()

        candidates = set(range(1, 10))

        # Remove numbers in same row
        candidates -= set(self.board[row])

        # Remove numbers in same column
        candidates -= {self.board[r][col] for r in range(9)}

        # Remove numbers in same 3x3 box
        box_row, box_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(box_row, box_row + 3):
            for j in range(box_col, box_col + 3):
                candidates.discard(self.board[i][j])

        return candidates

    def get_hint(self) -> Optional[Tuple[int, int, int]]:
        """Get a hint: (row, col, correct_value) or None if board complete."""
        for r in range(9):
            for c in range(9):
                if self.board[r][c] == 0 and (r, c) not in self.initial_cells:
                    return (r, c, self.solution[r][c])
        return None
