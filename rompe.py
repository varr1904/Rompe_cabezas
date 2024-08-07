import pygame
import random
import sys

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
WIDTH, HEIGHT = 400, 400
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rompecabezas Deslizante")

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLUE = (0, 123, 255)

# Fuente
FONT = pygame.font.Font(None, 36)

# Tamaño de las fichas
TILE_SIZE = WIDTH // 3

class Puzzle:
    def __init__(self):
        self.board = self.create_board()
        self.empty_pos = self.find_empty()

    def create_board(self):
        numbers = list(range(1, 9)) + [None]
        random.shuffle(numbers)
        return [numbers[i:i+3] for i in range(0, 9, 3)]

    def find_empty(self):
        for i, row in enumerate(self.board):
            for j, cell in enumerate(row):
                if cell is None:
                    return i, j

    def is_valid_move(self, row, col):
        return (
            (abs(row - self.empty_pos[0]) == 1 and col == self.empty_pos[1]) or
            (abs(col - self.empty_pos[1]) == 1 and row == self.empty_pos[0])
        )

    def move(self, row, col):
        if self.is_valid_move(row, col):
            self.board[self.empty_pos[0]][self.empty_pos[1]] = self.board[row][col]
            self.board[row][col] = None
            self.empty_pos = (row, col)

    def is_solved(self):
        numbers = [cell for row in self.board for cell in row if cell is not None]
        return numbers == list(range(1, 9)) and self.board[2][2] is None

def draw_board(puzzle):
    SCREEN.fill(WHITE)
    for i in range(3):
        for j in range(3):
            if puzzle.board[i][j] is not None:
                pygame.draw.rect(SCREEN, BLUE, (j*TILE_SIZE, i*TILE_SIZE, TILE_SIZE, TILE_SIZE))
                pygame.draw.rect(SCREEN, WHITE, (j*TILE_SIZE, i*TILE_SIZE, TILE_SIZE, TILE_SIZE), 2)
                text = FONT.render(str(puzzle.board[i][j]), True, WHITE)
                text_rect = text.get_rect(center=(j*TILE_SIZE + TILE_SIZE//2, i*TILE_SIZE + TILE_SIZE//2))
                SCREEN.blit(text, text_rect)
    pygame.display.flip()

def animate_move(puzzle, start_pos, end_pos):
    start_x, start_y = start_pos[1] * TILE_SIZE, start_pos[0] * TILE_SIZE
    end_x, end_y = end_pos[1] * TILE_SIZE, end_pos[0] * TILE_SIZE
    distance_x, distance_y = end_x - start_x, end_y - start_y
    steps = 30

    for step in range(steps + 1):
        SCREEN.fill(WHITE)
        for i in range(3):
            for j in range(3):
                if puzzle.board[i][j] is not None:
                    if (i, j) == start_pos:
                        x = start_x + distance_x * step // steps
                        y = start_y + distance_y * step // steps
                    else:
                        x, y = j * TILE_SIZE, i * TILE_SIZE
                    
                    pygame.draw.rect(SCREEN, BLUE, (x, y, TILE_SIZE, TILE_SIZE))
                    pygame.draw.rect(SCREEN, WHITE, (x, y, TILE_SIZE, TILE_SIZE), 2)
                    text = FONT.render(str(puzzle.board[i][j]), True, WHITE)
                    text_rect = text.get_rect(center=(x + TILE_SIZE//2, y + TILE_SIZE//2))
                    SCREEN.blit(text, text_rect)
        
        pygame.display.flip()
        pygame.time.wait(10)

def main():
    puzzle = Puzzle()
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                row, col = y // TILE_SIZE, x // TILE_SIZE
                if puzzle.is_valid_move(row, col):
                    start_pos = (row, col)
                    end_pos = puzzle.empty_pos
                    animate_move(puzzle, start_pos, end_pos)
                    puzzle.move(row, col)

        draw_board(puzzle)

        if puzzle.is_solved():
            font = pygame.font.Font(None, 48)
            text = font.render("¡Felicidades!", True, BLUE)
            text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2))
            SCREEN.blit(text, text_rect)
            pygame.display.flip()
            pygame.time.wait(3000)
            puzzle = Puzzle()

        clock.tick(60)

if __name__ == "__main__":
    main()