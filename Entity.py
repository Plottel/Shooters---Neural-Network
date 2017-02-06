from Renderer import Renderer
import pygame
import math
from pygame.rect import Rect
import Params
from NeuralNets import NeuralNet

class Bullet:
    # Read-only property. Rect is derived from x, y, width, height
    @property
    def rect(self):
        return Rect(self.x, self.y, self.size, self.size)

    def move(self):
        self.x += self.dx * self.speed
        self.y += self.dy * self.speed

    def __init__(self, x, y, dx, dy):
        self.size = 5
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.speed = 6

    def render(self):
        pygame.draw.rect(Renderer.SCREEN, (0, 0, 0), self.rect, 0)

class Entity:
    # Read-only property. Rect is derived from x, y, width, height
    @property
    def rect(self):
        return Rect(self.x, self.y, self.size, self.size)

    def get_vector_to_bullet(self, bullet):
        x_offset = bullet.rect.centerx - self.rect.centerx
        y_offset = bullet.rect.centery - self.rect.centery

        vector_length = math.sqrt((x_offset * x_offset) + (y_offset * y_offset))

        if x_offset == 0 or vector_length == 0:
            x_vel = 0
        else:
            x_vel = x_offset / vector_length

        if y_offset == 0 or vector_length == 0:
            y_vel = 0
        else:
            y_vel = y_offset / vector_length

        self.vector_to_bullet = x_vel, y_vel

    def get_vector_to_enemy(self, enemy):
        x_offset = enemy.rect.centerx - self.rect.centerx
        y_offset = enemy.rect.centery - self.rect.centery

        vector_length = math.sqrt((x_offset * x_offset) + (y_offset * y_offset))

        if x_offset == 0 or vector_length == 0:
            x_vel = 0
        else:
            x_vel = x_offset / vector_length

        if y_offset == 0 or vector_length == 0:
            y_vel = 0
        else:
            y_vel = y_offset / vector_length

        self.vector_to_enemy = x_vel, y_vel

    def can_shoot(self):
        return self.bullet is None

    def shoot(self):
        self.bullet = Bullet(self.rect.centerx, self.rect.centery, self.dx, self.dy)

    def hit_target(self, target):
        if self.bullet is not None:
            if self.bullet.rect.colliderect(target.rect):
                self.bullet = None
                return True
            return False

    def handle_outputs(self, outputs):
        # Output decisions
        left = outputs[0]
        right = outputs[1]
        shoot = outputs[2] >= 0.5

        self.change_angle((right - left) * Params.MAX_TURN_RATE)
        self.speed = left + right

        if shoot and self.can_shoot():
            self.shoot()

    def change_angle(self, angle_change):
        # Change the angle
        self.heading += angle_change

        # Assign new movement vector
        self.dx = math.cos(math.radians(self.heading))
        self.dy = math.sin(math.radians(self.heading))

    def move(self):
        self.x += self.dx * self.speed * 4
        self.y += self.dy * self.speed * 4

        # Don't move outside bounds of screen
        if self.x < 0:
            self.x = 0
        elif self.x + self.size > Renderer.SCREEN_WIDTH:
            self.x = Renderer.SCREEN_WIDTH - self.size
        elif self.y < 0:
            self.y = 0
        elif self.y + self.size > Renderer.SCREEN_HEIGHT:
            self.y = Renderer.SCREEN_HEIGHT - self.size

        #
        # BULLET
        #
        if self.bullet is not None:
            self.bullet.move()

            # Destroy bullet if outside bounds of screen
            if self.bullet.x < 0:
                self.bullet = None
            elif self.bullet.x > Renderer.SCREEN_WIDTH:
                self.bullet = None
            elif self.bullet.y < 0:
                self.bullet = None
            elif self.bullet.y > Renderer.SCREEN_HEIGHT:
                self.bullet = None

    def __init__(self,):
        # This is an optimisation opportunity.
        # Shouldn't need to create a NeuralNet and populate with random weights
        # when it's about to be replaced by the GenAlg.
        self.brain = NeuralNet()
        self.fitness = 0
        self.size = 40
        self.x = 100
        self.y = 100
        self.dx = 0
        self.dy = 0
        self.heading = 0
        self.change_angle(0)
        self.speed = 5
        self.health = Params.FIGHTER_HEALTH
        self.bullet = None
        self.vector_to_enemy = 0, 0
        self.vector_to_bullet = 0, 0

        self.image = pygame.image.load('shooter.png').convert()
        self.image.set_colorkey((255, 255, 255))

    def render(self):
        # circle(Surface, color, pos, radius, width=0) -> Rect
        radius = self.size / 2
        at_x = math.floor(self.x + radius + (self.dx * radius))
        at_y = math.floor(self.y + radius + (self.dy * radius))
        Renderer.SCREEN.blit(self.image, (self.x, self.y))
        pygame.draw.circle(Renderer.SCREEN, (255, 0, 0), (at_x, at_y), 5, 0)

        #start_point = (self.rect.centerx, self.rect.centery)
        #end_point = (start_point[0] + (self.vector_to_enemy[0] * 300), start_point[1] + (self.vector_to_enemy[1] * 300))

        #pygame.draw.line(Renderer.SCREEN, (255, 0, 0), start_point, end_point, 1)

        if self.bullet is not None:
            self.bullet.render()