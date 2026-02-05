"""
    Class: Background
    Info: Non-colliding decorative objects (stars, particles, etc.)
"""
import pygame
from pygame import Rect, Surface

from configs import screen_size
from classes.asset_manager import assets


class Background(pygame.sprite.Sprite):
    rect: Rect  # type: ignore[reportIncompatibleMethodOverride]
    image: Surface  # type: ignore[reportIncompatibleMethodOverride]
    def __init__(self, x_pos, y_pos, x_speed, y_speed):
        super().__init__()
        # Use pre-loaded image from asset manager
        self.image = assets.get_image('star')

        # Movement dimensions
        self.x_speed = x_speed
        self.y_speed = y_speed

        self.rect = self.image.get_rect(center=(x_pos, y_pos))

    def update(self):
        """Update position and remove when offscreen"""
        self.rect.centerx += self.x_speed
        self.rect.centery += self.y_speed

        # Remove offscreen sprites
        if self.rect.centery > screen_size[1] + 50:
            self.kill()
