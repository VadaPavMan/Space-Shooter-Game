import config
import arcade
import random
import time

class ShieldDemo(arcade.Sprite):
    def __init__(self, x, y):
        config.config()
        choose = random.randint(1, 10)
        health_texture = "assets/powerups/health.png"
        dual_shooter_texture = "assets/powerups/dual_shooter.png"

        shield_texture = "assets/powerups/shield.png"
        laser_texture = "assets/powerups/laser.png"
        allinone_texture = "assets/powerups/max.png"

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
            count=self.FRAME_COUNT,
        )

        self.sprite = arcade.Sprite()
        self.sprite.texture = self.frames[0]
        self.sprite.center_x, self.sprite.center_y = x, y

        self.current_frame = 0
        self.frame_timer = 0.0
        self.frame_duration = 0.07
        
        self.invincible = False
        self.invincible_timer = 0
        self.invincible_duration = 1.0
        
        self.spawn_time = time.time()

    def on_draw(self):
        arcade.draw_sprite(self.sprite)
        
        if self.invincible:
            if int(self.invincible_timer * 10) % 2 == 0:
                arcade.draw_sprite(self.sprite)
        else:
            arcade.draw_sprite(self.sprite)
        

    def on_update(self, delta_time: float):
        self.frame_timer += delta_time
        if self.frame_timer >= self.frame_duration:
            self.frame_timer = 0
            self.current_frame = (self.current_frame + 1) % self.FRAME_COUNT
            self.sprite.texture = self.frames[self.current_frame]
            
        # Invincibility
        if self.invincible:
            self.invincible_timer += delta_time
            if self.invincible_timer >= self.invincible_duration:
                self.invincible = False
                self.invincible_timer = 0

    def get_filePath(self):
        return self.filePath