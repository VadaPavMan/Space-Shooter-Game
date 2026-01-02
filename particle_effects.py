import arcade
import random
import math

class EngineFlame:
    def __init__(self, x, y, angle, is_player=True):
        self.x = x
        self.y = y
        self.lifetime = random.uniform(0.15, 0.3)
        self.max_lifetime = self.lifetime
        self.size = random.uniform(2, 5) if is_player else random.uniform(1.5, 4)
        
        angle_rad = math.radians(angle + 180)
        spread = random.uniform(-15, 15)
        spread_rad = math.radians(spread)
        
        speed = random.uniform(2, 4)
        self.dx = math.sin(angle_rad + spread_rad) * speed
        self.dy = math.cos(angle_rad + spread_rad) * speed
        
        if is_player:
            self.colors = [
                (255, 200, 50),   # Bright yellow
                (255, 150, 30),   # Orange
                (255, 100, 10),   # Deep orange
            ]
        else:
            self.colors = [
                (200, 50, 255),   # Purple (alien engine)
                (150, 30, 255),   # Deep purple
                (100, 10, 200),   # Dark purple
            ]
        
        self.color = random.choice(self.colors)
    
    def update(self, delta_time):
        self.lifetime -= delta_time
        self.x += self.dx
        self.y += self.dy
        
        #Fade
        progress = 1 - (self.lifetime / self.max_lifetime)
        self.size *= 0.95
        
        return self.lifetime > 0
    
    def draw(self):
        alpha = int(255 * (self.lifetime / self.max_lifetime))
        color = (*self.color, alpha)
        arcade.draw_circle_filled(self.x, self.y, self.size, color)


class HitParticle:
    def __init__(self, x, y, is_player=False):
        self.x = x
        self.y = y
        self.lifetime = random.uniform(0.3, 0.6)
        self.max_lifetime = self.lifetime
        self.size = random.uniform(2, 4)
        
        # Random direction
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(50, 120)
        self.dx = math.cos(angle) * speed
        self.dy = math.sin(angle) * speed
        
        self.friction = 0.92
        
        if is_player:
            self.color = random.choice([
                (50, 255, 150),   # Bright green
                (80, 255, 200),   # Cyan-green
                (100, 255, 180),  # Light green
                (150, 255, 150),  # Pale green
            ])
        else:
            self.color = random.choice([
                (255, 50, 50),    # Bright red
                (255, 100, 50),   # Red-orange
                (255, 80, 30),    # Deep orange-red
                (200, 50, 50),    # Dark red
            ])
    
    def update(self, delta_time):
        self.lifetime -= delta_time
        self.x += self.dx * delta_time
        self.y += self.dy * delta_time
        
        self.dx *= self.friction
        self.dy *= self.friction
        
        self.size *= 0.97
        
        return self.lifetime > 0
    
    def draw(self):
        alpha = int(255 * (self.lifetime / self.max_lifetime))
        color = (*self.color, alpha)
        arcade.draw_circle_filled(self.x, self.y, self.size, color)


class ExplosionParticle:
    def __init__(self, x, y, is_player=False):
        self.x = x
        self.y = y
        self.lifetime = random.uniform(0.5, 1.0)
        self.max_lifetime = self.lifetime
        self.size = random.uniform(3, 8) if not is_player else random.uniform(5, 12)
        
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(80, 200) if not is_player else random.uniform(100, 250)
        self.dx = math.cos(angle) * speed
        self.dy = math.sin(angle) * speed
        
        self.dy_accel = -100
        self.friction = 0.96
        
        if is_player:
            self.color = random.choice([
                (255, 255, 100),  # Bright yellow
                (255, 200, 50),   # Yellow-orange
                (255, 150, 50),   # Orange
                (255, 100, 50),   # Red-orange
                (200, 50, 50),    # Red
            ])
        else:
            self.color = random.choice([
                (255, 200, 50),   # Yellow
                (255, 150, 50),   # Orange
                (255, 100, 50),   # Red-orange
                (200, 80, 50),    # Dark orange
                (150, 50, 100),   # Purple tint (alien)
            ])
        
        self.glow = random.random() < 0.3
    
    def update(self, delta_time):
        self.lifetime -= delta_time
        self.x += self.dx * delta_time
        self.y += self.dy * delta_time
        
        self.dy += self.dy_accel * delta_time
        self.dx *= self.friction
        self.dy *= self.friction
        
        self.size *= 0.96
        
        return self.lifetime > 0
    
    def draw(self):
        progress = 1 - (self.lifetime / self.max_lifetime)
        alpha = int(255 * (self.lifetime / self.max_lifetime))
        
        if self.glow and progress < 0.5:
            glow_size = self.size * 2
            glow_color = (*self.color, alpha // 3)
            arcade.draw_circle_filled(self.x, self.y, glow_size, glow_color)
        
        # main particle
        color = (*self.color, alpha)
        arcade.draw_circle_filled(self.x, self.y, self.size, color)


class DebrisParticle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.lifetime = random.uniform(0.8, 1.5)
        self.max_lifetime = self.lifetime
        self.width = random.uniform(2, 5)
        self.height = random.uniform(2, 5)
        
        # Random DIrection
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(60, 150)
        self.dx = math.cos(angle) * speed
        self.dy = math.sin(angle) * speed
        
        self.rotation = random.uniform(0, 360)
        self.rotation_speed = random.uniform(-300, 300)
        
        self.dy_accel = -150
        self.friction = 0.98
        
        self.color = random.choice([
            (120, 120, 120),  # Gray
            (100, 100, 100),  # Dark Gray
            (80, 80, 90),     # Blue-Gray
            (90, 80, 70),     # Brown-Gray
        ])
    
    def update(self, delta_time):
        self.lifetime -= delta_time
        self.x += self.dx * delta_time
        self.y += self.dy * delta_time
        
        # Physics
        self.dy += self.dy_accel * delta_time
        self.dx *= self.friction
        self.dy *= self.friction
        
        # Rotation
        self.rotation += self.rotation_speed * delta_time
        
        return self.lifetime > 0
    
    def draw(self):
        alpha = int(255 * (self.lifetime / self.max_lifetime))
        color = (*self.color, alpha)
        
        half_width = self.width / 2
        half_height = self.height / 2
        
        angle_rad = math.radians(self.rotation)
        cos_angle = math.cos(angle_rad)
        sin_angle = math.sin(angle_rad)
        
        corners = [
            (-half_width, -half_height),
            (half_width, -half_height),
            (half_width, half_height),
            (-half_width, half_height)
        ]
        
        rotated_corners = []
        for x, y in corners:
            rx = x * cos_angle - y * sin_angle
            ry = x * sin_angle + y * cos_angle
            rotated_corners.append((self.x + rx, self.y + ry))
        
        arcade.draw_polygon_filled(rotated_corners, color)


class ParticleSystem:
    def __init__(self):
        self.engine_flames = []
        self.hit_particles = []
        self.explosion_particles = []
        self.debris_particles = []
    
    def create_engine_flame(self, x, y, angle, is_player=True, count=2):
        for _ in range(count):
            self.engine_flames.append(EngineFlame(x, y, angle, is_player))
    
    def create_hit_effect(self, x, y, is_player=False, count=8):
        for _ in range(count):
            self.hit_particles.append(HitParticle(x, y, is_player))
    
    def create_explosion(self, x, y, is_player=False):
        particle_count = 30 if is_player else 20
        for _ in range(particle_count):
            self.explosion_particles.append(ExplosionParticle(x, y, is_player))
        
        # Debris
        debris_count = 15 if is_player else 10
        for _ in range(debris_count):
            self.debris_particles.append(DebrisParticle(x, y))
    
    def update(self, delta_time):
        self.engine_flames = [p for p in self.engine_flames if p.update(delta_time)]
        self.hit_particles = [p for p in self.hit_particles if p.update(delta_time)]
        self.explosion_particles = [p for p in self.explosion_particles if p.update(delta_time)]
        self.debris_particles = [p for p in self.debris_particles if p.update(delta_time)]
    
    def draw(self):
        for particle in self.debris_particles:
            particle.draw()
        
        for particle in self.engine_flames:
            particle.draw()
        
        for particle in self.explosion_particles:
            particle.draw()
        
        for particle in self.hit_particles:
            particle.draw()
    
    def get_particle_count(self):
        return (len(self.engine_flames) + len(self.hit_particles) + 
                len(self.explosion_particles) + len(self.debris_particles))