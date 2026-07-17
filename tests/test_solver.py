"""Tests for Sudoku solver - ensures backtracking algorithm works correctly."""

import pytest
from sudoku.solver import SudokuSolver


class TestSudokuSolver:
    """Test suite for Sudoku solver."""

    def setup_method(self):
        """Set up test fixtures."""
        # Simple valid puzzle with unique solution
        self.valid_puzzle = [
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9]
        ]
        
        # Completely empty puzzle
        self.empty_puzzle = [[0] * 9 for _ in range(9)]
        
        # Invalid puzzle (two 5's in first row)
        self.invalid_puzzle = [
            [5, 5, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9]
        ]

    def test_solve_valid_puzzle(self):
        """Test that solver can solve a valid puzzle."""
        solver = SudokuSolver(self.valid_puzzle)
        solution = solver.solve()
        assert solution is not None, "Valid puzzle should have a solution"
        
        # Check that solution is complete
        for row in solution:
            for cell in row:
                assert cell != 0, "Solution should have no empty cells"

    def test_solved_puzzle_is_valid(self):
        """Test that solved puzzle contains only 1-9 with no duplicates."""
        solver = SudokuSolver(self.valid_puzzle)
        solution = solver.solve()
        
        # Check rows
        for row in solution:
            assert len(set(row)) == 9
            assert set(row) == set(range(1, 10))
        
        # Check columns
        for col in range(9):
            column = [solution[row][col] for row in range(9)]
            assert set(column) == set(range(1, 10))
        
        # Check 3x3 boxes
        for box_row in range(0, 9, 3):
            for box_col in range(0, 9, 3):
                box = []
                for i in range(3):
                    for j in range(3):
                        box.append(solution[box_row + i][box_col + j])
                assert set(box) == set(range(1, 10))

    def test_invalid_puzzle_returns_none(self):
        """Test that unsolvable puzzle returns None."""
        solver = SudokuSolver(self.invalid_puzzle)
        solution = solver.solve()
        assert solution is None, "Invalid puzzle should return None"

    def test_count_solutions_single_solution(self):
        """Test that puzzle with unique solution counts as 1."""
        solver = SudokuSolver(self.valid_puzzle)
        count = solver.count_solutions(limit=2)
        assert count == 1, "Valid puzzle should have exactly 1 solution"

    def test_count_solutions_early_termination(self):
        """Test that count_solutions stops after finding limit."""
        # Empty puzzle has many solutions
        solver = SudokuSolver(self.empty_puzzle)
        count = solver.count_solutions(limit=2)
        # Should stop at limit=2, so count <= 2
        assert count <= 2, "Should stop counting at limit"

    def test_is_valid_placement(self):
        """Test placement validation."""
        solver = SudokuSolver(self.valid_puzzle)
        # Row 0, Col 2 is empty in valid_puzzle
        # Should be valid to place numbers not in row 0
        assert solver._is_valid(self.valid_puzzle, 0, 2, 1) or \
               solver._is_valid(self.valid_puzzle, 0, 2, 2) or \
               solver._is_valid(self.valid_puzzle, 0, 2, 4)

    def test_get_conflicts(self):
        """Test conflict detection."""
        solver = SudokuSolver(self.valid_puzzle)
        # In row 0, we have [5, 3, 0, 0, 7, 0, 0, 0, 0]
        # Placing another 5 at position (0, 2) should conflict with (0, 0)
        conflicts = solver.get_conflicts(0, 2, 5)
        assert (0, 0) in conflicts, "Should detect conflict with (0, 0)"

    def test_solver_preserves_original_board(self):
        """Test that solver doesn't modify original puzzle."""
        original = [row[:] for row in self.valid_puzzle]
        solver = SudokuSolver(self.valid_puzzle)
        solution = solver.solve()
        # Original should be unchanged
        assert self.valid_puzzle == original, "Solver should not modify original puzzle"
