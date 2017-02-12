from Renderer import Renderer
import pygame
import math
import random
from pygame.rect import Rect
import Params
from NeuralNets import NeuralNet
import time


class Bullet:
    # Read-only property. Rect is derived from x, y, width, height
    @property
    def rect(self):
        return Rect(self.x, self.y, self.size, self.size)

    def move(self):
        self.x += self.dx * self.speed
        self.y += self.dy * self.speed

    def __init__(self, x, y, dx, dy):
        self.size = 10
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.speed = 12

    def render(self):
        pygame.draw.rect(Renderer.SCREEN, (0, 0, 0), self.rect, 0)


class Entity:
    # Read-only property. Rect is derived from x, y, width, height
    @property
    def rect(self):
        return Rect(self.x, self.y, self.size, self.size)

    def can_shoot(self):
        return self.bullet is None and time.time() - self.last_shot_at >= self.fire_rate

    def shoot(self):
        bullet_angle = random.uniform(self.heading - (self.fov_angle / 2), self.heading + (self.fov_angle / 2))
        bullet_dx = math.cos(math.radians(bullet_angle))
        bullet_dy = math.sin(math.radians(bullet_angle))

        self.bullet = Bullet(self.rect.centerx, self.rect.centery, bullet_dx, bullet_dy)
        self.last_shot_at = time.time()

    def hit_target(self, target):
        if self.bullet is not None:
            if self.bullet.rect.colliderect(target.rect):
                self.bullet = None
                return True
            return False

    def get_fov_triangle(self):
        angle_variance = self.fov_angle / 2
        left_angle = self.heading - angle_variance
        right_angle = self.heading + angle_variance

        pt_1 = self.rect.center
        pt_2_x = pt_1[0] + (math.cos(math.radians(left_angle)) * Params.FOV_DISTANCE)
        pt_2_y = pt_1[1] + (math.sin(math.radians(left_angle)) * Params.FOV_DISTANCE)
        pt_3_x = pt_1[0] + (math.cos(math.radians(right_angle)) * Params.FOV_DISTANCE)
        pt_3_y = pt_1[1] + (math.sin(math.radians(right_angle)) * Params.FOV_DISTANCE)

        return pt_1, (pt_2_x, pt_2_y), (pt_3_x, pt_3_y)

    def handle_outputs(self, outputs):
        # Output decisions
        left = outputs[0]
        right = outputs[1]
        shoot = outputs[2] >= 0.5
        self.move_decision = outputs[3] >= 0.3
        fov_change = outputs[4]

        if fov_change >= 0.55:
            self.fov_angle += Params.FOV_CHANGE_PER_FRAME
        elif fov_change <= 0.45:
            self.fov_angle -= Params.FOV_CHANGE_PER_FRAME

        if self.fov_angle < Params.MIN_FOV_ANGLE:
            self.fov_angle = Params.MIN_FOV_ANGLE
        elif self.fov_angle > Params.MAX_FOV_ANGLE:
            self.fov_angle = Params.MAX_FOV_ANGLE

        if shoot and self.can_shoot():
            self.shoot()

        self.change_angle((right - left) * Params.MAX_TURN_RATE)
        self.speed = left + right

    def change_angle(self, angle_change):
        # Change the angle
        self.heading += angle_change

        # Assign new movement vector
        self.dx = math.cos(math.radians(self.heading))
        self.dy = math.sin(math.radians(self.heading))

        # Recalculate fov triangle
        self.fov_triangle = self.get_fov_triangle()

    def move(self):
        if self.move_decision:
            self.x += self.dx * self.speed * 4
            self.y += self.dy * self.speed * 4

            # Don't move outside bounds of screen
            if self.x <= 0:
                self.x = 0
            elif self.x + self.size >= Renderer.SCREEN_WIDTH:
                self.x = Renderer.SCREEN_WIDTH - self.size

            if self.y <= 0:
                self.y = 0
            elif self.y + self.size >= Renderer.SCREEN_HEIGHT:
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
        self.x = 0
        self.y = 0
        self.dx = 0
        self.dy = 0
        self.heading = 0
        self.size = 60
        self.fov_angle = math.floor((Params.MAX_FOV_ANGLE + Params.MIN_FOV_ANGLE) / 2)
        self.fov_triangle = self.get_fov_triangle()
        self.brain = NeuralNet()
        self.fitness = 0
        self.change_angle(0)
        self.speed = 7
        self.move_decision = False
        self.health = Params.FIGHTER_HEALTH
        self.bullet = None
        self.fire_rate = Params.FIRE_RATE
        self.last_shot_at = 0
        self.can_see_enemy = False
        self.can_see_bullet = False
        self.image = pygame.image.load('shooter.png').convert()
        self.image.set_colorkey((255, 255, 255))

    def render(self):
        # Render entity
        Renderer.SCREEN.blit(self.image, (self.x, self.y))

        # Render red dot representing entity's current facing
        radius = math.floor(self.size / 2)
        nose_x = math.floor(self.x + radius + (self.dx * radius))
        nose_y = math.floor(self.y + radius + (self.dy * radius))
        pygame.draw.circle(Renderer.SCREEN, (255, 0, 0), (nose_x, nose_y), 5, 0)

        # Render fov triangle
        if self.can_see_bullet:
            pygame.draw.polygon(Renderer.SCREEN, (0, 255, 0), (self.fov_triangle[0], self.fov_triangle[1], self.fov_triangle[2]), 1)
        else:
            pygame.draw.polygon(Renderer.SCREEN, (220, 220, 220), (self.fov_triangle[0], self.fov_triangle[1], self.fov_triangle[2]), 1)

        if self.can_see_enemy:
            pygame.draw.circle(Renderer.SCREEN, (0, 255, 0), (math.floor(self.x + radius), math.floor(self.y + radius)), 5, 0)

        # Render bullet
        if self.bullet is not None:
            self.bullet.render()

