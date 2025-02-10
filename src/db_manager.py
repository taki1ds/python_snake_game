"""Database management for player stats and UI components."""
from typing import Tuple
import pygame
from pymongo import MongoClient
from .constants import (
    WIDTH, HEIGHT, BLACK, WHITE, GREEN, RED, YELLOW, BLUE, PURPLE,
    BLOCK_SIZE, CLOCK, FONT, INPUT_FONT, SCREEN
)

# MongoDB setup
CLIENT = MongoClient("mongodb://localhost:27017/")
DB = CLIENT["snake_game_db"]
PLAYERS_COLLECTION = DB["players"]

def update_player_stats(name: str, result: str, score: int) -> None:
    """Update player stats in the database based on game result."""
    try:
        player = PLAYERS_COLLECTION.find_one({"name": name})
        update_data = {"$inc": {"total_score": score}}

        if result == "win":
            update_data["$inc"]["wins"] = 1
        elif result == "loss":
            update_data["$inc"]["losses"] = 1

        if player:
            PLAYERS_COLLECTION.update_one({"name": name}, update_data)
        else:
            new_player = {
                "name": name,
                "wins": 1 if result == "win" else 0,
                "losses": 1 if result == "loss" else 0,
                "total_score": score
            }
            PLAYERS_COLLECTION.insert_one(new_player)

    except Exception as e:
        print(f"Error updating stats for {name}: {e}")

def get_player_names() -> Tuple[str, str]:
    """Get player names through GUI input."""
    input_active = [True, True]
    names = ['', '']
    current_player = 0

    while any(input_active):
        SCREEN.fill(BLACK)
        title_text = FONT.render("Enter Player 1 Name (Press Enter to confirm)", True, WHITE)
        SCREEN.blit(title_text, (50, 100))
        SCREEN.blit(INPUT_FONT.render(names[0], True, WHITE), (50, 150))

        if current_player == 1:
            title_text = FONT.render("Enter Player 2 Name (Press Enter to confirm)", True, WHITE)
            SCREEN.blit(title_text, (50, 250))
            SCREEN.blit(INPUT_FONT.render(names[1], True, WHITE), (50, 300))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if names[current_player].strip():
                        current_player = 1 - current_player
                        input_active[current_player] = False
                elif event.key == pygame.K_BACKSPACE:
                    names[current_player] = names[current_player][:-1]
                else:
                    names[current_player] += event.unicode

        pygame.display.flip()
        CLOCK.tick(30)

    for name in names:
        if not PLAYERS_COLLECTION.find_one({"name": name}):
            PLAYERS_COLLECTION.insert_one({
                "name": name,
                "wins": 0,
                "losses": 0,
                "total_score": 0
            })

    return names[0], names[1]

def display_player_results() -> None:
    """Display leaderboard with scrolling functionality."""
    scroll_offset = 0
    running = True

    while running:
        SCREEN.fill(BLACK)
        SCREEN.blit(FONT.render("Player Stats", True, WHITE), (WIDTH//2-100, 50))
        
        players = list(PLAYERS_COLLECTION.find().sort("wins", -1))
        y_pos = 150 - scroll_offset

        for player in players:
            text = INPUT_FONT.render(
                f"{player['name']}: Wins {player['wins']} Losses {player['losses']} Score {player['total_score']}",
                True, WHITE
            )
            SCREEN.blit(text, (50, y_pos))
            y_pos += 40

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    running = False
                elif event.key == pygame.K_UP:
                    scroll_offset = max(0, scroll_offset - 20)
                elif event.key == pygame.K_DOWN:
                    scroll_offset += 20

        pygame.display.flip()
        CLOCK.tick(30)

def display_winner_screen(winner: str, loser: str, win_score: int, lose_score: int) -> None:
    """Display endgame results screen."""
    running = True
    while running:
        SCREEN.fill(BLACK)
        SCREEN.blit(FONT.render(f"{winner} WINS!", True, YELLOW), (WIDTH//2-100, HEIGHT//3))
        SCREEN.blit(FONT.render(f"{winner}: {win_score}", True, WHITE), (WIDTH//2-100, HEIGHT//2))
        SCREEN.blit(FONT.render(f"{loser}: {lose_score}", True, WHITE), (WIDTH//2-100, HEIGHT//2+50))
        SCREEN.blit(FONT.render("Press ENTER to continue", True, GREEN), (WIDTH//2-150, HEIGHT-100))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                running = False

        pygame.display.flip()
        CLOCK.tick(30)
