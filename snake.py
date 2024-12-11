from constants import WIDTH, HEIGHT, BLACK, WHITE, GREEN, RED, YELLOW, BLUE, PURPLE, BLOCK_SIZE, clock, font, input_font
import pygame
import time

class Snake:
    def __init__(self, color, start_pos, controls):
        self.body = [start_pos, (start_pos[0] - BLOCK_SIZE, start_pos[1]), (start_pos[0] - 2 * BLOCK_SIZE, start_pos[1])]
        self.direction = (BLOCK_SIZE, 0)  # Initial direction (moving right)
        self.color = color
        self.controls = controls  # Dictionary for controls
        self.speed_boosted = False  # Flag for speed boost
        self.boost_end_time = 0  # Time when the boost should end
        self.score = 0

    def move(self):
        """Move the snake in the current direction."""
        head_x, head_y = self.body[0]
        new_head = (head_x + self.direction[0], head_y + self.direction[1])

        # Wrap the snake around the screen if it hits the walls
        if new_head[0] >= WIDTH:
            new_head = (0, new_head[1])  # Wrap to the right side
        elif new_head[0] < 0:
            new_head = (WIDTH - BLOCK_SIZE, new_head[1])  # Wrap to the left side

        if new_head[1] >= HEIGHT:
            new_head = (new_head[0], 0)  # Wrap to the bottom
        elif new_head[1] < 0:
            new_head = (new_head[0], HEIGHT - BLOCK_SIZE)  # Wrap to the top

        self.body = [new_head] + self.body[:-1]

    def grow(self):
        self.body.append(self.body[-1])  # Duplicate the last segment
        self.score += 1

    def lengthen(self):
        self.body += [self.body[-1]] * 4
        self.score += 4

    def check_collision(self, other_snake=None):
        head_x, head_y = self.body[0]
        # Self collision
        if self.body[0] in self.body[1:]:
            return True
        # Collision with the other snake
        if other_snake and self.body[0] in other_snake.body:
            return True
        return False

    def change_direction(self, new_direction):
        if (
            (new_direction[0] != -self.direction[0]) or
            (new_direction[1] != -self.direction[1])
        ):
            self.direction = new_direction

    def draw(self, surface):
        for segment in self.body:
            pygame.draw.rect(surface, self.color, pygame.Rect(segment[0], segment[1], BLOCK_SIZE, BLOCK_SIZE))

    def apply_boost(self):
        if self.speed_boosted and time.time() > self.boost_end_time:
            self.speed_boosted = False
            return 10  # Return normal speed
        elif self.speed_boosted:
            return 20  # Return increased speed
        else:
            return 10  # Return normal speed

    def get_score(self):
        return self.score
    
