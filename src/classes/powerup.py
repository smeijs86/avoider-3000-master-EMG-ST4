"""
    Class: PowerUp
    Info: Collectable items that restore health, ammo, or apply effects
"""
import pygame
from pygame import Rect, Surface

from configs import screen_size
from classes.asset_manager import assets


class PowerUp(pygame.sprite.Sprite):
    rect: Rect  # type: ignore[reportIncompatibleMethodOverride]
    image: Surface  # type: ignore[reportIncompatibleMethodOverride]
    # Movement speed
    FALL_SPEED = 2

    def __init__(self, powerup_type, x_pos, y_pos):
        super().__init__()
        self.powerup_type = powerup_type

        # Map powerup type to asset key
        asset_keys = {
            'health': 'health_powerup',
            'ammo': 'ammo_powerup',
            'slowdown': 'slowdown_powerup',
        }

        asset_key = asset_keys.get(powerup_type, 'health_powerup')
        self.image = assets.get_image(asset_key)
        self.rect = self.image.get_rect(center=(x_pos, y_pos))

    def update(self):
        self.rect.centery += self.FALL_SPEED

        # Remove offscreen powerups
        if self.rect.centery > screen_size[1] + 50:
            self.kill()
