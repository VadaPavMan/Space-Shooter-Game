import config
import arcade
import random

class ShieldDemo(arcade.Sprite):
    def __init__(self, x, y):
        choose = random.randint(1, 10) 
        health_texture = "assets/powerups/health.png"
        dual_shooter_texture = "assets/powerups/dual_shooter.png"
        
        shield_texture = "assets/powerups/shield.png"
        laser_texture = "assets/powerups/laser.png"
        allinone_texture = "assets/powerups/shield_health_max.png"
        
        regular_powerups = [health_texture, shield_texture]
        strong_powerups = [shield_texture, laser_texture, dual_shooter_texture]
        ultimate_powerups = [dual_shooter_texture, laser_texture, allinone_texture]
        
        if choose <= 4:
            self.SPRITE_SHEET = random.choice(regular_powerups)
            self.filePath = self.SPRITE_SHEET
        elif choose <= 8:
            self.SPRITE_SHEET = random.choice(strong_powerups)
            self.filePath = self.SPRITE_SHEET
        else:
            self.SPRITE_SHEET = random.choice(ultimate_powerups)
            self.filePath = self.SPRITE_SHEET
                
        self.FRAME_WIDTH = 32
        self.FRAME_HEIGHT = 32
        self.COLUMNS = 15
        self.FRAME_COUNT = 15
        
        sheet = arcade.load_spritesheet(self.SPRITE_SHEET)
        self.frames = sheet.get_texture_grid(
            size=(self.FRAME_WIDTH, self.FRAME_HEIGHT),
            columns=self.COLUMNS,
            count=self.FRAME_COUNT
        )

        self.sprite = arcade.Sprite()
        self.sprite.texture = self.frames[0]
        self.sprite.center_x, self.sprite.center_y = x, y

        self.current_frame = 0
        self.frame_timer = 0.0
        self.frame_duration = 0.07 

    def on_draw(self):
        arcade.draw_sprite(self.sprite)

    def on_update(self, delta_time: float):
        self.frame_timer += delta_time
        if self.frame_timer >= self.frame_duration:
            self.frame_timer = 0
            self.current_frame = (self.current_frame + 1) % self.FRAME_COUNT
            self.sprite.texture = self.frames[self.current_frame]
        
    def get_filePath(self):
        return self.filePath


# class display_power(ShieldDemo):
#     def __init__(self, x, y, type):
#         health_texture = "assets/powerups/health.png"
#         dual_shooter_texture = "assets/powerups/dual_shooter.png"
#         shield_texture = "assets/powerups/shield.png"
#         laser_texture = "assets/powerups/laser.png"
#         allinone_texture = "assets/powerups/shield_health_max.png"
        
#         if type == "rapid":
#             self.SPRITE_SHEET = laser_texture
#         elif type == "dual":
#             self.SPRITE_SHEET = dual_shooter_texture
#         elif type == "shield":
#             self.SPRITE_SHEET = shield_texture
        
#         self.FRAME_WIDTH = 32
#         self.FRAME_HEIGHT = 32
#         self.COLUMNS = 15
#         self.FRAME_COUNT = 15
        
#         sheet = arcade.load_spritesheet(self.SPRITE_SHEET)
#         self.frames = sheet.get_texture_grid(
#             size=(self.FRAME_WIDTH, self.FRAME_HEIGHT),
#             columns=self.COLUMNS,
#             count=self.FRAME_COUNT
#         )

#         self.sprite = arcade.Sprite()
#         self.sprite.texture = self.frames[0]
#         self.sprite.center_x, self.sprite.center_y = x, y

#         self.current_frame = 0
#         self.frame_timer = 0.0
#         self.frame_duration = 0.07 
        
#     def on_draw(self):
#         arcade.draw_sprite(self.sprite)

#     def on_update(self, delta_time: float):
#         self.frame_timer += delta_time
#         if self.frame_timer >= self.frame_duration:
#             self.frame_timer = 0
#             self.current_frame = (self.current_frame + 1) % self.FRAME_COUNT
#             self.sprite.texture = self.frames[self.current_frame]
        
#     # def on_draw(self):
#     #     pass
#     # def on_update(self, delta_time: float):
#     #     pass