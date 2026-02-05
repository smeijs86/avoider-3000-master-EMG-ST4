"""
    Configuration and constants for Avoider-3000
"""
import os
import re

import pygame

# Root directory for asset paths
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# Initialize pygame to get display info
pygame.init()
display_info = pygame.display.Info()
screen_size = (display_info.current_w - 15, display_info.current_h - 15)

# Game metadata
game_name = 'Avoider-3000'

# Asset paths - images
spaceship_assets_path = ROOT_DIR + '/assets/spaceship/'
meteor_assets_path = ROOT_DIR + '/assets/meteors/'

# Meteor types (without trailing slash for cleaner usage)
METEOR_TYPES = ('asteroid', 'planetoid', 'space-door', 'comet')


def natural_sort(file_list):
    """
    Sort a list of filenames naturally (e.g., frame1, frame2, frame10)
    instead of lexicographically (frame1, frame10, frame2)
    """
    def convert(text):
        return int(text) if text.isdigit() else text.lower()

    def alphanum_key(key):
        return [convert(c) for c in re.split('([0-9]+)', key)]

    return sorted(file_list, key=alphanum_key)
