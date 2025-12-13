import arcade
from resources import resource_path  
import random
import particles
import __hero__
import shoot
import enemies
import powerups
import time

WINDOW_HEIGHT = 720
WINDOW_WIDTH = 1280
WINDOW_TITLE = "Space Shooter"

HEALTH_POWERUP = "health"
DUALs_POWERUP = "dual_shooter"
SHIELD_POWERUP = "shield"
LASER_POWERUP = "laser"
ALLIN1_POWERUP = "shield_health_max"
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
        self.mouse_circle_color = arcade.color.PINK

        self.enemies = []
        self.particles = []
        self.bullets = []
        self.enemy_bullets = [] 
        
        self.powerups = []
        self.powerups_target = 0.90
        self.powerups_increase_chance = 500
        self.powerups_timer = 0
        self.powerups_active = False
        self.powerup_type = ""
        self.dual_shoot_powerup = False
        

        self.spawn_timer = 0
        self.max_enemies = 3
        self.spawn_interval = 2.0 
        self.score = 0
        self.TARGET_TO_INCREASE_ENEMIES = 200
        self.TARGET_TO_DECREASE_INTERVAL = 300
        
        for _ in range(self.max_enemies):
            self.enemies.append(enemies.Enemies(width, height))
        
        for _ in range(5):
            self.particles.append(particles.Particle(width, height))
            
    def update_background_size(self, width, height):
        self.background.center_x = width // 2
        self.background.center_y = height // 2
        self.background.width = width
        self.background.height = height
        
    def draw_score_box(self):
        # Score Box
        bar_width = 100
        bar_height = 20
        x = 20
        y = self.height - 70
        
        # Score Text Content
        current_score = "Score: "+str(self.score)
        text_color = arcade.color.WHITE
        text_size = 12
        text_x = 40
        text_y = y+11
        if self.score >= 100:
            text_x  += 10
        elif self.score >= 1000:
            text_x  += 10
        
        arcade.draw_lrbt_rectangle_filled(
            x, x+bar_width, y, y+bar_height, arcade.color.BLUE
        )
        
        arcade.draw_lrbt_rectangle_outline(
            x, x + bar_width, y, y + bar_height, 
            arcade.color.WHITE, 2
        )
        
        arcade.draw_text(current_score, text_x, text_y,
                         text_color, text_size,
                         width=bar_width, align="center",
                         anchor_x="center", anchor_y="center", bold=True)
        
                
    
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
        
        for pu in self.powerups:
            pu.on_draw()

        for particle in self.particles:
            particle.draw()
        
        for bullet in self.bullets:
            bullet.draw()
        
        for enemy_bullet in self.enemy_bullets:
            enemy_bullet.draw()
        
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
        self.draw_score_box()
        
    def on_resize(self, width, height):
        super().on_resize(width, height)
        self.update_background_size(width, height)
            
    def on_update(self, delta_time):
        self.player.update(self.width, self.height, delta_time)
        
        self.powerup_timer()
        # Player SHooting
        if self.player.shoot():
            bullet_x, bullet_y = self.player.get_position()
            angle = self.player.get_angle()
            if not(self.dual_shoot_powerup):
                new_bullet = shoot.Bullet(angle, bullet_x, bullet_y)
            else:
                new_bullet = shoot.Player_Bullet_Dual(angle, bullet_x, bullet_y)
            self.bullets.append(new_bullet)
        
        pos_x, pos_y = self.player.get_position()
        
        for enemy in self.enemies:
            old_bullet_count = len(enemy.bullets)
            
            enemy.update(delta_time, pos_x, pos_y, self.width+50, self.height+50, self.enemies)
            
            if len(enemy.bullets) > old_bullet_count:
                new_bullets = enemy.bullets[old_bullet_count:]
                self.enemy_bullets.extend(new_bullets)
        
        for bullet in self.bullets:
            bullet.update()
        
        for enemy_bullet in self.enemy_bullets:
            enemy_bullet.update()
        
        bullets_to_remove = []
        enemies_to_remove = []
        enemy_bullets_to_remove = []

        for bullet in self.bullets:
            # Dual Bullets
            if isinstance(bullet, shoot.Player_Bullet_Dual):
                bullet_sprites = [bullet.bullet_left, bullet.bullet_right]
            else:
            # Single Bullet
                bullet_sprite = getattr(bullet, 'bullet', getattr(bullet, 'sprite', bullet))
                bullet_sprites = [bullet_sprite]
            
            hit_enemy = None
            for enemy in self.enemies:
                if enemy in enemies_to_remove:
                    continue
                
                # Collision for dual bullets
                for bs in bullet_sprites:
                    if arcade.check_for_collision(bs, enemy.enemy):
                        hit_enemy = enemy
                        break
                
                if hit_enemy:
                    break
            
            if hit_enemy:
                bullets_to_remove.append(bullet)
                
                is_dead = hit_enemy.take_damage()
                
                if is_dead:
                    enemies_to_remove.append(hit_enemy)
                    self.score += 10
                    print(f"Score: {self.score}")
                    
                    if random.random() <= self.powerups_target:            
                        if int(delta_time) % 2 == 0:
                            ex , ey = hit_enemy.get_position()
                            self.powerups.append(powerups.ShieldDemo(ex, ey))
                            if self.score >= self.powerups_increase_chance:
                                self.powerups_target += 0.05
                                self.powerups_increase_chance += 500
                                print(f"Target: {self.powerups_target}, Chance: {self.powerups_increase_chance}")
                    
                    if self.max_enemies < 26:
                        if self.score >= self.TARGET_TO_INCREASE_ENEMIES:
                            self.max_enemies += 1
                            self.TARGET_TO_INCREASE_ENEMIES += 200
                            print(f"Increase Max Enemies: {self.max_enemies}")
               
        powerups_to_remove = []
        for pu in self.powerups:
            pu.on_update(delta_time)

            if arcade.check_for_collision(self.player.player, pu.sprite):
                self.player.invincible = True
                self.player.invincible_timer = 0.0
                if HEALTH_POWERUP in pu.get_filePath():
                    self.powerups_active = True
                    self.powerup_type = pu.get_filePath()
                    heal_amount = 20
                    if self.powerups_active:
                        self.player.current_health = min(self.player.max_health, self.player.current_health + heal_amount)
                        self.powerups_active = False
                    print(f"Path: {pu.get_filePath()} And {HEALTH_POWERUP}")
                elif DUALs_POWERUP in pu.get_filePath():
                    self.dual_shoot_powerup = True
                    print(f"Path: {pu.get_filePath()} And {DUALs_POWERUP}")
                elif LASER_POWERUP in pu.get_filePath():
                    self.powerups_active = True
                    self.powerup_type = pu.get_filePath()
                    self.powerups_timer = time.time()
                    if self.powerups_active:
                        self.player.rapidfire(1)
                        self.player.player.texture = self.player.rapid_texture
                        print("Rapid Fire Active")
                        print(f"Timer: {self.powerups_timer}")
                    print(f"Path: {pu.get_filePath()} And {LASER_POWERUP}")
                elif SHIELD_POWERUP in pu.get_filePath():
                    print(f"Path: {pu.get_filePath()} And {SHIELD_POWERUP}")
                elif ALLIN1_POWERUP in pu.get_filePath():
                    print(f"Path: {pu.get_filePath()} And {ALLIN1_POWERUP}")
                self.player.update_texture()
                powerups_to_remove.append(pu)

        for pu in powerups_to_remove:
            if pu in self.powerups:
                self.powerups.remove(pu)
        
        player_sprite = self.player.player
        for enemy_bullet in self.enemy_bullets:
            if enemy_bullet in enemy_bullets_to_remove:
                continue
            
            # For Big Monster
            if isinstance(enemy_bullet, shoot.Enemy_Bullet_Dual):
                if (arcade.check_for_collision(player_sprite, enemy_bullet.bullet_left) or 
                    arcade.check_for_collision(player_sprite, enemy_bullet.bullet_right)):
                    
                    player_died = self.player.take_damage(20)
                    enemy_bullets_to_remove.append(enemy_bullet)
                    
                    
                    if player_died:
                        print("Game Over! Player died!")
            
            # For Monster            
            elif isinstance(enemy_bullet, shoot.Enemy_Bullet):
                if arcade.check_for_collision(player_sprite, enemy_bullet.bullet):
                    player_died = self.player.take_damage(10) 
                    enemy_bullets_to_remove.append(enemy_bullet)
                    
                    if player_died:
                        print("Game Over! Player died!")
        
        # Crab 
        for enemy in self.enemies:
            if enemy in enemies_to_remove:
                continue
            if arcade.check_for_collision(player_sprite, enemy.enemy):
                player_died = self.player.take_damage(10)
                
                if player_died:
                    print("Game Over! Player died!")
                
                enemies_to_remove.append(enemy) 

        for bullet in bullets_to_remove:
            if bullet in self.bullets:
                self.bullets.remove(bullet)
        
        for enemy_bullet in enemy_bullets_to_remove:
            if enemy_bullet in self.enemy_bullets:
                self.enemy_bullets.remove(enemy_bullet)
        
        for enemy in enemies_to_remove:
            if enemy in self.enemies:
                enemy.bullets.clear()
                self.enemies.remove(enemy)

        # Spawn NEw Enemies
        if len(self.enemies) < self.max_enemies:
            self.spawn_timer += delta_time
            if self.spawn_timer >= self.spawn_interval:
                self.enemies.append(enemies.Enemies(self.width+300, self.height+300))
                
                # Increase Difficulty
                if self.max_enemies < 26:
                    if self.score >= self.TARGET_TO_DECREASE_INTERVAL:
                        self.spawn_interval -= 0.1
                        self.TARGET_TO_DECREASE_INTERVAL += 300
                        print(f"Spawn Interval: {self.spawn_interval}")
                    
                if self.spawn_interval <= 0.5:
                    self.spawn_interval = 0.5
                    
                self.spawn_timer = 0 
        
        for i in range(len(self.bullets) - 1, -1, -1):
            if self.bullets[i].off_screen(self.width, self.height):
                self.bullets.pop(i)
        
        for i in range(len(self.enemy_bullets) - 1, -1, -1):
            if self.enemy_bullets[i].off_screen(self.width, self.height):
                self.enemy_bullets.pop(i)
        
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
            
    def powerup_timer(self):
        if self.powerups_active and (time.time() - self.powerups_timer) > 15:
            self.powerups_active = False
            if LASER_POWERUP in self.powerup_type:
                self.player.rapidfire(0) 
             


if __name__ == "__main__":
    game = Gameview(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
    arcade.run()