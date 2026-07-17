"""Tests for Sudoku leaderboard storage - ensures top 10 scores are saved correctly."""

import pytest
import json
import tempfile
from pathlib import Path
from sudoku.storage import LeaderboardManager


class TestLeaderboardManager:
    """Test suite for leaderboard storage and management."""

    def setup_method(self):
        """Set up test fixtures with temporary file."""
        # Create temporary file for testing
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_file = Path(self.temp_dir.name) / "test_scores.json"
        self.manager = LeaderboardManager(str(self.temp_file))

    def teardown_method(self):
        """Clean up temporary files."""
        self.temp_dir.cleanup()

    def test_load_empty_leaderboard(self):
        """Test loading from non-existent file returns empty leaderboard."""
        scores = self.manager.get_leaderboard()
        assert scores == []

    def test_save_score(self):
        """Test saving a score to leaderboard."""
        result = self.manager.save_score("Alice", 120, "medium", 2)
        assert result is True
        scores = self.manager.get_leaderboard()
        assert len(scores) == 1
        assert scores[0]['name'] == "Alice"
        assert scores[0]['time'] == 120

    def test_save_multiple_scores(self):
        """Test saving multiple scores."""
        self.manager.save_score("Alice", 120, "medium", 2)
        self.manager.save_score("Bob", 100, "hard", 1)
        self.manager.save_score("Charlie", 150, "easy", 3)
        scores = self.manager.get_leaderboard()
        assert len(scores) == 3

    def test_scores_sorted_by_time(self):
        """Test that scores are sorted by fastest time."""
        self.manager.save_score("Charlie", 150, "medium", 1)
        self.manager.save_score("Alice", 100, "medium", 2)
        self.manager.save_score("Bob", 120, "medium", 3)
        scores = self.manager.get_leaderboard()
        assert scores[0]['name'] == "Alice"
        assert scores[1]['name'] == "Bob"
        assert scores[2]['name'] == "Charlie"

    def test_keep_only_top_10(self):
        """Test that only top 10 scores are kept."""
        # Add 15 scores
        for i in range(15):
            self.manager.save_score(f"Player{i}", 100 + i, "medium", 0)
        scores = self.manager.get_leaderboard()
        assert len(scores) == 10, "Should keep only top 10"

    def test_validate_empty_name(self):
        """Test that empty name is rejected."""
        result = self.manager.save_score("", 100, "medium", 1)
        assert result is False
        scores = self.manager.get_leaderboard()
        assert len(scores) == 0

    def test_validate_negative_time(self):
        """Test that negative time is rejected."""
        result = self.manager.save_score("Alice", -10, "medium", 1)
        assert result is False
        scores = self.manager.get_leaderboard()
        assert len(scores) == 0

    def test_validate_invalid_difficulty(self):
        """Test that invalid difficulty is rejected."""
        result = self.manager.save_score("Alice", 100, "extreme", 1)
        assert result is False
        scores = self.manager.get_leaderboard()
        assert len(scores) == 0

    def test_name_whitespace_trimmed(self):
        """Test that names have whitespace trimmed."""
        self.manager.save_score("  Alice  ", 100, "medium", 1)
        scores = self.manager.get_leaderboard()
        assert scores[0]['name'] == "Alice"

    def test_timestamp_recorded(self):
        """Test that timestamp is recorded with score."""
        self.manager.save_score("Alice", 100, "medium", 1)
        scores = self.manager.get_leaderboard()
        assert 'timestamp' in scores[0]
        assert scores[0]['timestamp'] is not None

    def test_format_leaderboard(self):
        """Test leaderboard formatting."""
        self.manager.save_score("Alice", 120, "medium", 2)
        self.manager.save_score("Bob", 100, "hard", 1)
        formatted = self.manager.format_leaderboard()
        assert "TOP 10 SCORES" in formatted
        assert "Alice" in formatted
        assert "Bob" in formatted
        assert "120" in formatted or "02:00" in formatted

    def test_empty_leaderboard_format(self):
        """Test formatting empty leaderboard."""
        formatted = self.manager.format_leaderboard()
        assert "No scores yet" in formatted

    def test_dark_mode_persistence(self):
        """Test that dark mode setting persists."""
        self.manager.set_dark_mode(True)
        dark_mode = self.manager.get_dark_mode()
        assert dark_mode is True

    def test_dark_mode_toggle(self):
        """Test toggling dark mode."""
        assert self.manager.get_dark_mode() is False
        self.manager.set_dark_mode(True)
        assert self.manager.get_dark_mode() is True
        self.manager.set_dark_mode(False)
        assert self.manager.get_dark_mode() is False

    def test_persist_data_across_instances(self):
        """Test that data persists across LeaderboardManager instances."""
        self.manager.save_score("Alice", 100, "medium", 1)
        # Create new instance with same file
        manager2 = LeaderboardManager(str(self.temp_file))
        scores = manager2.get_leaderboard()
        assert len(scores) == 1
        assert scores[0]['name'] == "Alice"

    def test_corrupted_json_fallback(self):
        """Test that corrupted JSON file falls back to empty leaderboard."""
        # Write invalid JSON
        with open(self.temp_file, 'w') as f:
            f.write("{ invalid json")
        # Load should not crash
        manager = LeaderboardManager(str(self.temp_file))
        scores = manager.get_leaderboard()
        assert scores == []

    def test_clear_leaderboard(self):
        """Test clearing leaderboard (for testing purposes)."""
        self.manager.save_score("Alice", 100, "medium", 1)
        self.manager.save_score("Bob", 120, "hard", 2)
        assert len(self.manager.get_leaderboard()) == 2
        self.manager.clear_leaderboard()
        assert len(self.manager.get_leaderboard()) == 0
