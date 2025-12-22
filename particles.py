import config
import arcade

arcade.gl.DEFAULT_FILTER = (arcade.gl.NEAREST, arcade.gl.NEAREST)
import random


class Particle:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.reset()
    
    def update_screen_size(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height

    def reset(self):
        self.start_edge = random.randint(0, 3)  # 0=Top, 1=Right, 2=Bottom, 3=Left

        if self.start_edge == 0:  # Top
            self.x = random.randint(0, self.screen_width)
            self.y = self.screen_height
            self.dx = random.uniform(-1, 1)
            self.dy = random.uniform(-3, -1)

        elif self.start_edge == 1:  # Right
            self.x = self.screen_width
            self.y = random.randint(0, self.screen_height)
            self.dx = random.uniform(-3, -1)
            self.dy = random.uniform(-1, 1)

        elif self.start_edge == 2:  # Bottom
            self.x = random.randint(0, self.screen_width)
            self.y = 0
            self.dx = random.uniform(-1, 1)
            self.dy = random.uniform(1, 3)

        elif self.start_edge == 3:  # Left
            self.x = 0
            self.y = random.randint(0, self.screen_height)
            self.dx = random.uniform(1, 3)
            self.dy = random.uniform(-1, 1)

        self.radius = random.randint(1, 3)
        self.color = random.choice(
            [
                arcade.color.GRAY,
                arcade.color.LIGHT_GRAY,
                arcade.color.DARK_GRAY,
                arcade.color.DARK_BLUE_GRAY,
            ]
        )

        self.speed = random.uniform(1, 3)

    def update(self):
        self.x += self.dx * self.speed
        self.y += self.dy * self.speed

        if self.off_screen():
            self.reset()

    def draw(self):
        arcade.draw_circle_filled(self.x, self.y, self.radius, self.color)

    def off_screen(self):
        return (
            self.x < -10
            or self.x > self.screen_width + 10
            or self.y < -10
            or self.y > self.screen_height + 10
        )