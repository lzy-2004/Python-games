import pygame
import random
import sys

# 初始化Pygame
pygame.init()

# 游戏窗口设置
WIDTH, HEIGHT = 600, 600
BLOCK_SIZE = 20
assert WIDTH % BLOCK_SIZE == 0 and HEIGHT % BLOCK_SIZE == 0  # 确保窗口能被方块整除
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("贪吃蛇")

# 颜色定义
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# 游戏参数
clock = pygame.time.Clock()
direction = 'RIGHT'
score = 0
target_score = 5


class Snake:
    def __init__(self):
        self.length = 3
        self.positions = [(WIDTH // 2, HEIGHT // 2)]
        for i in range(1, self.length):
            self.positions.append((self.positions[0][0] - i * BLOCK_SIZE, self.positions[0][1]))
        self.direction = direction

    def get_head_position(self):
        return self.positions[0]

    def turn(self, new_dir):
        if (new_dir == 'LEFT' and self.direction != 'RIGHT') or \
                (new_dir == 'RIGHT' and self.direction != 'LEFT') or \
                (new_dir == 'UP' and self.direction != 'DOWN') or \
                (new_dir == 'DOWN' and self.direction != 'UP'):
            self.direction = new_dir

    def move(self):
        cur_head = list(self.get_head_position())
        if self.direction == 'RIGHT':
            cur_head[0] += BLOCK_SIZE
        elif self.direction == 'LEFT':
            cur_head[0] -= BLOCK_SIZE
        elif self.direction == 'UP':
            cur_head[1] -= BLOCK_SIZE
        elif self.direction == 'DOWN':
            cur_head[1] += BLOCK_SIZE
        self.positions.insert(0, tuple(cur_head))
        if len(self.positions) > self.length:
            self.positions.pop()

    def draw(self):
        for p in self.positions:
            pygame.draw.rect(screen, GREEN, (p[0], p[1], BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(screen, BLACK, (p[0], p[1], BLOCK_SIZE, BLOCK_SIZE), 1)


class Food:
    def __init__(self):
        self.position = (0, 0)
        self.randomize()

    def randomize(self):
        x = random.randint(0, (WIDTH / BLOCK_SIZE) - 1)
        y = random.randint(0, (HEIGHT / BLOCK_SIZE) - 1)
        self.position = (int(x * BLOCK_SIZE), int(y * BLOCK_SIZE))

    def draw(self):
        pygame.draw.rect(screen, RED, (self.position[0], self.position[1], BLOCK_SIZE, BLOCK_SIZE))


def game_over():
    font = pygame.font.Font('msyh.ttc', 72)
    text = font.render("游戏结束!", True, (255, 0, 0))
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
    pygame.display.flip()
    pygame.time.wait(2000)
    pygame.quit()
    sys.exit()


def game_win():
    """显示胜利界面并结束游戏"""
    font = pygame.font.Font('msyh.ttc', 72)
    text = font.render("恭喜通关!", True, (0, 255, 0))
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
    pygame.display.flip()
    pygame.time.wait(2000)
    pygame.quit()
    sys.exit()


def start_screen():
    """显示开始界面并等待用户操作"""
    font_title = pygame.font.Font('msyh.ttc', 72)
    font_prompt = pygame.font.Font('msyh.ttc', 36)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                return  # 开始游戏

        # 绘制开始界面内容
        screen.fill(WHITE)
        title_text = font_title.render("贪吃蛇", True, GREEN)
        prompt_text = font_prompt.render("点击开始，按ESC退出，按空格暂停", True, BLACK)

        # 居中显示文字
        screen.blit(title_text,
                    (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 3 - title_text.get_height()))
        screen.blit(prompt_text,
                    (WIDTH // 2 - prompt_text.get_width() // 2, HEIGHT // 2 + prompt_text.get_height()))

        pygame.display.update()
        clock.tick(10)


def main():
    global direction, score
    paused = False
    start_screen()

    direction = 'RIGHT'
    score = 0
    snake = Snake()
    food = Food()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_SPACE:
                    paused = not paused
                elif event.key == pygame.K_UP:
                    snake.turn('UP')
                elif event.key == pygame.K_DOWN:
                    snake.turn('DOWN')
                elif event.key == pygame.K_LEFT:
                    snake.turn('LEFT')
                elif event.key == pygame.K_RIGHT:
                    snake.turn('RIGHT')
        if not paused:
            snake.move()

            # 碰撞检测
            if snake.get_head_position() in snake.positions[1:]:
                game_over()
            if (snake.get_head_position()[0] < 0 or
                    snake.get_head_position()[0] >= WIDTH or
                    snake.get_head_position()[1] < 0 or
                    snake.get_head_position()[1] >= HEIGHT):
                game_over()

            # 食物逻辑
            if snake.get_head_position() == food.position:
                score += 1
                food.randomize()
                # 防止食物生成在蛇身上
                while food.position in snake.positions:
                    food.randomize()
                snake.length += 1

                if score >= target_score:
                    game_win()

        screen.fill(WHITE)
        snake.draw()
        food.draw()

        # 显示得分
        font = pygame.font.Font('msyh.ttc', 36)
        text = font.render(f"得分: {score}/{target_score}", True, BLACK)
        screen.blit(text, (10, 10))

        # 暂停界面显示
        if paused:
            font_paused = pygame.font.Font('msyh.ttc', 48)
            paused_text = font_paused.render("游戏已暂停", True, (255, 0, 0))
            screen.blit(paused_text,
                        (WIDTH // 2 - paused_text.get_width() // 2,
                         HEIGHT // 2 - paused_text.get_height() // 2))

        pygame.display.update()
        clock.tick(5)  # 控制游戏速度（5帧/秒）


if __name__ == '__main__':
    main()
