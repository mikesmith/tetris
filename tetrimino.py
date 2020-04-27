import arcade
from enum import Enum

from constants import SIDE_MARGIN, BOTTOM_MARGIN


class Shape(Enum):
    O = ([[0, 1, 1],
          [0, 1, 1],
          [0, 0, 0]],
         1,
         2,
         1)

    I = ([[0, 0, 0, 0],
          [1, 1, 1, 1],
          [0, 0, 0, 0],
          [0, 0, 0, 0]],
         0,
         3,
         2)

    T = ([[0, 1, 0],
          [1, 1, 1],
          [0, 0, 0]],
         0,
         2,
         1)

    L = ([[0, 0, 1],
          [1, 1, 1],
          [0, 0, 0]],
         0,
         2,
         1)

    J = ([[1, 0, 0],
          [1, 1, 1],
          [0, 0, 0]],
         0,
         2,
         1)

    S = ([[0, 1, 1],
          [1, 1, 0],
          [0, 0, 0]],
         0,
         2,
         1)

    Z = ([[1, 1, 0],
          [0, 1, 1],
          [0, 0, 0]],
         0,
         2,
         1)


class Tetrimino():

    def __init__(self, shape):
        """Initialize the tetrimino."""
        self.shape = shape.value[0]
        self.location = (4, 15)

        self.left = shape.value[1]
        self.right = shape.value[2]
        self.bottom = shape.value[3]

        self.left_pressed = False
        self.right_pressed = False
        self.down_pressed = False

    def on_key_press(self, symbol: int, modifiers: int):
        """Handle user keyboard input.

        Left Arrow: Move Left
        Right Arrow: Move Right
        Up: Rotate Clockwise
        X: Rotate Clockwise
        Z: Rotate Counter-Clockwise
        L-CTRL: Rotate Counter-Clockwise

        Arguments:
            symbol {int} -- Which key was pressed
            modifiers {int} -- Which modifiers were pressed
        """
        if symbol == arcade.key.LEFT:
            self.left_pressed = True
        elif symbol == arcade.key.RIGHT:
            self.right_pressed = True
        elif symbol == arcade.key.DOWN:
            self.down_pressed = True
        elif symbol == arcade.key.UP:
            self.rotate_clockwise()
        elif symbol == arcade.key.X:
            self.rotate_clockwise()
        elif symbol == arcade.key.LCTRL:
            self.rotate_counter_clockwise()
        elif symbol == arcade.key.Z:
            self.rotate_counter_clockwise()

    def on_key_release(self, symbol: int, modifiers: int):
        """Undo movement vectors when movement keys are released.

        Arguments:
            symbol {int} -- Which key was pressed
            modifiers {int} -- Which modifiers were pressed
        """
        if symbol == arcade.key.LEFT:
            self.left_pressed = False
        elif symbol == arcade.key.RIGHT:
            self.right_pressed = False
        elif symbol == arcade.key.DOWN:
            self.down_pressed = False
        elif symbol == arcade.key.UP:
            self.up_pressed = False

    def move_left(self):
        """Move X coordinate of tetrimino location to the left."""
        if not self.left_blocked():
            self.location = (self.location[0] - 1, self.location[1])

    def left_blocked(self):
        """Check if the tetrimino is blocked from moving left.

        Returns:
            bool -- True if blocked. False otherwise.
        """
        blocked = False
        if self.location[0] + self.left <= 0:
            blocked = True
        return blocked

    def move_right(self):
        """Move X coordinate of tetrimino location to the right."""
        if not self.right_blocked():
            self.location = (self.location[0] + 1, self.location[1])

    def right_blocked(self):
        """Check if the tetrimino is blocked from moving right.

        Returns:
            bool -- True if blocked. False otherwise.
        """
        blocked = False
        if self.location[0] + self.right >= 9:
            blocked = True
        return blocked

    def move_down(self):
        """Move Y coordinate of tetrimino location down."""
        if not self.down_blocked():
            self.location = (self.location[0], self.location[1] - 1)

    def down_blocked(self):
        """Check if the tetrimino is blocked from moving down.

        Returns:
            bool -- True if blocked. False otherwise.
        """
        blocked = False
        if self.location[1] + self.bottom <= 0:
            blocked = True
        return blocked

    def rotate_clockwise(self):
        """Rotate the tetrimino clockwise."""
        self.shape = list(zip(*reversed(self.shape)))

    def rotate_counter_clockwise(self):
        """Rotate the tetrimino counter-clockwise."""
        self.shape = list(reversed(list(zip(*self.shape))))

    def on_update(self, delta_time: float):
        """Update the position and status of the tetrimino.

        Arguments:
            delta_time {float} -- Time since the last update
        """
        if self.left_pressed:
            self.move_left()
        if self.right_pressed:
            self.move_right()
        if self.down_pressed:
            self.move_down()

    def draw(self):
        """Draw the tetrimino."""
        for i, row in enumerate(reversed(self.shape)):
            for j, column in enumerate(row):
                if column == 1:
                    x = SIDE_MARGIN + (j + self.location[0]) * 24
                    y = BOTTOM_MARGIN + (i + self.location[1]) * 24
                    arcade.draw_rectangle_filled(x, y, 24, 24, arcade.color.WHITE)
                    arcade.draw_rectangle_outline(x, y, 24, 24, arcade.color.BLACK)
