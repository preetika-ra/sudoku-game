"""Main Sudoku application UI."""

import tkinter as tk
from tkinter import simpledialog, messagebox
import logging
from typing import Optional, Dict, Set, Tuple
from sudoku.board import SudokuBoard
from sudoku.generator import SudokuGenerator
from sudoku.storage import LeaderboardManager
from sudoku.theme import Theme

logger = logging.getLogger(__name__)


class SudokuApp(tk.Tk):
    """Main Sudoku application."""

    def __init__(self) -> None:
        """Initialize the Sudoku app."""
        super().__init__()

        self.title("Sudoku Game")
        self.geometry("700x900")
        self.resizable(False, False)

        # Initialize managers
        self.leaderboard = LeaderboardManager()
        self.dark_mode = self.leaderboard.get_dark_mode()
        self.generator = SudokuGenerator()

        # Game state
        self.board: Optional[SudokuBoard] = None
        self.selected_cell: Optional[Tuple[int, int]] = None
        self.conflicts: Set[Tuple[int, int]] = set()
        self.errors: Set[Tuple[int, int]] = set()
        self.highlighted_number: Optional[int] = None
        self.game_active = False
        self.hint_count = 0
        self.time_elapsed = 0
        self.difficulty = 'medium'

        # UI elements
        self.cells = {}
        self.timer_label: Optional[tk.Label] = None
        self.hint_label: Optional[tk.Label] = None
        self.difficulty_var = tk.StringVar(value='medium')

        # Setup UI
        self._setup_ui()
        self._new_game()

        # Bind keyboard events
        self.bind('<Key>', self._on_key_press)
        self.bind('<FocusIn>', self._on_window_focus)

    def _setup_ui(self) -> None:
        """Set up the user interface."""
        # Main container
        main_frame = tk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Control panel
        control_frame = tk.Frame(main_frame)
        control_frame.pack(fill=tk.X, pady=(0, 10))

        # Title
        title = tk.Label(control_frame, text="SUDOKU", font=("Arial", 24, "bold"))
        title.pack()

        # Difficulty selector
        diff_frame = tk.Frame(control_frame)
        diff_frame.pack(fill=tk.X, pady=5)
        tk.Label(diff_frame, text="Difficulty:", font=("Arial", 10)).pack(side=tk.LEFT)
        for level in ['easy', 'medium', 'hard']:
            tk.Radiobutton(diff_frame, text=level.capitalize(),
                          variable=self.difficulty_var,
                          value=level,
                          command=self._new_game,
                          font=("Arial", 10)).pack(side=tk.LEFT, padx=5)

        # Timer and stats
        stats_frame = tk.Frame(control_frame)
        stats_frame.pack(fill=tk.X, pady=5)
        self.timer_label = tk.Label(stats_frame, text="Time: 00:00",
                                    font=("Arial", 12, "bold"))
        self.timer_label.pack(side=tk.LEFT, padx=10)
        self.hint_label = tk.Label(stats_frame, text="Hints: 0",
                                   font=("Arial", 12, "bold"))
        self.hint_label.pack(side=tk.LEFT, padx=10)

        # Buttons
        button_frame = tk.Frame(control_frame)
        button_frame.pack(fill=tk.X, pady=5)
        tk.Button(button_frame, text="Hint", command=self._give_hint,
                 font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Check", command=self._check_board,
                 font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="New Game", command=self._new_game,
                 font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Toggle Theme", command=self._toggle_theme,
                 font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Leaderboard", command=self._show_leaderboard,
                 font=("Arial", 10)).pack(side=tk.LEFT, padx=5)

        # Sudoku grid
        grid_frame = tk.Frame(main_frame)
        grid_frame.pack(pady=10)
        self._create_grid(grid_frame)

    def _create_grid(self, parent: tk.Frame) -> None:
        """Create the 9x9 Sudoku grid."""
        palette = Theme.get_palette(self.dark_mode)

        for row in range(9):
            for col in range(9):
                # Create cell frame
                cell = tk.Entry(parent, width=3, font=("Arial", 14, "bold"),
                               justify=tk.CENTER, bd=1)
                cell.grid(row=row, column=col, padx=1, pady=1)

                # Apply box coloring
                bg_color = Theme.get_box_color(row, col, self.dark_mode)
                cell.config(bg=bg_color, fg=palette['cell_fg'])

                # Bind events
                cell.bind('<FocusIn>', lambda e, r=row, c=col: self._on_cell_select(r, c))
                cell.bind('<KeyRelease>', lambda e, r=row, c=col: self._on_cell_change(r, c))

                self.cells[(row, col)] = cell

    def _new_game(self) -> None:
        """Start a new game."""
        self.difficulty = self.difficulty_var.get()
        puzzle, solution = self.generator.generate(self.difficulty)
        self.board = SudokuBoard(puzzle, solution)
        self.game_active = True
        self.hint_count = 0
        self.time_elapsed = 0
        self.conflicts.clear()
        self.errors.clear()

        # Update grid
        self._update_grid()
        self._update_timer()
        self._start_timer()

    def _update_grid(self) -> None:
        """Update grid display from board state."""
        if not self.board:
            return

        palette = Theme.get_palette(self.dark_mode)

        for row in range(9):
            for col in range(9):
                cell = self.cells[(row, col)]
                value = self.board.get_cell(row, col)
                cell.delete(0, tk.END)

                # Set cell content and styling
                if value != 0:
                    cell.insert(0, str(value))
                    cell.config(state=tk.NORMAL)
                else:
                    cell.config(state=tk.NORMAL)

                # Apply styling
                if self.board.is_locked(row, col):
                    cell.config(bg=palette['locked_bg'], fg=palette['locked_fg'],
                               state='readonly')
                else:
                    # Check for conflicts and errors
                    if (row, col) in self.conflicts:
                        cell.config(bg=palette['conflict_bg'])
                    elif (row, col) in self.errors:
                        cell.config(bg=palette['error_bg'])
                    else:
                        bg_color = Theme.get_box_color(row, col, self.dark_mode)
                        cell.config(bg=bg_color)

                    cell.config(fg=palette['cell_fg'])

    def _on_cell_select(self, row: int, col: int) -> None:
        """Handle cell selection."""
        self.selected_cell = (row, col)

    def _on_cell_change(self, row: int, col: int) -> None:
        """Handle cell value change."""
        if not self.board or not self.game_active:
            return

        cell = self.cells[(row, col)]
        value_str = cell.get()

        try:
            if value_str == '':
                self.board.clear_cell(row, col)
                self.conflicts.clear()
            elif len(value_str) == 1 and value_str.isdigit():
                num = int(value_str)
                if 1 <= num <= 9:
                    self.board.set_cell(row, col, num)
                    self.conflicts = self.board.get_conflicts(row, col)
                    self.errors.clear()
                else:
                    cell.delete(0, tk.END)
            else:
                cell.delete(0, tk.END)
        except Exception as e:
            logger.error(f"Error changing cell: {e}")
            cell.delete(0, tk.END)

        self._update_grid()

        # Check for completion
        if self.board.is_complete() and self.board.is_solved():
            self._on_completion()

    def _give_hint(self) -> None:
        """Give a hint by filling one empty cell."""
        if not self.board or not self.game_active:
            return

        hint = self.board.get_hint()
        if hint:
            row, col, value = hint
            self.board.set_cell(row, col, value)
            self.hint_count += 1
            self._update_grid()
            self._update_hints()

    def _check_board(self) -> None:
        """Check board for errors and highlight them."""
        if not self.board or not self.game_active:
            return

        self.errors = self.board.get_errors()
        self._update_grid()

    def _toggle_theme(self) -> None:
        """Toggle between light and dark mode."""
        self.dark_mode = not self.dark_mode
        self.leaderboard.set_dark_mode(self.dark_mode)

        # Clear and recreate grid
        for widget in self.cells.values():
            widget.destroy()
        self.cells.clear()

        # Recreate UI with new theme
        self._setup_ui()
        self._update_grid()

    def _show_leaderboard(self) -> None:
        """Display the leaderboard."""
        leaderboard_text = self.leaderboard.format_leaderboard()
        messagebox.showinfo("Leaderboard", leaderboard_text)

    def _on_completion(self) -> None:
        """Handle puzzle completion."""
        self.game_active = False

        # Get player name
        name = simpledialog.askstring("Congratulations!",
                                      "Puzzle solved! Enter your name:")
        if name:
            self.leaderboard.save_score(name, self.time_elapsed,
                                       self.difficulty, self.hint_count)
            messagebox.showinfo("Score Saved",
                              f"Your score has been saved!\n"
                              f"Time: {self.time_elapsed}s\n"
                              f"Hints: {self.hint_count}")

    def _start_timer(self) -> None:
        """Start the game timer."""
        if self.game_active:
            self.time_elapsed += 1
            self._update_timer()
            self.after(1000, self._start_timer)

    def _update_timer(self) -> None:
        """Update timer display."""
        if self.timer_label:
            minutes, seconds = divmod(self.time_elapsed, 60)
            self.timer_label.config(text=f"Time: {minutes:02d}:{seconds:02d}")

    def _update_hints(self) -> None:
        """Update hints display."""
        if self.hint_label:
            self.hint_label.config(text=f"Hints: {self.hint_count}")

    def _on_key_press(self, event) -> None:
        """Handle keyboard input."""
        # This is for future keyboard navigation enhancements
        pass

    def _on_window_focus(self, event) -> None:
        """Handle window focus."""
        pass
