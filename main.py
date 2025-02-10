"""Main game loop and setup."""
import pygame
import random
from src.snake import Snake
from src.fruit import Fruit
from src.db_manager import update_player_stats, display_player_results, get_player_names, display_winner_screen
from src.constants import WIDTH, HEIGHT, GREEN, PURPLE, BLACK, WHITE, SCREEN, CLOCK, FONT

def main() -> None:
    """Main game execution loop."""
    pygame.init()
    pygame.display.set_caption("Snake Dual")

    display_player_results()
    p1_name, p2_name = get_player_names()

    snake1 = Snake(GREEN, (200, 200), {'up': pygame.K_UP, 'down': pygame.K_DOWN, 
                                      'left': pygame.K_LEFT, 'right': pygame.K_RIGHT}, p1_name)
    snake2 = Snake(PURPLE, (800, 800), {'up': pygame.K_w, 'down': pygame.K_s,
                                       'left': pygame.K_a, 'right': pygame.K_d}, p2_name)
    fruits = [Fruit(random.choice(['normal', 'boost', 'lengthen'])) for _ in range(5)]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        snake1.handle_input(keys)
        snake2.handle_input(keys)

        # Update snake states first
        snake1.update()
        snake2.update()

        # Move snakes according to their speed
        snake1.move()
        snake2.move()

        # Collision checks
        if snake1.check_self_collision() or snake1.check_collision(snake2):
            update_player_stats(p2_name, 'win', snake2.score)
            update_player_stats(p1_name, 'loss', snake1.score)
            display_winner_screen(p2_name, p1_name, snake2.score, snake1.score)
            running = False
        elif snake2.check_self_collision() or snake2.check_collision(snake1):
            update_player_stats(p1_name, 'win', snake1.score)
            update_player_stats(p2_name, 'loss', snake2.score)
            display_winner_screen(p1_name, p2_name, snake1.score, snake2.score)
            running = False

        # Fruit interactions
        for fruit in fruits[:]:
            if (fruit.x, fruit.y) in snake1.body:
                fruit.effect(snake1)
                fruits.remove(fruit)
                fruits.append(Fruit(random.choice(['normal', 'boost', 'lengthen'])))
            elif (fruit.x, fruit.y) in snake2.body:
                fruit.effect(snake2)
                fruits.remove(fruit)
                fruits.append(Fruit(random.choice(['normal', 'boost', 'lengthen'])))

        # Rendering
        SCREEN.fill(BLACK)
        snake1.draw(SCREEN)
        snake2.draw(SCREEN)
        for fruit in fruits:
            fruit.draw(SCREEN)

        # Score display
        SCREEN.blit(FONT.render(f"{p1_name}: {snake1.score}", True, WHITE), (10, 10))
        SCREEN.blit(FONT.render(f"{p2_name}: {snake2.score}", True, WHITE), (WIDTH-200, 10))
        pygame.display.flip()
        CLOCK.tick(20)

    pygame.quit()

if __name__ == "__main__":
    main()
