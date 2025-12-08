import arcade
from resources import resource_path  
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
        
        self.background = arcade.Sprite(resource_path("assets/background.png"))
        self.update_background_size(width, height)
        
        self.set_minimum_size(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.set_mouse_visible(False)
        
        self.player = __hero__.Player(width, height)
        
        # Mouse Cursor
        self.mouse_circle_center_x = width // 2
        self.mouse_circle_center_y = height // 2
        self.mouse_circle_radius = 10
        self.mouse_circle_color = arcade.color.YELLOW
        
        self.enemies = []
        self.particles = []
        self.bullets = []
        

        self.spawn_timer = 0
        self.max_enemies = 3
        self.spawn_interval = 2.0 
        self.score = 0
        self.TARGET_TO_INCREASE_ENEMIES = 100
        self.TARGET_TO_DECREASE_INTERVAL = 200
        
        for _ in range(self.max_enemies):
            self.enemies.append(enemies.Enemies(width, height))
        
        for _ in range(1):
            self.particles.append(particles.Particle(width, height))
            
    def update_background_size(self, width, height):
        self.background.center_x = width // 2
        self.background.center_y = height // 2
        self.background.width = width
        self.background.height = height
    
    def draw_player_health_bar(self):
        bar_width = 200
        bar_height = 20
        x = 20  
        y = self.height - 40  
        
        current_health, max_health = self.player.get_health()
        health_ratio = current_health / max_health
        current_bar_width = bar_width * health_ratio
        
        arcade.draw_lrbt_rectangle_filled(
            x, x + bar_width, y, y + bar_height, 
            arcade.color.DARK_RED
        )
        
        if health_ratio > 0.6:
            bar_color = arcade.color.GREEN
        elif health_ratio > 0.3:
            bar_color = arcade.color.YELLOW
        else:
            bar_color = arcade.color.RED
        
        arcade.draw_lrbt_rectangle_filled(
            x, x + current_bar_width, y, y + bar_height, 
            bar_color
        )
        
        arcade.draw_lrbt_rectangle_outline(
            x, x + bar_width, y, y + bar_height, 
            arcade.color.WHITE, 2
        )
        
        health_text = f"HP: {int(current_health)}/{int(max_health)}"
        arcade.draw_text(
            health_text, 
            x + bar_width + 10, y + 2, 
            arcade.color.WHITE, 14, 
            bold=True
        )
        
    def on_draw(self):
        self.clear()
        arcade.draw_sprite(self.background)
        
        for particle in self.particles:
            particle.draw()
        
        for bullet in self.bullets:
            bullet.draw()
        
        for enemy in self.enemies:
            enemy.draw()
        
        arcade.draw_circle_outline(
            self.mouse_circle_center_x, 
            self.mouse_circle_center_y, 
            self.mouse_circle_radius, 
            self.mouse_circle_color, 
            3
        )
        
        self.player.draw()
        
        self.draw_player_health_bar()
        
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
            enemy.update(delta_time, pos_x, pos_y, self.width+50, self.height+50, self.enemies)
        
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
                    self.score += 10
                    print(self.score)
                    
                    if self.score >= self.TARGET_TO_INCREASE_ENEMIES:
                        self.max_enemies += 1
                        self.TARGET_TO_INCREASE_ENEMIES += 100
                        print(f"Increase Max Enemies: {self.max_enemies}, Target: {self.TARGET_TO_INCREASE_ENEMIES}") #Debug
        
        player_sprite = self.player.player
        for enemy in self.enemies:
            if enemy in enemies_to_remove:
                continue
            if arcade.check_for_collision(player_sprite, enemy.enemy):
                player_died = self.player.take_damage(10)
                
                if player_died:
                    print("Game Over! Player died!") #Debug
                
                enemies_to_remove.append(enemy) 

        for bullet in bullets_to_remove:
            if bullet in self.bullets:
                self.bullets.remove(bullet)
        
        for enemy in enemies_to_remove:
            if enemy in self.enemies:
                self.enemies.remove(enemy)

        if len(self.enemies) < self.max_enemies:
            self.spawn_timer += delta_time
            if self.spawn_timer >= self.spawn_interval:
                self.enemies.append(enemies.Enemies(self.width+300, self.height+300))
                # Enemies Fast Spawn
                if self.score >= self.TARGET_TO_DECREASE_INTERVAL:
                    self.spawn_interval -= 0.1
                    self.TARGET_TO_DECREASE_INTERVAL += 200
                    print(f"Spawn Interval: {self.spawn_interval}, Target: {self.TARGET_TO_DECREASE_INTERVAL}") #Debug
                elif self.spawn_interval <= 0.5:
                    self.spawn_interval = 0.5
                    print(f"Spawn Interval: {self.spawn_interval}, Target: {self.TARGET_TO_DECREASE_INTERVAL}") #Debug
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