import pygame
import random
import time

# 초기화
pygame.init()

# 화면 크기
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
BLOCK_SIZE = 20

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# 화면 설정
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("뱀 게임")

# 시계 객체
clock = pygame.time.Clock()

# 뱀 초기화
snake_pos = [100, 50]
snake_body = [[100, 50], [90, 50], [80, 50]]
snake_direction = 'RIGHT'
change_to = snake_direction

# 점수
score = 0

# 음식 초기화
food_pos = [random.randrange(1, (SCREEN_WIDTH // BLOCK_SIZE)) * BLOCK_SIZE,
            random.randrange(1, (SCREEN_HEIGHT // BLOCK_SIZE)) * BLOCK_SIZE]
food_spawn = True

# 점수 표시 함수
def show_score(choice, color, font, size):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render('Score : ' + str(score), True, color)
    score_rect = score_surface.get_rect()
    screen.blit(score_surface, score_rect)

# 게임 종료 함수
def game_over():
    font = pygame.font.SysFont('times new roman', 50)
    game_over_surface = font.render('Your Score is : ' + str(score), True, RED)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4)
    screen.fill(BLACK)
    screen.blit(game_over_surface, game_over_rect)
    pygame.display.flip()
    time.sleep(2)
    pygame.quit()
    quit()

# 게임 루프
while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and not change_to == 'DOWN':
                change_to = 'UP'
            elif event.key == pygame.K_DOWN and not change_to == 'UP':
                change_to = 'DOWN'
            elif event.key == pygame.K_LEFT and not change_to == 'RIGHT':
                change_to = 'LEFT'
            elif event.key == pygame.K_RIGHT and not change_to == 'LEFT':
                change_to = 'RIGHT'
        elif event.type == pygame.QUIT:
            pygame.quit()
            quit()

    # 방향 변경
    if change_to == 'UP':
        snake_direction = 'UP'
    if change_to == 'DOWN':
        snake_direction = 'DOWN'
    if change_to == 'LEFT':
        snake_direction = 'LEFT'
    if change_to == 'RIGHT':
        snake_direction = 'RIGHT'

    # 뱀 이동
    if snake_direction == 'UP':
        snake_pos[1] -= BLOCK_SIZE
    if snake_direction == 'DOWN':
        snake_pos[1] += BLOCK_SIZE
    if snake_direction == 'LEFT':
        snake_pos[0] -= BLOCK_SIZE
    if snake_direction == 'RIGHT':
        snake_pos[0] += BLOCK_SIZE

    # 뱀 몸 길이 증가
    snake_body.insert(0, list(snake_pos))
    if snake_pos == food_pos:
        score += 10
        food_spawn = False
    else:
        snake_body.pop()

    if not food_spawn:
        food_pos = [random.randrange(1, (SCREEN_WIDTH // BLOCK_SIZE)) * BLOCK_SIZE,
                    random.randrange(1, (SCREEN_HEIGHT // BLOCK_SIZE)) * BLOCK_SIZE]
    food_spawn = True

    # 화면 경계 충돌
    if (snake_pos[0] < 0 or snake_pos[0] >= SCREEN_WIDTH or
            snake_pos[1] < 0 or snake_pos[1] >= SCREEN_HEIGHT):
        game_over()

    # 뱀 자기 자신과 충돌
    for block in snake_body[1:]:
        if snake_pos == block:
            game_over()

    # 화면 그리기
    screen.fill(BLACK)
    for pos in snake_body:
        pygame.draw.rect(screen, GREEN, pygame.Rect(pos[0], pos[1], BLOCK_SIZE, BLOCK_SIZE))
    pygame.draw.rect(screen, RED, pygame.Rect(food_pos[0], food_pos[1], BLOCK_SIZE, BLOCK_SIZE))

    # 점수 표시
    show_score(1, WHITE, 'times new roman', 20)

    # 화면 업데이트
    pygame.display.update()

    # 게임 속도 조절
    clock.tick(15)