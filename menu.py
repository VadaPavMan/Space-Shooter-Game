import config
import arcade
from resources import resource_path, load_texture_cached, load_sound_cached
import time
import main
import webbrowser


class Button:
    def __init__(self, x, y, width, height, text, color, hover_color):
        config.config()
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


class Checkbox:
    def __init__(self, x, y, size, checked=False):
        self.x = x
        self.y = y
        self.size = size
        self.checked = checked
        self.rect = None
        
    def draw(self):
        arcade.draw_lrbt_rectangle_outline(
            self.x - self.size // 2,
            self.x + self.size // 2,
            self.y - self.size // 2,
            self.y + self.size // 2,
            arcade.color.WHITE,
            2
        )
        
        if self.checked:
            arcade.draw_lrbt_rectangle_filled(
                self.x - self.size // 2 + 4,
                self.x + self.size // 2 - 4,
                self.y - self.size // 2 + 4,
                self.y + self.size // 2 - 4,
                arcade.color.GREEN
            )
            
        self.rect = (
            self.x - self.size // 2,
            self.y - self.size // 2,
            self.size,
            self.size
        )
    
    def is_hovered(self, mouse_x, mouse_y):
        if not self.rect:
            return False
        left, bottom, width, height = self.rect
        return (left <= mouse_x <= left + width and 
                bottom <= mouse_y <= bottom + height)
    
    def toggle(self):
        self.checked = not self.checked
        return self.checked


class StartMenuView(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        config.config()
        self.game_view = game_view
        
        self.mouse_x = 0
        self.mouse_y = 0
        self.background = None
        bg_start_music = load_sound_cached("assets/sound/start_menu.mp3")
        self.background_music = arcade.play_sound(bg_start_music, loop=True, volume=1.0)
        
        if self.background_music:
            self.background_music.volume = 0.3 
        
    def on_show_view(self):
        if self.background is None:
            self.background = arcade.Sprite(load_texture_cached("assets/startscreen.png"))
        
        self.background.center_x = self.width // 2
        self.background.center_y = self.height // 2
        self.background.alpha = 100
        self.window.set_mouse_visible(True)
        self.create_buttons()
    
    def create_buttons(self):
        center_x = self.window.width // 2
        start_y = self.window.height // 2 + 80
        button_width = 250
        button_height = 60
        button_spacing = 80
        
        self.buttons = [
            Button(center_x, start_y, button_width, button_height, 
                   "START", arcade.color.NAPIER_GREEN, arcade.color.GREEN),
            Button(center_x, start_y - button_spacing, button_width, button_height, 
                   "OPTIONS", arcade.color.DARK_BLUE, arcade.color.BLUE),
            Button(center_x, start_y - button_spacing * 2, button_width, button_height, 
                   "CREDITS", arcade.color.SAE, arcade.color.AMBER),
            Button(center_x, start_y - button_spacing * 3, button_width, button_height, 
                   "EXIT", arcade.color.DARK_RED, arcade.color.RED)
        ]
    
    def on_draw(self):
        self.clear()
        arcade.draw_sprite(self.background)
        arcade.draw_text(
            "GALACTIC COMBAT",
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
            arcade.stop_sound(self.background_music)
            self.window.show_view(self.game_view)
            
        elif self.buttons[1].is_hovered(x, y):
            print("OPTIONS clicked")
            arcade.stop_sound(self.background_music)
            options_view = OptionsMenuView(self.game_view)
            self.window.show_view(options_view)
            
        elif self.buttons[2].is_hovered(x, y):
            print("CREDITS clicked")
            arcade.stop_sound(self.background_music)
            credits_view = CreditTab(self.game_view)
            self.window.show_view(credits_view)
            
        elif self.buttons[3].is_hovered(x, y):
            arcade.exit()


class OptionsMenuView(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        config.config()
        self.game_view = game_view
        self.mouse_x = 0
        self.mouse_y = 0
        self.background = None
        bg_options_music = load_sound_cached("assets/sound/pause_menu.mp3")
        self.background_music = arcade.play_sound(bg_options_music, loop=True, volume=1.0)
        
        if self.background_music:
            self.background_music.volume = 0.3
            
        self.back_button = None
        if not hasattr(self.window, 'music_enabled'):
            self.window.music_enabled = True
        self.music_checkbox = None
        
    def on_show_view(self):
        if self.background is None:
            self.background = arcade.Sprite(load_texture_cached("assets/startscreen.png"))
        
        self.background.center_x = self.width // 2
        self.background.center_y = self.height // 2
        self.background.alpha = 100
        self.window.set_mouse_visible(True)
        
        center_x = self.window.width // 2
        button_y = 100
        self.back_button = Button(
            center_x, button_y, 250, 60,
            "BACK TO MENU", arcade.color.AMBER, arcade.color.SAE
        )
        
        checkbox_x = center_x + 130
        checkbox_y = self.window.height // 2 + 47
        self.music_checkbox = Checkbox(checkbox_x, checkbox_y, 30, self.window.music_enabled)
    
    def on_draw(self):
        self.clear()
        arcade.draw_sprite(self.background)
        arcade.draw_lrbt_rectangle_filled(
            0, self.window.width,
            0, self.window.height,
            (0, 0, 0, 100)
        )
        
        arcade.draw_text(
            "OPTIONS",
            self.window.width // 2,
            self.window.height - 100,
            arcade.color.YELLOW,
            50,
            anchor_x="center",
            anchor_y="center",
            bold=True
        )
        
        center_x = self.window.width // 2
        music_text_y = self.window.height // 2 + 50
        
        arcade.draw_text(
            "BACKGROUND MUSIC:",
            center_x - 100,
            music_text_y,
            arcade.color.WHITE,
            28,
            anchor_x="center",
            anchor_y="center",
            bold=True
        )
        
        if self.music_checkbox:
            self.music_checkbox.draw()
            
            status_text = "ENABLED" if self.music_checkbox.checked else "DISABLED"
            status_color = arcade.color.GREEN if self.music_checkbox.checked else arcade.color.RED
            
            arcade.draw_text(
                f"({status_text})",
                center_x + 230,
                music_text_y,
                status_color,
                22,
                anchor_x="center",
                anchor_y="center",
                bold=True
            )
        
        instruction_y = self.window.height // 2 - 10
        arcade.draw_text(
            "CLICK THE CHECKBOX TO TOGGLE BACKGROUND MUSIC",
            center_x,
            instruction_y,
            arcade.color.LIGHT_GRAY,
            18,
            anchor_x="center",
            anchor_y="center"
        )
        
        if self.back_button:
            self.back_button.draw()
    
    def on_mouse_motion(self, x, y, dx, dy):
        self.mouse_x = x
        self.mouse_y = y
        
        if self.back_button:
            self.back_button.update_hover(x, y)
    
    def on_mouse_press(self, x, y, button, modifiers):
        if self.music_checkbox and self.music_checkbox.is_hovered(x, y):
            self.music_checkbox.toggle()
            self.window.music_enabled = self.music_checkbox.checked
            
            if not self.music_checkbox.checked:
                if self.background_music:
                    arcade.stop_sound(self.background_music)
            else:
                if not self.background_music.playing:
                    self.background_music.play()
                    
            print(f"Background music: {'ENABLED' if self.music_checkbox.checked else 'DISABLED'}")
            return
        
        if self.back_button and self.back_button.is_hovered(x, y):
            arcade.stop_sound(self.background_music)
            self.window.show_view(StartMenuView(self.game_view))
    
    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            arcade.stop_sound(self.background_music)
            self.window.show_view(StartMenuView(self.game_view))


class PauseMenuView(arcade.View):
    def __init__(self, game_view, dead= False):
        super().__init__()
        config.config()
        self.game_view = game_view
        self.is_dead = dead
        self.mouse_x = 0
        self.mouse_y = 0
        bg_start_music = load_sound_cached("assets/sound/pause_menu.mp3")
        self.background_music = arcade.play_sound(bg_start_music, loop=True, volume=1.0)
        
        if self.background_music:
            self.background_music.volume = 0.3  
        
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
                   "EXIT MENU", arcade.color.DARK_RED, arcade.color.RED)
        ]
    
    def on_draw(self):
        self.game_view.on_draw()
        
        if self.is_dead:
            text = "GAME OVER"
        else:
            text = "PAUSED"
        
        arcade.draw_lrbt_rectangle_filled(
            0, self.window.width,
            0, self.window.height,
            (0, 0, 0, 200)
        )
        
        arcade.draw_text(
            text,
            self.window.width // 2,
            self.window.height - 150,
            arcade.color.YELLOW,
            50,
            anchor_x="center",
            anchor_y="center",
            bold=True
        )
        
        if self.is_dead:
            self.buttons[1].draw()
            self.buttons[2].draw()
        else:
            self.buttons[0].draw()
            self.buttons[1].draw()
            self.buttons[2].draw()
    
    def on_mouse_motion(self, x, y, dx, dy):
        self.mouse_x = x
        self.mouse_y = y
        
        for button in self.buttons:
            button.update_hover(x, y)
    
    def on_mouse_press(self, x, y, button, modifiers):
        if not self.is_dead and self.buttons[0].is_hovered(x, y):
            arcade.stop_sound(self.background_music)
            countdown_view = CountdownView(self.game_view, 3)
            self.window.show_view(countdown_view)
            
        elif self.buttons[1].is_hovered(x, y):
            self.game_view.reset_game()
            arcade.stop_sound(self.background_music)
            countdown_view = CountdownView(self.game_view, 3)
            self.window.show_view(countdown_view)
            
        elif self.buttons[2].is_hovered(x, y):
            self.game_view.reset_game()
            arcade.stop_sound(self.background_music)
            self.window.show_view(StartMenuView(self.game_view))
    
    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE and not self.is_dead:
            arcade.stop_sound(self.background_music)
            countdown_view = CountdownView(self.game_view, 3)
            self.window.show_view(countdown_view)


class CountdownView(arcade.View):
    def __init__(self, game_view, countdown_seconds):
        super().__init__()
        config.config()
        self.game_view = game_view
        self.countdown_seconds = countdown_seconds
        self.start_time = 0
        
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


class CreditTab(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        config.config()
        self.game_view = game_view
        self.mouse_x = 0
        self.mouse_y = 0
        self.background = None
        bg_start_music = load_sound_cached("assets/sound/pause_menu.mp3")
        self.background_music = arcade.play_sound(bg_start_music, loop=True)
        
        if self.background_music:
            self.background_music.volume = 0.3  
        
        self.back_button = None
        
        # Credits
        self.credits = [
            {
                "label": "CREATOR:",
                "author": "vadapavman",
                "url": "https://github.com/VadaPavMan",
                "rect": None,
                "hovered": False
            },
            {
                "label": "SHIPS & POWERUPS ASSETS, CREDIT:",
                "author": "foozlecc",
                "url": "https://foozlecc.itch.io",
                "rect": None,
                "hovered": False
            },
            {
                "label": "BACKGROUND SPACE ASSETS, CREDIT:",
                "author": "fraang",
                "url": "https://opengameart.org/users/fraang",
                "rect": None,
                "hovered": False
            },
            {
                "label": "BACKGROUND MUSIC, CREDIT:",
                "author": "oblidivm",
                "url": "https://opengameart.org/users/oblidivm",
                "rect": None,
                "hovered": False
            },
            {
                "label": "SHOOTING SFX, CREDIT:",
                "author": "bolkmar",
                "url": "https://freesound.org/people/bolkmar/sounds/421704/",
                "rect": None,
                "hovered": False
            },
            {
                "label": "",
                "author": "djfroyd",
                "url": "https://freesound.org/people/djfroyd/sounds/348163/",
                "rect": None,
                "hovered": False
            },
            {
                "label": "",
                "author": "freesound_community",
                "url": "https://pixabay.com/users/freesound_community-46691455/",
                "rect": None,
                "hovered": False
            }
        ]
        
    def on_show_view(self):
        if self.background is None:
            self.background = arcade.Sprite(load_texture_cached("assets/startscreen.png"))
        
        self.background.center_x = self.width // 2
        self.background.center_y = self.height // 2
        self.background.alpha = 255
        self.window.set_mouse_visible(True)
        center_x = self.window.width // 2
        button_y = 100
        self.back_button = Button(
            center_x, button_y, 250, 60,
            "BACK TO MENU", arcade.color.AMBER, arcade.color.SAE
        )
        
    def on_draw(self):
        self.clear()
        arcade.draw_sprite(self.background)
        arcade.draw_lrbt_rectangle_filled(
            0, self.window.width,
            0, self.window.height,
            (0, 0, 0, 100)
        )
        
        arcade.draw_text(
            "CREDITS",
            self.window.width // 2,
            self.window.height - 100,
            arcade.color.YELLOW,
            50,
            anchor_x="center",
            anchor_y="center",
            bold=True
        )
             
        start_y = self.window.height - 200
        line_spacing = 50
        current_y = start_y
        
        arcade.draw_text(
                "(click on names to view)",
                self.window.width // 2,
                current_y + 30,
                arcade.color.LIGHT_GRAY,
                11,
                anchor_x="center",
                anchor_y="center",
                italic=True
            )
        
        prev_label = None
        for credit in self.credits:
            if credit["label"] and credit["label"] != prev_label:
                arcade.draw_text(
                    credit["label"],
                    self.window.width // 2,
                    current_y,
                    arcade.color.WHITE,
                    24,
                    anchor_x="center",
                    anchor_y="center",
                    bold=True
                )
                current_y -= 35
                prev_label = credit["label"]
            elif not credit["label"] and prev_label:
                current_y -= 1
            
            author_color = arcade.color.ORANGE if credit["hovered"] else arcade.color.YELLOW
            arcade.draw_text(
                credit["author"],
                self.window.width // 2,
                current_y,
                author_color,
                22,
                anchor_x="center",
                anchor_y="center",
                bold=True
            )
            
            text_width = len(credit["author"]) * 12  
            text_height = 22
            
            credit["rect"] = (
                self.window.width // 2 - text_width // 2,  
                current_y - text_height // 2,
                text_width,  
                text_height  
            )
            
            current_y -= line_spacing
        
        current_y -= 20
        arcade.draw_text(
            "GAME DEVELOPED WITH ARCADE LIBRARY",
            self.window.width // 2,
            current_y,
            arcade.color.LIGHT_GRAY,
            18,
            anchor_x="center",
            anchor_y="center",
            bold=True
        )
        
        current_y -= 40
        arcade.draw_text(
            "Press ESC or click BACK TO MENU to return",
            self.window.width // 2,
            current_y,
            arcade.color.LIGHT_GRAY,
            16,
            anchor_x="center",
            anchor_y="center"
        )
        
        if self.back_button:
            self.back_button.draw()
    
    def on_mouse_motion(self, x, y, dx, dy):
        self.mouse_x = x
        self.mouse_y = y
        
        if self.back_button:
            self.back_button.update_hover(x, y)
        
        for credit in self.credits:
            if credit["rect"]:
                left, bottom, width, height = credit["rect"]
                if (left <= x <= left + width and 
                    bottom <= y <= bottom + height):
                    credit["hovered"] = True
                else:
                    credit["hovered"] = False
    
    def on_mouse_press(self, x, y, button, modifiers):
        for credit in self.credits:
            if credit["rect"]:
                left, bottom, width, height = credit["rect"]
                if (left <= x <= left + width and 
                    bottom <= y <= bottom + height):
                    webbrowser.open(credit["url"])
                    return
        
        if self.back_button and self.back_button.is_hovered(x, y):
            arcade.stop_sound(self.background_music)
            self.window.show_view(StartMenuView(self.game_view))
        
    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            arcade.stop_sound(self.background_music)
            self.window.show_view(StartMenuView(self.game_view))
