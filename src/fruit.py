"""Fruit class handling game items and their effects."""
from typing import Tuple
import random
import pygame
from .snake import Snake
from .constants import BLOCK_SIZE, WIDTH, HEIGHT

class Fruit:
    """Represents a game fruit with position and effect."""
    def __init__(self, fruit_type: str) -> None:
        self.fruit_type = fruit_type
        self.x = random.randint(0, (WIDTH // BLOCK_SIZE) - 1) * BLOCK_SIZE
        self.y = random.randint(0, (HEIGHT // BLOCK_SIZE) - 1) * BLOCK_SIZE
        self.color = self._get_color()

    def _get_color(self) -> Tuple[int, int, int]:
        color_map = {
            'normal': (255, 0, 0),    # Red
            'boost': (255, 255, 0),   # Yellow
            'lengthen': (0, 0, 255)   # Blue
        }
        return color_map[self.fruit_type]

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the fruit on the game surface."""
        pygame.draw.rect(surface, self.color, (self.x, self.y, BLOCK_SIZE, BLOCK_SIZE))

    def effect(self, snake: Snake) -> None:
        """Apply effect to snake based on fruit type."""
        if self.fruit_type == 'normal':
            # Random growth between 1-3 segments
            for _ in range(random.randint(1, 3)):
                snake.grow()
        elif self.fruit_type == 'boost':
            snake.activate_speed_boost()
        elif self.fruit_type == 'lengthen':
            for _ in range(4):
                snake.grow()
