"""
    Class: Meteor
    Info: Obstacle objects that the player must avoid or destroy
"""
import pygame
from pygame import Rect, Surface

from configs import screen_size
from classes.asset_manager import assets


class Meteor(pygame.sprite.Sprite):
    rect: Rect  # type: ignore[reportIncompatibleMethodOverride]
    image: Surface  # type: ignore[reportIncompatibleMethodOverride]
    # Animation settings
    FRAME_DURATION = 50  # milliseconds per animation frame

    def __init__(self, meteor_type, x_pos, y_pos, x_speed, y_speed, rotation_speed):
        super().__init__()
        self.angle = 0
        self.slow_speed = False
        self.meteor_type = meteor_type

        # Use pre-loaded frames from asset manager
        # meteor_type is like 'asteroid', 'planetoid', etc.
        asset_key = f'meteor_{meteor_type.rstrip("/")}'
        self.frames = assets.get_frames(asset_key)

        self.image_index = 0
        self.image = self.frames[self.image_index]
        self.clean_image = self.image.copy()

        # Movement dimensions
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.original_x_speed = x_speed
        self.original_y_speed = y_speed

        self.rect = self.image.get_rect(center=(x_pos, y_pos))
        self.rotation_speed = rotation_speed

        # Delta-time animation tracking
        self.last_update = pygame.time.get_ticks()
        self.animation_timer = 0

    def update(self):
        now = pygame.time.get_ticks()
        dt = now - self.last_update
        self.last_update = now

        self.rect.centerx += self.x_speed
        self.rect.centery += self.y_speed

        self.animate_meteors(dt)

        if 'planetoid' not in self.meteor_type:
            self.rotate_meteors()

        # Remove offscreen meteors
        if (self.rect.centery > screen_size[1] + 50 or
                self.rect.centerx < -50 or
                self.rect.centerx > screen_size[0] + 50):
            self.kill()

    def slow_down_movement_speed(self):
        """Reduce meteor speed to 40% of original"""
        self.slow_speed = True
        self.x_speed = round((self.original_x_speed * 40) / 100)
        self.y_speed = round((self.original_y_speed * 40) / 100)

    def animate_meteors(self, dt):
        """Delta-time based animation"""
        self.animation_timer += dt
        if self.animation_timer >= self.FRAME_DURATION:
            self.animation_timer = 0
            self.image_index = (self.image_index + 1) % len(self.frames)

        self.image = self.frames[self.image_index]
        self.clean_image = self.image.copy()

    def rotate_meteors(self):
        """Apply rotation animation to meteor"""
        rotation_tuple = self.rot_center(self.clean_image, self.angle)
        self.image = rotation_tuple[0]
        self.rect = rotation_tuple[1]
        self.angle += self.rotation_speed

    def rot_center(self, image, angle):
        """Rotate image around its center"""
        rotated_image = pygame.transform.rotate(image, angle)
        new_rect = rotated_image.get_rect(center=self.rect.center)
        return rotated_image, new_rect
