import arcade

from constants import SIDE_MARGIN, BOTTOM_MARGIN


class Grid():

    def __init__(self):
        self._grid = [[0]*20 for j in range(10)]

        self.rect_list = arcade.ShapeElementList()

        for i, row in enumerate(self._grid):
            for j, column in enumerate(row):
                x = SIDE_MARGIN + i * 24
                y = BOTTOM_MARGIN + j * 24
                rect = arcade.create_rectangle_outline(x, y, 24, 24, arcade.color.BLACK)
                self.rect_list.append(rect)

    def draw(self):
        """Draw the play grid."""
        self.rect_list.draw()
        for i, row in enumerate(self._grid):
            for j, column in enumerate(row):
                if column == 1:
                    x = SIDE_MARGIN + i * 24
                    y = BOTTOM_MARGIN + j * 24
                    arcade.draw_rectangle_filled(x, y, 24, 24, arcade.color.WHITE)
                    arcade.draw_rectangle_outline(x, y, 24, 24, arcade.color.BLACK)
