"""
    Class: GameState
    Info: Encapsulates all mutable game state in a single class
          Replaces scattered global variables for cleaner architecture
"""
import pygame


class GameState:
    # Spawn counter reset values
    SLOWDOWN_SPAWN_INTERVAL = 120
    HEALTH_SPAWN_INTERVAL = 90
    AMMO_SPAWN_INTERVAL = 35

    # Difficulty settings
    BASE_SPAWN_INTERVAL = 1000  # milliseconds; originally 250
    MIN_SPAWN_INTERVAL = 250  # milliseconds; originally 100
    DIFFICULTY_SCORE_STEP = 500  # Score increment for difficulty increase
    DIFFICULTY_TIME_REDUCTION = 10  # ms reduction per difficulty step

    def __init__(self):
        self.reset()

    def reset(self):
        """Reset all game state to initial values"""
        self.started = False
        self.laser_ready = True
        self.laser_timer = 0
        self.laser_cooldown = 125  # milliseconds between shots

        self.spawn_counters = {
            'slowdown': self.SLOWDOWN_SPAWN_INTERVAL,
            'health': self.HEALTH_SPAWN_INTERVAL,
            'ammo': self.AMMO_SPAWN_INTERVAL,
        }

        self.current_spawn_interval = self.BASE_SPAWN_INTERVAL
        self.last_difficulty_score = 0

    def can_fire(self, current_time):
        """Check if enough time has passed to fire again"""
        if current_time - self.laser_timer >= self.laser_cooldown:
            self.laser_ready = True
        return self.laser_ready

    def fire(self, current_time):
        """Record that a shot was fired"""
        self.laser_timer = current_time
        self.laser_ready = False

    def tick_spawn_counters(self):
        """
        Decrement spawn counters and return list of powerups to spawn.
        Returns: list of powerup keys that should spawn this tick
        """
        to_spawn = []

        reset_values = {
            'slowdown': self.SLOWDOWN_SPAWN_INTERVAL,
            'health': self.HEALTH_SPAWN_INTERVAL,
            'ammo': self.AMMO_SPAWN_INTERVAL,
        }

        for key in self.spawn_counters:
            self.spawn_counters[key] -= 1
            if self.spawn_counters[key] <= 0:
                to_spawn.append(key)
                self.spawn_counters[key] = reset_values[key]

        return to_spawn

    def update_difficulty(self, current_score):
        """
        Update spawn interval based on current score.
        Returns: new spawn interval if changed, None otherwise
        """
        difficulty_level = current_score // self.DIFFICULTY_SCORE_STEP

        if difficulty_level > self.last_difficulty_score // self.DIFFICULTY_SCORE_STEP:
            reduction = difficulty_level * self.DIFFICULTY_TIME_REDUCTION
            new_interval = max(
                self.MIN_SPAWN_INTERVAL,
                self.BASE_SPAWN_INTERVAL - reduction
            )

            if new_interval != self.current_spawn_interval:
                self.current_spawn_interval = new_interval
                self.last_difficulty_score = current_score
                return new_interval

        return None

    def get_spawn_interval(self):
        """Get current meteor spawn interval in milliseconds"""
        return self.current_spawn_interval
