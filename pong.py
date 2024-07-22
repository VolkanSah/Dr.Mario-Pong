import pygame
import sys

# Initialisiere Pygame
pygame.init()

# Farben
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Bildschirmgröße
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Paddle Parameter
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 100
PADDLE_SPEED = 10

# Ball Parameter
BALL_SIZE = 10
BALL_SPEED_X = 5
BALL_SPEED_Y = 5

# Bildschirm einrichten
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pong")

# Paddle Klasse
class Paddle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)
    
    def move(self, y_change):
        self.rect.y += y_change
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
    
    def draw(self):
        pygame.draw.rect(screen, WHITE, self.rect)

# Ball Klasse
class Ball:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, BALL_SIZE, BALL_SIZE)
        self.speed_x = BALL_SPEED_X
        self.speed_y = BALL_SPEED_Y
    
    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        
        if self.rect.top <= 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.speed_y *= -1
        
        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            self.speed_x *= -1
    
    def draw(self):
        pygame.draw.rect(screen, WHITE, self.rect)
    
    def check_collision(self, paddle1, paddle2):
        if self.rect.colliderect(paddle1.rect) or self.rect.colliderect(paddle2.rect):
            self.speed_x *= -1

# Initialisiere Paddles und Ball
paddle1 = Paddle(30, (SCREEN_HEIGHT - PADDLE_HEIGHT) // 2)
paddle2 = Paddle(SCREEN_WIDTH - 40, (SCREEN_HEIGHT - PADDLE_HEIGHT) // 2)
ball = Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# Spiel-Loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        paddle1.move(-PADDLE_SPEED)
    if keys[pygame.K_s]:
        paddle1.move(PADDLE_SPEED)
    if keys[pygame.K_UP]:
        paddle2.move(-PADDLE_SPEED)
    if keys[pygame.K_DOWN]:
        paddle2.move(PADDLE_SPEED)
    
    ball.move()
    ball.check_collision(paddle1, paddle2)
    
    screen.fill(BLACK)
    paddle1.draw()
    paddle2.draw()
    ball.draw()
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
