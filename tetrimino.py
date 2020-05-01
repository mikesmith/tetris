import arcade
from enum import Enum

from constants import SIDE_MARGIN, BOTTOM_MARGIN, WHITE, BLACK


class Shape(Enum):
    O = [[0, 1, 1],
         [0, 1, 1],
         [0, 0, 0]]

    I = [[0, 0, 0, 0],
         [1, 1, 1, 1],
         [0, 0, 0, 0],
         [0, 0, 0, 0]]

    T = [[0, 1, 0],
         [1, 1, 1],
         [0, 0, 0]]

    L = [[0, 0, 1],
         [1, 1, 1],
         [0, 0, 0]]

    J = [[1, 0, 0],
         [1, 1, 1],
         [0, 0, 0]]

    S = [[0, 1, 1],
         [1, 1, 0],
         [0, 0, 0]]

    Z = [[1, 1, 0],
         [0, 1, 1],
         [0, 0, 0]]


class Tetrimino():

    def __init__(self, shape, grid):
        """Initialize the tetrimino."""
        self.shape = shape.value
        self._grid = grid._grid
        self.grid = grid

        # Initial position (Temporary until spawning implemented)
        self.x = 4
        self.y = 15

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
        elif symbol == arcade.key.SPACE:
            self.add_tetrimino_to_grid()

    def move_left(self):
        """Move X coordinate of tetrimino location to the left."""
        new_x, new_y = self.x - 1, self.y
        if not self.is_collision_on_move(new_x, new_y):
            self.x, self.y = new_x, new_y

    def move_right(self):
        """Move X coordinate of tetrimino location to the right."""
        new_x, new_y = self.x + 1, self.y
        if not self.is_collision_on_move(new_x, new_y):
            self.x, self.y = new_x, new_y

    def move_down(self):
        """Move Y coordinate of tetrimino location down."""
        new_x, new_y = self.x, self.y - 1
        if not self.is_collision_on_move(new_x, new_y):
            self.x, self.y = new_x, new_y

    def rotate_clockwise(self):
        """Rotate the tetrimino clockwise."""
        shape_attempt = list(zip(*reversed(self.shape)))
        if not self.is_collision_on_rotate(shape_attempt):
            self.shape = shape_attempt

    def rotate_counter_clockwise(self):
        """Rotate the tetrimino counter-clockwise."""
        self.shape = list(reversed(list(zip(*self.shape))))

    def is_collision_on_move(self, new_x, new_y):
        """Check for collision with a proposed new location.

        Arguments:
            new_location {(x, y)} -- The x,y coordinates of proposed location

        Returns:
            bool -- True if a collision is detected. False, otherwise.
        """
        for i, row in enumerate(reversed(self.shape)):
            for j, column in enumerate(row):
                if self._grid[new_y + i][new_x + j] + row[j] >= 2:
                    return True
        return False

    def is_collision_on_rotate(self, new_shape):
        """Check for collision with a proposed new shape.

        Arguments:
            new_shape {[[]]} -- The proposed shape after rotation

        Returns:
            bool -- True if a collision is detected. False, otherwise.
        """
        for i, row in enumerate(reversed(new_shape)):
            for j, column in enumerate(row):
                if self._grid[self.y + i][self.x + j] + row[j] >= 2:
                    return True
        return False

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
                    x = SIDE_MARGIN + (j + self.x) * 24
                    y = BOTTOM_MARGIN + (i + self.y) * 24
                    arcade.draw_rectangle_filled(x, y, 24, 24, WHITE)
                    arcade.draw_rectangle_outline(x, y, 24, 24, BLACK)

    def add_tetrimino_to_grid(self):
        for i, row in enumerate(reversed(self.shape)):
            for j, column in enumerate(row):
                y = self.y + i
                x = self.x + j

                if x != 0 and x != 11 and y != 0 and row[j] != 0:
                    self._grid[self.y + i][self.x + j] = row[j]

        self.grid.refresh()

    def __str__(self):
        return '\n'.join([str(x) for x in self.shape])
