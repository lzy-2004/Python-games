import pygame
import random
import sys

# 初始化 pygame
pygame.init()

# 设置窗口大小
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 740
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("连连看")

# 配置
BACKGROUND_COLOR = (0, 128, 0)  # 绿色背景
ICON_SIZE = 64
GRID_SIZE = 10  # 10x10网格

score = 0


def draw_score():
    font = pygame.font.Font('msyh.ttc', 30)
    score_text = font.render(f"分数: {score}", True, (255, 255, 255))
    text_rect = score_text.get_rect(center=(SCREEN_WIDTH//2, 50))  # 居中顶部
    screen.blit(score_text, text_rect)


# 加载图标
icons = []
for i in range(1, 7):  # 加载6个图标（根据实际文件数量调整）
    img_path = f'./images/icon{i}.png'
    icon = pygame.image.load(img_path)
    icon = pygame.transform.scale(icon, (ICON_SIZE, ICON_SIZE))
    icons.append(icon)


# 创建图标数组（-1表示已消除）
def create_icon_array():
    array = []
    for _ in range(GRID_SIZE):
        row = [random.randint(0, len(icons) - 1) for _ in range(GRID_SIZE)]
        array.append(row)
    return array


icon_array = create_icon_array()


# 绘制函数
def draw_icons():
    screen.fill(BACKGROUND_COLOR)
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            if icon_array[y][x] != -1:
                icon = icons[icon_array[y][x]]
                screen.blit(icon, (x * ICON_SIZE, y * ICON_SIZE+100))


# 修改后的路径检测逻辑
def can_connect(p1, p2):
    if p1 == p2:
        return False

    x1, y1 = p1
    x2, y2 = p2

    # 必须在同一行或同一列
    if x1 != x2 and y1 != y2:
        return False
    # 路径长度不能超过2
    if abs(x1-x2)>1 or abs(y1-y2)>1:
        return False

    # 检查路径是否畅通（中间无阻挡）
    if x1 == x2:  # 同一列，检查y方向
        start, end = sorted((y1, y2))
        for y in range(start + 1, end):
            if icon_array[y][x1] != -1:  # 中间有未消除的图标
                return False
    else:  # 同一行，检查x方向
        start, end = sorted((x1, x2))
        for x in range(start + 1, end):
            if icon_array[y1][x] != -1:  # 中间有未消除的图标
                return False

    return True


# 消除逻辑
selected = []


def check_and_remove():
    if len(selected) != 2:
        return

    p1, p2 = selected
    pos1 = (p1[0], p1[1])  # (x,y)
    pos2 = (p2[0], p2[1])

    if (icon_array[pos1[1]][pos1[0]] == icon_array[pos2[1]][pos2[0]] and
            can_connect(pos1, pos2)):

        # 标记消除
        icon_array[pos1[1]][pos1[0]] = -1
        icon_array[pos2[1]][pos2[0]] = -1
        print("消除成功！")
        drop_icons()

        global score
        score += 10
    else:
        print("无法消除")

    selected.clear()
    draw_icons()


# 图标下落逻辑（保持不变）
def drop_icons():
    for x in range(GRID_SIZE):
        column = []
        for y in range(GRID_SIZE):
            if icon_array[y][x] != -1:
                column.append(icon_array[y][x])
        new_column = [-1] * (GRID_SIZE - len(column)) + column
        for y in range(GRID_SIZE):
            icon_array[y][x] = new_column[y]


# 点击处理
def handle_click(pos):
    x, y = pos
    grid_x = x // ICON_SIZE
    grid_y = (y - 100) // ICON_SIZE  # 减去顶部偏移

    if (0 <= grid_x < GRID_SIZE and
        0 <= grid_y < GRID_SIZE and
        icon_array[grid_y][grid_x] != -1):  # 确保坐标有效

        selected.append((grid_x, grid_y))
        if len(selected) == 2:
            check_and_remove()


# 胜利检测（保持不变）
def is_game_won():
    for row in icon_array:
        if any(icon != -1 for icon in row):
            return False
    return True


# 游戏状态管理
game_started = False
running = True


def draw_start_screen():
    screen.fill(BACKGROUND_COLOR)
    font_title = pygame.font.Font('msyh.ttc', 60)
    text_title = font_title.render("连连看", True, (255, 255, 255))
    screen.blit(text_title, (SCREEN_WIDTH // 2 - text_title.get_width() // 2, 200))

    font_prompt = pygame.font.Font('msyh.ttc', 30)
    text_prompt = font_prompt.render("点击屏幕开始游戏,按ESC结束游戏", True, (255, 255, 255))
    screen.blit(text_prompt, (SCREEN_WIDTH // 2 - text_prompt.get_width() // 2, 350))


# 主循环
while running:
    # 初始界面状态
    while not game_started and running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                game_started = True

        draw_start_screen()
        pygame.display.flip()

    # 游戏进行中状态
    if game_started:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                handle_click(event.pos)
                if is_game_won():
                    print("恭喜你，游戏胜利！")
                    running = False

        draw_icons()

        if len(selected) >= 2:
            p1, p2 = selected[0], selected[1]
            center1 = (p1[0] * ICON_SIZE + ICON_SIZE // 2, p1[1] * ICON_SIZE + ICON_SIZE // 2)
            center2 = (p2[0] * ICON_SIZE + ICON_SIZE // 2, p2[1] * ICON_SIZE + ICON_SIZE // 2)
            pygame.draw.line(screen, (255, 0, 0), center1, center2, 2)

        draw_score()

        pygame.display.flip()

pygame.quit()
sys.exit()  # 确保程序完全退出

