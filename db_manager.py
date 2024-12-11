import pymongo
import pygame
from pymongo import MongoClient
from constants import WIDTH, HEIGHT, BLACK, WHITE, GREEN, RED, YELLOW, BLUE, PURPLE, BLOCK_SIZE, clock, font, input_font, screen

client = MongoClient("mongodb://localhost:27017/")
db = client["snake_game_db"]
players_collection = db["players"]  

def update_player_stats(name, result, score):
    try:
        # Check if player exists in the database
        player = players_collection.find_one({"name": name})

        if player:
            # Player exists: update the player's stats
            if result == "win":
                players_collection.update_one(
                    {"name": name},
                    {"$inc": {"wins": 1, "total_score": score}}
                )
            elif result == "loss":
                players_collection.update_one(
                    {"name": name},
                    {"$inc": {"losses": 1, "total_score": score}}
                )
        else:
            # Player doesn't exist, create a new entry based on the result
            if result == "win":
                players_collection.insert_one({
                    "name": name,
                    "wins": 1,
                    "losses": 0,
                    "total_score": score
                })
            elif result == "loss":
                players_collection.insert_one({
                    "name": name,
                    "wins": 0,
                    "losses": 1,
                    "total_score": score
                })

        print(f"Successfully updated stats for {name}.")
    except Exception as e:
        print(f"Error updating player stats for {name}: {e}")


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

    # After names are entered, check and insert into the database if not already present
    for name in names:
        if not players_collection.find_one({"name": name}):  # Check if player exists
            players_collection.insert_one({
                "name": name,
                "wins": 0,
                "losses": 0,
                "total_score": 0
            })

    return names[0], names[1]

def display_player_results():
    running = True
    while running:
        screen.fill(BLACK)

        title_text = font.render("Player Stats", True, WHITE)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 50))

        players = players_collection.find().sort("wins", -1)  # Sort by wins descending
        y_offset = 150  # Starting Y position for player stats

        for player in players:
            player_stats = f"{player['name']} - Wins: {player['wins']}, Losses: {player['losses']}, Total Score: {player['total_score']}"
            stats_text = input_font.render(player_stats, True, WHITE)
            screen.blit(stats_text, (50, y_offset))
            y_offset += 40  # Increment Y position for the next player

        instructions_text = font.render("Press ENTER to start the game", True, YELLOW)
        screen.blit(instructions_text, (WIDTH // 2 - instructions_text.get_width() // 2, HEIGHT - 100))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:  # ENTER key stops the loop
                running = False  # Exit the loop to start the game

        pygame.display.flip()
        clock.tick(30)  # Limit FPS for smooth rendering

