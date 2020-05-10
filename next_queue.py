import arcade

from constants import (SIDE_MARGIN, BOTTOM_MARGIN, NEXT_QUEUE_CX,
                       NEXT_QUEUE_CY, NEXT_QUEUE_X_OFFSET, NEXT_QUEUE_Y_OFFSET,
                       NEXT_QUEUE_HEIGHT, NEXT_QUEUE_WIDTH, COLORS, WHITE,
                       BLACK,)


class NextQueue():

    def __init__(self):
        """Initialize the Next Queue which displays the next Tetrimino that
        will be in play.
        """
        self.t_next = None
        self.rects = arcade.ShapeElementList()
        self.minos = arcade.ShapeElementList()
        self.box = arcade.create_rectangle_filled(
            center_x=SIDE_MARGIN + NEXT_QUEUE_CX,
            center_y=BOTTOM_MARGIN + NEXT_QUEUE_CY,
            width=NEXT_QUEUE_WIDTH,
            height=NEXT_QUEUE_HEIGHT,
            color=WHITE)
        self.outline = arcade.create_rectangle_outline(
            center_x=SIDE_MARGIN + NEXT_QUEUE_CX,
            center_y=BOTTOM_MARGIN + NEXT_QUEUE_CY,
            width=NEXT_QUEUE_WIDTH,
            height=NEXT_QUEUE_HEIGHT,
            color=BLACK)
        self.rects.append(self.box)
        self.rects.append(self.outline)

    def update_next_queue(self, t_next):
        """Update the next queue box with the next piece in the queue.

        Arguments:
            t_next {Shape} -- The next shape that will be in play
        """
        self.minos = arcade.ShapeElementList()
        self.t_next = t_next

        for i, row in enumerate(reversed(self.t_next.value[0])):
            for j, block in enumerate(row):
                if block > 1:
                    x = SIDE_MARGIN + NEXT_QUEUE_X_OFFSET + (j) * 24 + 12
                    y = BOTTOM_MARGIN + NEXT_QUEUE_Y_OFFSET + (i) * 24

                    # Offset the tetrimino pieces to center in next queue box
                    if self.t_next.value[1] in [2, 3]:
                        x = SIDE_MARGIN + NEXT_QUEUE_X_OFFSET + (j) * 24
                    if self.t_next.value[1] == 3:
                        y = BOTTOM_MARGIN + NEXT_QUEUE_Y_OFFSET + (i) * 24 - 12

                    self.minos.append(arcade.create_rectangle_filled(
                        center_x=x,
                        center_y=y,
                        width=24,
                        height=24,
                        color=COLORS[self.t_next.value[1]]))

                    self.minos.append(arcade.create_rectangle_outline(
                        center_x=x,
                        center_y=y,
                        width=24,
                        height=24,
                        color=BLACK))

    def draw(self):
        """Draw the background and tetrimino."""
        self.rects.draw()
        self.minos.draw()
