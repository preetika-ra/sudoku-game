"""Tests for Sudoku generator - ensures puzzles have exactly one unique solution."""

import pytest
from sudoku.generator import SudokuGenerator
from sudoku.solver import SudokuSolver


class TestSudokuGenerator:
    """Test suite for Sudoku puzzle generation."""

    def setup_method(self):
        """Set up test fixtures."""
        self.generator = SudokuGenerator()

    def test_generate_returns_puzzle_and_solution(self):
        """Test that generate() returns both puzzle and solution."""
        puzzle, solution = self.generator.generate('medium')
        assert puzzle is not None
        assert solution is not None
        assert len(puzzle) == 9
        assert len(solution) == 9

    def test_puzzle_has_correct_structure(self):
        """Test that generated puzzle has correct 9x9 grid structure."""
        puzzle, solution = self.generator.generate('medium')
        assert len(puzzle) == 9
        for row in puzzle:
            assert len(row) == 9
            for cell in row:
                assert 0 <= cell <= 9

    def test_solution_is_complete(self):
        """Test that solution has no empty cells."""
        puzzle, solution = self.generator.generate('medium')
        for row in solution:
            for cell in row:
                assert cell != 0, "Solution should have no empty cells"

    def test_solution_is_valid(self):
        """Test that solution is a valid Sudoku."""
        puzzle, solution = self.generator.generate('medium')
        # Check rows
        for row in solution:
            assert len(set(row)) == 9, "All rows should have 1-9"
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

    def test_puzzle_has_unique_solution(self):
        """Test that each generated puzzle has exactly one unique solution."""
        puzzle, solution = self.generator.generate('medium')
        solver = SudokuSolver(puzzle)
        num_solutions = solver.count_solutions(limit=2)
        assert num_solutions == 1, f"Puzzle should have exactly 1 solution, found {num_solutions}"

    def test_easy_difficulty_has_45_plus_clues(self):
        """Test that Easy difficulty leaves 45 or more clues."""
        puzzle, solution = self.generator.generate('easy')
        clue_count = sum(1 for row in puzzle for cell in row if cell != 0)
        assert clue_count >= 45, f"Easy should have 45+ clues, got {clue_count}"

    def test_medium_difficulty_has_32_plus_clues(self):
        """Test that Medium difficulty leaves 32 or more clues."""
        puzzle, solution = self.generator.generate('medium')
        clue_count = sum(1 for row in puzzle for cell in row if cell != 0)
        assert clue_count >= 32, f"Medium should have 32+ clues, got {clue_count}"

    def test_hard_difficulty_has_25_plus_clues(self):
        """Test that Hard difficulty leaves 25 or more clues."""
        puzzle, solution = self.generator.generate('hard')
        clue_count = sum(1 for row in puzzle for cell in row if cell != 0)
        assert clue_count >= 25, f"Hard should have 25+ clues, got {clue_count}"

    def test_easy_has_more_clues_than_medium(self):
        """Test that Easy has more clues than Medium."""
        puzzle_easy, _ = self.generator.generate('easy')
        puzzle_medium, _ = self.generator.generate('medium')
        clues_easy = sum(1 for row in puzzle_easy for cell in row if cell != 0)
        clues_medium = sum(1 for row in puzzle_medium for cell in row if cell != 0)
        assert clues_easy > clues_medium, "Easy should have more clues than Medium"

    def test_medium_has_more_clues_than_hard(self):
        """Test that Medium has more clues than Hard."""
        puzzle_medium, _ = self.generator.generate('medium')
        puzzle_hard, _ = self.generator.generate('hard')
        clues_medium = sum(1 for row in puzzle_medium for cell in row if cell != 0)
        clues_hard = sum(1 for row in puzzle_hard for cell in row if cell != 0)
        assert clues_medium > clues_hard, "Medium should have more clues than Hard"

    def test_puzzle_clues_match_solution_values(self):
        """Test that puzzle clues match their values in the solution."""
        puzzle, solution = self.generator.generate('medium')
        for row in range(9):
            for col in range(9):
                if puzzle[row][col] != 0:
                    assert puzzle[row][col] == solution[row][col], \
                        f"Puzzle clue at ({row},{col}) doesn't match solution"

    def test_invalid_difficulty_defaults_to_medium(self):
        """Test that invalid difficulty level defaults to medium."""
        puzzle, solution = self.generator.generate('impossible')
        clue_count = sum(1 for row in puzzle for cell in row if cell != 0)
        assert 32 <= clue_count <= 45, "Invalid difficulty should default to medium"
