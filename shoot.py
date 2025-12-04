import arcade
import math
import random

class Bullet(arcade.Sprite):
    def __init__(self, angle, x, y):
        self.radius = 0.4
        self.bullet = arcade.Sprite("assets/bullets/06.png", self.radius)
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
