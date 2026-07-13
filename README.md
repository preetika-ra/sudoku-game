# Sudoku App - GitHub Copilot Project

A desktop Sudoku game built with Python and tkinter, featuring unique-solution puzzle generation, difficulty levels, real-time timer, conflict highlighting, hint system, dark/light mode toggle, and a top-10 leaderboard with local JSON storage.

## Features

- **Puzzle Generation**: Generates Sudoku puzzles with exactly one unique solution
- **Difficulty Levels**: Easy (≥45 clues), Medium (≥32 clues), Hard (≥25 clues)
- **Real-time Feedback**: Immediate conflict highlighting on cell entry
- **Timer**: Tracks completion time in MM:SS format
- **Hint System**: Reveals one correct cell and locks it
- **Check Function**: Highlights incorrect cells in orange
- **Dark/Light Mode**: Toggle theme with persistent state
- **Leaderboard**: Top 10 scores by fastest time, stored in local JSON
- **Accessibility**: Keyboard navigation, high-contrast colors, minimum 12pt font

## Project Structure

```
sudoku-app/
├── main.py                 # Entry point
├── README.md              # This file
├── COPILOT_EVALUATION.md  # Critical evaluation of Copilot suggestions
├── instructions.md        # Development guidelines
├── prompts.json          # Saved Copilot prompt templates
├── scores.json           # Leaderboard data (auto-generated)
├── sudoku/
│   ├── __init__.py
│   ├── generator.py      # Puzzle generation and validation
│   ├── solver.py         # Backtracking solver
│   ├── board.py          # Board state model
│   ├── ui.py             # Main App class and UI rendering
│   ├── storage.py        # Leaderboard storage management
│   └── theme.py          # Color palettes
└── Screenshots/          # Feature and evaluation screenshots
```

## Getting Started

```bash
python main.py
```

## Requirements

- Python 3.10+
- tkinter (included with Python)

## Development Notes

See `COPILOT_EVALUATION.md` for documentation on critical evaluation of GitHub Copilot suggestions used in this project.