import config
import arcade
from resources import resource_path, load_texture_cached, load_sound_cached
import random
import particles
import __hero__
import shoot
import enemies
import powerups
import time
import menu

WINDOW_HEIGHT = 720
WINDOW_WIDTH = 1280
WINDOW_TITLE = "Galactic Combat"

HEALTH_POWERUP = "health"
DUALs_POWERUP = "dual_shooter"
SHIELD_POWERUP = "shield"
LASER_POWERUP = "laser"
ALLIN1_POWERUP = "max"


class Gameview(arcade.View):

    def __init__(self, window):
        super().__init__(window)
        config.config()
        self.background = arcade.SpriteList()
        self.bg_speed = 30
        self.bg_y_offset = 0

        self.player = __hero__.Player(window.width, window.height)
        # Mouse Cursor
        self.mouse_circle_center_x = window.width // 2
        self.mouse_circle_center_y = window.height // 2
        self.mouse_circle_radius = 10
        self.mouse_circle_color = arcade.color.FELDSPAR

        self.enemies = []
        self.particles = []
        self.bullets = []
        self.enemy_bullets = []

        # All Powerups
        self.powerups = []
        self.powerups_cooldown_timer = 0
        self.powerups_target = 0.9
        self.powerup_type = ""
        self.health_power_active = False
        self.rapid_power_active = False
        self.rapid_power_timer = 0
        self.dual_shoot_powerup = False
        self.dual_shoot_timer = 0
        self.player_shield = False
        self.player_damage = 10
        self.shield_timer = 0
        self.superultra_active = False
        self.superultra_timer = 0

        # Powerup timer
        self.active_powerup_end_time = 0
        self.active_powerup_type = ""

        self.spawn_timer = 0
        self.max_enemies = 3
        self.spawn_interval = 2.0
        self.score = 0
        self.TARGET_TO_INCREASE_ENEMIES = 200
        self.TARGET_TO_DECREASE_INTERVAL = 300
        
        # Sound Effects
        explosion1 = load_sound_cached("assets/sound/explosion/explosion-1.wav")
        explosion2 = load_sound_cached("assets/sound/explosion/explosion-2.wav")
        explosion3 = load_sound_cached("assets/sound/explosion/explosion-3.wav")
        explosion4 = load_sound_cached("assets/sound/explosion/explosion-4.wav")
        explosion5 = load_sound_cached("assets/sound/explosion/explosion-5.wav")
        explosion6 = load_sound_cached("assets/sound/explosion/explosion-6.wav")
        explosion7 = load_sound_cached("assets/sound/explosion/explosion-7.wav")
        self.explosion = (explosion1, explosion2, explosion3, explosion4, explosion5, explosion6, explosion7)
        self.pickup_sound = arcade.load_sound("assets/sound/pickups.mp3")
        self.music = arcade.load_sound("assets/sound/background_music.mp3")
        
        # Player shooting sounds
        self.fire_normal = arcade.load_sound("assets/sound/shoot/fire-normal.wav")
        self.fire_dual = arcade.load_sound("assets/sound/shoot/fire-dual.wav")
        self.fire = None
        
        # Enemy shooting sounds
        self.enemy_fire_normal = load_sound_cached("assets/sound/shoot/fire-enemies.wav")
        self.enemy_fire_dual = load_sound_cached("assets/sound/shoot/dual-enemies.wav")
        self.normal_en_fire = arcade.load_sound("assets/sound/shoot/fire-enemies.wav")
        self.dual_en_fire = arcade.load_sound("assets/sound/shoot/dual-enemies.wav")
        self.enemies_fire = None
        self.gameview_background_music = None
        self.hit = arcade.load_sound("assets/sound/hit.wav")
        self.hit_sound = None

        # Starting Fade Effect
        self.fade_alpha = 255
        self.fade_timer = 0
        self.fade_duration = 1.0
        self.fade_effect = True
        
        # background textures 
        bg_texture_1 = load_texture_cached("assets/space-1.png")
        bg_texture_2 = load_texture_cached("assets/space-2.png")
        

        scale_x = self.window.width / bg_texture_1.width
        scale_y = self.window.height / bg_texture_1.height
        self.bg_scale = max(scale_x, scale_y)
        
        self.bg_height = bg_texture_1.height * self.bg_scale
        
        self.bg1 = arcade.Sprite(path_or_texture=bg_texture_1, scale=self.bg_scale)
        self.bg1.center_x = self.window.width // 2
        self.bg1.center_y = self.window.height // 2
        
        self.bg2 = arcade.Sprite(path_or_texture=bg_texture_2, scale=self.bg_scale)
        self.bg2.center_x = self.window.width // 2
        self.bg2.center_y = self.window.height // 2 + self.bg_height
        
        self.background.append(self.bg1)
        self.background.append(self.bg2)
            
        for _ in range(self.max_enemies):
            self.enemies.append(enemies.Enemies(window.width, window.height))

        for _ in range(5):
            self.particles.append(particles.Particle(window.width, window.height))

    def on_show_view(self):
        self.window.set_mouse_visible(False)
        if self.gameview_background_music is None:
            self.gameview_background_music = arcade.play_sound(self.music, loop=True, volume=0.35)
        else:
            self.gameview_background_music.play()
        for particle in self.particles:
            particle.update_screen_size(self.window.width, self.window.height)

    def reset_game(self):
        self.player = __hero__.Player(self.window.width, self.window.height)
        self.enemies.clear()
        self.particles.clear()
        self.bullets.clear()
        self.enemy_bullets.clear()
        self.powerups.clear()
        
        if self.gameview_background_music:
            arcade.stop_sound(self.gameview_background_music)
            self.gameview_background_music = None
            
        self.bg_speed = 30
        self.bg_y_offset = 0
        self.bg_scaled_height = 0

        self.health_power_active = False
        self.rapid_power_active = False
        self.rapid_power_timer = 0
        self.dual_shoot_powerup = False
        self.dual_shoot_timer = 0
        self.player_shield = False
        self.player_damage = 10
        self.shield_timer = 0
        self.superultra_active = False
        self.superultra_timer = 0
        self.active_powerup_end_time = 0
        self.active_powerup_type = ""

        self.spawn_timer = 0
        self.max_enemies = 3
        self.spawn_interval = 2.0
        self.score = 0
        self.TARGET_TO_INCREASE_ENEMIES = 200
        self.TARGET_TO_DECREASE_INTERVAL = 300

        self.fade_alpha = 255
        self.fade_timer = 0
        self.fade_duration = 1.0
        self.fade_effect = True

        self.background.clear()
        
        # Use cached textures instead of reloading
        bg_texture_1 = load_texture_cached("assets/space-1.png")
        bg_texture_2 = load_texture_cached("assets/space-2.png")
        
        scale_x = self.window.width / bg_texture_1.width
        scale_y = self.window.height / bg_texture_1.height
        self.bg_scale = max(scale_x, scale_y)
        
        self.bg_height = bg_texture_1.height * self.bg_scale
        
        self.bg1 = arcade.Sprite(path_or_texture=bg_texture_1, scale=self.bg_scale)
        self.bg1.center_x = self.window.width // 2
        self.bg1.center_y = self.window.height // 2
        
        self.bg2 = arcade.Sprite(path_or_texture=bg_texture_2, scale=self.bg_scale)
        self.bg2.center_x = self.window.width // 2
        self.bg2.center_y = self.window.height // 2 + self.bg_height
        
        self.background.append(self.bg1)
        self.background.append(self.bg2)
            
        for _ in range(self.max_enemies):
            self.enemies.append(enemies.Enemies(self.window.width+200, self.window.height+200))

        for _ in range(5):
            self.particles.append(particles.Particle(self.window.width, self.window.height))

    def draw_score_box(self):
        # Score Box
        bar_width = 100
        bar_height = 20
        x = 20
        y = self.height - 70

        # Score Text Content
        current_score = "Score: " + str(self.score)
        text_color = arcade.color.WHITE
        text_size = 12
        text_x = 40
        text_y = y + 11
        if self.score >= 100:
            text_x += 10
        elif self.score >= 1000:
            text_x += 10

        arcade.draw_lrbt_rectangle_filled(
            x, x + bar_width, y, y + bar_height, arcade.color.BLUE
        )

        arcade.draw_lrbt_rectangle_outline(
            x, x + bar_width, y, y + bar_height, arcade.color.WHITE, 2
        )

        arcade.draw_text(
            current_score,
            text_x+5,
            text_y,
            text_color,
            text_size,
            width=bar_width,
            align="center",
            anchor_x="center",
            anchor_y="center",
            bold=True,
        )

    def draw_player_health_bar(self):
        bar_width = 200
        bar_height = 20
        x = 20
        y = self.height - 40

        current_health, max_health = self.player.get_health()
        health_ratio = current_health / max_health
        current_bar_width = bar_width * health_ratio

        arcade.draw_lrbt_rectangle_filled(
            x, x + bar_width, y, y + bar_height, arcade.color.DARK_RED
        )

        if health_ratio > 0.6:
            bar_color = arcade.color.GREEN
        elif health_ratio > 0.3:
            bar_color = arcade.color.YELLOW
        else:
            bar_color = arcade.color.RED

        arcade.draw_lrbt_rectangle_filled(
            x, x + current_bar_width, y, y + bar_height, bar_color
        )

        arcade.draw_lrbt_rectangle_outline(
            x, x + bar_width, y, y + bar_height, arcade.color.WHITE, 2
        )

        health_text = f"HP: {int(current_health)}/{int(max_health)}"
        arcade.draw_text(
            health_text, x + bar_width + 10, y + 2, arcade.color.WHITE, 14, bold=True
        )

    def draw_powerup_timer_bar(self):
        bar_width = 200
        bar_height = 15
        x = 60
        y = 20

        current_time = time.time()
        remaining_time = 0
        bar_color = arcade.color.AMBER
        bg_bar_color = arcade.color.DARK_RED

        if self.active_powerup_end_time > current_time:
            remaining_time = self.active_powerup_end_time - current_time
            if self.superultra_active:
                remaining_ratio = remaining_time / 30.0
                bar_width = 400
            else:
                remaining_ratio = remaining_time / 15.0
            current_bar_width = bar_width * remaining_ratio

            if self.active_powerup_type == "rapid":
                bar_color = arcade.color.DARK_PASTEL_GREEN
                bg_bar_color = arcade.color.DARK_GREEN
            elif self.active_powerup_type == "dual":
                bar_color = arcade.color.AMBER
                bg_bar_color = arcade.color.COFFEE
            elif self.active_powerup_type == "shield":
                bar_color = arcade.color.CELESTIAL_BLUE
                bg_bar_color = arcade.color.DARK_MIDNIGHT_BLUE
            elif self.active_powerup_type == "super":
                bar_color = arcade.color.CADMIUM_ORANGE
                bg_bar_color = arcade.color.SEPIA
            else:
                bar_color = arcade.color.AMBER
                bg_bar_color = arcade.color.DARK_RED

            arcade.draw_lrbt_rectangle_filled(
                x, x + bar_width, y, y + bar_height, bg_bar_color
            )

            arcade.draw_lrbt_rectangle_filled(
                x, x + current_bar_width, y, y + bar_height, bar_color
            )

            arcade.draw_lrbt_rectangle_outline(
                x, x + bar_width, y, y + bar_height, arcade.color.WHITE, 2
            )

            powerup_path = self.get_powerup_display_name()
            self.pimage = arcade.Sprite(resource_path(powerup_path))
            self.pimage.center_x = x - 20
            self.pimage.center_y = bar_height + 14
            arcade.draw_sprite(self.pimage)

    def get_powerup_display_name(self):
        if self.active_powerup_type == "rapid":
            return "assets/powerups/display_rapid.png"
        elif self.active_powerup_type == "dual":
            return "assets/powerups/display_dual.png"
        elif self.active_powerup_type == "shield":
            return "assets/powerups/display_shield.png"
        elif self.active_powerup_type == "super":
            return "assets/powerups/display_allin1.png"
        else:
            return "Powerup"

    def on_draw(self):
        self.clear()
        
        self.background.draw()

        for pu in self.powerups:
            pu.on_draw()

        for particle in self.particles:
            particle.draw()

        for bullet in self.bullets:
            bullet.draw()

        for enemy_bullet in self.enemy_bullets:
            enemy_bullet.draw()

        for enemy in self.enemies:
            enemy.draw()

        arcade.draw_circle_outline(
            self.mouse_circle_center_x,
            self.mouse_circle_center_y,
            self.mouse_circle_radius,
            self.mouse_circle_color,
            3,
        )

        self.player.draw()

        self.draw_player_health_bar()
        self.draw_score_box()

        current_time = time.time()
        if (
            (self.rapid_power_active and current_time < self.rapid_power_timer + 15)
            or (self.dual_shoot_powerup and current_time < self.dual_shoot_timer + 15)
            or (self.player_shield and current_time < self.shield_timer + 15)
            or (self.superultra_active and current_time < self.superultra_timer + 30)
        ):
            self.draw_powerup_timer_bar()

        arcade.draw_lrbt_rectangle_filled(
            0, self.width, 0, self.height, (0, 0, 0, self.fade_alpha)
        )

    def on_resize(self, width, height):
        super().on_resize(width, height)
        
        if hasattr(self, 'bg1'):
            scale_x = width / self.bg1.texture.width
            scale_y = height / self.bg1.texture.height
            self.bg_scale = max(scale_x, scale_y)
            self.bg_height = self.bg1.texture.height * self.bg_scale
            
            self.bg1.scale = self.bg_scale
            self.bg2.scale = self.bg_scale
            self.bg1.center_x = width // 2
            self.bg2.center_x = width // 2
        
        for particle in self.particles:
            particle.update_screen_size(width, height)

    def on_update(self, delta_time):
        self.fade_timer += delta_time
        progress = self.fade_timer / self.fade_duration
        self.fade_alpha = int(255 * (1 - progress))
        if self.fade_timer >= self.fade_duration:
            self.fade_alpha = 0
            
        self.player.update(self.width, self.height, delta_time)
        
        move_amount = self.bg_speed * delta_time
        
        self.bg1.center_y -= move_amount
        self.bg2.center_y -= move_amount
        
        if self.bg1.center_y + self.bg_height / 2 < 0:
            self.bg1.center_y = self.bg2.center_y + self.bg_height
        
        if self.bg2.center_y + self.bg_height / 2 < 0:
            self.bg2.center_y = self.bg1.center_y + self.bg_height
                
        self.powerup_timer()
        self.update_active_powerup()

        # Player SHooting
        if self.player.shoot():
            bullet_x, bullet_y = self.player.get_position()
            angle = self.player.get_angle()
            if not (self.dual_shoot_powerup):
                new_bullet = shoot.Bullet(angle, bullet_x, bullet_y)
                self.fire = self.fire_normal
            else:
                new_bullet = shoot.Player_Bullet_Dual(angle, bullet_x, bullet_y)
                self.fire = self.fire_dual
            self.bullets.append(new_bullet)
            arcade.play_sound(self.fire, loop=False, volume=0.6)

        pos_x, pos_y = self.player.get_position()

        for enemy in self.enemies:
            old_bullet_count = len(enemy.bullets)

            enemy.update(
                delta_time,
                pos_x,
                pos_y,
                self.width + 50,
                self.height + 50,
                self.enemies,
            )

            if len(enemy.bullets) > old_bullet_count:
                new_bullets = enemy.bullets[old_bullet_count:]
                self.enemy_bullets.extend(new_bullets)
                
                last_bullet = new_bullets[-1]
                
                if isinstance(last_bullet, shoot.Enemy_Bullet_Dual):
                    arcade.play_sound(self.enemy_fire_dual, volume=0.4)
                else:
                    arcade.play_sound(self.enemy_fire_normal, volume=0.4)

        for bullet in self.bullets:
            bullet.update()

        for enemy_bullet in self.enemy_bullets:
            enemy_bullet.update()

        bullets_to_remove = []
        enemies_to_remove = []
        enemy_bullets_to_remove = []

        for bullet in self.bullets:
            if isinstance(bullet, shoot.Player_Bullet_Dual):
                bullet_sprites = [bullet.bullet_left, bullet.bullet_right]
            else:
                bullet_sprite = getattr(
                    bullet, "bullet", getattr(bullet, "sprite", bullet)
                )
                bullet_sprites = [bullet_sprite]

            hit_enemy = None
            for enemy in self.enemies:
                if enemy in enemies_to_remove:
                    continue

                # Check collision
                for bs in bullet_sprites:
                    if arcade.check_for_collision(bs, enemy.enemy):
                        hit_enemy = enemy
                        break

                if hit_enemy:
                    break

            if hit_enemy:
                bullets_to_remove.append(bullet)
                self.hit_sound = arcade.play_sound(self.hit, loop=False, volume=1.0)

                is_dead = hit_enemy.take_damage(
                    isinstance(bullet, shoot.Player_Bullet_Dual)
                )

                if is_dead:
                    enemies_to_remove.append(hit_enemy)
                    self.score += 10
                    print(f"Score: {self.score}")

                    if random.random() <= self.powerups_target:
                        if int(delta_time) % 2 == 0:
                            ex, ey = hit_enemy.get_position()
                            self.powerups.append(powerups.ShieldDemo(ex, ey))
                            self.powerups_cooldown_timer = time.time()

                    if self.max_enemies < 26:
                        if self.score >= self.TARGET_TO_INCREASE_ENEMIES:
                            self.max_enemies += 1
                            self.TARGET_TO_INCREASE_ENEMIES += 200
                            print(f"Increase Max Enemies: {self.max_enemies}")

        powerups_to_remove = []
        for pu in self.powerups:
            pu.on_update(delta_time)
            
            time_elapsed = time.time() - pu.spawn_time
            if time_elapsed > 8:
                pu.invincible = True
            
            if time_elapsed > 10:
                powerups_to_remove.append(pu)
                
            if arcade.check_for_collision(self.player.player, pu.sprite):
                self.player.invincible = True
                self.player.invincible_timer = 0.0
                arcade.play_sound(self.pickup_sound,loop=False, volume=0.8)
                if HEALTH_POWERUP in pu.get_filePath():
                    self.health_power_active = True
                    self.powerup_type = pu.get_filePath()
                    heal_amount = 20
                    if self.health_power_active:
                        self.player.current_health = min(
                            self.player.max_health,
                            self.player.current_health + heal_amount,
                        )
                        self.health_power_active = False
                    print(f"Path: {pu.get_filePath()} And {HEALTH_POWERUP}")
                elif DUALs_POWERUP in pu.get_filePath():
                    self.dual_shoot_powerup = True
                    self.rapid_power_active = False
                    if self.rapid_power_active == False:
                        self.player.rapidfire(0)
                    self.dual_shoot_timer = time.time()
                    self.active_powerup_type = "dual"
                    self.active_powerup_end_time = self.dual_shoot_timer + 15
                    print(f"Timer Dual: {self.dual_shoot_timer}")
                    self.powerup_type = pu.get_filePath()
                    print(f"Path: {pu.get_filePath()} And {DUALs_POWERUP}")
                elif LASER_POWERUP in pu.get_filePath():
                    self.rapid_power_active = True
                    self.dual_shoot_powerup = False
                    self.powerup_type = pu.get_filePath()
                    self.rapid_power_timer = time.time()
                    self.active_powerup_type = "rapid"
                    self.active_powerup_end_time = self.rapid_power_timer + 15
                    print(f"Timer Rapid: {self.rapid_power_timer}")
                    if self.rapid_power_active:
                        self.player.rapidfire(1)
                        print("Rapid Fire Active")
                        print(f"Timer: {self.rapid_power_timer}")
                    print(f"Path: {pu.get_filePath()} And {LASER_POWERUP}")
                elif SHIELD_POWERUP in pu.get_filePath():
                    self.player_shield = True
                    self.shield_timer = time.time()
                    self.active_powerup_type = "shield"
                    self.active_powerup_end_time = self.shield_timer + 15
                    print(f"Timer Shield: {self.shield_timer}")
                    self.powerup_type = pu.get_filePath()
                    if self.player_shield:
                        self.player_damage = 0
                    print(f"Path: {pu.get_filePath()} And {SHIELD_POWERUP}")
                elif ALLIN1_POWERUP in pu.get_filePath():
                    self.superultra_active = True
                    self.player_shield = self.rapid_power_active = (
                        self.dual_shoot_powerup
                    ) = self.health_power_active = True
                    self.active_powerup_type = "super"
                    self.superultra_timer = time.time()
                    self.active_powerup_end_time = self.superultra_timer + 30
                    self.shield_timer = time.time()
                    self.rapid_power_timer = time.time()
                    self.dual_shoot_timer = time.time()

                    heal_amount = 50

                    if self.player_shield:
                        self.player_damage = 0

                    self.player.current_health = min(
                        self.player.max_health, self.player.current_health + heal_amount
                    )
                    self.player.rapidfire(1)

                    print(f"Path: {pu.get_filePath()} And {ALLIN1_POWERUP}")
                self.player.update_texture()
                powerups_to_remove.append(pu)
                
        for pu in powerups_to_remove:
            if pu in self.powerups:
                self.powerups.remove(pu)

        player_sprite = self.player.player
        for enemy_bullet in self.enemy_bullets:
            if enemy_bullet in enemy_bullets_to_remove:
                continue

            # For Big Monster
            if isinstance(enemy_bullet, shoot.Enemy_Bullet_Dual):
                if arcade.check_for_collision(
                    player_sprite, enemy_bullet.bullet_left
                ) or arcade.check_for_collision(
                    player_sprite, enemy_bullet.bullet_right
                ):

                    if self.player_shield:
                        player_died = self.player.take_damage(self.player_damage)
                    else:
                        player_died = self.player.take_damage(20)
                    enemy_bullets_to_remove.append(enemy_bullet)
                    self.hit_sound = arcade.play_sound(self.hit, loop=False, volume=1.0)

                    if player_died:
                        print("Game Over! Player died!")

            # For Monster
            elif isinstance(enemy_bullet, shoot.Enemy_Bullet):
                if arcade.check_for_collision(player_sprite, enemy_bullet.bullet):
                    if self.player_shield:
                        player_died = self.player.take_damage(self.player_damage)
                    else:
                        player_died = self.player.take_damage(10)
                    enemy_bullets_to_remove.append(enemy_bullet)
                    self.hit_sound = arcade.play_sound(self.hit, loop=False, volume=1.0)

                    if player_died:
                        print("Game Over! Player died!")

            elif isinstance(enemy_bullet, shoot.Enemy_Bullet_High_Damage):
                if arcade.check_for_collision(player_sprite, enemy_bullet.bullet):
                    if self.player_shield:
                        player_died = self.player.take_damage(self.player_damage)
                    else:
                        player_died = self.player.take_damage(50)
                    enemy_bullets_to_remove.append(enemy_bullet)
                    self.hit_sound = arcade.play_sound(self.hit, loop=False, volume=1.0)

                    if player_died:
                        print("Game Over! Player died!")

        # Crab
        for enemy in self.enemies:
            if enemy in enemies_to_remove:
                continue
            if arcade.check_for_collision(player_sprite, enemy.enemy):

                if self.player_shield:
                    player_died = self.player.take_damage(self.player_damage)
                else:
                    player_died = self.player.take_damage(10)

                if player_died:
                    print("Game Over! Player died!")

                enemies_to_remove.append(enemy)
                self.hit_sound = arcade.play_sound(self.hit, loop=False, volume=1.0)

        for bullet in bullets_to_remove:
            if bullet in self.bullets:
                self.bullets.remove(bullet)

        for enemy_bullet in enemy_bullets_to_remove:
            if enemy_bullet in self.enemy_bullets:
                self.enemy_bullets.remove(enemy_bullet)

        for enemy in enemies_to_remove:
            if enemy in self.enemies:
                enemy.bullets.clear()
                self.enemies.remove(enemy)
                self.explosion_sound = random.choice(self.explosion)
                arcade.play_sound(self.explosion_sound, loop=False, volume=1.0)

        # Spawn NEw Enemies
        if len(self.enemies) < self.max_enemies:
            self.spawn_timer += delta_time
            if self.spawn_timer >= self.spawn_interval:
                self.enemies.append(
                    enemies.Enemies(width=(self.width+300),height=(self.height+300))
                )

                # Increase Difficulty
                if self.max_enemies < 26:
                    if self.score >= self.TARGET_TO_DECREASE_INTERVAL:
                        self.spawn_interval -= 0.15
                        self.TARGET_TO_DECREASE_INTERVAL += 300
                        print(f"Spawn Interval: {self.spawn_interval}")

                if self.spawn_interval <= 0.5:
                    self.spawn_interval = 0.5

                self.spawn_timer = 0

        for i in range(len(self.bullets) - 1, -1, -1):
            if self.bullets[i].off_screen(self.width, self.height):
                self.bullets.pop(i)

        for i in range(len(self.enemy_bullets) - 1, -1, -1):
            if self.enemy_bullets[i].off_screen(self.width, self.height):
                self.enemy_bullets.pop(i)

        for particle in self.particles:
            particle.update()
        
        self.is_dead(delta_time)
        
    def is_dead(self, delta_time):
        # Check Death
        is_dead = self.player.get_current_health()
        if is_dead <= 0:
            if self.gameview_background_music:
                self.gameview_background_music.pause()
            pause_view = menu.PauseMenuView(self, True)
            self.window.show_view(pause_view)
            
            
    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            if self.gameview_background_music:
                self.gameview_background_music.pause()
            pause_view = menu.PauseMenuView(self, False)
            self.window.show_view(pause_view)
        else:
            self.player.on_key_press(key, modifiers)

    def on_key_release(self, key, modifiers):
        self.player.on_key_release(key, modifiers)

    def on_mouse_motion(self, x, y, dx, dy):
        self.player.on_mouse_motion(x, y, dx, dy)

        self.mouse_circle_center_x = x
        self.mouse_circle_center_y = y

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.player.on_mouse_press()

    def on_mouse_release(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.player.on_mouse_release()

    def powerup_timer(self):
        if not self.superultra_active:
            if self.rapid_power_active and (time.time() - self.rapid_power_timer) > 15:
                self.player.rapidfire(0)
                print(f"Time Out Rapid: {time.time()}")
                self.rapid_power_active = False
                self.active_powerup_type = ""

            if self.dual_shoot_powerup and (time.time() - self.dual_shoot_timer) > 15:
                print(f"Time Out Dual: {time.time()}")
                self.dual_shoot_powerup = False
                self.active_powerup_type = ""

            if self.player_shield and (time.time() - self.shield_timer) > 15:
                print(f"Time Out Sheild: {time.time()}")
                self.player_shield = False
                self.player_damage = 10
                self.active_powerup_type = ""
        else:
            if self.superultra_active and (time.time() - self.superultra_timer) > 30:
                print(f"Time Out Super: {time.time()}")
                self.superultra_active = False
                self.player_shield = self.rapid_power_active = (
                    self.dual_shoot_powerup
                ) = self.health_power_active = False
                self.player_damage = 10
                self.player.rapidfire(0)
                self.active_powerup_type = ""

    def update_active_powerup(self):
        current_time = time.time()

        active_types = []

        if self.superultra_active:
            if self.superultra_active and current_time < self.superultra_timer + 30:
                active_types.append(("super", self.superultra_timer + 30))
        else:
            if self.rapid_power_active and current_time < self.rapid_power_timer + 15:
                active_types.append(("rapid", self.rapid_power_timer + 15))
            if self.dual_shoot_powerup and current_time < self.dual_shoot_timer + 15:
                active_types.append(("dual", self.dual_shoot_timer + 15))
            if self.player_shield and current_time < self.shield_timer + 15:
                active_types.append(("shield", self.shield_timer + 15))

        if active_types:
            active_types.sort(key=lambda x: x[1], reverse=True)
            self.active_powerup_type = active_types[0][0]
            self.active_powerup_end_time = active_types[0][1]
        else:
            self.active_powerup_type = ""
            self.active_powerup_end_time = 0
    
            

if __name__ == "__main__":
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE, fullscreen=True, resizable=True)
    game_view = Gameview(window)
    start_menu = menu.StartMenuView(game_view)
    window.show_view(start_menu)
    arcade.run()