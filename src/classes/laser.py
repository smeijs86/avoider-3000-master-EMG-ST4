"""
    Class: Laser
    Info: Player projectile that destroys meteors
"""
import pygame
from pygame import Rect, Surface

from classes.asset_manager import assets


class Laser(pygame.sprite.Sprite):
    rect: Rect  # type: ignore[reportIncompatibleMethodOverride]
    image: Surface  # type: ignore[reportIncompatibleMethodOverride]
    def __init__(self, pos, speed):
        super().__init__()
        # Use pre-loaded image from asset manager
        self.image = assets.get_image('laser')
        self.speed = speed
        self.rect = self.image.get_rect(center=pos)

    def update(self):
        self.rect.centery -= self.speed

        # Remove offscreen lasers
        if self.rect.centery < -20:
            self.kill()
