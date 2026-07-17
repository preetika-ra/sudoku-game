"""Tests for Sudoku board model - ensures board state management works correctly."""

import pytest
from sudoku.board import SudokuBoard


class TestSudokuBoard:
    """Test suite for Sudoku board state management."""

    def setup_method(self):
        """Set up test fixtures."""
        # Simple puzzle
        self.puzzle = [
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
        
        # Solution
        self.solution = [
            [5, 3, 4, 6, 7, 8, 9, 1, 2],
            [6, 7, 2, 1, 9, 5, 3, 4, 8],
            [1, 9, 8, 3, 4, 2, 5, 6, 7],
            [8, 5, 9, 7, 6, 1, 4, 2, 3],
            [4, 2, 6, 8, 5, 3, 7, 9, 1],
            [7, 1, 3, 9, 2, 4, 8, 5, 6],
            [9, 6, 1, 5, 3, 7, 2, 8, 4],
            [2, 8, 7, 4, 1, 9, 6, 3, 5],
            [3, 4, 5, 2, 8, 6, 1, 7, 9]
        ]
        
        self.board = SudokuBoard(self.puzzle, self.solution)

    def test_board_initialization(self):
        """Test that board initializes correctly."""
        assert self.board.board is not None
        assert self.board.solution is not None
        assert len(self.board.board) == 9

    def test_initial_cells_are_locked(self):
        """Test that initial puzzle cells are locked."""
        assert self.board.is_locked(0, 0), "(0,0) with value 5 should be locked"
        assert self.board.is_locked(0, 1), "(0,1) with value 3 should be locked"
        assert not self.board.is_locked(0, 2), "(0,2) with value 0 should not be locked"

    def test_set_cell_on_unlocked_position(self):
        """Test setting value on unlocked cell."""
        result = self.board.set_cell(0, 2, 4)
        assert result is True
        assert self.board.get_cell(0, 2) == 4

    def test_set_cell_on_locked_position_fails(self):
        """Test that setting value on locked cell fails."""
        result = self.board.set_cell(0, 0, 9)
        assert result is False
        assert self.board.get_cell(0, 0) == 5, "Locked cell should not change"

    def test_clear_cell(self):
        """Test clearing a cell."""
        self.board.set_cell(0, 2, 4)
        result = self.board.clear_cell(0, 2)
        assert result is True
        assert self.board.get_cell(0, 2) == 0

    def test_clear_locked_cell_fails(self):
        """Test that clearing locked cell fails."""
        result = self.board.clear_cell(0, 0)
        assert result is False
        assert self.board.get_cell(0, 0) == 5

    def test_get_conflicts_row(self):
        """Test conflict detection in row."""
        self.board.set_cell(0, 2, 5)  # Duplicate 5 in row 0
        conflicts = self.board.get_conflicts(0, 2)
        assert (0, 0) in conflicts, "Should detect conflict with (0,0)"
        assert (0, 2) in conflicts, "Cell itself should be in conflicts"

    def test_get_conflicts_column(self):
        """Test conflict detection in column."""
        self.board.set_cell(1, 0, 5)  # Duplicate 5 in column 0
        conflicts = self.board.get_conflicts(1, 0)
        assert (0, 0) in conflicts, "Should detect conflict with (0,0)"

    def test_get_conflicts_box(self):
        """Test conflict detection in 3x3 box."""
        self.board.set_cell(1, 1, 5)  # Duplicate 5 in box
        conflicts = self.board.get_conflicts(1, 1)
        assert (0, 0) in conflicts, "Should detect conflict with (0,0)"

    def test_no_conflicts_when_valid(self):
        """Test that valid placement has no conflicts."""
        self.board.set_cell(0, 2, 4)  # Valid number
        conflicts = self.board.get_conflicts(0, 2)
        # Only the cell itself, no other conflicts
        assert len(conflicts) == 0 or len(conflicts) == 1

    def test_get_errors(self):
        """Test error detection (wrong values)."""
        self.board.set_cell(0, 2, 9)  # Wrong value (should be 4)
        errors = self.board.get_errors()
        assert (0, 2) in errors, "Should detect error at (0,2)"

    def test_is_complete_when_empty(self):
        """Test is_complete returns False for partially filled board."""
        assert not self.board.is_complete(), "Board with zeros is not complete"

    def test_is_complete_when_full(self):
        """Test is_complete returns True when all cells filled."""
        # Fill the board completely
        for r in range(9):
            for c in range(9):
                if self.board.board[r][c] == 0:
                    self.board.set_cell(r, c, self.solution[r][c])
        assert self.board.is_complete(), "Filled board should be complete"

    def test_is_solved_correct(self):
        """Test is_solved when board matches solution."""
        # Fill with correct solution
        for r in range(9):
            for c in range(9):
                if self.board.board[r][c] == 0:
                    self.board.set_cell(r, c, self.solution[r][c])
        assert self.board.is_solved(), "Correctly filled board should be solved"

    def test_is_solved_incorrect(self):
        """Test is_solved when board has wrong values."""
        self.board.set_cell(0, 2, 9)  # Wrong value
        for r in range(9):
            for c in range(9):
                if self.board.board[r][c] == 0 and (r != 0 or c != 2):
                    self.board.set_cell(r, c, self.solution[r][c])
        assert not self.board.is_solved(), "Board with errors should not be solved"

    def test_get_candidates(self):
        """Test getting valid candidates for a cell."""
        candidates = self.board.get_candidates(0, 2)
        assert 5 not in candidates, "5 already in row"
        assert 3 not in candidates, "3 already in row"
        assert 4 in candidates, "4 should be valid candidate"

    def test_get_hint(self):
        """Test getting a hint."""
        hint = self.board.get_hint()
        assert hint is not None
        row, col, value = hint
        assert 0 <= row < 9
        assert 0 <= col < 9
        assert 1 <= value <= 9
        assert value == self.solution[row][col]

    def test_board_copy_independence(self):
        """Test that board copy is independent from puzzle."""
        self.board.set_cell(0, 2, 4)
        # Puzzle should remain unchanged
        assert self.puzzle[0][2] == 0, "Original puzzle should not be modified"
