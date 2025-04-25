import pygame
import random

# 初始化 Pygame
pygame.init()

# 颜色定义
COLORS = {
    0: (204, 192, 179),
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 94),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46),
    'bg': (186, 172, 158),
    'score_bg': (186, 172, 158)
}

# 字体设置
FONT = pygame.font.SysFont('arial', 40, bold=True)
SCORE_FONT = pygame.font.SysFont('arial', 30, bold=True)

# 游戏板大小
BOARD_SIZE = 4

# 窗口大小
WINDOW_SIZE = 400
CELL_SIZE = WINDOW_SIZE // BOARD_SIZE

# 初始化屏幕
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE + 100))
pygame.display.set_caption('2048')


def initialize_board():
    board = [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]
    add_new_tile(board)
    add_new_tile(board)
    return board


def add_new_tile(board):
    available = []
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if board[i][j] == 0:
                available.append((i, j))
    if not available:
        return False
    i, j = random.choice(available)
    board[i][j] = 2 if random.random() < 0.9 else 4
    return True


def move_left(board):
    new_board = []
    changed = False
    for row in board:
        new_row = []
        current = [num for num in row if num != 0]
        merged = []
        skip = False
        for num in current:
            if skip:
                merged.append(num)
                skip = False
                continue
            if merged and merged[-1] == num:
                merged[-1] *= 2
                skip = True
                changed = True
            else:
                merged.append(num)
        new_row = merged + [0] * (BOARD_SIZE - len(merged))
        new_board.append(new_row)
    return new_board, (new_board != board or changed)


def move_right(board):
    new_board = [row[::-1] for row in board]
    new_board, changed = move_left(new_board)
    new_board = [row[::-1] for row in new_board]
    return new_board, changed


def move_up(board):
    transposed = list(zip(*board))
    transposed = [list(row) for row in transposed]
    transposed, changed = move_left(transposed)
    new_board = list(zip(*transposed))
    new_board = [list(row) for row in new_board]
    return new_board, changed


def move_down(board):
    transposed = list(zip(*board))
    transposed = [row[::-1] for row in transposed]
    transposed, changed = move_left(transposed)
    transposed = [row[::-1] for row in transposed]
    new_board = list(zip(*transposed))
    new_board = [list(row) for row in new_board]
    return new_board, changed


def get_score(board):
    return sum(sum(row) for row in board)


def game_win(board):
    for row in board:
        if 2048 in row:
            return True
    return False


def game_over(board):
    for direction in [move_left, move_right, move_up, move_down]:
        temp = [row.copy() for row in board]
        new_board, moved = direction(temp)
        if moved:
            return False
    return True


def draw_board(board, score):
    screen.fill(COLORS['bg'])
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            value = board[i][j]
            rect = pygame.Rect(j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, COLORS.get(value, (0, 0, 0)), rect, 0, 5)
            if value > 0:
                text_surface = FONT.render(str(value), True, (0, 0, 0))
                text_rect = text_surface.get_rect(center=rect.center)
                screen.blit(text_surface, text_rect)

    # 绘制分数
    score_surface = SCORE_FONT.render(f"Score: {score}", True, (0, 0, 0))
    score_rect = score_surface.get_rect(center=(WINDOW_SIZE // 2, WINDOW_SIZE + 50))
    pygame.draw.rect(screen, COLORS['score_bg'], (0, WINDOW_SIZE, WINDOW_SIZE, 100))
    screen.blit(score_surface, score_rect)

    pygame.display.update()


def main():
    board = initialize_board()
    score = get_score(board)
    draw_board(board, score)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                new_board = board.copy()
                moved = False
                if event.key == pygame.K_LEFT:
                    new_board, moved = move_left(board)
                elif event.key == pygame.K_RIGHT:
                    new_board, moved = move_right(board)
                elif event.key == pygame.K_UP:
                    new_board, moved = move_up(board)
                elif event.key == pygame.K_DOWN:
                    new_board, moved = move_down(board)

                if moved:
                    board = new_board
                    if not add_new_tile(board):
                        print("游戏结束！")
                        running = False

                score = get_score(board)
                draw_board(board, score)

                if game_win(board):
                    print("恭喜！你赢了！")
                    running = False
                if game_over(board):
                    print("无路可走，游戏结束！")
                    running = False

    pygame.quit()


if __name__ == "__main__":
    main()

