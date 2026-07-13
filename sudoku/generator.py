"""Sudoku puzzle generator."""

import random
from typing import List, Tuple
from sudoku.solver import SudokuSolver


class SudokuGenerator:
    """Generates Sudoku puzzles with difficulty levels."""

    DIFFICULTY_LEVELS = {
        'easy': 45,      # Leave 45+ clues
        'medium': 32,    # Leave 32+ clues
        'hard': 25       # Leave 25+ clues
    }

    def generate(self, difficulty: str = 'medium') -> Tuple[List[List[int]],
                                                             List[List[int]]]:
        """Generate a Sudoku puzzle with unique solution.

        Args:
            difficulty: 'easy', 'medium', or 'hard'

        Returns:
            Tuple of (puzzle, solution) both as 9x9 lists
        """
        if difficulty not in self.DIFFICULTY_LEVELS:
            difficulty = 'medium'

        # Generate complete solved board
        solution = self._generate_solution()
        puzzle = [row[:] for row in solution]

        # Remove cells based on difficulty
        target_clues = self.DIFFICULTY_LEVELS[difficulty]
        self._remove_cells(puzzle, solution, target_clues)

        return puzzle, solution

    def _generate_solution(self) -> List[List[int]]:
        """Generate a complete valid Sudoku solution."""
        board = [[0] * 9 for _ in range(9)]

        # Fill diagonal 3x3 boxes first (no conflicts possible)
        for box in range(3):
            nums = list(range(1, 10))
            random.shuffle(nums)
            for i in range(3):
                for j in range(3):
                    board[box * 3 + i][box * 3 + j] = nums[i * 3 + j]

        # Fill rest using backtracking
        solver = SudokuSolver(board)
        solver._backtrack(board)
        return board

    def _remove_cells(self, puzzle: List[List[int]],
                      solution: List[List[int]], min_clues: int) -> None:
        """Remove cells from puzzle ensuring unique solution.

        Args:
            puzzle: Board to remove cells from
            solution: Complete solution for verification
            min_clues: Minimum clues to keep
        """
        cells = [(r, c) for r in range(9) for c in range(9)]
        random.shuffle(cells)

        removed_count = 0
        target_removals = 81 - min_clues

        for row, col in cells:
            if removed_count >= target_removals:
                break

            if puzzle[row][col] == 0:
                continue

            # Try removing this cell
            original = puzzle[row][col]
            puzzle[row][col] = 0

            # Check uniqueness
            solver = SudokuSolver(puzzle)
            if solver.count_solutions(limit=2) == 1:
                removed_count += 1
            else:
                # Restore if creates multiple solutions
                puzzle[row][col] = original

    def _is_valid_placement(self, board: List[List[int]], row: int,
                            col: int, num: int) -> bool:
        """Check if placement is valid (no conflicts)."""
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
