import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 1000, 1000

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)  # Color for boost fruit
BLUE = (0, 0, 255)  # Color for lengthening fruit
PURPLE = (128, 0, 128)  # Color for second snake

# Block size
BLOCK_SIZE = 20

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game with Two Players")

# Clock for controlling the game speed
clock = pygame.time.Clock()

# Font for score and text
font = pygame.font.Font(None, 36)
input_font = pygame.font.Font(None, 28)

# Snake Class
class Snake:
    def __init__(self, color, start_pos, controls):
        self.body = [start_pos, (start_pos[0] - BLOCK_SIZE, start_pos[1]), (start_pos[0] - 2 * BLOCK_SIZE, start_pos[1])]
        self.direction = (BLOCK_SIZE, 0)  # Initial direction (moving right)
        self.color = color
        self.controls = controls  # Dictionary for controls
        self.speed_boosted = False  # Flag for speed boost
        self.boost_end_time = 0  # Time when the boost should end

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
        """Add a new segment to the snake."""
        self.body.append(self.body[-1])  # Duplicate the last segment

    def lengthen(self):
        """Increase the snake's length by 4 segments."""
        self.body += [self.body[-1]] * 4

    def check_collision(self, other_snake=None):
        """Check for collision with itself or the other snake."""
        head_x, head_y = self.body[0]
        # Self collision
        if self.body[0] in self.body[1:]:
            return True
        # Collision with the other snake
        if other_snake and self.body[0] in other_snake.body:
            return True
        return False

    def change_direction(self, new_direction):
        """Change the direction of the snake."""
        if (
            (new_direction[0] != -self.direction[0]) or
            (new_direction[1] != -self.direction[1])
        ):
            self.direction = new_direction

    def draw(self, surface):
        """Draw the snake on the screen."""
        for segment in self.body:
            pygame.draw.rect(surface, self.color, pygame.Rect(segment[0], segment[1], BLOCK_SIZE, BLOCK_SIZE))

    def apply_boost(self):
        """Apply speed boost for 5 seconds."""
        if self.speed_boosted and time.time() > self.boost_end_time:
            self.speed_boosted = False
            return 10  # Return normal speed
        elif self.speed_boosted:
            return 20  # Return increased speed
        else:
            return 10  # Return normal speed

# Fruit Class
class Fruit:
    def __init__(self, fruit_type):
        self.fruit_type = fruit_type
        self.x = random.randint(0, (WIDTH // BLOCK_SIZE) - 1) * BLOCK_SIZE
        self.y = random.randint(0, (HEIGHT // BLOCK_SIZE) - 1) * BLOCK_SIZE
        self.color = self.get_color()

    def get_color(self):
        """Return the color of the fruit based on its type."""
        if self.fruit_type == 'normal':
            return RED
        elif self.fruit_type == 'boost':
            return YELLOW
        elif self.fruit_type == 'lengthen':
            return BLUE

    def draw(self, surface):
        """Draw the fruit on the screen."""
        pygame.draw.rect(surface, self.color, pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE))

    def effect(self, snake):
        """Apply the effect of the fruit to the snake."""
        if self.fruit_type == 'normal':
            snake.grow()  # Grow the snake
        elif self.fruit_type == 'boost':
            snake.speed_boosted = True
            snake.boost_end_time = time.time() + 5  # Boost lasts for 5 seconds
        elif self.fruit_type == 'lengthen':
            snake.lengthen()  # Make the snake 4 spaces longer

# Start screen for player name input
def get_player_names():
    input_active = [True, True]  # Track if player1 and player2 are still typing
    names = ['', '']  # Empty names for both players
    current_player = 0  # 0 for player1, 1 for player2
    while input_active[0] or input_active[1]:
        screen.fill(BLACK)
        # Draw instructions and current name being typed
        title_text = font.render("Enter Player 1 Name (Press Enter to confirm)", True, WHITE)
        screen.blit(title_text, (50, 100))
        player_name_text = input_font.render(names[0], True, WHITE)
        screen.blit(player_name_text, (50, 150))

        if current_player == 1:
            title_text2 = font.render("Enter Player 2 Name (Press Enter to confirm)", True, WHITE)
            screen.blit(title_text2, (50, 250))
            player_name_text2 = input_font.render(names[1], True, WHITE)
            screen.blit(player_name_text2, (50, 300))

        # Event loop for typing player names
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Switch to the next player when 'Enter' is pressed
                    if current_player == 0 and names[0] != '':
                        current_player = 1
                    elif current_player == 1 and names[1] != '':
                        input_active[0] = False
                        input_active[1] = False
                elif event.key == pygame.K_BACKSPACE:  # Remove last character
                    names[current_player] = names[current_player][:-1]
                else:
                    names[current_player] += event.unicode  # Add typed character

        pygame.display.flip()
        clock.tick(30)  # Limit FPS for smooth input handling

    return names[0], names[1]

# Main game loop
def main():
    # Get player names
    player1_name, player2_name = get_player_names()
    
    # Create two snakes with different controls and colors
    snake1 = Snake(GREEN, (100, 100), {'up': pygame.K_UP, 'down': pygame.K_DOWN, 'left': pygame.K_LEFT, 'right': pygame.K_RIGHT})
    snake2 = Snake(PURPLE, (400, 100), {'up': pygame.K_w, 'down': pygame.K_s, 'left': pygame.K_a, 'right': pygame.K_d})

    # Create multiple fruits
    fruits = [Fruit(random.choice(['normal', 'boost', 'lengthen'])) for _ in range(5)]  # 5 fruits on the board
    score1, score2 = 0, 0
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Control snake1 (arrow keys)
        keys = pygame.key.get_pressed()
        if keys[snake1.controls['up']]:
            snake1.change_direction((0, -BLOCK_SIZE))
        if keys[snake1.controls['down']]:
            snake1.change_direction((0, BLOCK_SIZE))
        if keys[snake1.controls['left']]:
            snake1.change_direction((-BLOCK_SIZE, 0))
        if keys[snake1.controls['right']]:
            snake1.change_direction((BLOCK_SIZE, 0))

        # Control snake2 (WASD)
        if keys[snake2.controls['up']]:
            snake2.change_direction((0, -BLOCK_SIZE))
        if keys[snake2.controls['down']]:
            snake2.change_direction((0, BLOCK_SIZE))
        if keys[snake2.controls['left']]:
            snake2.change_direction((-BLOCK_SIZE, 0))
        if keys[snake2.controls['right']]:
            snake2.change_direction((BLOCK_SIZE, 0))

        # Move snakes
        snake1.move()
        snake2.move()

        # Check for collisions
        if snake1.check_collision(snake2):
            running = False
        if snake2.check_collision(snake1):
            running = False

        # Check if snakes eat any fruit
        for fruit in fruits[:]:
            if snake1.body[0] == (fruit.x, fruit.y):
                fruit.effect(snake1)
                score1 += 1
                fruits.remove(fruit)  # Remove the fruit after it is eaten
                fruits.append(Fruit(random.choice(['normal', 'boost', 'lengthen'])))  # Spawn a new fruit

            if snake2.body[0] == (fruit.x, fruit.y):
                fruit.effect(snake2)
                score2 += 1
                fruits.remove(fruit)
                fruits.append(Fruit(random.choice(['normal', 'boost', 'lengthen'])))

        # Draw everything
        screen.fill(BLACK)
        snake1.draw(screen)
        snake2.draw(screen)

        for fruit in fruits:
            fruit.draw(screen)

        # Display scores
        score_text1 = font.render(f"{player1_name}: {score1}", True, WHITE)
        score_text2 = font.render(f"{player2_name}: {score2}", True, WHITE)
        screen.blit(score_text1, (10, 10))
        screen.blit(score_text2, (WIDTH - 200, 10))

        pygame.display.flip()
        clock.tick(snake1.apply_boost())  # Control speed based on boost status

    pygame.quit()

if __name__ == "__main__":
    main()

