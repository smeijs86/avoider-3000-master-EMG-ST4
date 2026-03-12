"""
    Class: SpaceShip
    Info: Player character class with animation, health, ammo, and movement
"""
import pygame
from pygame import Rect, Surface
# serial will be handled by main; spaceship just accepts the decoded value
from configs import screen_size
from classes.asset_manager import assets

class SpaceShip(pygame.sprite.Sprite):
    rect: Rect  # type: ignore[reportIncompatibleMethodOverride]
    image: Surface  # type: ignore[reportIncompatibleMethodOverride]
    # Animation settings
    FRAME_DURATION = 40  # milliseconds per animation frame

    # Invincibility settings
    INVINCIBILITY_DURATION = 1000  # milliseconds of immunity after taking damage
    BLINK_INTERVAL = 100  # milliseconds between visibility toggles when invincible

    # Player stats
    MAX_HEALTH = 5
    MAX_AMMO = 30

    def __init__(self, x_pos, y_pos, screen_obj):
        super().__init__()
        self.x = screen_size[0] / 2 #Start in middle of screen, originally x_pos
        self.y = screen_size[1]     #Start at bottom of screen, originally y_pos    
        self.screen = screen_obj

        # Use pre-loaded frames from asset manager
        self.frames = assets.get_frames('spaceship')
        self.image_index = 0
        self.image = self.frames[self.image_index]
        self.clean_image = self.image.copy()
        self.center = (x_pos, y_pos)
        self.rect = self.image.get_rect(center=self.center)

        # Pre-loaded heart image for health display
        self.shield_surface = assets.get_image('heart')

        # Player stats
        self.health = self.MAX_HEALTH
        self.ammo = self.MAX_AMMO

        # Delta-time animation tracking
        self.last_update = pygame.time.get_ticks()
        self.animation_timer = 0

        # Invincibility state
        self.invincible = False
        self.invincible_timer = 0
        self.blink_timer = 0
        self.visible = True

    def update(self, input_data):
        """Advance ship state one frame using the latest input.

        ``input_data`` is provided by the caller (main.py) and should be a
        small primitive such as ``1`` for left, ``2`` for right, ``3`` for
        shoot, or ``None`` when nothing has arrived.  Defaulting to ``None``
        keeps the method callable without arguments during transition.
        """
        now = pygame.time.get_ticks()
        dt = now - self.last_update
        self.last_update = now

        # horizontal movement comes from the serial‑supplied value
        if input_data == 1:   # Move left
            self.x -= 5
        elif input_data == 2: # Move right
            self.x += 5

        self.rect.center = (int(self.x), self.y)

        self.animate_space_ship(dt)
        self.update_invincibility(dt)
        self.display_health()
        self.display_ammo()
        self.screen_constrain()

        # keep the latest input for use during rotation
        self.latest_input = input_data
        self.rotate()

    def animate_space_ship(self, dt):
        """Delta-time based animation - consistent speed regardless of framerate"""
        self.animation_timer += dt
        if self.animation_timer >= self.FRAME_DURATION:
            self.animation_timer = 0
            self.image_index = (self.image_index + 1) % len(self.frames)

        self.image = self.frames[self.image_index]
        self.clean_image = self.image.copy()

    def update_invincibility(self, dt):
        """Handle invincibility timer and blinking effect"""
        if self.invincible:
            self.invincible_timer -= dt
            self.blink_timer += dt

            # Toggle visibility for blinking effect
            if self.blink_timer >= self.BLINK_INTERVAL:
                self.blink_timer = 0
                self.visible = not self.visible

            # End invincibility
            if self.invincible_timer <= 0:
                self.invincible = False
                self.visible = True

            # Apply visibility to image alpha
            if not self.visible:
                self.image = self.image.copy()
                self.image.set_alpha(100)

    def display_health(self):
        for index in range(self.health):
            self.screen.blit(
                self.shield_surface,
                ((index + 1) * 25, screen_size[1] - 40)
            )

    def display_ammo(self):
        font = assets.get_font(18)
        text_surface_center = (screen_size[0] - 70, screen_size[1] - 23)
        text_surface = font.render(
            'AMMO: ' + str(self.ammo), False, (255, 255, 255)
        )
        text_rect = text_surface.get_rect(center=text_surface_center)
        self.screen.blit(text_surface, text_rect)

    def get_damage(self, damage_amount):
        """
        Apply damage to player if not invincible.
        Returns True if damage was applied, False if blocked by invincibility.
        """
        if not self.invincible:
            self.health -= damage_amount
            self.invincible = True
            self.invincible_timer = self.INVINCIBILITY_DURATION
            self.blink_timer = 0
            return True
        return False

    def decrease_ammo(self, shot_amount):
        """Decrease ammo when player shoots"""
        self.ammo -= shot_amount

    def restore_health(self):
        if self.health == self.MAX_HEALTH:
            return

        self.health += 1

    def restore_ammo(self):
        self.ammo = self.MAX_AMMO

    def screen_constrain(self):
        """Keep player within screen boundaries"""
        if self.rect.left <= 0:
            self.rect.left = 0

        if self.rect.right >= screen_size[0]:
            self.rect.right = screen_size[0]

        if self.rect.top <= 0:
            self.rect.top = 0

        if self.rect.bottom >= screen_size[1] - 50:
            self.rect.bottom = screen_size[1] - 50

    def rotate(self):
        """Tilt spaceship based on the last movement input."""
        # mouse_rel = pygame.mouse.get_rel()  # no longer used
        inp = getattr(self, "latest_input", None)

        if inp == 1:
            self.image = self.rotate_from_center(self.clean_image, 15)
        elif inp == 2:
            self.image = self.rotate_from_center(self.clean_image, -15)
        else:
            # Reset to upright when not moving
            self.image = self.rotate_from_center(self.clean_image, 0)

    def rotate_from_center(self, image, angle):
        """Rotate image around its center without changing dimensions"""
        orig_rect = image.get_rect()
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        return rot_image
