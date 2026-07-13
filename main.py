"""Entry point for the Sudoku app."""

from sudoku.ui import SudokuApp


def main() -> None:
    """Launch the Sudoku application."""
    app = SudokuApp()
    app.mainloop()


if __name__ == "__main__":
    main()
