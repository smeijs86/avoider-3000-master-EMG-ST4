"""
Avoider-3000: A retro-style endless arcade space shooter
Main game loop and orchestration
"""

import os
import random
import sys
import serial

from classes.asset_manager import assets
from classes.background import Background
from classes.game_state import GameState
from classes.laser import Laser
from classes.meteors import Meteor
from classes.powerup import PowerUp
from classes.scoreboard import Score
from classes.spaceship import SpaceShip
from configs import METEOR_TYPES, game_name, screen_size

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

# Initialize pygame
import pygame

pygame.init()
pygame.display.set_caption(game_name)
screen = pygame.display.set_mode(screen_size)  # Windowed mode for debugging
clock = pygame.time.Clock()

# Load all assets after display is initialized
assets.load_all()

# Sprite groups
spaceship_group = pygame.sprite.GroupSingle()
laser_group = pygame.sprite.Group()
meteor_group = pygame.sprite.Group()
star_group = pygame.sprite.Group()
healing_group = pygame.sprite.Group()
slow_down_group = pygame.sprite.Group()
ammo_group = pygame.sprite.Group()

# Meteor spawn timer
METEOR_EVENT = pygame.USEREVENT
pygame.time.set_timer(METEOR_EVENT, GameState.BASE_SPAWN_INTERVAL)

# Create player and score (using lowercase to avoid shadowing class names)
player = SpaceShip(400, 500, screen)
spaceship_group.add(player)
score = Score(screen)

# Game state manager
state = GameState()


def game_menu():
    """Display the main menu screen"""
    render_msg("-= AVOIDER =-", 100, (screen_size[0] / 2, 100))
    render_msg("3000", 72, (screen_size[0] / 2, 200))

    hot_dog = assets.get_image("health_powerup")
    screen.blit(hot_dog, (screen_size[0] / 2 - 30, screen_size[1] / 2 - 60))

    render_msg(
        "Press SPACE to start!", 32, (screen_size[0] / 2, screen_size[1] / 2 + 100)
    )
    render_msg("Press Q to quit!", 22, (screen_size[0] / 2, screen_size[1] / 2 + 140))

    render_msg(
        "- Designed by: Sargis Mardirossian - Developed by: Harutyun Mardirossian -",
        18,
        (screen_size[0] / 2, screen_size[1] - 70),
    )
    render_msg("@Corrupted.bit", 22, (screen_size[0] / 2, screen_size[1] - 40))


def spawn_powerup(powerup_type, group):
    """Spawn a powerup at a random position"""
    random_x = random.randrange(50, screen_size[0] - 50)
    random_y = random.randrange(-200,50)
    powerup = PowerUp(powerup_type, random_x, random_y)
    group.add(powerup)


def draw_background():
    """Update and draw background elements"""
    star_group.draw(screen)
    star_group.update()


def run_gameplay(score_obj):
    """Main gameplay loop logic - handle rendering, updates, and collisions"""
    pygame.mouse.set_visible(False)

    # Draw and update all sprite groups
    meteor_group.draw(screen)
    meteor_group.update()

    laser_group.draw(screen)
    laser_group.update()

    healing_group.draw(screen)
    healing_group.update()

    ammo_group.draw(screen)
    ammo_group.update()

    slow_down_group.draw(screen)
    slow_down_group.update()

    spaceship_group.draw(screen)
    spaceship_group.update()

    score_obj.draw()

    # Check collisions with player
    if pygame.sprite.spritecollide(player, meteor_group, True):
        damage = random.randrange(1, 3)
        if player.get_damage(damage):
            assets.play_sound("metal_impact")

    if pygame.sprite.spritecollide(player, healing_group, True):
        player.restore_health()
        assets.play_sound("healing")

    if pygame.sprite.spritecollide(player, ammo_group, True):
        player.restore_ammo()
        assets.play_sound("laser_reload")

    if pygame.sprite.spritecollide(player, slow_down_group, True):
        meteor: Meteor
        for meteor in meteor_group.sprites():
            if not meteor.slow_speed:
                meteor.slow_down_movement_speed()

    # Check laser-meteor collisions
    for laser in laser_group:
        if pygame.sprite.spritecollide(laser, meteor_group, True):
            laser_group.remove(laser)
            points = random.randrange(10, 55, 5)
            score_obj.add_score(points)
            assets.play_sound("explosion")

    # Update difficulty based on score
    current_score = score_obj.get_score()
    new_interval = state.update_difficulty(current_score)
    if new_interval:
        pygame.time.set_timer(METEOR_EVENT, new_interval)


def game_over_screen():
    """Display the game over screen"""
    pygame.mouse.set_visible(True)
    final_score = score.get_score()

    render_msg("GAME OVER", 58, (screen_size[0] / 2, screen_size[1] / 2 - 100))
    render_msg(str(final_score), 48, (screen_size[0] / 2, screen_size[1] / 2 - 40))
    render_msg(
        "Press SPACE to try again!", 32, (screen_size[0] / 2, screen_size[1] / 2 + 100)
    )
    render_msg(
        "Press Q to quit the game", 22, (screen_size[0] / 2, screen_size[1] / 2 + 160)
    )


def render_msg(msg, font_size, text_pos):
    """Render text message on screen using cached font"""
    font = assets.get_font(font_size)
    text_surface = font.render(msg, False, (255, 255, 255))
    text_rect = text_surface.get_rect(center=text_pos)
    screen.blit(text_surface, text_rect)


def reset_game():
    """Reset all game state for a new game"""
    player.health = SpaceShip.MAX_HEALTH
    player.restore_ammo()
    player.restore_health()
    player.invincible = False

    meteor_group.empty()
    star_group.empty()
    healing_group.empty()
    ammo_group.empty()
    slow_down_group.empty()
    laser_group.empty()

    score.reset()
    state.reset()

    # Reset spawn timer to base interval
    pygame.time.set_timer(METEOR_EVENT, GameState.BASE_SPAWN_INTERVAL)


def start_background_music():
    """Start the background music loop"""
    # assets.play_sound("music")


# Start the game
start_background_music()

# Main game loop
while True:
    for event in pygame.event.get():
        # Quit game
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                pygame.quit()
                sys.exit()

            if event.key == pygame.K_ESCAPE:
                state.started = False

            if event.key == pygame.K_SPACE:
                if not state.started:
                    reset_game()
                    state.started = True
                elif player.health <= 0:
                    reset_game()
                    state.started = True

        # Shooting
        if event.type == pygame.MOUSEBUTTONDOWN:    #Adjust this to serial input.
            current_time = pygame.time.get_ticks()
            if player.ammo > 0 and state.can_fire(current_time):
                assets.play_sound("laser_shot")
                laser = Laser(player.rect.center, 20)   #Originally: pygame.mouse.get_pos()
                player.decrease_ammo(1)
                laser_group.add(laser)
                state.fire(current_time)

        # Spawn meteors and powerups
        if event.type == METEOR_EVENT:
            if state.started:
                # Spawn meteor
                meteor_type = random.choice(METEOR_TYPES)
                random_x = random.randrange(5, screen_size[0] - 5)
                random_y = random.randrange(-200, -50)
                random_x_speed = random.randrange(-1, 2)    #Slowed down, originally (-2, 3)
                random_y_speed = random.randrange(1, 3)     #Slowed down, originally (1, 6)
                rotation_speed = random.randrange(3, 8)

                meteor = Meteor(
                    meteor_type,
                    random_x,
                    random_y,
                    random_x_speed,
                    random_y_speed,
                    rotation_speed,
                )
                meteor_group.add(meteor)

                # Check for powerup spawns
                powerups_to_spawn = state.tick_spawn_counters()
                for powerup_type in powerups_to_spawn:
                    if powerup_type == "slowdown":
                        spawn_powerup("slowdown", slow_down_group)
                    elif powerup_type == "health":
                        spawn_powerup("health", healing_group)
                    elif powerup_type == "ammo":
                        spawn_powerup("ammo", ammo_group)

            # Always spawn background stars
            random_x = random.randrange(50, screen_size[0] - 50)
            random_y = random.randrange(-50, 0)
            star = Background(random_x, random_y, 0, 3)
            star_group.add(star)

    # Render frame
    screen.fill((20, 20, 0))
    draw_background()

    if state.started:
        if player.health > 0:
            run_gameplay(score)
        else:
            game_over_screen()
    else:
        game_menu()

    pygame.display.update()
    clock.tick(60)  # Increased to 60 FPS for smoother gameplay
