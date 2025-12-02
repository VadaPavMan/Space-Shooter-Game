import arcade
import math
import random

class Bullet:
    def __init__(self, angle, x, y):
        self.x = x
        self.y = y
        self.angle = angle
        
        self.speed = 10
        self.radius = 3
        
    def update(self):
        angle_rad = math.radians(self.angle)
        self.x += math.sin(angle_rad) * self.speed
        self.y += math.cos(angle_rad) * self.speed
    
    def draw(self):
        arcade.draw_circle_filled(self.x, self.y, self.radius, arcade.color.YELLOW)
    
    def off_screen(self, width, height):
        return (self.x < -10 or self.x > width + 10 or self.y < -10 or self.y > height + 10)
