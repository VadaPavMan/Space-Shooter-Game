import random, arcade


class Particle:
    def __init__(self, screen_width, screen_height):
        self.start_edge = random.randint(0, 3); # 0 for Top, 1 for Right, 2 for Bottom, 3 for Left;
        
        if self.start_edge == 0: # Top
            self.x = random.randint(0, screen_width)
            self.y = screen_height
            self.dx = random.uniform(-1, 1)
            self.dy = random.uniform(-3, -1)
        
        elif self.start_edge == 1: # Right
            self.x = screen_width
            self.y = random.randint(0, screen_height)
            self.dx = random.uniform(-3, -1)
            self.dy = random.uniform(-1, 1)
        
        elif self.start_edge == 2: # Bottom
            self.x = random.randint(0, screen_width)
            self.y = 0
            self.dx = random.uniform(-1, 1)
            self.dy = random.uniform(1, 3)
            
        elif self.start_edge == 3: # Left
            self.x = 0
            self.y = random.randint(0, screen_height)
            self.dx = random.uniform(1, 3)
            self.dy = random.uniform(-1, 1)
            
        self.radius = random.randint(1, 3)
        self.color = random.choice([
            arcade.color.GRAY,
            arcade.color.LIGHT_GRAY,
            arcade.color.DARK_GRAY,
            arcade.color.DARK_BLUE_GRAY,
            arcade.color.LIGHT_BROWN,
        ])
        
        self.speed = random.uniform(1, 3)
    
    def update(self):
        self.x += self.dx * self.speed
        self.y += self.dy * self.speed
        
    def draw(self):
        arcade.draw_circle_filled(self.x, self.y, self.radius, self.color)
        
    def off_screen(self, screen_width, screen_height):
        return (self.x < -10 or self.x > screen_width + 10 or 
                self.y < -10 or self.y > screen_height + 10)
            

