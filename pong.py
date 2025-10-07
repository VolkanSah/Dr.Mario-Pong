import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
VIRUS_COLORS = [RED, YELLOW, BLUE] 

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Paddle parameters
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 100
PADDLE_SPEED = 10

# Ball parameters
BALL_SIZE = 10
BALL_SPEED_X = 5
BALL_SPEED_Y = 5
BALL_COLOR = random.choice(VIRUS_COLORS) 

# Virus parameters
VIRUS_SIZE = 30
VIRUS_COUNT = 10 

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dr. Mario Pong")

# Font for the score
font = pygame.font.Font(None, 36)

# Global score variable
score = 0

# Paddle Class
class Paddle:
    def __init__(self, x, y, color):
        self.rect = pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.color = color
    
    def move(self, y_change):
        self.rect.y += y_change
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
    
    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)

# Virus Class
class Virus:
    def __init__(self, x, y, color):
        self.rect = pygame.Rect(x, y, VIRUS_SIZE, VIRUS_SIZE)
        self.color = color
    
    def draw(self):
        pygame.draw.circle(screen, self.color, self.rect.center, VIRUS_SIZE // 2)

# Ball Class
class Ball:
    def __init__(self, x, y, color):
        self.rect = pygame.Rect(x, y, BALL_SIZE, BALL_SIZE)
        self.speed_x = BALL_SPEED_X
        self.speed_y = BALL_SPEED_Y
        self.color = color
    
    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        
        if self.rect.top <= 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.speed_y *= -1
    
    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)
        
    def check_paddle_collision(self, paddle1, paddle2):
        if self.rect.colliderect(paddle1.rect) or self.rect.colliderect(paddle2.rect):
            self.speed_x *= -1

    def check_virus_collision(self, viruses):
        global score
        collided_viruses = self.rect.collidelistall([v.rect for v in viruses])
        
        if collided_viruses:
            self.speed_x *= -1
            
            viruses_to_remove = []
            
            for index in sorted(collided_viruses, reverse=True):
                virus = viruses[index]
                if self.color == virus.color:
                    score += 10 
                    viruses_to_remove.append(index)
                    
            for index in viruses_to_remove:
                viruses.pop(index)

            self.color = random.choice(VIRUS_COLORS)
            self.speed_y *= -1
            
            return True 
        return False 

# Initialize Viruses
def create_viruses():
    viruses = []
    for _ in range(VIRUS_COUNT):
        x = random.randint(SCREEN_WIDTH // 4, SCREEN_WIDTH * 3 // 4 - VIRUS_SIZE)
        y = random.randint(0, SCREEN_HEIGHT - VIRUS_SIZE)
        color = random.choice(VIRUS_COLORS)
        viruses.append(Virus(x, y, color))
    return viruses

# Initialize Paddles, Ball, and Viruses
paddle1 = Paddle(30, (SCREEN_HEIGHT - PADDLE_HEIGHT) // 2, YELLOW)
paddle2 = Paddle(SCREEN_WIDTH - 40, (SCREEN_HEIGHT - PADDLE_HEIGHT) // 2, BLUE)
ball = Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, BALL_COLOR)
viruses = create_viruses()

# Function to draw the score
def draw_score():
    score_text = font.render(f"Viruses Destroyed: {score}", True, WHITE)
    screen.blit(score_text, (SCREEN_WIDTH - score_text.get_width() - 10, 10))

# Game Loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Controls: W/S for Paddle 1, UP/DOWN for Paddle 2
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        paddle1.move(-PADDLE_SPEED)
    if keys[pygame.K_s]:
        paddle1.move(PADDLE_SPEED)
    
    # Paddle 2 manual control
    if keys[pygame.K_UP]:
        paddle2.move(-PADDLE_SPEED)
    if keys[pygame.K_DOWN]:
        paddle2.move(PADDLE_SPEED)
    
    # Game Logic
    ball.move()
    ball.check_paddle_collision(paddle1, paddle2)
    ball.check_virus_collision(viruses)
    
    # Check if all viruses are destroyed
    if not viruses:
        print(f"You won! Total score: {score}")
        running = False 

    # Drawing
    screen.fill(BLACK)
    paddle1.draw()
    paddle2.draw()
    ball.draw()
    
    for virus in viruses:
        virus.draw()
        
    draw_score()
    
    # Reset ball if it goes off screen
    if ball.rect.left <= 0 or ball.rect.right >= SCREEN_WIDTH:
        ball = Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, random.choice(VIRUS_COLORS))
        paddle1.rect.centery = (SCREEN_HEIGHT // 2)
        paddle2.rect.centery = (SCREEN_HEIGHT // 2)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
