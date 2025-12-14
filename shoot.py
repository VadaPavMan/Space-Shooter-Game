import config
import arcade
import math
from resources import resource_path
import random
import enemies

class Bullet(arcade.Sprite):
    def __init__(self, angle, x, y):
        self.radius = 0.3
        self.bullet = arcade.Sprite(resource_path("assets/bullets/06.png"), self.radius)
        self.bullet.center_x = x
        self.bullet.center_y = y
        self.bullet.angle = angle
        
        self.speed = 10
        
        
    def update(self):
        angle_rad = math.radians(self.bullet.angle)
        self.bullet.center_x += math.sin(angle_rad) * self.speed
        self.bullet.center_y += math.cos(angle_rad) * self.speed
    
    def draw(self):
        arcade.draw_sprite(self.bullet)
    
    def off_screen(self, width, height):
        return (self.bullet.center_x < -10 or self.bullet.center_x > width + 10 or self.bullet.center_y < -10 or self.bullet.center_y > height + 10)



class Enemy_Bullet(arcade.Sprite):
    def __init__(self, angle, x, y, speed= 4):
        self.radius = 0.2
        angle_rad = math.radians(angle)
        forward_offset = 10
        forward_x = math.sin(angle_rad) * forward_offset
        forward_y = math.cos(angle_rad) * forward_offset
        self.normal_bullet = arcade.load_texture(resource_path("assets/bullets/02.png"))
        self.bullet = arcade.Sprite(self.normal_bullet, self.radius)
        self.bullet.center_x = x + forward_x
        self.bullet.center_y = y + forward_y
        self.bullet.angle = angle
        
        if not speed:
            self.speed = 4
        else:
            self.speed = speed
        
    def update(self):
        angle_rad = math.radians(self.bullet.angle)
        self.bullet.center_x += math.sin(angle_rad) * self.speed
        self.bullet.center_y += math.cos(angle_rad) * self.speed
        
    def draw(self):
        arcade.draw_sprite(self.bullet)
    
    def off_screen(self, width, height):
        return (self.bullet.center_x < -10 or self.bullet.center_x > width + 10 or self.bullet.center_y < -10 or self.bullet.center_y > height + 10)
    
class Enemy_Bullet_High_Damage(arcade.Sprite):
    def __init__(self, angle, x, y, speed= 4):
        self.radius = 0.2
        angle_rad = math.radians(angle)
        forward_offset = 15
        forward_x = math.sin(angle_rad) * forward_offset
        forward_y = math.cos(angle_rad) * forward_offset
        self.high_damage_bullet = arcade.load_texture(resource_path("assets/bullets/19.png"))
        self.bullet = arcade.Sprite(self.high_damage_bullet, 0.15)
        self.bullet.center_x = x + forward_x
        self.bullet.center_y = y + forward_y
        self.bullet.angle = angle
        
        if not speed:
            self.speed = 4
        else:
            self.speed = speed
            
    def high_damage(self):
        if enemies.Enemies.high_damage_enemy:
            return True
        else:
            return False
        
        
    def update(self):
        angle_rad = math.radians(self.bullet.angle)
        self.bullet.center_x += math.sin(angle_rad) * self.speed
        self.bullet.center_y += math.cos(angle_rad) * self.speed
        
    def draw(self):
        arcade.draw_sprite(self.bullet)
    
    def off_screen(self, width, height):
        return (self.bullet.center_x < -10 or self.bullet.center_x > width + 10 or self.bullet.center_y < -10 or self.bullet.center_y > height + 10)
    

class Enemy_Bullet_Dual(arcade.Sprite):
    def __init__(self, angle, x, y):
        self.radius = 0.1
        angle_rad = math.radians(angle)
        
        gun_offset = 15 
        forward_offset = 30  

        perpendicular_angle_rad = angle_rad + math.radians(90)
        
        forward_x = math.sin(angle_rad) * forward_offset
        forward_y = math.cos(angle_rad) * forward_offset
        
        perp_x = math.sin(perpendicular_angle_rad) * gun_offset
        perp_y = math.cos(perpendicular_angle_rad) * gun_offset
        
        self.bullet_right = arcade.Sprite("assets/bullets/14.png", self.radius)
        self.bullet_right.center_x = x + perp_x + forward_x
        self.bullet_right.center_y = y + perp_y + forward_y
        self.bullet_right.angle = angle
        
        self.bullet_left = arcade.Sprite("assets/bullets/14.png", self.radius)
        self.bullet_left.center_x = x - perp_x + forward_x
        self.bullet_left.center_y = y - perp_y + forward_y
        self.bullet_left.angle = angle
        
        self.speed = 4
        
    def update(self):
        angle_rad = math.radians(self.bullet_left.angle)
        self.bullet_left.center_x += math.sin(angle_rad) * self.speed
        self.bullet_left.center_y += math.cos(angle_rad) * self.speed
        
        angle_rad = math.radians(self.bullet_right.angle)
        self.bullet_right.center_x += math.sin(angle_rad) * self.speed
        self.bullet_right.center_y += math.cos(angle_rad) * self.speed
    
    def draw(self):
        arcade.draw_sprite(self.bullet_left)
        arcade.draw_sprite(self.bullet_right)
    
    def off_screen(self, width, height):
        return ((self.bullet_right.center_x < -10 or self.bullet_right.center_x > width + 10 or 
                 self.bullet_right.center_y < -10 or self.bullet_right.center_y > height + 10) or 
                (self.bullet_left.center_x < -10 or self.bullet_left.center_x > width + 10 or 
                 self.bullet_left.center_y < -10 or self.bullet_left.center_y > height + 10))


class Player_Bullet_Dual(arcade.Sprite):
    def __init__(self, angle, x, y):
        self.radius = 0.15
        angle_rad = math.radians(angle)
        
        gun_offset = 12 
        forward_offset = 5  

        perpendicular_angle_rad = angle_rad + math.radians(90)
        
        forward_x = math.sin(angle_rad) * forward_offset
        forward_y = math.cos(angle_rad) * forward_offset
        
        perp_x = math.sin(perpendicular_angle_rad) * gun_offset
        perp_y = math.cos(perpendicular_angle_rad) * gun_offset
        
        self.bullet_right = arcade.Sprite("assets/bullets/18.png", self.radius)
        self.bullet_right.center_x = x + perp_x + forward_x
        self.bullet_right.center_y = y + perp_y + forward_y
        self.bullet_right.angle = angle
        
        self.bullet_left = arcade.Sprite("assets/bullets/18.png", self.radius)
        self.bullet_left.center_x = x - perp_x + forward_x
        self.bullet_left.center_y = y - perp_y + forward_y
        self.bullet_left.angle = angle
        
        self.speed = 10
        
    def update(self):
        angle_rad = math.radians(self.bullet_left.angle)
        self.bullet_left.center_x += math.sin(angle_rad) * self.speed
        self.bullet_left.center_y += math.cos(angle_rad) * self.speed
        
        angle_rad = math.radians(self.bullet_right.angle)
        self.bullet_right.center_x += math.sin(angle_rad) * self.speed
        self.bullet_right.center_y += math.cos(angle_rad) * self.speed
    
    def draw(self):
        arcade.draw_sprite(self.bullet_left)
        arcade.draw_sprite(self.bullet_right)
    
    def off_screen(self, width, height):
        return ((self.bullet_right.center_x < -10 or self.bullet_right.center_x > width + 10 or 
                 self.bullet_right.center_y < -10 or self.bullet_right.center_y > height + 10) or 
                (self.bullet_left.center_x < -10 or self.bullet_left.center_x > width + 10 or 
                 self.bullet_left.center_y < -10 or self.bullet_left.center_y > height + 10))
