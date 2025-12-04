import arcade
import math
import random

class Enemies():
    
    def __init__(self, width, height):
        self.radius = 0.15
        self.enemy = arcade.Sprite("assets/plane.png", self.radius)
        self.start_edge = random.randint(0, 3)
        
        if self.start_edge == 0:
            self.enemy.center_x = random.randint(0, width)
            self.enemy.center_y = height + 300
        elif self.start_edge == 1:
            self.enemy.center_x = width + 300
            self.enemy.center_y = random.randint(0, height)
        elif self.start_edge == 2:
            self.enemy.center_x = random.randint(0, width)
            self.enemy.center_y = -300
        elif self.start_edge == 3:
            self.enemy.center_x = -300
            self.enemy.center_y = random.randint(0, height)
        
        self.enemy.angle = 0
        self.speed = random.uniform(1, 2)
        self.follow_distance = 200
        self.separation_distance = 80  
        
        self.enemy_active = True
        
        self.max_health = 4
        self.current_health = self.max_health
        
    def update(self, delta_time, pos_x, pos_y, width, height, other_enemies):
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
        
        if distance > self.follow_distance:
            move_x = direction_x * self.speed
            move_y = direction_y * self.speed
        elif distance < self.follow_distance - 50:
            move_x = -direction_x * self.speed
            move_y = -direction_y * self.speed
        
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
        
        # Movement
        self.enemy.center_x += move_x
        self.enemy.center_y += move_y
        
        # In_Screen
        if self.enemy.center_x <= 20:
            self.enemy.center_x = 20
        elif self.enemy.center_x >= width - 20:
            self.enemy.center_x = width - 20
        
        if self.enemy.center_y <= 20:
            self.enemy.center_y = 20
        elif self.enemy.center_y >= height - 20:
            self.enemy.center_y = height - 20

    def take_damage(self):
        self.current_health -= 1
        return self.current_health <= 0
    
    def draw(self):
        arcade.draw_sprite(self.enemy)
        
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
        
        arcade.draw_lrbt_rectangle_filled(left, right, bottom,top, arcade.color.RED)
        
        green_right = left + current_bar_width
        arcade.draw_lrbt_rectangle_filled(left, green_right, bottom, top, arcade.color.GREEN)
    
    def get_position(self):
        return self.enemy.center_x, self.enemy.center_y