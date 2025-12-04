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
        self.set_mouse_visible(False)
        
        self.player = __hero__.Player(width, height)
        
        # Mouse Cursor
        self.mouse_circle_center_x = width // 2
        self.mouse_circle_center_y = height // 2
        self.mouse_circle_radius = 20
        self.mouse_circle_color = arcade.color.YELLOW
        
        self.enemies = []
        self.particles = []
        self.bullets = []
        
        self.spawn_timer = 0
        self.max_enemies = 5
        self.spawn_interval = 1.0 
        
        for _ in range(self.max_enemies):
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
            
        self.mouse_circle = arcade.draw_circle_outline(self.mouse_circle_center_x, self.mouse_circle_center_y, self.mouse_circle_radius, self.mouse_circle_color, 3)
        self.player.draw()
        
    def on_resize(self, width, height):
        super().on_resize(width, height)
        self.update_background_size(width, height)
            
    def on_update(self, delta_time):
        self.player.update(self.width, self.height, delta_time)
        
        if self.player.shoot():
                bullet_x, bullet_y = self.player.get_position()
                angle = self.player.get_angle()
                new_bullet = shoot.Bullet(angle, bullet_x, bullet_y)
                self.bullets.append(new_bullet)
        
        pos_x, pos_y = self.player.get_position()
        for enemy in self.enemies:
            enemy.update(delta_time, pos_x, pos_y, self.width, self.height, self.enemies)
        
        for bullet in self.bullets:
            bullet.update()
        
        bullets_to_remove = []
        enemies_to_remove = []

        for bullet in self.bullets:
            bullet_sprite = getattr(bullet, 'bullet', getattr(bullet, 'sprite', bullet))
            
            hit_enemy = None
            for enemy in self.enemies:
                if enemy in enemies_to_remove:
                    continue
                
                if arcade.check_for_collision(bullet_sprite, enemy.enemy):
                    hit_enemy = enemy
                    break 
            
            if hit_enemy:
                bullets_to_remove.append(bullet)
                
                is_dead = hit_enemy.take_damage()
                
                if is_dead:
                    enemies_to_remove.append(hit_enemy)

        for cal in bullets_to_remove:
            if cal in self.bullets:
                self.bullets.remove(cal)
        
        for enm in enemies_to_remove:
            if enm in self.enemies:
                self.enemies.remove(enm)

        if len(self.enemies) < self.max_enemies:
            self.spawn_timer += delta_time
            if self.spawn_timer >= self.spawn_interval:
                self.enemies.append(enemies.Enemies(self.width, self.height))
                self.spawn_timer = 0 
            
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
        
        self.mouse_circle_center_x = x
        self.mouse_circle_center_y = y
        
    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.player.on_mouse_press()
            
    def on_mouse_release(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.player.on_mouse_release()


if __name__ == "__main__":
    game = Gameview(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
    arcade.run()