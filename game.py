import arcade

from constants import SCALING, SCREEN_HEIGHT, SCREEN_WIDTH, SCREEN_TITLE

class Tetris(arcade.Window):

    def __init__(self, width, height, title):
        """Initialize the game."""
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.GRAY)

    def on_key_press(self, symbol: int, modifiers: int):
        """Handle user keyboard input.
        Q: Quit the game
        
        Arguments:
            symbol {int} -- Which key was pressed
            modifiers {int} -- Which modifiers were pressed
        """
        if symbol == arcade.key.Q:
            # Quit immediately
            arcade.close_window()


    def on_update(self, delta_time: float):
        """Update game objects and status."""
        pass

    def on_draw(self):
        """Draw all game objects."""
        arcade.start_render()  # Needs to be called before drawing



if __name__ == '__main__':
    tetris = Tetris(
        int(SCREEN_WIDTH * SCALING), int(SCREEN_HEIGHT * SCALING), SCREEN_TITLE
    )
    arcade.run()