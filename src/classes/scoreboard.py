"""
    Class: Score
    Info: Manages and displays the player's score
"""
import pygame

from configs import screen_size
from classes.asset_manager import assets


class Score:
    def __init__(self, screen):
        self.score = 0
        self.screen = screen

    def reset(self):
        """Reset score to zero"""
        self.score = 0

    def add_score(self, score_to_add):
        """Add points to the score"""
        self.score += score_to_add

    def get_score(self):
        """Get current score value"""
        return self.score

    def draw(self):
        """Render score on screen"""
        font = assets.get_font(26)
        text_surface_center = (screen_size[0] / 2, 55)
        text_surface = font.render(
            str(self.score), False, (255, 255, 255)
        )
        text_rect = text_surface.get_rect(center=text_surface_center)
        self.screen.blit(text_surface, text_rect)
