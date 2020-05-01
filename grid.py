import arcade

from constants import SIDE_MARGIN, BOTTOM_MARGIN, WHITE_SMOKE, DARK_GRAY, BLACK


class Grid():

    def __init__(self):
        self._grid = [[0]*12 for y in range(21)]
        self.refresh()

    def refresh(self):
        self.rect_list = arcade.ShapeElementList()

        for i, row in enumerate(self._grid):
            for j, column in enumerate(row):
                x = SIDE_MARGIN + j * 24
                y = BOTTOM_MARGIN + i * 24
                if j == 0 or j == 11 or i == 0:
                    self._grid[i][j] = 1
                    # Color in left, bottom and right borders
                    self.create_border_rect(x, y)
                elif self._grid[i][j] == 1:
                    # Color in any game pieces on the board
                    self.create_game_piece_rect(x, y)
                self.create_grid_rect(x, y)

    def create_border_rect(self, x, y):
        rect = arcade.create_rectangle_filled(
                        center_x=x,
                        center_y=y,
                        width=24,
                        height=24,
                        color=DARK_GRAY)
        self.rect_list.append(rect)

    def create_game_piece_rect(self, x, y):
        rect = arcade.create_rectangle_filled(
                        center_x=x,
                        center_y=y,
                        width=24,
                        height=24,
                        color=WHITE_SMOKE)
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
