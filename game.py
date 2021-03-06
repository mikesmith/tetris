import arcade
import timeit
import random

from grid import Grid
from shape import Shape
from tetrimino import Tetrimino
from next_queue import NextQueue

from constants import (SCALING, SCREEN_HEIGHT, SCREEN_WIDTH, SCREEN_TITLE,
                       NEXT_QUEUE_CX, NEXT_QUEUE_CY,)


class Tetris(arcade.Window):

    def __init__(self, width, height, title):
        """Initialize the game."""
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.GRAY)

        # Sounds
        self.single_clear_sound = arcade.load_sound('sounds/ClearSingle.ogg')
        self.double_clear_sound = arcade.load_sound('sounds/ClearDouble.ogg')
        self.triple_clear_sound = arcade.load_sound('sounds/ClearTriple.ogg')
        self.tetris_clear_sound = arcade.load_sound('sounds/ClearQuad.ogg')
        self.level_up_sound = arcade.load_sound('sounds/LevelUp.ogg')

        # Game State
        self.paused = False
        self.game_over = False

        # Game Stats
        self.level = 1
        self.level_line_counter = 0
        self.prev_lines_cleared = 0
        self.lines_cleared = 0
        self.points = 0

        # Game Objects
        self.grid = Grid()
        self.tetrimino_bag = random.sample(list(Shape), len(Shape))
        self.t_index = 0
        self.t = None
        self.next_queue = NextQueue()

        # Diagnostics
        self.diagnostics = False
        self.draw_time = 0
        self.frame_count = 0
        self.fps_start_timer = None
        self.fps = None

    def on_key_press(self, symbol: int, modifiers: int):
        """Handle user keyboard input.
        Q: Quit the game
        D: Diagnostics
        ESC: Pause the game
        F1: Pause the game
        P: Print grid to console

        Arguments:
            symbol {int} -- Which key was pressed
            modifiers {int} -- Which modifiers were pressed
        """
        if symbol == arcade.key.Q:
            # Quit immediately
            arcade.close_window()

        if symbol == arcade.key.ESCAPE:
            self.paused = not self.paused

        if symbol == arcade.key.F1:
            self.paused = not self.paused

        if symbol == arcade.key.D:
            self.diagnostics = not self.diagnostics

        if symbol == arcade.key.P:
            print(self.grid)

        self.t.on_key_press(symbol, modifiers)

    def on_key_release(self, symbol: int, modifiers: int):
        """Undo movement vectors when movement keys are released.
        Arguments:
            symbol {int} -- Which key was pressed
            modifiers {int} -- Which modifiers were pressed
        """
        self.t.on_key_release(symbol, modifiers)

    def on_update(self, delta_time: float):
        """Update the positions and statuses of all game objects.

        If paused, do nothing

        Check the Matrix and current Tetrimino status for game updates

        Arguments:
            delta_time {float} -- Time since the last update
        """
        if self.paused:
            return

        if self.grid.refreshed:
            # If grid is refreshed and a tetrimino exists, a lock down
            # occurred. Calculate any points accrued or if the tetrimino
            # was locked out.
            if self.t:
                self.calculate_points(self.grid.lines_cleared,
                                      self.t.hard_drop_lock,
                                      self.t.soft_drop_lock)
                self.grid.lines_cleared = 0

                if self.t.locked_out:
                    self.game_over = True

            self.t = self.get_next_tetrimino()

            if self.t.blocked_out:
                self.game_over = True

            self.grid.refreshed = False

        self.t.on_update(delta_time)

        if self.game_over:
            self.trigger_game_over()

    def on_draw(self):
        """Draw all game objects."""
        # Start timing how long this takes
        draw_start_time = timeit.default_timer()

        if self.frame_count % 60 == 0:
            if self.fps_start_timer is not None:
                total_time = timeit.default_timer() - self.fps_start_timer
                self.fps = 60 / total_time
            self.fps_start_timer = timeit.default_timer()
        self.frame_count += 1

        arcade.start_render()  # Needs to be called before drawing

        self.grid.draw()
        self.t.draw()
        self.next_queue.draw()

        arcade.draw_text(f'Level: {self.level}',
                         NEXT_QUEUE_CX,
                         NEXT_QUEUE_CY - 40,
                         arcade.color.BLACK,
                         12,
                         align='center')
        arcade.draw_text(f'Lines Cleared: {self.lines_cleared}',
                         NEXT_QUEUE_CX,
                         NEXT_QUEUE_CY - 60,
                         arcade.color.BLACK,
                         12,
                         align='center')
        arcade.draw_text(f'Score: {self.points}',
                         NEXT_QUEUE_CX,
                         NEXT_QUEUE_CY - 80,
                         arcade.color.BLACK,
                         12,
                         align='center')

        if self.paused:
            arcade.draw_text("PAUSED",
                             SCREEN_WIDTH / 2,
                             SCREEN_HEIGHT - 40,
                             arcade.color.BLACK,
                             26,
                             align='center')

        if self.diagnostics:
            # Show diagnostics (Draw Time, FPS)
            output = f"Drawing time: {self.draw_time:.3f}"
            arcade.draw_text(output,
                             20,
                             SCREEN_HEIGHT - 20,
                             arcade.color.BLACK,
                             12)

            if self.fps is not None:
                output = f"FPS: {self.fps:.0f}"
                arcade.draw_text(output,
                                 20,
                                 SCREEN_HEIGHT - 40,
                                 arcade.color.BLACK,
                                 12)

        self.draw_time = timeit.default_timer() - draw_start_time

    def get_next_tetrimino(self):
        """Retrieve the next random tetrimino using the "bag" system."""
        t = Tetrimino(self.tetrimino_bag[self.t_index], self.grid, self.level)
        self.t_index += 1
        if self.t_index == len(Shape):
            self.t_index = 0
            self.tetrimino_bag = random.sample(list(Shape), len(Shape))

        self.next_queue.update_next_queue(self.tetrimino_bag[self.t_index])
        return t

    def calculate_points(self, lines, hard_drop_rows, soft_drop_rows):
        """Update score with given number of lines cleared.

        Arguments:
            lines {int} -- Number of lines cleared in latest grid refresh
            hard_drop_rows {int} -- Number of rows the tetrimino hard dropped
            soft_drop_rows {int} -- Number of rows the tetrimino soft dropped
        """
        self.lines_cleared += lines
        if lines == 1:
            self.points += 100 * self.level
            arcade.play_sound(self.single_clear_sound)
        elif lines == 2:
            self.points += 300 * self.level
            arcade.play_sound(self.double_clear_sound)
        elif lines == 3:
            self.points += 500 * self.level
            arcade.play_sound(self.triple_clear_sound)
        elif lines == 4:
            self.points += 800 * self.level
            arcade.play_sound(self.tetris_clear_sound)

        self.level_line_counter += lines
        if self.level_line_counter >= 10:
            self.level += 1
            self.level_line_counter -= 10
            arcade.play_sound(self.level_up_sound)

        if self.prev_lines_cleared == 4 and lines == 4:
            self.points += 400  # B2B Bonus 0.5 of Tetris points

        if hard_drop_rows > 0:
            self.points += (hard_drop_rows * 2)

        if soft_drop_rows > 0:
            self.points += soft_drop_rows

        self.prev_lines_cleared = lines

    def trigger_game_over(self):
        """Game Over."""
        print('Game Over')
        # Quit immediately
        arcade.close_window()  # TODO: Implement Game Over Screen


if __name__ == '__main__':
    tetris = Tetris(
        int(SCREEN_WIDTH * SCALING), int(SCREEN_HEIGHT * SCALING), SCREEN_TITLE
    )
    arcade.run()
