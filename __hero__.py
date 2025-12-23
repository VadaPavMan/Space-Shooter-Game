import config
import arcade
from resources import resource_path
import random
import math
import powerups


class Player:

    def __init__(self, width, height):
        self.radius = 1.5
        self.full_health_texture = arcade.load_texture(
            resource_path("assets/hero_spaceship/ship_full.png")
        )
        self.health_60_texture = arcade.load_texture(
            resource_path("assets/hero_spaceship/ship_less_damage.png")
        )
        self.health_30_texture = arcade.load_texture(
            resource_path("assets/hero_spaceship/ship_damage.png")
        )
        self.health_10_texture = arcade.load_texture(
            resource_path("assets/hero_spaceship/ship_very_damage.png")
        )
        self.rapid_texture = arcade.load_texture(
            resource_path("assets/hero_spaceship/rapidfire.png")
        )
        self.dual_shooter_texture = arcade.load_texture(
            resource_path("assets/hero_spaceship/dual_shooter.png")
        )
        self.allin1_texture = arcade.load_texture(
            resource_path("assets/hero_spaceship/allin1.png")
        )

        self.player = arcade.Sprite(
            path_or_texture=self.full_health_texture, scale=self.radius
        )

        self.player.center_x = width // 2
        self.player.center_y = height // 2
        self.player._angle = 180

        self.PLAYERSPEED = 5
        self.PLAYERSPEED_BOOST = 10
        self.current_speed = self.PLAYERSPEED
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.space_pressed = False

        self.shoot_active = True
        self.shoot_timer = 0
        self.shoot_cooldown = 0.2
        self.mouse_held = False

        # Health system
        self.max_health = 100
        self.current_health = self.max_health
        self.invincible = False
        self.invincible_timer = 0
        self.invincible_duration = 1.0

    def draw(self):
        if not self.is_alive():
            return
        
        if self.invincible:
            if int(self.invincible_timer * 10) % 2 == 0:
                arcade.draw_sprite(self.player)
        else:
            arcade.draw_sprite(self.player)

    def update(self, width, height, delta_time):

        target_speed = (
            self.PLAYERSPEED_BOOST if self.space_pressed else self.PLAYERSPEED
        )
        self.current_speed += (target_speed - self.current_speed) * 0.1
        self.player.change_x = 0
        self.player.change_y = 0

        # Normal Speed
        if self.left_pressed and not self.right_pressed:
            self.player.change_x -= self.current_speed
        elif self.right_pressed and not self.left_pressed:
            self.player.change_x += self.current_speed

        if self.up_pressed and not self.down_pressed:
            self.player.change_y += self.current_speed
        elif self.down_pressed and not self.up_pressed:
            self.player.change_y -= self.current_speed

        # Diagonal Movement
        if self.left_pressed and self.right_pressed:
            self.player.change_x = 0
        if self.up_pressed and self.down_pressed:
            self.player.change_y = 0

        # Off Screen
        if self.player.center_x > (width - 20):
            self.player.center_x = width - 20
        elif self.player.center_x < 20:
            self.player.center_x = 20
        elif self.player.center_y > (height - 20):
            self.player.center_y = height - 20
        elif self.player.center_y < 30:
            self.player.center_y = 30

        # SHooting Cooldown
        if not self.shoot_active:
            self.shoot_timer += delta_time
            if self.shoot_timer >= self.shoot_cooldown:
                self.shoot_active = True
                self.shoot_timer = 0

        # Invincibility
        if self.invincible:
            self.invincible_timer += delta_time
            if self.invincible_timer >= self.invincible_duration:
                self.invincible = False
                self.invincible_timer = 0
        
        self.player.update()

    def update_texture(self):

        new_texture = self.full_health_texture
        if self.current_health <= 10:
            new_texture = self.health_10_texture
        elif self.current_health <= 30:
            new_texture = self.health_30_texture
        elif self.current_health <= 60:
            new_texture = self.health_60_texture

        if self.player.texture != new_texture:
            self.player.texture = new_texture

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = True
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = True
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = True
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = True
        elif key == arcade.key.SPACE:
            self.space_pressed = True

    def on_key_release(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = False
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = False
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = False
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = False
        elif key == arcade.key.SPACE:
            self.space_pressed = False

    def on_mouse_motion(self, x, y, dx, dy):
        dx = x - self.player.center_x
        dy = y - self.player.center_y
        angle_rad = math.atan2(dx, dy)
        angle_deg = math.degrees(angle_rad)
        self.player._angle = angle_deg

    def on_mouse_press(self):
        self.mouse_held = True

    def on_mouse_release(self):
        self.mouse_held = False

    def shoot(self):
        if self.shoot_active and self.mouse_held:
            self.shoot_active = False
            return True
        return False

    def get_bullet_spawn_position(self):
        return self.player.center_x, self.player.center_y

    def get_position(self):
        return self.player.center_x, self.player.center_y

    def get_angle(self):
        return self.player._angle

    def take_damage(self, damage_amount):
        if self.invincible:
            return False

        self.current_health -= damage_amount
        if damage_amount != 0:
            self.invincible = True
            self.invincible_timer = 0

            if self.current_health < 0:
                self.current_health = 0
            self.update_texture()
            return self.current_health <= 0

    def is_alive(self):
        return self.current_health > 0

    def get_health(self):
        return self.current_health, self.max_health
    
    def get_current_health(self):
        return self.current_health

    def rapidfire(self, num):
        if num:
            self.shoot_cooldown = 0.05
        else:
            self.shoot_cooldown = 0.2
            self.player.update()
            return
