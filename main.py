import pygame
import random
import time
from snake import Snake
from fruit import Fruit
from  db_manager import *
from constants import WIDTH, HEIGHT, BLOCK_SIZE, screen, clock, font, input_font, screen

pygame.display.set_caption("Snake Game with Two Players")

def main():
    
    display_player_results()

    name1, name2 = get_player_names()

    snake1 = Snake(GREEN, (100, 100), {'up': pygame.K_UP, 'down': pygame.K_DOWN, 'left': pygame.K_LEFT, 'right': pygame.K_RIGHT}, name1)
    snake2 = Snake(PURPLE, (400, 100), {'up': pygame.K_w, 'down': pygame.K_s, 'left': pygame.K_a, 'right': pygame.K_d}, name2)

    fruits = [Fruit(random.choice(['normal', 'boost', 'lengthen'])) for _ in range(5)]
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        
        snake1.key_action(keys)
        snake2.key_action(keys)

        snake1.move()
        snake2.move()
        
        if snake1.check_collision(snake2):
            update_player_stats(name2, 'win', snake2.get_score())
            update_player_stats(name1, 'loss', snake1.get_score())
            display_winner_screen(name2, name1, snake2.get_score(), snake1.get_score())
            running = False

        elif snake2.check_collision(snake1):
            update_player_stats(name1, 'win', snake1.get_score())
            update_player_stats(name2, 'loss', snake2.get_score())
            display_winner_screen(name1, name2, snake1.get_score(), snake2.get_score())
            running = False

        for fruit in fruits[:]:
            if snake1.body[0] == (fruit.x, fruit.y):
                fruit.effect(snake1)
                fruits.remove(fruit) 
                fruits.append(Fruit(random.choice(['normal', 'boost', 'lengthen'])))

            if snake2.body[0] == (fruit.x, fruit.y):
                fruit.effect(snake2)
                fruits.remove(fruit)
                fruits.append(Fruit(random.choice(['normal', 'boost', 'lengthen'])))

       
        screen.fill(BLACK)
        snake1.draw(screen)
        snake2.draw(screen)

        for fruit in fruits:
            fruit.draw(screen)

  
        score_text1 = font.render(f"{name1}: {snake1.get_score()}", True, WHITE)
        score_text2 = font.render(f"{name2}: {snake2.get_score()}", True, WHITE)
        screen.blit(score_text1, (10, 10))
        screen.blit(score_text2, (WIDTH - 200, 10))

        pygame.display.flip()
        clock.tick(snake1.apply_boost())


    pygame.quit()

if __name__ == "__main__":
    main()

