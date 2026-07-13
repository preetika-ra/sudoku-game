"""Sudoku leaderboard storage and management."""

import json
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional
from pathlib import Path

logger = logging.getLogger(__name__)


class LeaderboardManager:
    """Manages Sudoku leaderboard with JSON storage."""

    def __init__(self, filepath: str = 'scores.json') -> None:
        """Initialize leaderboard manager.

        Args:
            filepath: Path to scores.json file
        """
        self.filepath = Path(filepath)
        self.data = self._load_data()

    def _load_data(self) -> Dict[str, Any]:
        """Load leaderboard from JSON file with fallback."""
        try:
            if self.filepath.exists():
                with open(self.filepath, 'r') as f:
                    data = json.load(f)
                    if 'scores' not in data:
                        data['scores'] = []
                    if 'dark_mode' not in data:
                        data['dark_mode'] = False
                    return data
        except (json.JSONDecodeError, IOError) as e:
            logger.warning(f"Failed to load scores: {e}. Using defaults.")

        return {'scores': [], 'dark_mode': False}

    def _save_data(self) -> None:
        """Save leaderboard to JSON file."""
        try:
            with open(self.filepath, 'w') as f:
                json.dump(self.data, f, indent=2)
        except IOError as e:
            logger.error(f"Failed to save scores: {e}")

    def save_score(self, name: str, time_seconds: int, difficulty: str,
                   hints: int) -> bool:
        """Save a new score to leaderboard.

        Args:
            name: Player name
            time_seconds: Time taken in seconds
            difficulty: 'easy', 'medium', or 'hard'
            hints: Number of hints used

        Returns:
            True if score was saved to top 10, False otherwise
        """
        # Validate inputs
        if not name or len(name.strip()) == 0:
            logger.warning("Empty player name")
            return False

        if time_seconds < 0:
            logger.warning(f"Invalid time: {time_seconds}")
            return False

        if difficulty not in ['easy', 'medium', 'hard']:
            logger.warning(f"Invalid difficulty: {difficulty}")
            return False

        # Create score entry
        score_entry = {
            'name': name.strip(),
            'time': time_seconds,
            'difficulty': difficulty,
            'hints': hints,
            'timestamp': datetime.now().isoformat()
        }

        self.data['scores'].append(score_entry)

        # Keep only top 10 by fastest time
        self.data['scores'].sort(key=lambda x: x['time'])
        if len(self.data['scores']) > 10:
            self.data['scores'] = self.data['scores'][:10]

        self._save_data()
        return True

    def get_leaderboard(self) -> List[Dict[str, Any]]:
        """Get top 10 scores.

        Returns:
            List of score entries, sorted by time (fastest first)
        """
        return self.data['scores'][:10]

    def format_leaderboard(self) -> str:
        """Format leaderboard for display.

        Returns:
            Formatted string of top 10 scores
        """
        scores = self.get_leaderboard()
        if not scores:
            return "No scores yet!"

        lines = ["TOP 10 SCORES\n" + "=" * 50]
        for i, score in enumerate(scores, 1):
            minutes, seconds = divmod(score['time'], 60)
            time_str = f"{minutes:02d}:{seconds:02d}"
            diff_str = score['difficulty'].upper()
            name = score['name'][:15]  # Limit name length
            line = (f"{i:2}. {name:15} {time_str}  "
                   f"{diff_str:6} (Hints: {score['hints']})")
            lines.append(line)

        return "\n".join(lines)

    def get_dark_mode(self) -> bool:
        """Get dark mode preference."""
        return self.data.get('dark_mode', False)

    def set_dark_mode(self, enabled: bool) -> None:
        """Set dark mode preference and save."""
        self.data['dark_mode'] = enabled
        self._save_data()

    def clear_leaderboard(self) -> None:
        """Clear all scores (for testing)."""
        self.data['scores'] = []
        self._save_data()
