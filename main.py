import arcade
import random
import particles

WINDOW_HEIGHT = 720;
WINDOW_WIDTH = 1280;
WINDOW_TITLE = "Space Shooter";

class Gameview(arcade.Window):
    
    def __init__(self, width, height, title):
        super().__init__(width, height, title, False, True);
        arcade.set_background_color(arcade.color.BLACK)
        
        self.set_minimum_size(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.circle_x = width //2;  # Starting Position Of Ball (x,y);
        self.circle_y = height //2;
        self.circle_radius = 50;
        self.circle_dx = 3; # Velocity in x direction
        self.circle_dy = 3; # Velocity in y direction
        
        self.particles = []
        for _ in range(3):
            self.particles.append(particles.Particle(width, height))
    
    def on_draw(self):
        self.clear();
        arcade.draw_circle_filled(self.circle_x, self.circle_y, self.circle_radius, arcade.color.AERO_BLUE)
        for particle in self.particles:
            particle.draw()

    def on_update(self, delta_time):
        
        self.circle_x += self.circle_dx;
        self.circle_y += self.circle_dy;
        
        if self.circle_x + self.circle_radius > self.width: 
            self.circle_dx = -abs(self.circle_dx)
            self.circle_x = self.width - self.circle_radius;
            
        if self.circle_x - self.circle_radius < 0: 
            self.circle_dx = abs(self.circle_dx)
            self.circle_x = self.circle_radius;
            
        if self.circle_y + self.circle_radius > self.height: 
            self.circle_dy = -abs(self.circle_dy)
            self.circle_y = self.height - self.circle_radius;
            
        if self.circle_y - self.circle_radius < 0: 
            self.circle_dy = abs(self.circle_dy)
            self.circle_y = self.circle_radius;
            
        for particle in self.particles:
            particle.update()
            
        for i in range(len(self.particles) -1, -1, -1):
            if self.particles[i].off_screen(self.width, self.height):
                self.particles.pop(i)
                self.particles.append(particles.Particle(self.width, self.height))
    
        

if __name__ == "__main__":
    game = Gameview(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE);
    arcade.run()
