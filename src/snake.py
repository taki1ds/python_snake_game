"""Snake class handling movement and growth logic."""
from typing import Tuple, Dict, Optional
import time
import pygame
from .constants import BLOCK_SIZE, WIDTH, HEIGHT

class Snake:
    """Represents a player-controlled snake."""
    BASE_SPEED = 1

    def __init__(self, color: Tuple[int, int, int], start_pos: Tuple[int, int],
                 controls: Dict[str, int], name: str) -> None:
        self.body = [start_pos, (start_pos[0]-BLOCK_SIZE, start_pos[1]),
                     (start_pos[0]-2*BLOCK_SIZE, start_pos[1])]
        self.direction = (BLOCK_SIZE, 0)
        self.color = color
        self.controls = controls
        self.name = name
        self.speed = self.BASE_SPEED
        self.score = 0
        self.boost_end = 0.0

    def move(self) -> None:
        """Update snake position with wrap-around."""
        for _ in range(self.speed):
            head_x, head_y = self.body[0]
            new_head = (
                (head_x + self.direction[0]) % WIDTH,
                (head_y + self.direction[1]) % HEIGHT
            )
            self.body.insert(0, new_head)
            self.body.pop()

    def grow(self) -> None:
        """Increase snake length and score."""
        self.body.append(self.body[-1])
        self.score += 1

    def check_self_collision(self) -> bool:
        """Check if head collides with body."""
        return self.body[0] in self.body[1:]

    def check_collision(self, other: 'Snake') -> bool:
        """Check collision with another snake."""
        return self.body[0] in other.body

    def handle_input(self, keys: pygame.key.ScancodeWrapper) -> None:
        """Handle keyboard input for direction changes."""
        if keys[self.controls['up']]:
            self._change_direction((0, -BLOCK_SIZE))
        elif keys[self.controls['down']]:
            self._change_direction((0, BLOCK_SIZE))
        elif keys[self.controls['left']]:
            self._change_direction((-BLOCK_SIZE, 0))
        elif keys[self.controls['right']]:
            self._change_direction((BLOCK_SIZE, 0))

    def _change_direction(self, new_dir: Tuple[int, int]) -> None:
        """Change direction if not reversing."""
        if (new_dir[0], new_dir[1]) != (-self.direction[0], -self.direction[1]):
            self.direction = new_dir

    def activate_speed_boost(self) -> None:
        """Enable temporary speed boost."""
        self.speed = self.BASE_SPEED * 2
        self.boost_end = time.time() + 5

    def update(self) -> None:
        """Update speed state and handle boosts."""
        if time.time() > self.boost_end and self.speed > self.BASE_SPEED:
            self.speed = self.BASE_SPEED

    def draw(self, surface: pygame.Surface) -> None:
        """Draw snake on the game surface."""
        for segment in self.body:
            pygame.draw.rect(surface, self.color, (segment[0], segment[1], BLOCK_SIZE, BLOCK_SIZE))
