# Copilot Instruction File — Sudoku App

## Project Overview
A desktop Sudoku game built with Python and tkinter. The app generates unique-solution puzzles,
supports difficulty levels, tracks time, stores a top-10 leaderboard in a local JSON file,
and offers dark/light mode toggling.

## Code Style
- Python 3.10+. Follow PEP 8: 4-space indents, snake_case for variables and functions, PascalCase for classes.
- Maximum line length: 100 characters.
- Use type hints on all function signatures.
- One class per file where possible; keep files under 300 lines.
- Prefer explicit over implicit. Avoid one-liners that sacrifice readability.

## Architecture
```
sudoku-app/
  main.py               # Entry point — creates Tk root, launches App
  instructions.md       # This file
  prompts.json          # Saved Copilot prompt templates
  sudoku/
    __init__.py
    generator.py        # Puzzle generation and unique-solution validation
    solver.py           # Backtracking solver (used by generator and Hint)
    ui.py               # Main App class and board rendering
    board.py            # Board state model (not UI)
    storage.py          # Leaderboard read/write to scores.json
    theme.py            # Color palettes for light and dark mode
  Screenshots/          # Copilot prompt screenshots, labeled descriptively
```

## Key Requirements (from rubric)
1. **Unique solution** — generate then verify exactly one solution before presenting puzzle.
2. **Difficulty** — Easy (≥45 clues), Medium (≥32), Hard (≥25). Adjust by removing cells after generating.
3. **Locked cells** — prefilled cells are read-only and styled differently.
4. **Conflict highlighting** — on every cell entry, mark row/col/box conflicts in red.
5. **Completion** — detect full valid board, show congratulations dialog, prompt for player name, save score.
6. **Hint** — fill one correct empty cell; lock it; increment hint counter.
7. **Check** — highlight all cells whose value differs from the solution in orange.
8. **Timer** — counts up in MM:SS, pauses on completion.
9. **Dark mode** — toggle button swaps entire palette; state persists in scores.json.
10. **Leaderboard** — top 10 by fastest time; stored in scores.json.

## Theming
- 3×3 boxes alternate between two background colors so the 9 boxes are visually distinct.
- Use `theme.py` for all color constants; never hard-code colors elsewhere.
- Light mode: white background, subtle box alternation. Dark mode: dark gray base, muted alternation.

## Error Handling
- Wrap file I/O (scores.json) in try/except; fall back to empty leaderboard on read errors.
- Catch and log exceptions in generator/solver; never let them silently corrupt board state.
- Validate all user inputs (name field, difficulty selection).

## Comments
- Add a one-line docstring to every class and public function.
- Use inline comments only when the logic is non-obvious (e.g., backtracking recursion, uniqueness check).

## Accessibility
- Minimum font size 12pt for all labels and grid cells.
- Keyboard navigation: Tab between cells, arrow keys to move, 1–9 to enter digits, Delete/Backspace to clear.
- High-contrast conflict colors that work in both light and dark mode.
- Sufficient contrast ratio for all text (target WCAG 2.1 AA).
