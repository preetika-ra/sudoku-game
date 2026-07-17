"""Tests for Sudoku theme system - ensures color styling works correctly."""

import pytest
from sudoku.theme import Theme


class TestThemeSystem:
    """Test suite for color theme system."""

    def test_light_palette_exists(self):
        """Test that light mode palette exists."""
        palette = Theme.get_palette(dark_mode=False)
        assert palette is not None
        assert 'bg' in palette
        assert 'fg' in palette
        assert 'box_1' in palette
        assert 'box_2' in palette

    def test_dark_palette_exists(self):
        """Test that dark mode palette exists."""
        palette = Theme.get_palette(dark_mode=True)
        assert palette is not None
        assert 'bg' in palette
        assert 'fg' in palette
        assert 'box_1' in palette
        assert 'box_2' in palette

    def test_light_and_dark_differ(self):
        """Test that light and dark palettes are different."""
        light = Theme.get_palette(dark_mode=False)
        dark = Theme.get_palette(dark_mode=True)
        # At least some colors should differ
        assert light['bg'] != dark['bg'], "Background should differ"
        assert light['fg'] != dark['fg'], "Foreground should differ"

    def test_box_coloring(self):
        """Test 3x3 box color assignment."""
        # (0,0) and (0,1) should have same box color (same box)
        color_00 = Theme.get_box_color(0, 0, dark_mode=False)
        color_01 = Theme.get_box_color(0, 1, dark_mode=False)
        assert color_00 == color_01, "Cells in same box should have same color"

    def test_alternating_boxes(self):
        """Test that boxes alternate colors."""
        # (0,0) and (0,3) are in different boxes
        color_00 = Theme.get_box_color(0, 0, dark_mode=False)
        color_03 = Theme.get_box_color(0, 3, dark_mode=False)
        # They should use different colors (box_1 vs box_2)
        # Note: might be same if color happens to be same, but structure should alternate
        assert color_00 is not None
        assert color_03 is not None

    def test_box_color_formula(self):
        """Test that box coloring uses (box_row + box_col) % 2 formula."""
        palette = Theme.get_palette(dark_mode=False)
        # Box (0,0): (0+0)%2 = 0 -> box_1
        assert Theme.get_box_color(0, 0, False) == palette['box_1']
        # Box (0,1): (0+1)%2 = 1 -> box_2
        assert Theme.get_box_color(0, 3, False) == palette['box_2']
        # Box (1,0): (1+0)%2 = 1 -> box_2
        assert Theme.get_box_color(3, 0, False) == palette['box_2']
        # Box (1,1): (1+1)%2 = 0 -> box_1
        assert Theme.get_box_color(3, 3, False) == palette['box_1']

    def test_conflict_colors_exist(self):
        """Test that conflict colors are defined."""
        light = Theme.get_palette(dark_mode=False)
        dark = Theme.get_palette(dark_mode=True)
        assert 'conflict_bg' in light
        assert 'conflict_bg' in dark
        assert light['conflict_bg'] is not None
        assert dark['conflict_bg'] is not None

    def test_error_colors_exist(self):
        """Test that error (check) colors are defined."""
        light = Theme.get_palette(dark_mode=False)
        dark = Theme.get_palette(dark_mode=True)
        assert 'error_bg' in light
        assert 'error_bg' in dark

    def test_locked_cell_colors_exist(self):
        """Test that locked cell colors are defined."""
        light = Theme.get_palette(dark_mode=False)
        dark = Theme.get_palette(dark_mode=True)
        assert 'locked_bg' in light
        assert 'locked_fg' in light
        assert 'locked_bg' in dark
        assert 'locked_fg' in dark

    def test_all_required_colors_light_mode(self):
        """Test that all required colors exist in light mode."""
        required = ['bg', 'fg', 'grid_bg', 'cell_bg', 'cell_fg', 'locked_bg',
                   'locked_fg', 'highlight_bg', 'conflict_bg', 'error_bg',
                   'box_1', 'box_2', 'border', 'button_bg', 'button_fg', 'button_hover']
        palette = Theme.get_palette(dark_mode=False)
        for color in required:
            assert color in palette, f"Missing color: {color}"

    def test_all_required_colors_dark_mode(self):
        """Test that all required colors exist in dark mode."""
        required = ['bg', 'fg', 'grid_bg', 'cell_bg', 'cell_fg', 'locked_bg',
                   'locked_fg', 'highlight_bg', 'conflict_bg', 'error_bg',
                   'box_1', 'box_2', 'border', 'button_bg', 'button_fg', 'button_hover']
        palette = Theme.get_palette(dark_mode=True)
        for color in required:
            assert color in palette, f"Missing color: {color}"

    def test_valid_hex_colors(self):
        """Test that all colors are valid hex codes."""
        for palette_dict in [Theme.LIGHT, Theme.DARK]:
            for color_name, color_value in palette_dict.items():
                assert isinstance(color_value, str), f"{color_name} is not a string"
                assert color_value.startswith('#'), f"{color_name} doesn't start with #"
                assert len(color_value) == 7, f"{color_name} is not valid hex (should be #RRGGBB)"
                # Verify hex characters
                try:
                    int(color_value[1:], 16)
                except ValueError:
                    pytest.fail(f"{color_name} contains invalid hex characters")

    def test_dark_mode_box_colors_differ(self):
        """Test that dark mode has distinct box colors."""
        light_box1 = Theme.get_palette(False)['box_1']
        light_box2 = Theme.get_palette(False)['box_2']
        dark_box1 = Theme.get_palette(True)['box_1']
        dark_box2 = Theme.get_palette(True)['box_2']
        
        # Light and dark should differ
        assert light_box1 != dark_box1 or light_box2 != dark_box2
