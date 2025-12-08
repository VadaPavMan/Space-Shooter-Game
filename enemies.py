import arcade
import math
from resources import resource_path
import random
import shoot

class Enemies():
    
    def __init__(self, width, height):
        self.choose = random.randint(1, 3)
        self.hard_choose = random.randint(0, 1)
        self.crab_texture = arcade.load_texture(resource_path("assets/enemies_ship/enemy_crab.png"))
        self.moster_texture = arcade.load_texture(resource_path("assets/enemies_ship/enemy_moster.png"))
        self.big_moster_texture = arcade.load_texture(resource_path("assets/enemies_ship/enemy_big_moster.png"))
        # self.enemy = arcade.Sprite(self.crab_texture, self.radius)
        
        if self.choose == 1:
            self.enemy = arcade.Sprite(self.crab_texture, 1.5)
        elif self.choose == 2:
            self.enemy = arcade.Sprite(self.moster_texture, 1.8)
        elif self.choose == 3:
            self.enemy = arcade.Sprite(self.big_moster_texture, 0.7)
            
            
        self.start_edge = random.randint(0, 3)
        
        if self.start_edge == 0:  # Top
            self.enemy.center_x = random.randint(0, width)
            self.enemy.center_y = height + 500
        elif self.start_edge == 1:  # Right
            self.enemy.center_x = width + 500
            self.enemy.center_y = random.randint(0, height)
        elif self.start_edge == 2:  # Bottom
            self.enemy.center_x = random.randint(0, width)
            self.enemy.center_y = -500
        elif self.start_edge == 3:  # Left
            self.enemy.center_x = -500
            self.enemy.center_y = random.randint(0, height)
        
        self.enemy.angle = 0
        self.speed = random.uniform(1, 2)
        self.follow_distance = 0
        if self.enemy.texture != self.crab_texture:
            self.follow_distance = 200
        if self.enemy.texture == self.crab_texture:
            self.speed = 3
        self.separation_distance = 80  
        
        self.just_spawned = True
        self.spawn_time = 0
        self.spawn_duration = 2.0  
        
        self.shoot_active = True
        self.shoot_cooldown = 2
        self.shoot_timer = 0
        self.max_health = 4
        self.current_health = self.max_health
        
        self.bullets = []
        
    def update(self, delta_time, pos_x, pos_y, width, height, other_enemies):
        if self.just_spawned:
            self.spawn_time += delta_time
            if self.spawn_time >= self.spawn_duration:
                self.just_spawned = False
            speed_multiplier = 0.4  
        else:
            speed_multiplier = 1.0  
        
        diff_x = pos_x - self.enemy.center_x
        diff_y = pos_y - self.enemy.center_y
        distance = math.sqrt(diff_x * diff_x + diff_y * diff_y)
        
        if distance == 0:
            return
        
        angle_to_player_rad = math.atan2(diff_x, diff_y)
        angle_to_player_deg = math.degrees(angle_to_player_rad)
        self.enemy.angle = angle_to_player_deg
        
        move_x = 0
        move_y = 0
        
        direction_x = diff_x / distance
        direction_y = diff_y / distance
        
        actual_speed = self.speed * speed_multiplier
        
        # To Prevent Collision Glitch
        if distance > self.follow_distance:
            move_x = direction_x * actual_speed
            move_y = direction_y * actual_speed
            
        elif distance < self.follow_distance - 50:
            move_x = -direction_x * actual_speed
            move_y = -direction_y * actual_speed
        
        separation_x = 0
        separation_y = 0
        
        for other in other_enemies:
            if other is self:  
                continue
            
            other_x, other_y = other.get_position()
            dist_x = self.enemy.center_x - other_x
            dist_y = self.enemy.center_y - other_y
            dist_to_other = math.sqrt(dist_x * dist_x + dist_y * dist_y)
            
            if dist_to_other < self.separation_distance and dist_to_other > 0:
                separation_strength = (self.separation_distance - dist_to_other) / self.separation_distance
                separation_x += (dist_x / dist_to_other) * separation_strength * 3
                separation_y += (dist_y / dist_to_other) * separation_strength * 3
        
        move_x += separation_x
        move_y += separation_y
        
        self.enemy.center_x += move_x
        self.enemy.center_y += move_y
        
        if self.enemy.center_x <= 20:
            self.enemy.center_x = 20
        elif self.enemy.center_x >= width - 20:
            self.enemy.center_x = width - 20
        
        if self.enemy.center_y <= 20:
            self.enemy.center_y = 20
        elif self.enemy.center_y >= height - 20:
            self.enemy.center_y = height - 20
            
        if self.enemy.texture == self.big_moster_texture:
            if self.shoot():
                bullet_x, bullet_y = self.get_position()
                angle = self.get_angle()
                new_bullet = shoot.Enemy_Bullet_Dual(angle, bullet_x, bullet_y)
                self.bullets.append(new_bullet)
        
        for bullet in self.bullets:
            bullet.update()
            
        if not self.shoot_active:
            self.shoot_timer += delta_time
            if self.shoot_timer >= self.shoot_cooldown:
                self.shoot_active = True
                self.shoot_timer = 0
                
        for i in range(len(self.bullets) - 1, -1, -1):
            if self.bullets[i].off_screen(width,height):
                self.bullets.pop(i)

    def take_damage(self):
        self.current_health -= 1
        return self.current_health <= 0
    
    def draw(self):
        arcade.draw_sprite(self.enemy)
        
        if self.enemy.texture == self.big_moster_texture:
            for bullet in self.bullets:
                bullet.draw()
                
        if self.current_health < self.max_health and self.current_health > 0:
            self.draw_health_bar()

    def draw_health_bar(self):
        bar_width = 40
        bar_height = 5
        y_offset = 35 
        
        health_ratio = self.current_health / self.max_health
        current_bar_width = bar_width * health_ratio
        
        cx = self.enemy.center_x
        cy = self.enemy.center_y + y_offset
        
        left = cx - bar_width / 2
        right = cx + bar_width / 2
        bottom = cy - bar_height / 2
        top = cy + bar_height / 2
        
        arcade.draw_lrbt_rectangle_filled(left, right, bottom, top, arcade.color.RED)
        
        green_right = left + current_bar_width
        arcade.draw_lrbt_rectangle_filled(left, green_right, bottom, top, arcade.color.GREEN)
    
    def get_position(self):
        return self.enemy.center_x, self.enemy.center_y
    
    def get_angle(self):
        return self.enemy.angle
    
    def shoot(self):
        if self.shoot_active:
            self.shoot_active = False
            return True
        return False