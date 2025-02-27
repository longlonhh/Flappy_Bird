from pprint import pp 
import pygame, sys, random

# tao ham cho tro choi
def draw_floor():
    screen.blit(floor, (floor_x_pos, 650))
    screen.blit(floor, (floor_x_pos + 432, 650))

def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop=(550, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midtop=(550, random_pipe_pos - 650))
    return bottom_pipe, top_pipe

def move_pipe(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes

def draw_pipe(pipes):
    for pipe in pipes:
        if pipe.bottom >= 600:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)

# xu li va cham
def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            death_sound.play()
            return False
    if bird_rect.top <= -75 or bird_rect.bottom >= 650:
        return False
    return True

def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -bird_movement * 3, 1)
    return new_bird

def bird_animation():
    new_bird = bird_list[bird_index]
    new_bird_rect = new_bird.get_rect(center=(100, bird_rect.centery))
    return new_bird, new_bird_rect

def score_display(game_state):
    if game_state == 'main_game':
        score_surface = game_font.render(str(int(score)), True, (255, 20, 147))  # Màu hồng đậm
        score_rect = score_surface.get_rect(center=(216, 100))
        screen.blit(score_surface, score_rect)
        high_score_surface = game_font.render(f'High Score: {int(high_score)}', True, (255, 20, 147))  # Màu hồng đậm
        high_score_rect = high_score_surface.get_rect(center=(216, 50))
        screen.blit(high_score_surface, high_score_rect)
    if game_state == 'game_over':
        score_surface = game_font.render(f'Score: {int(score)}', True, (255, 20, 147))  # Màu hồng đậm
        score_rect = score_surface.get_rect(center=(216, 100))
        screen.blit(score_surface, score_rect)
        high_score_surface = game_font.render(f'High Score: {int(high_score)}', True, (255, 20, 147))  # Màu hồng đậm
        high_score_rect = high_score_surface.get_rect(center=(216, 50))
        screen.blit(high_score_surface, high_score_rect)

def update_high_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score

pygame.mixer.pre_init(frequency=44100, size=16, channels=1, buffer=512)
pygame.init()
screen = pygame.display.set_mode((432, 768))  # tao bien cua so
clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19.ttf', 40)

# bien cho tro choi
gravity = 0.25
bird_movement = 0
bg = pygame.image.load('assets/pink-background-7552922_1280.webp').convert()  # them background vao cua so
bg = pygame.transform.scale2x(bg)  # gap doi background
game_active = False
score = 0
high_score = 0

# chen san:
floor = pygame.image.load('assets/floor.png').convert()
floor = pygame.transform.scale2x(floor)
floor_x_pos = 0

# tao chim
bird_down = pygame.transform.scale2x(pygame.image.load('assets/yellowbird-downflap.png').convert_alpha())
bird_mid = pygame.transform.scale2x(pygame.image.load('assets/yellowbird-midflap.png').convert_alpha())
bird_up = pygame.transform.scale2x(pygame.image.load('assets/yellowbird-upflap.png').convert_alpha())
bird_list = [bird_down, bird_mid, bird_up]  # 0 1 2
bird_index = 0
bird = bird_list[bird_index]
bird_rect = bird.get_rect(center=(100, 384))

# tao timer cho bird
birdflap = pygame.USEREVENT + 1
pygame.time.set_timer(birdflap, 200)

# tao ong
pipe_surface = pygame.image.load('assets/pipe-green.png').convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []

# tao ong lien tuc
spawnpipe = pygame.USEREVENT
pygame.time.set_timer(spawnpipe, 1200)
pipe_height = [200, 300, 400, 500, 600]

# tao man hinh ket thuc
game_over_surface = pygame.transform.scale2x(pygame.image.load('assets/message.png').convert_alpha())
game_over_rect = game_over_surface.get_rect(center=(216, 384))

# chen am thanh
flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
death_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')
score_sound_countdown = 100

# while loop cua game
while True:
    # tao cua so game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement = -7
                flap_sound.play()
            if event.key == pygame.K_SPACE and not game_active:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100, 384)
                bird_movement = 0
                score = 0  # Reset score when restarting the game
        if event.type == spawnpipe and game_active:
            pipe_list.extend(create_pipe())
        if event.type == birdflap and game_active:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            bird, bird_rect = bird_animation()

    screen.blit(bg, (0, 0))
    rotated_bird = rotate_bird(bird)  # Đảm bảo rotated_bird được định nghĩa
    if game_active:
        # chim
        bird_movement += gravity
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird, bird_rect)
        # xu li va cham
        game_active = check_collision(pipe_list)
        # ong
        pipe_list = move_pipe(pipe_list)
        draw_pipe(pipe_list)
        # diem so
        score += 0.01
        score_display('main_game')
        score_sound_countdown -= 1
        if score_sound_countdown <= 0:
            score_sound.play()
            score_sound_countdown = 100
    else:
        screen.blit(rotated_bird, bird_rect)  # Giữ chim trên màn hình
        draw_pipe(pipe_list)  # Giữ ống trên màn hình
        screen.blit(game_over_surface, game_over_rect)
        high_score = update_high_score(score, high_score)
        score_display('game_over')

    # san
    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -432:
        floor_x_pos = 0

    pygame.display.update()
    clock.tick(120)