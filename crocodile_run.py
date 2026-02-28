import pygame
import random
import sys

# 初始化Pygame
pygame.init()

# 游戏常量
WIDTH = 800
HEIGHT = 400
FPS = 60
GRAVITY = 0.8
JUMP_STRENGTH = -15
SPEED_INCREMENT = 0.001

# 颜色
WHITE = (255, 255, 255)
GREEN = (34, 139, 34)
DARK_GREEN = (0, 100, 0)
BROWN = (139, 69, 19)
SKY_BLUE = (135, 206, 235)
GROUND_COLOR = (107, 142, 35)

# 设置屏幕
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("小鳄鱼跑酷")
clock = pygame.time.Clock()

# 字体
font = pygame.font.Font(None, 36)


class Crocodile:
    def __init__(self):
        self.width = 60
        self.height = 40
        self.x = 100
        self.y = HEIGHT - 100 - self.height
        self.velocity_y = 0
        self.is_jumping = False
        self.animation_frame = 0
        self.animation_timer = 0

    def jump(self):
        if not self.is_jumping:
            self.velocity_y = JUMP_STRENGTH
            self.is_jumping = True

    def update(self):
        # 应用重力
        self.velocity_y += GRAVITY
        self.y += self.velocity_y

        # 地面碰撞
        ground_y = HEIGHT - 100 - self.height
        if self.y >= ground_y:
            self.y = ground_y
            self.velocity_y = 0
            self.is_jumping = False

        # 动画
        self.animation_timer += 1
        if self.animation_timer >= 5:
            self.animation_timer = 0
            self.animation_frame = (self.animation_frame + 1) % 2

    def draw(self, screen):
        # 身体（绿色椭圆形）
        body_rect = pygame.Rect(self.x, self.y + 10, self.width - 10, self.height - 15)
        pygame.draw.ellipse(screen, GREEN, body_rect)
        pygame.draw.ellipse(screen, DARK_GREEN, body_rect, 2)

        # 头部
        head_rect = pygame.Rect(self.x + self.width - 25, self.y + 5, 30, 25)
        pygame.draw.ellipse(screen, GREEN, head_rect)
        pygame.draw.ellipse(screen, DARK_GREEN, head_rect, 2)

        # 眼睛
        eye_y = self.y + 10
        pygame.draw.circle(screen, WHITE, (self.x + self.width - 10, eye_y), 6)
        pygame.draw.circle(screen, (0, 0, 0), (self.x + self.width - 8, eye_y), 3)

        # 腿（动画效果）
        leg_offset = 5 if self.animation_frame == 0 else -5
        if not self.is_jumping:
            # 前腿
            pygame.draw.rect(screen, GREEN, (self.x + 15, self.y + self.height - 10 + leg_offset, 8, 15))
            pygame.draw.rect(screen, DARK_GREEN, (self.x + 15, self.y + self.height - 10 + leg_offset, 8, 15), 1)
            # 后腿
            pygame.draw.rect(screen, GREEN, (self.x + 35, self.y + self.height - 10 - leg_offset, 8, 15))
            pygame.draw.rect(screen, DARK_GREEN, (self.x + 35, self.y + self.height - 10 - leg_offset, 8, 15), 1)
        else:
            # 跳跃时的腿
            pygame.draw.rect(screen, GREEN, (self.x + 15, self.y + self.height - 10, 8, 12))
            pygame.draw.rect(screen, DARK_GREEN, (self.x + 15, self.y + self.height - 10, 8, 12), 1)
            pygame.draw.rect(screen, GREEN, (self.x + 35, self.y + self.height - 10, 8, 12))
            pygame.draw.rect(screen, DARK_GREEN, (self.x + 35, self.y + self.height - 10, 8, 12), 1)

        # 尾巴
        tail_points = [
            (self.x, self.y + 20),
            (self.x - 20, self.y + 25),
            (self.x, self.y + 30)
        ]
        pygame.draw.polygon(screen, GREEN, tail_points)
        pygame.draw.polygon(screen, DARK_GREEN, tail_points, 1)

    def get_hitbox(self):
        return pygame.Rect(self.x + 5, self.y + 10, self.width - 20, self.height - 15)


class Obstacle:
    def __init__(self, x):
        self.type = random.choice(['rock', 'tree', 'bird'])
        self.x = x

        if self.type == 'rock':
            self.width = 40
            self.height = 35
            self.y = HEIGHT - 100 - self.height
            self.color = (128, 128, 128)
        elif self.type == 'tree':
            self.width = 30
            self.height = 60
            self.y = HEIGHT - 100 - self.height
            self.color = BROWN
        else:  # bird
            self.width = 40
            self.height = 30
            self.y = HEIGHT - 200 - random.randint(0, 50)
            self.color = (255, 165, 0)
            self.wing_frame = 0

    def update(self, speed):
        self.x -= speed
        if self.type == 'bird':
            self.wing_frame = (self.wing_frame + 0.2) % 2

    def draw(self, screen):
        if self.type == 'rock':
            # 石头
            rock_rect = pygame.Rect(self.x, self.y, self.width, self.height)
            pygame.draw.ellipse(screen, self.color, rock_rect)
            pygame.draw.ellipse(screen, (80, 80, 80), rock_rect, 2)
        elif self.type == 'tree':
            # 树干
            pygame.draw.rect(screen, self.color, (self.x + 10, self.y + 20, 10, 40))
            # 树叶
            leaf_rect = pygame.Rect(self.x, self.y, self.width, 30)
            pygame.draw.ellipse(screen, DARK_GREEN, leaf_rect)
            pygame.draw.ellipse(screen, (0, 80, 0), leaf_rect, 2)
        else:  # bird
            # 鸟身体
            bird_body = pygame.Rect(self.x + 5, self.y + 10, 30, 15)
            pygame.draw.ellipse(screen, self.color, bird_body)
            # 翅膀
            wing_y = self.y + 5 if int(self.wing_frame) == 0 else self.y + 15
            wing_rect = pygame.Rect(self.x + 10, wing_y, 20, 10)
            pygame.draw.ellipse(screen, (255, 140, 0), wing_rect)
            # 鸟头
            pygame.draw.circle(screen, self.color, (self.x + 35, self.y + 12), 8)
            # 鸟嘴
            pygame.draw.polygon(screen, (255, 100, 0), [
                (self.x + 42, self.y + 12),
                (self.x + 52, self.y + 14),
                (self.x + 42, self.y + 16)
            ])

    def get_hitbox(self):
        if self.type == 'rock':
            return pygame.Rect(self.x + 5, self.y + 5, self.width - 10, self.height - 10)
        elif self.type == 'tree':
            return pygame.Rect(self.x + 5, self.y, self.width - 10, self.height)
        else:  # bird
            return pygame.Rect(self.x + 5, self.y + 5, self.width - 10, self.height - 10)

    def is_off_screen(self):
        return self.x + self.width < 0


def draw_ground(screen, scroll_offset):
    # 地面
    pygame.draw.rect(screen, GROUND_COLOR, (0, HEIGHT - 100, WIDTH, 100))
    # 草地纹理
    for i in range(0, WIDTH + 50, 50):
        grass_x = (i + scroll_offset) % (WIDTH + 50) - 50
        pygame.draw.rect(screen, (124, 179, 66), (grass_x, HEIGHT - 100, 25, 10))


def draw_clouds(screen, cloud_offset):
    for i in range(3):
        cloud_x = ((i * 300) + cloud_offset) % (WIDTH + 200) - 100
        cloud_y = 50 + i * 40
        # 云朵
        pygame.draw.ellipse(screen, WHITE, (cloud_x, cloud_y, 80, 40))
        pygame.draw.ellipse(screen, WHITE, (cloud_x + 30, cloud_y - 10, 60, 30))
        pygame.draw.ellipse(screen, WHITE, (cloud_x + 60, cloud_y, 50, 35))


def main():
    running = True
    game_over = False
    score = 0
    high_score = 0
    speed = 5
    scroll_offset = 0
    cloud_offset = 0

    crocodile = Crocodile()
    obstacles = []
    obstacle_timer = 0

    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_SPACE or event.key == pygame.K_UP) and not game_over:
                    crocodile.jump()
                if event.key == pygame.K_r and game_over:
                    # 重新开始游戏
                    game_over = False
                    score = 0
                    speed = 5
                    crocodile = Crocodile()
                    obstacles = []
                    obstacle_timer = 0

        if not game_over:
            # 更新
            crocodile.update()
            speed += SPEED_INCREMENT
            score += 1

            # 滚动效果
            scroll_offset -= speed
            cloud_offset -= speed * 0.3

            # 生成障碍物
            obstacle_timer += 1
            if obstacle_timer > 60 + random.randint(0, 40):
                obstacles.append(Obstacle(WIDTH))
                obstacle_timer = 0

            # 更新障碍物
            for obstacle in obstacles[:]:
                obstacle.update(speed)
                if obstacle.is_off_screen():
                    obstacles.remove(obstacle)

            # 碰撞检测
            crocodile_hitbox = crocodile.get_hitbox()
            for obstacle in obstacles:
                if crocodile_hitbox.colliderect(obstacle.get_hitbox()):
                    game_over = True
                    if score > high_score:
                        high_score = score

        # 绘制
        screen.fill(SKY_BLUE)
        draw_clouds(screen, cloud_offset)
        draw_ground(screen, scroll_offset)

        for obstacle in obstacles:
            obstacle.draw(screen)

        crocodile.draw(screen)

        # 分数显示
        score_text = font.render(f"分数: {score}", True, (0, 0, 0))
        high_score_text = font.render(f"最高分: {high_score}", True, (0, 0, 0))
        screen.blit(score_text, (10, 10))
        screen.blit(high_score_text, (10, 50))

        if game_over:
            game_over_text = font.render("游戏结束! 按 R 重新开始", True, (255, 0, 0))
            text_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(game_over_text, text_rect)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()