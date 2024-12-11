from constants import WIDTH, HEIGHT, BLACK, WHITE, GREEN, RED, YELLOW, BLUE, PURPLE, BLOCK_SIZE, clock, font, input_font
import random
import pygame
import time 

class Fruit:
    def __init__(self, fruit_type):
        self.fruit_type = fruit_type
        self.x = random.randint(0, (WIDTH // BLOCK_SIZE) - 1) * BLOCK_SIZE
        self.y = random.randint(0, (HEIGHT // BLOCK_SIZE) - 1) * BLOCK_SIZE
        self.color = self.get_color()

    def get_color(self):
        if self.fruit_type == 'normal':
            return RED
        elif self.fruit_type == 'boost':
            return YELLOW
        elif self.fruit_type == 'lengthen':
            return BLUE

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE))

    def effect(self, snake):
        if self.fruit_type == 'normal':
            snake.grow()  # Grow the snake
        elif self.fruit_type == 'boost':
            snake.speed_boosted = True
            snake.boost_end_time = time.time() + 5  # Boost lasts for 5 seconds
        elif self.fruit_type == 'lengthen':
            snake.lengthen()  # Make the snake 4 spaces longer

