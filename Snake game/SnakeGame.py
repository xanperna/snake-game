import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the screen
WIDTH, HEIGHT = 1200, 800
CELL_SIZE = 20
GRID_WIDTH, GRID_HEIGHT = WIDTH // CELL_SIZE, HEIGHT // CELL_SIZE
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake Game')

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Snake class
class Snake:
    def __init__(self):
        self.body = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = random.choice([pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT])
        self.grow = False

    def move(self):
        head = self.body[0]
        x, y = head
        if self.direction == pygame.K_UP:
            y -= 1
        elif self.direction == pygame.K_DOWN:
            y += 1
        elif self.direction == pygame.K_LEFT:
            x -= 1
        elif self.direction == pygame.K_RIGHT:
            x += 1
        self.body.insert(0, (x, y))
        if not self.grow:
            self.body.pop()
        else:
            self.grow = False

    def grow_snake(self):
        self.grow = True

    def draw(self):
        for segment in self.body:
            pygame.draw.rect(screen, GREEN, (segment[0] * CELL_SIZE, segment[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

# Food class
class Food:
    def __init__(self):
        self.position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))

    def draw(self):
        pygame.draw.rect(screen, RED, (self.position[0] * CELL_SIZE, self.position[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

# Start screen function
def show_start_screen():
    screen.fill(BLACK)
    font = pygame.font.Font(None, 36)
    text = font.render("Snake Game", True, WHITE)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    screen.blit(text, text_rect)
    font = pygame.font.Font(None, 24)
    controls_text = [
        "Use arrow keys to control the snake",
        "Press any key to start"
    ]
    for i, line in enumerate(controls_text):
        line_text = font.render(line, True, WHITE)
        line_rect = line_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + i * 30))
        screen.blit(line_text, line_rect)
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                waiting = False

# Main function
def main():
    clock = pygame.time.Clock()
    snake = Snake()
    food = Food()
    running = True
    game_over = False

    show_start_screen()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake.direction != pygame.K_DOWN:
                    snake.direction = pygame.K_UP
                elif event.key == pygame.K_DOWN and snake.direction != pygame.K_UP:
                    snake.direction = pygame.K_DOWN
                elif event.key == pygame.K_LEFT and snake.direction != pygame.K_RIGHT:
                    snake.direction = pygame.K_LEFT
                elif event.key == pygame.K_RIGHT and snake.direction != pygame.K_LEFT:
                    snake.direction = pygame.K_RIGHT
                elif event.key == pygame.K_ESCAPE:  # Restart the game when Escape is pressed
                    main()

        if not game_over:
            # Move snake
            snake.move()

            # Check for collision with food
            if snake.body[0] == food.position:
                snake.grow_snake()
                food = Food()

            # Check for collision with walls
            if snake.body[0][0] < 0 or snake.body[0][0] >= GRID_WIDTH or snake.body[0][1] < 0 or snake.body[0][1] >= GRID_HEIGHT:
                game_over = True

            # Check for collision with itself
            if len(snake.body) != len(set(snake.body)):
                game_over = True

        # Clear the screen
        screen.fill(BLACK)

        # Draw snake and food
        snake.draw()
        food.draw()

        if game_over:
            # Display game over text
            font = pygame.font.Font(None, 36)
            text = font.render("Game Over. Press Escape to restart.", True, WHITE)
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(text, text_rect)

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(10)

    pygame.quit()

if __name__ == '__main__':
    main()
