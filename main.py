import pygame
import random

# Initialize pygame
pygame.init()

# Game constants
WIDTH, HEIGHT = 400, 600
GRAVITY = 0.5
FLAP_STRENGTH = -8
PIPE_GAP = 150
PIPE_WIDTH = 70
PIPE_SPEED = 3

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
BLUE = (0, 100, 200)

# Load assets
pygame.font.init()
FONT = pygame.font.Font(None, 36)

# Create window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Crypto")

# Bird (crypto coin)
class Bird:
    def __init__(self):
        self.x = 50
        self.y = HEIGHT // 2
        self.velocity = 0
    
    def flap(self):
        self.velocity = FLAP_STRENGTH
    
    def move(self):
        self.velocity += GRAVITY
        self.y += self.velocity
    
    def draw(self):
        pygame.draw.circle(screen, BLUE, (self.x, int(self.y)), 15)

# Pipe
class Pipe:
    def __init__(self, x):
        self.x = x
        self.height = random.randint(100, HEIGHT - PIPE_GAP - 100)
    
    def move(self):
        self.x -= PIPE_SPEED
    
    def draw(self):
        pygame.draw.rect(screen, GREEN, (self.x, 0, PIPE_WIDTH, self.height))
        pygame.draw.rect(screen, GREEN, (self.x, self.height + PIPE_GAP, PIPE_WIDTH, HEIGHT))
    
    def collide(self, bird):
        if bird.x + 15 > self.x and bird.x - 15 < self.x + PIPE_WIDTH:
            if bird.y - 15 < self.height or bird.y + 15 > self.height + PIPE_GAP:
                return True
        return False

# Game loop
def game():
    clock = pygame.time.Clock()
    bird = Bird()
    pipes = [Pipe(WIDTH + i * 200) for i in range(3)]
    score = 0
    running = True
    
    while running:
        screen.fill(WHITE)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                bird.flap()
        
        bird.move()
        bird.draw()
        
        for pipe in pipes:
            pipe.move()
            pipe.draw()
            
            if pipe.collide(bird):
                running = False
            
            if pipe.x + PIPE_WIDTH < 0:
                pipes.remove(pipe)
                pipes.append(Pipe(WIDTH))
                score += 1
        
        if bird.y > HEIGHT or bird.y < 0:
            running = False
        
        score_text = FONT.render(f"Score: {score}", True, (0, 0, 0))
        screen.blit(score_text, (10, 10))
        
        pygame.display.update()
        clock.tick(30)
    
    pygame.quit()

if __name__ == "__main__":
    game()
