import arcade
from datetime import datetime

from shape import Shape

from constants import SIDE_MARGIN, BOTTOM_MARGIN, COLORS, BLACK


class Tetrimino():

    def __init__(self, shape, grid, level):
        """Initialize the tetrimino."""

        # Initialize Sounds
        self.fall_sound = arcade.load_sound('sounds/PieceFall.ogg')
        self.move_sound = arcade.load_sound('sounds/PieceMoveLR.ogg')
        self.rotate_sound = arcade.load_sound('sounds/PieceRotateLR.ogg')
        self.rotate_fail = arcade.load_sound('sounds/PieceRotateFail.ogg')
        self.lockdown_sound = arcade.load_sound('sounds/PieceLockdown.ogg')
        self.touchdown_sound = arcade.load_sound('sounds/PieceTouchDown.ogg')
        self.hard_drop_sound = arcade.load_sound('sounds/PieceHardDrop.ogg')

        # Initialize tetrimino values
        self.shape = shape.value[0]
        self.color = shape.value[1]
        self._grid = grid._grid
        self.grid = grid
        self.level = level

        self.down_pressed = False
        self.hard_drop = False

        self.hard_drop_start = 0
        self.hard_drop_lock = 0
        self.soft_drop_start = 0
        self.soft_drop_lock = 0

        # Timers
        self.move_down_timer = datetime.now()
        self.lock_down_timer = None

        # Initial Position
        self.x = 4
        self.y = 19
        if shape == Shape.I:
            self.y = 18

        # Failure flags
        self.locked_out = False
        self.blocked_out = self.is_blocked_out()

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
        if symbol == arcade.key.DOWN:
            self.down_pressed = True
            self.soft_drop_start = self.y
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
            if not self.hard_drop:
                self.move_left()
        elif symbol == arcade.key.RIGHT:
            if not self.hard_drop:
                self.move_right()
        elif symbol == arcade.key.DOWN:
            self.down_pressed = False
            self.soft_drop_start = 0
        elif symbol == arcade.key.SPACE:
            self.hard_drop = True
            arcade.play_sound(self.hard_drop_sound)
            self.hard_drop_start = self.y

    def speed(self, level):
        """Calculate fall speed of the tetrimino.

        Arguments:
            level {int} -- The current level

        Returns:
            float -- The time in ms between each block movement
        """
        n = level - 1
        return 1000 * (0.8 - (n * 0.007)) ** n

    def move_left(self):
        """Move X coordinate of tetrimino location to the left."""
        new_x, new_y = self.x - 1, self.y
        if not self.is_collision_on_move(new_x, new_y):
            self.x, self.y = new_x, new_y
            arcade.play_sound(self.move_sound)

    def move_right(self):
        """Move X coordinate of tetrimino location to the right."""
        new_x, new_y = self.x + 1, self.y
        if not self.is_collision_on_move(new_x, new_y):
            self.x, self.y = new_x, new_y
            arcade.play_sound(self.move_sound)

    def move_down(self):
        """Move Y coordinate of tetrimino location down."""
        new_x, new_y = self.x, self.y - 1
        if not self.is_collision_on_move(new_x, new_y):
            self.x, self.y = new_x, new_y
            arcade.play_sound(self.fall_sound)
        elif not self.lock_down_timer:
            self.lock_down_timer = datetime.now()
            self.soft_drop_lock = self.soft_drop_start - self.y
            self.hard_drop_lock = self.hard_drop_start - self.y
            arcade.play_sound(self.touchdown_sound)

    def rotate_clockwise(self):
        """Rotate the tetrimino clockwise."""
        shape_attempt = list(zip(*reversed(self.shape)))
        if not self.is_collision_on_rotate(shape_attempt):
            self.shape = shape_attempt
            arcade.play_sound(self.rotate_sound)
        else:
            arcade.play_sound(self.rotate_fail)

    def rotate_counter_clockwise(self):
        """Rotate the tetrimino counter-clockwise."""
        shape_attempt = list(reversed(list(zip(*self.shape))))
        if not self.is_collision_on_rotate(shape_attempt):
            self.shape = shape_attempt
            arcade.play_sound(self.rotate_sound)
        else:
            arcade.play_sound(self.rotate_fail)

    def is_blocked_out(self):
        """Check if Tetrimino is colliding in current position.

        Return:
            bool -- True is collision is detected. False, otherwise.
        """
        return self.is_collision_on_move(self.x, self.y)

    def is_collision_on_move(self, new_x, new_y):
        """Check for collision with a proposed new location.

        Arguments:
            new_location {(x, y)} -- The x,y coordinates of proposed location

        Returns:
            bool -- True if a collision is detected. False, otherwise.
        """
        for i, row in enumerate(reversed(self.shape)):
            for j, column in enumerate(row):
                matrix_value = self._grid[new_y + i][new_x + j]
                col_sum = matrix_value + row[j]
                if col_sum != self.color and col_sum != matrix_value:
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
                matrix_value = self._grid[self.y + i][self.x + j]
                col_sum = matrix_value + row[j]
                if col_sum != self.color and col_sum != matrix_value:
                    return True
        return False

    def on_update(self, delta_time: float):
        """Update the position and status of the tetrimino.

        Arguments:
            delta_time {float} -- Time since the last update
        """
        if self.down_pressed or self.hard_drop:
            self.move_down()

        if self.lock_down_timer:
            if self.time_delta_ms(self.lock_down_timer) >= 500:
                self.lock_down()
                self.lock_down_timer = None

        if self.time_delta_ms(self.move_down_timer) >= self.speed(self.level):
            self.move_down()
            self.move_down_timer = datetime.now()

    def time_delta_ms(self, time):
        """Get delta time between now and a given time.

        Arguments:
            time {float} -- Time to compare against current time

        Returns:
            float -- The delta time in milliseconds
        """
        return (datetime.now() - time).total_seconds() * 1000

    def draw(self):
        """Draw the tetrimino."""
        for i, row in enumerate(reversed(self.shape)):
            for j, block in enumerate(row):
                if block > 1 and (self.y + i) < 21:
                    x = SIDE_MARGIN + (j + self.x) * 24
                    y = BOTTOM_MARGIN + (i + self.y) * 24
                    arcade.draw_rectangle_filled(
                        center_x=x,
                        center_y=y,
                        width=24,
                        height=24,
                        color=COLORS[self.color])
                    arcade.draw_rectangle_outline(
                        center_x=x,
                        center_y=y,
                        width=24,
                        height=24,
                        color=BLACK)

    def lock_down(self):
        """Enter Lock Down phase where the Tetrimino locks to the grid.

        If the Tetrimino locks down above the Skyline, update the
        Tetrimino status as locked out of the Matrix.
        """
        self.locked_out = False
        for i, row in enumerate(reversed(self.shape)):
            for j, block in enumerate(row):
                y = self.y + i
                x = self.x + j

                if x != 0 and x != 11 and y != 0 and row[j] != 0:
                    self._grid[y][x] = row[j]
                    if y >= 21:
                        self.locked_out = True

        arcade.play_sound(self.lockdown_sound)
        self.grid.refresh()

    def __str__(self):
        return '\n'.join([str(x) for x in self.shape])
