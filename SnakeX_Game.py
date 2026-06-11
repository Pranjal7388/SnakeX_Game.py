import pygame
import random
import os

# ------------------ INIT ------------------
pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 800, 600
BLOCK = 20

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🐍 Snake Game")

clock = pygame.time.Clock()

# ------------------ COLORS ------------------
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
GREEN = (0, 255, 0)
BLUE = (40, 120, 200)

# ------------------ FONT ------------------
font = pygame.font.SysFont("Arial", 28)

# ------------------ SOUND ------------------
eat_sound = pygame.mixer.Sound("sounds/eat.wav")
gameover_sound = pygame.mixer.Sound("sounds/gameover.wav")

pygame.mixer.music.load("sounds/bg.mp3")
pygame.mixer.music.set_volume(0.4)
pygame.mixer.music.play(-1)

# ------------------ HIGH SCORE ------------------
if not os.path.exists("highscore.txt"):
    with open("highscore.txt", "w") as f:
        f.write("0")

def get_high():
    return int(open("highscore.txt").read())

def save_high(score):
    if score > get_high():
        open("highscore.txt", "w").write(str(score))

# ------------------ DRAW TEXT ------------------
def draw_text(text, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

# ------------------ FOOD ------------------
def spawn_food(snake):
    while True:
        fx = random.randrange(0, WIDTH, BLOCK)
        fy = random.randrange(0, HEIGHT, BLOCK)
        if [fx, fy] not in snake:
            return fx, fy

# ------------------ GAME LOOP ------------------
def game():
    while True:  # restart loop

        x, y = WIDTH // 2, HEIGHT // 2
        dx, dy = 0, 0

        snake = []
        length = 1

        food_x, food_y = spawn_food(snake)

        score = 0
        high = get_high()

        game_over = False
        running = True

        while running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT and dx == 0:
                        dx, dy = -BLOCK, 0
                    elif event.key == pygame.K_RIGHT and dx == 0:
                        dx, dy = BLOCK, 0
                    elif event.key == pygame.K_UP and dy == 0:
                        dx, dy = 0, -BLOCK
                    elif event.key == pygame.K_DOWN and dy == 0:
                        dx, dy = 0, BLOCK

            if not game_over:
                x += dx
                y += dy

                # Wall collision
                if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT:
                    gameover_sound.play()
                    game_over = True

                screen.fill(BLACK)

                # Draw food
                pygame.draw.rect(screen, GREEN, (food_x, food_y, BLOCK, BLOCK))

                # Snake
                head = [x, y]
                snake.append(head)

                if len(snake) > length:
                    del snake[0]

                # Self collision
                if head in snake[:-1]:
                    gameover_sound.play()
                    game_over = True

                for part in snake:
                    pygame.draw.rect(screen, WHITE, (part[0], part[1], BLOCK, BLOCK))

                # Eat food
                if x == food_x and y == food_y:
                    eat_sound.play()
                    food_x, food_y = spawn_food(snake)
                    length += 1
                    score += 10

                    if score > high:
                        high = score

                # Score display
                draw_text(f"Score: {score}", GREEN, 10, 10)
                draw_text(f"High: {high}", RED, WIDTH - 160, 10)

            else:
                save_high(score)

                screen.fill(BLUE)
                draw_text("GAME OVER", RED, WIDTH // 2 - 100, HEIGHT // 2 - 40)
                draw_text("Press C to Restart", WHITE, WIDTH // 2 - 130, HEIGHT // 2)
                draw_text("Press Q to Quit", WHITE, WIDTH // 2 - 110, HEIGHT // 2 + 40)

                keys = pygame.key.get_pressed()
                if keys[pygame.K_c]:
                    return
                if keys[pygame.K_q]:
                    pygame.quit()
                    exit()

            pygame.display.update()
            clock.tick(10 + score // 20)

# ------------------ RUN ------------------
game()