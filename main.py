import pygame
import sys
import random

# Pygame Init
pygame.init()

# Screen Dimensions
WIDTH, HEIGHT = 450, 750
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ghost Room")

# Colors
DARK_RED = (40, 5, 10)
LIGHT_RED = (180, 20, 30)
GOLD = (255, 215, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (30, 200, 50)

# Game Variables
player_name = ""
game_state = "NAME_INPUT"  # States: NAME_INPUT, PLAYING, WINNER
current_room = 1
max_rooms = 50

# Key properties
key_size = 25
key_x = 0
key_y = 0

def spawn_key():
    global key_x, key_y
    key_x = random.randint(50, WIDTH - 50)
    key_y = random.randint(80, 250)

# Font Setup
font_small = pygame.font.SysFont("arial", 22)
font_large = pygame.font.SysFont("arial", 36)

# Main Loop
clock = pygame.time.Clock()

while True:
    screen.fill(DARK_RED)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # State 1: Name Input
        if game_state == "NAME_INPUT":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and len(player_name.strip()) > 0:
                    game_state = "PLAYING"
                    spawn_key()
                elif event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]
                else:
                    if len(player_name) < 12 and event.unicode.isalnum():
                        player_name += event.unicode

        # State 2: Key Touch Check
        elif game_state == "PLAYING":
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if key_x <= mx <= key_x + key_size and key_y <= my <= key_y + key_size:
                    if current_room < max_rooms:
                        current_room += 1
                        spawn_key()
                    else:
                        game_state = "WINNER"

    # --- RENDERING ---

    if game_state == "NAME_INPUT":
        # Game Header Name
        game_title = font_large.render("GHOST ROOM", True, LIGHT_RED)
        screen.blit(game_title, (WIDTH//2 - game_title.get_width()//2, 120))

        # Input Prompt
        title = font_small.render("Enter Player Name:", True, GOLD)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 200))

        # Input Box
        pygame.draw.rect(screen, BLACK, (50, 250, 350, 50), border_radius=10)
        pygame.draw.rect(screen, LIGHT_RED, (50, 250, 350, 50), 2, border_radius=10)

        name_text = font_small.render(player_name, True, WHITE)
        screen.blit(name_text, (65, 262))

        instruction = font_small.render("Press ENTER / OK to Start", True, WHITE)
        screen.blit(instruction, (WIDTH//2 - instruction.get_width()//2, 330))

    elif game_state == "PLAYING":
        # Room Frame
        pygame.draw.rect(screen, BLACK, (30, 60, WIDTH-60, HEIGHT-100), 3)
        
        # Room Info
        info_text = font_small.render(f"Ghost Room: {current_room}/{max_rooms} | Player: {player_name}", True, GOLD)
        screen.blit(info_text, (20, 20))

        # Hanging String & Key
        pygame.draw.line(screen, WHITE, (key_x + key_size//2, 60), (key_x + key_size//2, key_y), 2)
        pygame.draw.circle(screen, GOLD, (key_x + key_size//2, key_y + 6), 8, 2)
        pygame.draw.rect(screen, GOLD, (key_x + key_size//2 - 2, key_y + 12, 4, 12))
        pygame.draw.rect(screen, GOLD, (key_x + key_size//2, key_y + 18, 5, 3))

    elif game_state == "WINNER":
        win_title = font_large.render("GHOST ROOM ESCAPED!", True, GOLD)
        screen.blit(win_title, (WIDTH//2 - win_title.get_width()//2, 120))

        congrats = font_small.render(f"Congratulations {player_name}!", True, WHITE)
        screen.blit(congrats, (WIDTH//2 - congrats.get_width()//2, 180))

        # Winner Flag
        pygame.draw.rect(screen, WHITE, (180, 240, 8, 220))
        pygame.draw.polygon(screen, GREEN, [(188, 240), (280, 275), (188, 310)])
        
        win_msg = font_small.render("You passed all 50 Ghost Rooms!", True, GOLD)
        screen.blit(win_msg, (WIDTH//2 - win_msg.get_width()//2, 500))

    pygame.display.update()
    clock.tick(30)
