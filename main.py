import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 300, 600
GRID_SIZE = 30
ROWS, COLS = HEIGHT // GRID_SIZE, WIDTH // GRID_SIZE
FPS = 10

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Tetromino shapes
SHAPES = [
    [[1, 1, 1, 1]],
    [[1, 1, 1], [1]],
    [[1, 1, 1], [0, 0, 1]],
    [[1, 1, 1], [0, 1]],
    [[1, 1, 1], [1, 0]],
    [[1, 1], [1, 1]],
    [[1, 1, 0], [0, 1, 1]],
]

SHAPES_COLORS = [CYAN, MAGENTA, YELLOW, ORANGE, BLUE, GREEN, RED]

# Define the TetrisGame class
class TetrisGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Tetris Game")
        self.clock = pygame.time.Clock()
        self.grid = [[0] * COLS for _ in range(ROWS)]
        self.current_tetromino = self.get_random_tetromino()
        self.current_color = self.get_random_color()
        self.current_position = [0, COLS // 2 - len(self.current_tetromino[0]) // 2]

    def get_random_tetromino(self):
        return random.choice(SHAPES)

    def get_random_color(self):
        return random.choice(SHAPES_COLORS)

    def draw_grid(self):
        for row in range(ROWS):
            for col in range(COLS):
                pygame.draw.rect(self.screen, self.grid[row][col], (col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    def draw_tetromino(self):
        for row in range(len(self.current_tetromino)):
            for col in range(len(self.current_tetromino[0])):
                if self.current_tetromino[row][col] == 1:
                    pygame.draw.rect(self.screen, self.current_color,
                                     ((self.current_position[1] + col) * GRID_SIZE, (self.current_position[0] + row) * GRID_SIZE,
                                      GRID_SIZE, GRID_SIZE))

    def move_tetromino(self, dx, dy):
        new_position = [self.current_position[0] + dy, self.current_position[1] + dx]

        if self.is_valid_position(new_position):
            self.current_position = new_position
        else:
            self.merge_tetromino()
            self.check_lines()
            self.spawn_new_tetromino()

    def rotate_tetromino(self):
        rotated_tetromino = list(zip(*reversed(self.current_tetromino)))
        if self.is_valid_position(self.current_position, rotated_tetromino):
            self.current_tetromino = rotated_tetromino

    def is_valid_position(self, position, tetromino=None):
        tetromino = tetromino or self.current_tetromino

        for row in range(len(tetromino)):
            for col in range(len(tetromino[0])):
                if (
                    tetromino[row][col] == 1
                    and (position[0] + row >= ROWS or position[1] + col < 0 or position[1] + col >= COLS)
                    or (position[0] + row >= 0 and position[1] + col >= 0 and self.grid[position[0] + row][position[1] + col] != 0)
                ):
                    return False
        return True

    def merge_tetromino(self):
        for row in range(len(self.current_tetromino)):
            for col in range(len(self.current_tetromino[0])):
                if self.current_tetromino[row][col] == 1:
                    self.grid[self.current_position[0] + row][self.current_position[1] + col] = self.current_color

    def check_lines(self):
        lines_to_clear = []
        for row in range(ROWS):
            if all(cell != 0 for cell in self.grid[row]):
                lines_to_clear.append(row)

        for line in lines_to_clear:
            self.grid.pop(line)
            self.grid.insert(0, [0] * COLS)

    def spawn_new_tetromino(self):
        self.current_tetromino = self.get_random_tetromino()
        self.current_color = self.get_random_color()
        self.current_position = [0, COLS // 2 - len(self.current_tetromino[0]) // 2]

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.move_tetromino(0, -1)
                    elif event.key == pygame.K_RIGHT:
                        self.move_tetromino(0, 1)
                    elif event.key == pygame.K_DOWN:
                        self.move_tetromino(1, 0)
                    elif event.key == pygame.K_UP:
                        self.rotate_tetromino()

            self.move_tetromino(1, 0)

            self.screen.fill(WHITE)
            self.draw_grid()
            self.draw_tetromino()

            pygame.display.flip()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = TetrisGame()
    game.run()



    


    




              
