import arcade

from constants import SIDE_MARGIN, BOTTOM_MARGIN, COLORS, DARK_GRAY, BLACK


class Grid():

    def __init__(self):
        self._grid = [[0]*12 for y in range(24)]
        self.lines_cleared = 0
        self.refreshed = False
        self.refresh()

    def refresh(self):
        """Refresh the grid with the latest positions of all the pieces."""
        self.rect_list = arcade.ShapeElementList()

        for i, row in enumerate(self._grid):
            for j, column in enumerate(row):
                x = SIDE_MARGIN + j * 24
                y = BOTTOM_MARGIN + i * 24
                if i < 21:
                    if j == 0 or j == 11 or i == 0:
                        self._grid[i][j] = 1
                        # Color in left, bottom and right borders
                        self.create_border_rect(x, y)
                    elif self._grid[i][j] > 1:
                        # Color in any game pieces on the board
                        self.create_game_piece_rect(x, y, self._grid[i][j])
                    self.create_grid_rect(x, y)
        if self.check_for_line_clear():
            self.refresh()
        self.refreshed = True

    def check_for_line_clear(self):
        """Check and update any lines that should be cleared.

        Lines are cleared when the entire row is filled. Remove the row
        and add a new empty row into the grid.

        Returns:
            int -- Number of lines cleared
        """
        num_cleared = 0
        for i in range(1, 21):
            if 0 not in set(self._grid[i]):
                self._grid.append([1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1])
                self._grid.pop(i)
                num_cleared += 1
        self.lines_cleared += num_cleared
        return num_cleared

    def create_border_rect(self, x, y):
        rect = arcade.create_rectangle_filled(
                        center_x=x,
                        center_y=y,
                        width=24,
                        height=24,
                        color=DARK_GRAY)
        self.rect_list.append(rect)

    def create_game_piece_rect(self, x, y, color):
        rect = arcade.create_rectangle_filled(
                        center_x=x,
                        center_y=y,
                        width=24,
                        height=24,
                        color=COLORS[color])
        self.rect_list.append(rect)

    def create_grid_rect(self, x, y):
        rect = arcade.create_rectangle_outline(
                        center_x=x,
                        center_y=y,
                        width=24,
                        height=24,
                        color=BLACK)
        self.rect_list.append(rect)

    def draw(self):
        """Draw the play grid."""
        self.rect_list.draw()

    def __str__(self):
        return '\n'.join([str(x) for x in reversed(self._grid)])
