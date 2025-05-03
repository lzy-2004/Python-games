import pygame
import random
import sys

# 初始化Pygame
pygame.init()
pygame.mixer.init()  # 初始化音频模块

# 游戏窗口设置
WIDTH, HEIGHT = 400, 512
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("跳一跳")

# 颜色定义
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# 加载图片资源
BIRD_IMG = pygame.image.load("./images/bird.png")  # 小鸟图片
BIRD_IMG = pygame.transform.scale(BIRD_IMG, (30, 30))  # 调整为30x30像素

PIPE_IMG = pygame.image.load("./images/pipe.png")  # 管道图片（尺寸建议52x320）
PIPE_IMG = pygame.transform.scale(PIPE_IMG, (52, 320))  # 调整为52x320像素

# 加载音效
try:
    JUMP_SOUND = pygame.mixer.Sound("./sounds/jump.wav")
    SCORE_SOUND = pygame.mixer.Sound("./sounds/score.wav")
    HIT_SOUND = pygame.mixer.Sound("./sounds/hit.wav")
    # 背景音乐
    pygame.mixer.music.load("./sounds/bgm.mp3")
    pygame.mixer.music.set_volume(0.5)  # 设置音量
    sound_enabled = True
except:
    sound_enabled = False
    print("警告：无法加载音效文件，游戏将在无声模式下运行")

# 替换背景（纯色背景）
BACKGROUND = pygame.Surface((WIDTH, HEIGHT))
BACKGROUND.fill((135, 206, 250))  # 浅蓝色

# 尝试加载背景图片
try:
    BG_IMG = pygame.image.load("./images/background.png")
    BG_IMG = pygame.transform.scale(BG_IMG, (WIDTH, HEIGHT))
    use_bg_image = True
except:
    use_bg_image = False

# 游戏参数
gravity = 0.35
bird_velocity = 0
jump_strength = -10
pipe_speed = -4  # 管道移动速度（负值表示向左移动）
pipe_gap = 80  # 管道间隔
score = 0
high_score = 0  # 最高分
font = pygame.font.Font(None, 48)

# 游戏状态
game_active = False  # 游戏是否激活
difficulty_level = 1  # 难度级别


class Bird:
    def __init__(self):
        self.x = 100
        self.y = HEIGHT // 2
        self.rect = BIRD_IMG.get_rect(center=(self.x, self.y))

    def jump(self):
        global bird_velocity
        bird_velocity = jump_strength

    def update(self):
        global bird_velocity
        bird_velocity += gravity
        self.y += bird_velocity
        self.rect.center = (self.x, self.y)

    def draw(self):
        screen.blit(BIRD_IMG, self.rect)


class Pipe:
    def __init__(self):
        self.x = WIDTH + 100
        # 根据难度调整管道高度的随机范围
        min_height = 150 - (difficulty_level - 1) * 10
        max_height = 300 + (difficulty_level - 1) * 10
        self.height = random.randint(min_height, max_height)
        self.passed = False
        
    def update(self):
        # 根据难度调整管道速度
        current_speed = pipe_speed - (difficulty_level - 1) * 0.5
        self.x += current_speed
        if self.x + PIPE_IMG.get_width() < 0:
            self.__init__()  # 重新生成管道

    def draw(self):
        # 绘制上方管道（修正位置）
        screen.blit(pygame.transform.rotate(PIPE_IMG, 180),
                    (self.x, self.height - PIPE_IMG.get_height() - pipe_gap))
        # 绘制下方管道
        screen.blit(PIPE_IMG, (self.x, self.height + pipe_gap))

    def check_collision(self, bird):
        bird_mask = pygame.mask.from_surface(BIRD_IMG)
        pipe_mask = pygame.mask.from_surface(PIPE_IMG)

        # 上方管道碰撞检测（修正offset）
        offset_top = (
            int(self.x - bird.rect.x),
            int(self.height - PIPE_IMG.get_height() - pipe_gap - bird.rect.y)
        )
        if bird_mask.overlap(pipe_mask, offset_top):
            return True

        # 下方管道碰撞检测（修正offset）
        offset_bottom = (
            int(self.x - bird.rect.x),
            int(self.height + pipe_gap - bird.rect.y)
        )
        if bird_mask.overlap(pipe_mask, offset_bottom):
            return True
        return False


def game_over():
    """显示游戏结束界面并等待用户按ESC结束或按空格重新开始"""
    global high_score
    
    # 更新最高分
    if score > high_score:
        high_score = score
    
    font_game_over = pygame.font.Font('msyh.ttc', 50)
    font_score = pygame.font.Font('msyh.ttc', 36)
    clock = pygame.time.Clock()

    # 播放碰撞音效
    if sound_enabled:
        HIT_SOUND.play()

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
                    return True  # 返回True表示重新开始游戏

        # 绘制结束界面内容
        if use_bg_image:
            screen.blit(BG_IMG, (0, 0))
        else:
            screen.blit(BACKGROUND, (0, 0))

        # 游戏结束文本
        text = font_game_over.render("游戏结束", True, (255, 0, 0))
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 120))

        # 总得分文本
        score_text = font_score.render(f"得分: {score}", True, (255, 0, 0))
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 - 40))
        
        # 最高分文本
        high_score_text = font_score.render(f"最高分: {high_score}", True, (255, 0, 0))
        screen.blit(high_score_text, (WIDTH // 2 - high_score_text.get_width() // 2, HEIGHT // 2 + 10))

        # 提示文本
        prompt_text1 = font_score.render("按ESC退出", True, (0, 0, 0))
        prompt_text2 = font_score.render("按空格重新开始", True, (0, 0, 0))
        screen.blit(prompt_text1, (WIDTH // 2 - prompt_text1.get_width() // 2, HEIGHT // 2 + 70))
        screen.blit(prompt_text2, (WIDTH // 2 - prompt_text2.get_width() // 2, HEIGHT // 2 + 120))

        pygame.display.update()
        clock.tick(60)


def show_settings():
    """显示游戏设置界面"""
    global sound_enabled, difficulty_level
    
    font_title = pygame.font.Font('msyh.ttc', 48)
    font_option = pygame.font.Font('msyh.ttc', 36)
    clock = pygame.time.Clock()
    
    # 设置选项
    options = ["音效: 开启" if sound_enabled else "音效: 关闭", 
               f"难度: {difficulty_level}", 
               "返回"]
    selected = 0
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    if selected == 0:  # 音效设置
                        sound_enabled = not sound_enabled
                        options[0] = "音效: 开启" if sound_enabled else "音效: 关闭"
                        if sound_enabled:
                            pygame.mixer.music.play(-1)
                        else:
                            pygame.mixer.music.stop()
                    elif selected == 1:  # 难度设置
                        difficulty_level = difficulty_level % 5 + 1
                        options[1] = f"难度: {difficulty_level}"
                    elif selected == 2:  # 返回
                        return
                elif event.key == pygame.K_ESCAPE:
                    return
        
        # 绘制设置界面
        if use_bg_image:
            screen.blit(BG_IMG, (0, 0))
        else:
            screen.blit(BACKGROUND, (0, 0))
        
        # 标题
        title_text = font_title.render("游戏设置", True, (255, 0, 0))
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 4 - title_text.get_height() // 2))
        
        # 选项
        for i, option in enumerate(options):
            color = (255, 255, 0) if i == selected else (0, 0, 0)
            option_text = font_option.render(option, True, color)
            screen.blit(option_text, (WIDTH // 2 - option_text.get_width() // 2, HEIGHT // 2 + i * 60 - 30))
        
        # 操作提示
        hint_text = font_option.render("↑↓选择 回车确认", True, (0, 0, 0))
        screen.blit(hint_text, (WIDTH // 2 - hint_text.get_width() // 2, HEIGHT - 100))
        
        pygame.display.update()
        clock.tick(60)


def show_start_screen():
    """显示初始界面并等待用户操作"""
    font_title = pygame.font.Font('msyh.ttc', 72)
    font_prompt = pygame.font.Font('msyh.ttc', 36)
    clock = pygame.time.Clock()
    
    options = ["开始游戏", "游戏设置", "退出游戏"]
    selected = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    if selected == 0:  # 开始游戏
                        return
                    elif selected == 1:  # 游戏设置
                        show_settings()
                    elif selected == 2:  # 退出游戏
                        pygame.quit()
                        sys.exit()
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # 检查鼠标点击位置
                mouse_pos = pygame.mouse.get_pos()
                for i, option in enumerate(options):
                    option_text = font_prompt.render(option, True, (0, 0, 0))
                    option_rect = option_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + i * 60))
                    if option_rect.collidepoint(mouse_pos):
                        if i == 0:  # 开始游戏
                            return
                        elif i == 1:  # 游戏设置
                            show_settings()
                        elif i == 2:  # 退出游戏
                            pygame.quit()
                            sys.exit()

        # 绘制初始界面内容
        if use_bg_image:
            screen.blit(BG_IMG, (0, 0))
        else:
            screen.blit(BACKGROUND, (0, 0))

        # 标题文本
        title_text = font_title.render("跳一跳", True, (255, 0, 0))
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 4 - title_text.get_height() // 2))

        # 菜单选项
        for i, option in enumerate(options):
            color = (255, 255, 0) if i == selected else (0, 0, 0)
            option_text = font_prompt.render(option, True, color)
            screen.blit(option_text, (WIDTH // 2 - option_text.get_width() // 2, HEIGHT // 2 + i * 60))

        # 操作提示
        hint_text = font_prompt.render("↑↓选择 回车确认", True, (0, 0, 0))
        screen.blit(hint_text, (WIDTH // 2 - hint_text.get_width() // 2, HEIGHT - 100))

        pygame.display.update()
        clock.tick(60)


def pause_game():
    """暂停游戏界面"""
    font_pause = pygame.font.Font('msyh.ttc', 48)
    paused = True
    clock = pygame.time.Clock()
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    paused = False  # 按回车键继续游戏
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        # 绘制暂停界面
        screen.blit(BACKGROUND, (0, 0))
        pause_text = font_pause.render("游戏已暂停", True, (255, 0, 0))
        screen.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 2 - pause_text.get_height() // 2))

        pygame.display.update()
        clock.tick(60)


def main():
    global score, bird_velocity, game_active, difficulty_level
    
    # 播放背景音乐（循环播放）
    if sound_enabled:
        pygame.mixer.music.play(-1)  # -1表示无限循环

    # 创建云朵和地面
    clouds = [Cloud() for _ in range(3)]
    ground = Ground()

    while True:
        # 显示初始界面
        show_start_screen()
        
        # 重置游戏状态
        score = 0
        bird_velocity = 0
        difficulty_level = 1
        game_active = True
        
        bird = Bird()
        pipes = [Pipe()]
        clock = pygame.time.Clock()

        # 主游戏循环
        while game_active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        bird.jump()
                        # 播放跳跃音效
                        if sound_enabled:
                            JUMP_SOUND.play()
                    elif event.key == pygame.K_RETURN:
                        pause_game()  # 切换暂停状态
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

            # 更新逻辑
            bird.update()
            
            # 生成新管道（间隔2秒）
            if pipes[-1].x < WIDTH - 200:
                pipes.append(Pipe())
            # 移除屏幕外的管道
            pipes = [pipe for pipe in pipes if pipe.x > -PIPE_IMG.get_width()]

            # 检测碰撞
            for pipe in pipes:
                pipe.update()
                if pipe.check_collision(bird):
                    game_active = False
                if pipe.x + PIPE_IMG.get_width() < bird.rect.left and not pipe.passed:
                    score += 1
                    pipe.passed = True
                    # 播放得分音效
                    if sound_enabled:
                        SCORE_SOUND.play()
                    
                    # 移除自动增加难度的代码
                    # 每得5分增加一次难度
                    # if score % 5 == 0 and score > 0:
                    #     difficulty_level = min(difficulty_level + 1, 5)  # 最高难度为5

            # 更新云朵和地面
            for cloud in clouds:
                cloud.update()
            ground.update()

            # 渲染
            if use_bg_image:
                screen.blit(BG_IMG, (0, 0))
            else:
                screen.blit(BACKGROUND, (0, 0))
                
            # 绘制云朵
            for cloud in clouds:
                cloud.draw()
                
            bird.draw()
            for pipe in pipes:
                pipe.draw()
                
            # 绘制地面
            ground.draw()
            
            # 显示得分
            font = pygame.font.Font('msyh.ttc', 30)
            text = font.render(f"分数: {score}", True, BLACK)
            screen.blit(text, (10, 10))
            
            # 显示当前难度
            diff_text = font.render(f"难度: {difficulty_level}", True, BLACK)
            screen.blit(diff_text, (10, 50))
            
            # 显示最高分
            high_text = font.render(f"最高分: {high_score}", True, BLACK)
            screen.blit(high_text, (WIDTH - high_text.get_width() - 10, 10))

            # 游戏结束条件
            if bird.y >= HEIGHT or bird.y <= -20:
                game_active = False

            pygame.display.update()
            clock.tick(60)
            
        # 游戏结束，显示结束界面
        if not game_over():  # 如果返回False，表示用户选择退出
            break





class Cloud:
    def __init__(self):
        try:
            self.image = pygame.image.load("./images/cloud.png")
            self.image = pygame.transform.scale(self.image, (80, 40))
            self.available = True
        except:
            self.available = False
            return
            
        self.x = WIDTH + random.randint(50, 200)
        self.y = random.randint(50, 150)
        self.speed = random.uniform(0.5, 1.5)
        
    def update(self):
        if not self.available:
            return
            
        self.x -= self.speed
        if self.x < -self.image.get_width():
            self.x = WIDTH + random.randint(50, 200)
            self.y = random.randint(50, 150)
            self.speed = random.uniform(0.5, 1.5)
            
    def draw(self):
        if not self.available:
            return
        screen.blit(self.image, (int(self.x), int(self.y)))

class Ground:
    def __init__(self):
        try:
            self.image = pygame.image.load("./images/ground.png")
            self.image = pygame.transform.scale(self.image, (WIDTH, 70))
            self.available = True
        except:
            self.available = False
            return
            
        self.x1 = 0
        self.x2 = WIDTH
        self.y = HEIGHT - self.image.get_height()
        self.speed = 2
        
    def update(self):
        if not self.available:
            return
            
        self.x1 -= self.speed
        self.x2 -= self.speed
        
        if self.x1 + WIDTH <= 0:
            self.x1 = self.x2 + WIDTH
        if self.x2 + WIDTH <= 0:
            self.x2 = self.x1 + WIDTH
            
    def draw(self):
        if not self.available:
            return
        screen.blit(self.image, (int(self.x1), self.y))
        screen.blit(self.image, (int(self.x2), self.y))

if __name__ == "__main__":
    main()
