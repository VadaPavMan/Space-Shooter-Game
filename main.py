import arcade
import random
import particles
import __hero__
import shoot
import enemies

WINDOW_HEIGHT = 720
WINDOW_WIDTH = 1280
WINDOW_TITLE = "Space Shooter"


class Gameview(arcade.Window):
    
    def __init__(self, width, height, title):
        super().__init__(width, height, title, False, True)
        
        self.background = arcade.Sprite("assets/background.png")
        self.update_background_size(width, height)
        
        self.set_minimum_size(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.set_mouse_visible(True)
        
        self.player = __hero__.Player(width, height)
        
        self.enemies = []
        self.particles = []
        self.bullets = []
        
        for _ in range(5):
            self.enemies.append(enemies.Enemies(width, height))
        for _ in range(5):
            self.particles.append(particles.Particle(width, height))
            
    def update_background_size(self, width, height):
        self.background.center_x = width // 2
        self.background.center_y = height // 2
        self.background.width = width
        self.background.height = height
        
    def on_draw(self):
        self.clear()
        arcade.draw_sprite(self.background)
        
        for particle in self.particles:
            particle.draw()
        
        for bullet in self.bullets:
            bullet.draw()
        
        for enemy in self.enemies:
            enemy.draw()
            
        self.player.draw()
        
    def on_resize(self, width, height):
        super().on_resize(width, height)
        self.update_background_size(width, height)
            
    def on_update(self, delta_time):
        self.player.update(self.width, self.height, delta_time)
        pos_x, pos_y = self.player.get_position()
        
        for enemy in self.enemies:
            enemy.update(delta_time, pos_x, pos_y, self.width, self.height)
        # self.enemies.update(delta_time, pos_x, pos_y, self.width, self.height)
        
        for bullet in self.bullets:
            bullet.update()
            
        for i in range(len(self.bullets) - 1, -1, -1):
            if self.bullets[i].off_screen(self.width, self.height):
                self.bullets.pop(i)
        
        for particle in self.particles:
            particle.update()
    
    def on_key_press(self, key, modifiers):
        self.player.on_key_press(key, modifiers)
        
    def on_key_release(self, key, modifiers):
        self.player.on_key_release(key, modifiers)
        
    def on_mouse_motion(self, x, y, dx, dy):
        self.player.on_mouse_motion(x, y, dx, dy)
        
    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            if self.player.shoot():
                bullet_x, bullet_y = self.player.get_position()
                angle = self.player.get_angle()
                new_bullet = shoot.Bullet(angle, bullet_x, bullet_y)
                self.bullets.append(new_bullet)


if __name__ == "__main__":
    game = Gameview(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
    arcade.run()