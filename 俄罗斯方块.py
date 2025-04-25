import pygame
import random

pygame.init()

# 基础设置
WIDTH, HEIGHT = 480, 600
BLOCK_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 20
FPS = 60

# 颜色定义
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
VIOLET = (148, 0, 211)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)

# 方块形状数据（7种标准形状）
SHAPES = [
    {'shape': [[1, 1, 1, 1]], 'color': CYAN},  # I
    {'shape': [[1, 1, 1], [0, 1, 0]], 'color': YELLOW},  # T
    {'shape': [[1, 1], [1, 1]], 'color': BLUE},  # O
    {'shape': [[1, 1, 0], [0, 1, 1]], 'color': ORANGE},  # Z
    {'shape': [[0, 1, 1], [1, 1, 0]], 'color': GREEN},  # S
    {'shape': [[1, 1, 1], [0, 0, 1]], 'color': VIOLET},  # J
    {'shape': [[1, 1, 1], [1, 0, 0]], 'color': RED}  # L
]

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('俄罗斯方块')
clock = pygame.time.Clock()


class Tetromino:
    def __init__(self):
        self.data = random.choice(SHAPES)
        self.shape = self.data['shape']
        self.color = self.data['color']
        self.x = GRID_WIDTH // 2 - len(self.shape[0]) // 2
        self.y = 0

    def draw(self):
        for iy, row in enumerate(self.shape):
            for ix, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, self.color,
                                     (self.x * BLOCK_SIZE + ix * BLOCK_SIZE,
                                      self.y * BLOCK_SIZE + iy * BLOCK_SIZE,
                                      BLOCK_SIZE, BLOCK_SIZE), 0)
                    pygame.draw.rect(screen, WHITE,
                                     (self.x * BLOCK_SIZE + ix * BLOCK_SIZE,
                                      self.y * BLOCK_SIZE + iy * BLOCK_SIZE,
                                      BLOCK_SIZE, BLOCK_SIZE), 1)

    def move(self, dx=0, dy=0):
        new_x = self.x + dx
        new_y = self.y + dy
        if self.check_collision(new_x, new_y):
            return False
        self.x = new_x
        self.y = new_y
        return True

    def rotate(self):
        original_shape = self.shape
        rotated = list(zip(*reversed(self.shape)))  # 旋转形状
        if self.check_collision(self.x, self.y, rotated):
            self.shape = original_shape
            return False
        self.shape = rotated
        return True

    def check_collision(self, x, y, shape=None):
        shape = shape if shape else self.shape
        for iy, row in enumerate(shape):
            for ix, cell in enumerate(row):
                if cell:
                    nx = x + ix
                    ny = y + iy
                    if ny >= GRID_HEIGHT or nx < 0 or nx >= GRID_WIDTH:
                        return True
                    if game.grid[ny][nx] != 0:
                        return True
        return False


class Game:
    def __init__(self):
        self.grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.current = None
        self.next = None
        self.score = 0
        self.game_over = False
        self.paused = False  # 新增暂停状态
        self.state = "start"  # 新增游戏状态：start/playing/paused/game_over
        self.last_drop = pygame.time.get_ticks()
        self.font = pygame.font.Font('msyh.ttc', 36)

    def run(self):
        while True:
            clock.tick(FPS)
            current_time = pygame.time.get_ticks()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if self.state == "start":
                    if event.type == pygame.MOUSEBUTTONDOWN or (
                            event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN):
                        self.reset_game()  # 初始化游戏
                        self.state = "playing"
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        exit()
                elif self.state == "playing":
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            pygame.quit()
                            exit()
                        if event.key == pygame.K_SPACE:
                            self.paused = not self.paused
                        if not self.paused:
                            if event.key == pygame.K_LEFT:
                                self.current.move(dx=-1)
                            if event.key == pygame.K_RIGHT:
                                self.current.move(dx=1)
                            if event.key == pygame.K_DOWN:
                                self.current.move(dy=1)
                            if event.key == pygame.K_UP:
                                self.current.rotate()
                elif self.state == "game_over":
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                        self.reset_game()
                        self.state = "playing"

            self.update(current_time)
            self.draw()

    def draw(self):
        screen.fill(BLACK)
        if self.state == "start":
            self.draw_start_menu()
        elif self.state == "playing":
            pygame.draw.line(screen, WHITE, (300, 0), (300, HEIGHT), 2)
            self.current.draw()
            self.draw_grid()
            self.draw_next()
            self.draw_score()
            if self.paused:
                self.draw_pause()
        elif self.state == "game_over":
            self.show_game_over()
        pygame.display.flip()

    def draw_start_menu(self):
        font_large = pygame.font.Font('msyh.ttc', 48)
        font_medium = pygame.font.Font('msyh.ttc', 30)
        title = font_large.render("俄罗斯方块", True, BLUE)
        start_text = font_medium.render("点击或按回车开始", True, WHITE)
        esc_text = font_medium.render("按ESC退出", True, WHITE)
        pause_text = font_medium.render("按空格暂停", True, WHITE)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 100))
        screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2))
        screen.blit(esc_text, (WIDTH // 2 - esc_text.get_width() // 2, HEIGHT // 2 + 50))
        screen.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 2 + 100))

    def draw_pause(self):
        font = pygame.font.Font('msyh.ttc', 48)
        text = font.render("游戏已暂停", True, RED)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 24))

    def draw_grid(self):
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                rect = pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                pygame.draw.rect(screen, GRAY, rect, 1)  # 绘制网格线

        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, cell, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)
                    pygame.draw.rect(screen, WHITE, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

    def draw_next(self):
        font = pygame.font.Font('msyh.ttc', 30)
        text = font.render("下一个", True, WHITE)
        screen.blit(text, (320, 50))
        for iy, row in enumerate(self.next.shape):
            for ix, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, self.next.color,
                                     (320 + ix * BLOCK_SIZE, 100 + iy * BLOCK_SIZE,
                                      BLOCK_SIZE, BLOCK_SIZE), 0)
                    pygame.draw.rect(screen, WHITE,
                                     (320 + ix * BLOCK_SIZE, 100 + iy * BLOCK_SIZE,
                                      BLOCK_SIZE, BLOCK_SIZE), 1)

    def draw_score(self):
        font = pygame.font.Font('msyh.ttc', 30)
        score_text = font.render(f"分数: {self.score}", True, WHITE)
        screen.blit(score_text, (320, 250))  # 右侧显示

    def update(self, current_time):
        if self.state == "playing":
            if not self.paused:
                if current_time - self.last_drop > 500:
                    if not self.current.move(dy=1):
                        self.lock_tetromino()
                        self.check_lines()
                        self.current = self.next
                        self.next = Tetromino()
                        if not self.is_valid_spawn():
                            self.state = "game_over"
                    self.last_drop = current_time

    def reset_game(self):
        self.grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.current = Tetromino()
        self.next = Tetromino()
        self.score = 0
        self.game_over = False
        self.paused = False
        self.last_drop = pygame.time.get_ticks()

    def lock_tetromino(self):
        for iy, row in enumerate(self.current.shape):
            for ix, cell in enumerate(row):
                if cell and self.current.y + iy < GRID_HEIGHT:
                    self.grid[self.current.y + iy][self.current.x + ix] = self.current.color

    def check_lines(self):
        lines = [row for row in range(GRID_HEIGHT) if all(self.grid[row])]
        self.score += len(lines) * 100
        for line in reversed(lines):
            del self.grid[line]
            self.grid.insert(0, [0] * GRID_WIDTH)

    def is_valid_spawn(self):
        for iy, row in enumerate(self.current.shape):
            for ix, cell in enumerate(row):
                if cell and self.grid[self.current.y + iy][self.current.x + ix] != 0:
                    return False
        return True

    def show_game_over(self):
        font = pygame.font.Font('msyh.ttc', 48)
        text = font.render("游戏结束", True, RED)
        screen.blit(text, (WIDTH // 2 - 100, HEIGHT // 2 - 24))
        font1 = pygame.font.Font('msyh.ttc', 30)
        score_text = font1.render(f"最终分数是: {self.score}", True, WHITE)
        screen.blit(score_text, (WIDTH // 2 - 100, HEIGHT // 2 + 50))


if __name__ == "__main__":
    game = Game()
    game.run()
