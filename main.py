import arcade

WINDOW_HEIGHT = 720;
WINDOW_WIDTH = 1280;
WINDOW_TITLE = "Space Shooter";

class Gameview(arcade.Window):
    
    def __init__(self, width, height, title):
        self.min_width = WINDOW_WIDTH;
        self.min_height = WINDOW_HEIGHT;
        super().__init__(width, height, title, False, True, 1 / 60, True);
        self.set_minimum_size(WINDOW_WIDTH, WINDOW_HEIGHT);
        self.background = arcade.Sprite("assets/background.png")
        self.update_background_size(width, height)
        
    def update_background_size(self, width, height): 
        self.background.center_x = width//2;
        self.background.center_y = height//2;
        self.background.width = width;
        self.background.height = height;
        
    def on_draw(self):
        self.clear();
        arcade.draw_sprite(self.background);
        
    def on_resize(self, width, height):
        super().on_resize(width, height);
        print(f"Window resized to: {width}x{height}")
        self.update_background_size(width, height)
        

if __name__ == "__main__":
    game = Gameview(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE);
    arcade.run()