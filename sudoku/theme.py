"""Color themes for light and dark modes."""

from typing import Dict, Tuple


class Theme:
    """Color palette for Sudoku UI."""

    # Light mode colors
    LIGHT = {
        'bg': '#FFFFFF',           # Main background
        'fg': '#000000',           # Text color
        'grid_bg': '#F5F5F5',      # Grid background
        'cell_bg': '#FFFFFF',      # Cell background
        'cell_fg': '#000000',      # Cell text
        'locked_bg': '#E8E8E8',    # Locked cell background
        'locked_fg': '#000000',    # Locked cell text
        'highlight_bg': '#FFF8DC', # Highlighted cell
        'conflict_bg': '#FF6B6B',  # Conflict cell
        'error_bg': '#FFA500',     # Error cell (Check)
        'box_1': '#F0F0F0',        # 3x3 box color 1
        'box_2': '#FFFFFF',        # 3x3 box color 2
        'border': '#333333',       # Grid border
        'button_bg': '#E0E0E0',    # Button background
        'button_fg': '#000000',    # Button text
        'button_hover': '#D0D0D0', # Button hover
    }

    # Dark mode colors
    DARK = {
        'bg': '#1E1E1E',           # Main background
        'fg': '#E0E0E0',           # Text color
        'grid_bg': '#2D2D2D',      # Grid background
        'cell_bg': '#3A3A3A',      # Cell background
        'cell_fg': '#E0E0E0',      # Cell text
        'locked_bg': '#4A4A4A',    # Locked cell background
        'locked_fg': '#E0E0E0',    # Locked cell text
        'highlight_bg': '#5A4A2A', # Highlighted cell
        'conflict_bg': '#CC4433',  # Conflict cell (darker red)
        'error_bg': '#CC8833',     # Error cell (darker orange)
        'box_1': '#2D2D2D',        # 3x3 box color 1
        'box_2': '#3A3A3A',        # 3x3 box color 2
        'border': '#555555',       # Grid border
        'button_bg': '#4A4A4A',    # Button background
        'button_fg': '#E0E0E0',    # Button text
        'button_hover': '#5A5A5A', # Button hover
    }

    @staticmethod
    def get_palette(dark_mode: bool = False) -> Dict[str, str]:
        """Get color palette for current mode.

        Args:
            dark_mode: True for dark theme, False for light theme

        Returns:
            Dictionary of color names to hex values
        """
        return Theme.DARK if dark_mode else Theme.LIGHT

    @staticmethod
    def get_box_color(row: int, col: int, dark_mode: bool = False) -> str:
        """Get background color for 3x3 box.

        Args:
            row: Row index (0-8)
            col: Column index (0-8)
            dark_mode: True for dark theme

        Returns:
            Color hex value
        """
        palette = Theme.get_palette(dark_mode)
        box_row = row // 3
        box_col = col // 3
        # Alternate colors based on (box_row + box_col) % 2
        if (box_row + box_col) % 2 == 0:
            return palette['box_1']
        else:
            return palette['box_2']

    @staticmethod
    def get_contrast_text(bg_color: str) -> str:
        """Get appropriate text color for background.

        Args:
            bg_color: Background color hex value

        Returns:
            Text color hex value
        """
        # Simple heuristic: dark backgrounds get light text
        rgb = int(bg_color[1:], 16)
        brightness = (rgb >> 16) + (rgb >> 8) + rgb
        return '#FFFFFF' if brightness < 1500 else '#000000'
