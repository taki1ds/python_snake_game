"""Module containing constants and initializations for the game."""
import pygame

# Screen dimensions
WIDTH = 1000
HEIGHT = 1000

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (128, 0, 128)

# Game settings
BLOCK_SIZE = 20

# Initialize Pygame modules
pygame.init()

# Screen and timing
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
CLOCK = pygame.time.Clock()
FONT = pygame.font.Font(None, 36)
INPUT_FONT = pygame.font.Font(None, 28)
