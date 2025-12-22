import config
import arcade
from resources import resource_path
import time

class Button:
    def __init__(self, x, y, width, height, text, color, hover_color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.current_color = color
        
    def draw(self):
        arcade.draw_lrbt_rectangle_filled(
            self.x - self.width // 2,
            self.x + self.width // 2,
            self.y - self.height // 2,
            self.y + self.height // 2,
            self.current_color
        )
        
        arcade.draw_lrbt_rectangle_outline(
            self.x - self.width // 2,
            self.x + self.width // 2,
            self.y - self.height // 2,
            self.y + self.height // 2,
            arcade.color.WHITE,
            3
        )
        
        arcade.draw_text(
            self.text,
            self.x,
            self.y,
            arcade.color.WHITE,
            20,
            anchor_x="center",
            anchor_y="center",
            bold=True
        )
    
    def is_hovered(self, mouse_x, mouse_y):
        return (self.x - self.width // 2 < mouse_x < self.x + self.width // 2 and
                self.y - self.height // 2 < mouse_y < self.y + self.height // 2)
    
    def update_hover(self, mouse_x, mouse_y):
        if self.is_hovered(mouse_x, mouse_y):
            self.current_color = self.hover_color
        else:
            self.current_color = self.color


class StartMenuView(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view
        
        self.mouse_x = 0
        self.mouse_y = 0
        
    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)
        self.window.set_mouse_visible(True)
        self.create_buttons()
    
    def create_buttons(self):
        center_x = self.window.width // 2
        button_width = 250
        button_height = 60
        button_spacing = 80
        start_y = self.window.height // 2 + 80
        
        self.buttons = [
            Button(center_x, start_y, button_width, button_height, 
                   "START", arcade.color.NAPIER_GREEN, arcade.color.GREEN),
            Button(center_x, start_y - button_spacing, button_width, button_height, 
                   "LOAD", arcade.color.DARK_BLUE, arcade.color.BLUE),
            Button(center_x, start_y - button_spacing * 2, button_width, button_height, 
                   "OPTIONS", arcade.color.DARK_BLUE, arcade.color.BLUE),
            Button(center_x, start_y - button_spacing * 3, button_width, button_height, 
                   "EXIT", arcade.color.DARK_RED, arcade.color.RED)
        ]
    
    def on_draw(self):
        self.clear()
        
        arcade.draw_text(
            "SPACE SHOOTER",
            self.window.width // 2,
            self.window.height - 150,
            arcade.color.YELLOW,
            60,
            anchor_x="center",
            anchor_y="center",
            bold=True
        )
        
        for button in self.buttons:
            button.draw()
    
    def on_mouse_motion(self, x, y, dx, dy):
        self.mouse_x = x
        self.mouse_y = y
        
        for button in self.buttons:
            button.update_hover(x, y)
    
    def on_mouse_press(self, x, y, button, modifiers):
        if self.buttons[0].is_hovered(x, y):
            self.game_view.reset_game()
            self.window.show_view(self.game_view)
            
        elif self.buttons[1].is_hovered(x, y):
            print("LOAD clicked - Feature not implemented yet")
            
        elif self.buttons[2].is_hovered(x, y):
            print("OPTIONS clicked - Feature not implemented yet")
            
        elif self.buttons[3].is_hovered(x, y):
            arcade.exit()


class PauseMenuView(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view
        
        self.mouse_x = 0
        self.mouse_y = 0
        
    def on_show_view(self):
        self.window.set_mouse_visible(True)
        self.create_buttons()
    
    def create_buttons(self):
        center_x = self.window.width // 2
        button_width = 250
        button_height = 60
        button_spacing = 80
        start_y = self.window.height // 2 + 40
        
        self.buttons = [
            Button(center_x, start_y, button_width, button_height, 
                   "RESUME", arcade.color.NAPIER_GREEN, arcade.color.GREEN),
            Button(center_x, start_y - button_spacing, button_width, button_height, 
                   "NEW GAME", arcade.color.DARK_BLUE, arcade.color.BLUE),
            Button(center_x, start_y - button_spacing * 2, button_width, button_height, 
                   "EXIT", arcade.color.DARK_RED, arcade.color.RED)
        ]
    
    def on_draw(self):
        self.game_view.on_draw()
        
        arcade.draw_lrbt_rectangle_filled(
            0, self.window.width,
            0, self.window.height,
            (0, 0, 0, 200)
        )
        
        arcade.draw_text(
            "PAUSED",
            self.window.width // 2,
            self.window.height - 150,
            arcade.color.YELLOW,
            50,
            anchor_x="center",
            anchor_y="center",
            bold=True
        )
        
        for button in self.buttons:
            button.draw()
    
    def on_mouse_motion(self, x, y, dx, dy):
        self.mouse_x = x
        self.mouse_y = y
        
        for button in self.buttons:
            button.update_hover(x, y)
    
    def on_mouse_press(self, x, y, button, modifiers):
        if self.buttons[0].is_hovered(x, y):
            countdown_view = CountdownView(self.game_view, 3)
            self.window.show_view(countdown_view)
            
        elif self.buttons[1].is_hovered(x, y):
            self.game_view.reset_game()
            countdown_view = CountdownView(self.game_view, 3)
            self.window.show_view(countdown_view)
            
        elif self.buttons[2].is_hovered(x, y):
            arcade.exit()
    
    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            countdown_view = CountdownView(self.game_view, 3)
            self.window.show_view(countdown_view)


class CountdownView(arcade.View):
    def __init__(self, game_view, countdown_seconds):
        super().__init__()
        self.game_view = game_view
        self.countdown_seconds = countdown_seconds
        self.start_time = None
        
    def on_show_view(self):
        self.start_time = time.time()
        self.window.set_mouse_visible(False)
    
    def on_draw(self):
        self.game_view.on_draw()
        
        arcade.draw_lrbt_rectangle_filled(
            0, self.window.width,
            0, self.window.height,
            (0, 0, 0, 150)
        )
        
        elapsed = time.time() - self.start_time
        remaining = self.countdown_seconds - elapsed
        
        if remaining > 0:
            countdown_text = str(int(remaining) + 1)
            arcade.draw_text(
                countdown_text,
                self.window.width // 2,
                self.window.height // 2,
                arcade.color.WHITE,
                120,
                anchor_x="center",
                anchor_y="center",
                bold=True
            )
        else:
            self.window.show_view(self.game_view)
    
    def on_update(self, delta_time):
        elapsed = time.time() - self.start_time
        if elapsed >= self.countdown_seconds:
            self.window.show_view(self.game_view)