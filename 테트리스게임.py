import pygame
import random

# 초기화
pygame.init()

# 화면 크기
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30

# 색상 정의
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
COLORS = [
    (255, 0, 0),    # 빨강
    (0, 255, 0),    # 초록
    (0, 0, 255),    # 파랑
    (255, 255, 0),  # 노랑
    (0, 255, 255),  # 청록
    (255, 0, 255),  # 자홍
]

# 테트리스 블록 모양
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[0, 1, 0], [1, 1, 1]],  # T
    [[1, 0, 0], [1, 1, 1]],  # L
    [[0, 0, 1], [1, 1, 1]],  # J
    [[0, 1, 1], [1, 1, 0]],  # S
    [[1, 1, 0], [0, 1, 1]],  # Z
]

# 게임 보드 크기
BOARD_WIDTH = SCREEN_WIDTH // BLOCK_SIZE
BOARD_HEIGHT = SCREEN_HEIGHT // BLOCK_SIZE

# 블록 클래스
class Block:
    def __init__(self, shape):
        self.shape = shape
        self.color = random.choice(COLORS)
        self.x = BOARD_WIDTH // 2 - len(shape[0]) // 2
        self.y = 0

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

# 게임 보드 클래스
class Board:
    def __init__(self):
        self.grid = [[0] * BOARD_WIDTH for _ in range(BOARD_HEIGHT)]

    def is_valid_position(self, block, offset_x=0, offset_y=0):
        for y, row in enumerate(block.shape):
            for x, cell in enumerate(row):
                if cell:
                    new_x = block.x + x + offset_x
                    new_y = block.y + y + offset_y
                    if new_x < 0 or new_x >= BOARD_WIDTH or new_y >= BOARD_HEIGHT:
                        return False
                    if new_y >= 0 and self.grid[new_y][new_x]:
                        return False
        return True

    def place_block(self, block):
        for y, row in enumerate(block.shape):
            for x, cell in enumerate(row):
                if cell:
                    self.grid[block.y + y][block.x + x] = block.color

    def clear_lines(self):
        new_grid = [row for row in self.grid if any(cell == 0 for cell in row)]
        cleared_lines = BOARD_HEIGHT - len(new_grid)
        for _ in range(cleared_lines):
            new_grid.insert(0, [0] * BOARD_WIDTH)
        self.grid = new_grid
        return cleared_lines

# 게임 클래스
class Tetris:
    def __init__(self):
        self.board = Board()
        self.current_block = self.new_block()
        self.score = 0
        self.game_over = False

    def new_block(self):
        return Block(random.choice(SHAPES))

    def move_block(self, dx, dy):
        if self.board.is_valid_position(self.current_block, dx, dy):
            self.current_block.x += dx
            self.current_block.y += dy
        elif dy > 0:  # 블록이 아래로 이동할 수 없으면 고정
            self.board.place_block(self.current_block)
            self.board.clear_lines()
            self.current_block = self.new_block()
            if not self.board.is_valid_position(self.current_block):
                self.game_over = True

    def rotate_block(self):
        original_shape = self.current_block.shape
        self.current_block.rotate()
        if not self.board.is_valid_position(self.current_block):
            self.current_block.shape = original_shape

# 게임 루프
def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("테트리스")
    clock = pygame.time.Clock()
    game = Tetris()

    running = True
    fall_time = 0
    fall_speed = 50  # 밀리초
    FPS = 20  # 게임 속도를 조절하기 위한 FPS 설정

    while running:
        screen.fill(BLACK)
        fall_time += clock.get_rawtime()
        clock.tick(FPS)  # FPS 값을 설정하여 게임 속도 조절

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    game.move_block(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    game.move_block(1, 0)
                elif event.key == pygame.K_DOWN:
                    game.move_block(0, 1)
                elif event.key == pygame.K_UP:
                    game.rotate_block()

        if fall_time > fall_speed:
            game.move_block(0, 1)
            fall_time = 0

        # 게임 오버 처리
        if game.game_over:
            print("Game Over!")
            running = False

        # 보드 그리기
        for y, row in enumerate(game.board.grid):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, cell, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
                    pygame.draw.rect(screen, GRAY, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

        # 현재 블록 그리기
        for y, row in enumerate(game.current_block.shape):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(
                        screen,
                        game.current_block.color,
                        ((game.current_block.x + x) * BLOCK_SIZE, (game.current_block.y + y) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE),
                    )
                    pygame.draw.rect(
                        screen,
                        GRAY,
                        ((game.current_block.x + x) * BLOCK_SIZE, (game.current_block.y + y) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE),
                        1,
                    )

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()