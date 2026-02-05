"""
    Class: AssetManager
    Info: Singleton class for pre-loading and caching all game assets
          Prevents disk I/O during gameplay for better performance
"""
import glob
import pygame

from configs import ROOT_DIR, meteor_assets_path, spaceship_assets_path, natural_sort


class AssetManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self._images = {}
        self._frames = {}
        self._sounds = {}
        self._fonts = {}

    def load_all(self):
        """Call once at startup after pygame.init() and display setup"""
        self._load_spaceship_frames()
        self._load_meteor_frames()
        self._load_single_images()
        self._load_sounds()
        self._load_fonts()

    def _load_spaceship_frames(self):
        paths = natural_sort(glob.glob(spaceship_assets_path + '*.gif'))
        self._frames['spaceship'] = [
            pygame.image.load(p).convert_alpha() for p in paths
        ]

    def _load_meteor_frames(self):
        meteor_types = ('asteroid', 'planetoid', 'space-door', 'comet')
        for meteor_type in meteor_types:
            paths = natural_sort(glob.glob(f"{meteor_assets_path}{meteor_type}/*.gif"))
            self._frames[f'meteor_{meteor_type}'] = [
                pygame.image.load(p).convert_alpha() for p in paths
            ]

    def _load_single_images(self):
        singles = {
            'laser': '/assets/laser.png',
            'star': '/assets/star.png',
            'health_powerup': '/assets/powerups/hot-dog.png',
            'ammo_powerup': '/assets/powerups/nuclear-buletons.png',
            'slowdown_powerup': '/assets/powerups/slow-down-timer.gif',
            'heart': '/assets/hot-dog-heart.png',
        }
        for key, path in singles.items():
            self._images[key] = pygame.image.load(ROOT_DIR + path).convert_alpha()

    def _load_sounds(self):
        sounds = {
            'laser_shot': '/assets/sounds/sound-effects/laser-shot.wav',
            'metal_impact': '/assets/sounds/sound-effects/metal-impact.wav',
            'explosion': '/assets/sounds/sound-effects/exlosion.wav',
            'healing': '/assets/sounds/sound-effects/healing.wav',
            'laser_reload': '/assets/sounds/sound-effects/laser-reload.mp3',
            'music': '/assets/sounds/music/gameplay-music.mp3',
        }
        for key, path in sounds.items():
            self._sounds[key] = pygame.mixer.Sound(ROOT_DIR + path)

    def _load_fonts(self):
        font_path = ROOT_DIR + '/assets/fonts/retro-gaming.ttf'
        for size in (18, 22, 26, 32, 48, 58, 72, 100):
            self._fonts[size] = pygame.font.Font(font_path, size)

    def get_frames(self, key):
        """Get animation frames list by key"""
        return self._frames.get(key, [])

    def get_image(self, key):
        """Get single image by key"""
        return self._images[key]

    def get_sound(self, key):
        """Get sound object by key"""
        return self._sounds.get(key)

    def get_font(self, size):
        """Get cached font by size"""
        return self._fonts[size]

    def play_sound(self, key):
        """Play a cached sound effect"""
        sound = self._sounds.get(key)
        if sound:
            sound.play()


# Global singleton instance
assets = AssetManager()
