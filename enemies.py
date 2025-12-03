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
             self.enemy.center_y = height
             
         elif self.start_edge == 1:
             self.enemy.center_x = width
             self.enemy.center_y = random.randint(0, height)
         
         elif self.start_edge == 2:
             self.enemy.center_x = random.randint(0, width)
             self.enemy.center_y = 0
         
         elif self.start_edge == 3:
             self.enemy.center_x = 0
             self.enemy.center_y = random.randint(0 , height)
    
         self.enemy.angle = 0
         self.speed = random.uniform(1, 3)
         self.follow_distance = 200
         
    def update(self, delta_time, pos_x, pos_y, width, height):
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
        
    def draw(self):
        arcade.draw_sprite(self.enemy)
    
    def get_position(self):
        return self.enemy.center_x, self.enemy.center_y