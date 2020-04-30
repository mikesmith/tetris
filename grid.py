import arcade

from constants import SIDE_MARGIN, BOTTOM_MARGIN


class Grid():

    def __init__(self):
        self._grid = [[0]*12 for y in range(21)]

        self.rect_list = arcade.ShapeElementList()

        for i, row in enumerate(self._grid):
            for j, column in enumerate(row):
                x = SIDE_MARGIN + j * 24
                y = BOTTOM_MARGIN + i * 24
                if j == 0 or j == 11 or i == 0:
                    self._grid[i][j] = 1
                    rect = arcade.create_rectangle_filled(x, y, 24, 24, arcade.color.DARK_GRAY)
                    self.rect_list.append(rect)
                rect = arcade.create_rectangle_outline(x, y, 24, 24, arcade.color.BLACK)
                self.rect_list.append(rect)

    def draw(self):
        """Draw the play grid."""
        self.rect_list.draw()

    def __str__(self):
        return '\n'.join([str(x) for x in reversed(self._grid)])
