import pygame
import settings
from levels import levels
import time
import sys
import math
from collections import deque
import random

# ---------------------------------------------------------------
# Mapa e constantes
# ---------------------------------------------------------------
# 0: espaço livre
# 1: parede (bloqueada, a menos que o jogador tenha power-up C para pular)
# 2: obstáculo transponível (só pode ser cruzado se o jogador tiver power-up B)
# 3: power-up A – desacelera o tempo por 10 segundos (duas cores ou sprite)
# 4: power-up B – permite transpor 1 obstáculo transponível (duas cores ou sprite)
# 5: power-up C – permite pular sobre uma parede (duas cores ou sprite)
# 7: destino (verde)
# 8: partida (azul)

#maze = [
#    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
#    [1,8,0,0,0,0,2,0,0,0,0,0,0,0,1],
#    [1,0,1,1,1,0,1,1,1,1,1,0,1,0,1],
#    [1,0,1,3,1,0,0,0,4,0,1,0,1,0,1],
#    [1,0,1,0,1,1,1,0,1,0,1,0,1,0,1],
#    [1,0,0,0,0,0,1,0,1,0,1,0,0,0,1],
#    [1,1,1,1,1,0,1,0,1,0,1,1,1,0,1],
#    [1,0,0,0,1,0,0,0,1,0,0,0,1,0,1],
#    [1,0,1,0,1,1,1,1,1,1,1,0,1,0,1],
#    [1,0,1,0,0,0,0,0,0,0,1,0,1,0,1],
#    [1,0,1,1,1,1,1,1,1,0,1,0,1,0,1],
#    [1,0,0,0,0,0,0,0,1,0,0,7,1,5,1],
#    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
#]

global current_level
current_level = 0

global current_maze
current_maze = levels[current_level].maze

global total_time
global remaining_time

global ROWS
global COLS

pygame.init()
pygame.mixer.init()  # Inicializa o mixer, se ainda não estiver iniciado

# Carrega os efeitos sonoros (substitua os caminhos pelos arquivos corretos)
pickup_sound = pygame.mixer.Sound("sons/pickup_sound.wav")
use_sound = pygame.mixer.Sound("sons/use_sound.wav")
use_sound.set_volume(0.1)  # Ajuste o volume conforme necessário
game_over_sound = pygame.mixer.Sound("sons/game_over.mp3")
win_sound = pygame.mixer.Sound("sons/win_sound.wav")
win_sound.set_volume(0.1)  # Ajuste o volume conforme necessário
movement_sound = pygame.mixer.Sound("sons/player_movement_sound.wav")
colision_sound = pygame.mixer.Sound("sons/colision.wav")
main_drums = pygame.mixer.Sound("sons/main_drums.mp3")
main_melody = pygame.mixer.Sound("sons/main_melody.mp3")


def setup_sound():
    pygame.mixer.music.load("sons/main_bass.mp3")
    pygame.mixer.music.play(-1)  # -1 para repetir indefinidamente
    main_drums.play(loops = -1)  # -1 para repetir indefinidamente
    main_melody.play(loops = -1) 
    main_drums.set_volume(0)  # Ajuste o volume conforme necessário
    main_melody.set_volume(0)  # Ajuste o volume conforme necessário


SCREEN_WIDTH = 600
SCREEN_HEIGHT = 520
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Carrega as imagens para as mensagens de vitória e derrota
win_image = pygame.image.load("imagens/win_image.png").convert_alpha()
game_over_image = pygame.image.load("imagens/game_over_image.png").convert_alpha()
colision_image = pygame.image.load("imagens/colision_image.png").convert_alpha()

# Opcional: Redimensione as imagens para o tamanho desejado
win_image = pygame.transform.scale(win_image, (300, 200))
game_over_image = pygame.transform.scale(game_over_image, (300, 200))
colision_image = pygame.transform.scale(colision_image, (300, 200))

# Variável global inicial para direção
player_direction = "down"  # valor padrão

ROWS = len(current_maze)
COLS = len(current_maze[0])
TILE_SIZE = 16
WIDTH = COLS * TILE_SIZE
HEIGHT = ROWS * TILE_SIZE
#variavel usada para controlar a musica de fundo
emocao =False

# Supondo que cada spritesheet possua o mesmo número de frames e tamanho
num_frames = 3
frame_width = TILE_SIZE
frame_height = TILE_SIZE

def extract_frames(spritesheet):
    frames = []
    for i in range(num_frames):
        frame_rect = pygame.Rect(i * frame_width, 0, frame_width, frame_height)
        frame = spritesheet.subsurface(frame_rect)
        frame = pygame.transform.scale(frame, (TILE_SIZE, TILE_SIZE))
        frames.append(frame)
    return frames

# Carregar as spritesheets para cada direção
sprite_sheet_down = pygame.image.load("imagens/player_spritesheet_down.png").convert_alpha()
sprite_sheet_up = pygame.image.load("imagens/player_spritesheet_up.png").convert_alpha()
sprite_sheet_left = pygame.image.load("imagens/player_spritesheet_left.png").convert_alpha()
sprite_sheet_right = pygame.image.load("imagens/player_spritesheet_right.png").convert_alpha()

# Extrair os frames e armazenar em um dicionário
player_frames = {
    "down": extract_frames(sprite_sheet_down),
    "up": extract_frames(sprite_sheet_up),
    "left": extract_frames(sprite_sheet_left),
    "right": extract_frames(sprite_sheet_right)
}

# Carregar as spritesheets para a versão com poder B
sprite_sheet_down_B = pygame.image.load("imagens/player_spritesheet_down_B.png").convert_alpha()
sprite_sheet_up_B = pygame.image.load("imagens/player_spritesheet_up_B.png").convert_alpha()
sprite_sheet_left_B = pygame.image.load("imagens/player_spritesheet_left_B.png").convert_alpha()
sprite_sheet_right_B = pygame.image.load("imagens/player_spritesheet_right_B.png").convert_alpha()

player_frames_B = {
    "down": extract_frames(sprite_sheet_down_B),
    "up": extract_frames(sprite_sheet_up_B),
    "left": extract_frames(sprite_sheet_left_B),
    "right": extract_frames(sprite_sheet_right_B)
}

# Variáveis de controle da animação
current_frame = 0
animation_timer = 0
animation_delay = 0.1  # segundos entre frames

# ---------------------------------------------------------------
# NOVA SEÇÃO: Animação direcional para obstáculos móveis
# ---------------------------------------------------------------

# Função para determinar a direção a partir do vetor de movimento
def get_direction_from_vector(dx, dy):
    if dx == 1:
        return "right"
    elif dx == -1:
        return "left"
    elif dy == 1:
        return "down"
    elif dy == -1:
        return "up"
    return "down"  # padrão caso não haja movimento

# Carregar as spritesheets dos obstáculos móveis para cada direção
obstacle_sprite_sheet_down = pygame.image.load("imagens/obstacle_spritesheet_down.png").convert_alpha()
obstacle_sprite_sheet_up = pygame.image.load("imagens/obstacle_spritesheet_up.png").convert_alpha()
obstacle_sprite_sheet_left = pygame.image.load("imagens/obstacle_spritesheet_left.png").convert_alpha()
obstacle_sprite_sheet_right = pygame.image.load("imagens/obstacle_spritesheet_right.png").convert_alpha()

life_img = pygame.image.load("imagens/heart.png").convert_alpha()
life_img = pygame.transform.scale(life_img, (20, 20)) 

# Extrair os frames usando a função extract_frames
obstacle_frames = {
    "down": extract_frames(obstacle_sprite_sheet_down),
    "up": extract_frames(obstacle_sprite_sheet_up),
    "left": extract_frames(obstacle_sprite_sheet_left),
    "right": extract_frames(obstacle_sprite_sheet_right)
}

# Variáveis de controle da animação dos obstáculos
obstacle_animation_timer = 0
obstacle_animation_delay = 0.1  # segundos entre frames
obstacle_current_frame = 0

# ---------------------------------------------------------------
# Funções de apoio
# ---------------------------------------------------------------
def is_traversable(cell, b_count, jump_count):
    """Verifica se a célula pode ser atravessada dadas as cargas de B e C."""
    if cell in (0, 8, 3, 4, 5, 7, 9):
        return True
    if cell == 2 and b_count > 0:
        return True
    if cell == 1 and jump_count > 0:
        return True
    return False

def bfs_distance(maze, start, end, b_count, jump_count):
    """
    Faz uma busca em largura para verificar se existe um caminho entre start e end,
    considerando as cargas de B e C. Retorna a distância em passos se houver,
    ou None se não houver caminho.
    """
    from collections import deque
    queue = deque()
    visited = set()
    queue.append((start[0], start[1], 0))
    visited.add((start[0], start[1]))

    while queue:
        x, y, d = queue.popleft()
        if (x, y) == end:
            return d  # encontrou o destino
        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < COLS and 0 <= ny < ROWS and (nx, ny) not in visited:
                cell = maze[ny][nx]
                if is_traversable(cell, b_count, jump_count):
                    visited.add((nx, ny))
                    queue.append((nx, ny, d+1))
    return None  # sem caminho

def find_destination(maze):
    """Retorna as coordenadas (col, row) da célula com valor 7 (destino)."""
    for row in range(ROWS):
        for col in range(COLS):
            if maze[row][col] == 7:
                return (col, row)
    return None

def clamp_camera(camera_rect, world_width, world_height):
    """Garante que a câmera não saia dos limites do mundo."""
    if camera_rect.left < 0:
        camera_rect.left = 0
    if camera_rect.top < 0:
        camera_rect.top = 0
    if camera_rect.right > world_width:
        camera_rect.right = world_width
    if camera_rect.bottom > world_height:
        camera_rect.bottom = world_height
    return camera_rect

# Variáveis de controle, defina-as antes do loop principal
sound_game_over_played = False
sound_win_played = False

# Classe representando uma partícula individual
class Particle:
    def __init__(self, pos):
        self.x, self.y = pos
        # Velocidade aleatória para simular movimento (folhas ou confetes caindo)
        self.vx = random.uniform(-50, 50)  # velocidade horizontal (px/s)
        self.vy = random.uniform(20, 80)   # velocidade vertical (px/s)
        self.lifetime = random.uniform(20, 30)  # tempo de vida em segundos
        self.age = 0
        self.size = random.randint(1, 3)
        # Escolhe uma cor aleatória para as partículas (pode ser ajustada para folhas ou confetes)
        self.color = random.choice([
            (255, 215, 0),  # Amarelo Ouro
            (148, 0, 211),  # Roxo Carnaval
            (50, 205, 50),    # Verde Limão
            (65, 105, 225),    # Azul Royal
            (255, 20, 147),   # Rosa Choque
            (220, 20, 60) #vermelho
        ])
        
    def update(self, dt):
        self.age += dt
        self.x += self.vx * dt
        self.y += self.vy * dt
        # Simula uma leve oscilação horizontal para imitar movimento natural
        self.vx += random.uniform(-10, 10) * dt
        
    def is_dead(self):
        return self.age >= self.lifetime
        
    def draw(self, surface):
        # Calcula a opacidade (fade out conforme a partícula envelhece)
        alpha = max(0, int(255 * (1 - self.age / self.lifetime)))
        # Cria uma pequena superfície com suporte a transparência para desenhar a partícula
        particle_surface = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        pygame.draw.circle(particle_surface, self.color + (alpha,), (self.size, self.size), self.size)
        surface.blit(particle_surface, (int(self.x - self.size), int(self.y - self.size)))

particles = []

# ---------------------------------------------------------------
# Função principal (main)
# ---------------------------------------------------------------




def game_level():
    setup_sound()
    global current_maze
    global current_level
    global total_time
    global remaining_time

    play_drums = False
    play_melody = False
    
    current_maze = levels[current_level].maze
    pygame.display.set_caption("Jogo do Labirinto com Câmera e Movimentação Suave")
    clock = pygame.time.Clock()
    
    ZOOM = 4

    # Superfície de todo o mundo (todo o labirinto)
    world_surface = pygame.Surface((WIDTH, HEIGHT))

    # Carregar e escalonar as imagens
    # (Ajuste o caminho 'imagens/...' conforme sua estrutura de arquivos)
    floor_img = pygame.image.load("imagens/floor.png").convert_alpha()
    wall_img = pygame.image.load("imagens/wall.png").convert_alpha()
    obstacle_img = pygame.image.load("imagens/obstacle.png").convert_alpha()
    powerup_a_img = pygame.image.load("imagens/powerup_a.png").convert_alpha()
    powerup_b_img = pygame.image.load("imagens/powerup_b.png").convert_alpha()
    powerup_c_img = pygame.image.load("imagens/powerup_c.png").convert_alpha()
    mud_img = pygame.image.load("imagens/mud.png").convert_alpha()
    dest_img = pygame.image.load("imagens/destination.png").convert_alpha()
    start_img = pygame.image.load("imagens/start.png").convert_alpha()

    # Imagem de fundo da HUD
    hud_background = pygame.image.load("imagens/hud_background.png").convert_alpha()
    # Se necessário, ajuste o tamanho da imagem:
    hud_background = pygame.transform.scale(hud_background, (120, 70))
    # Fonte para o texto da HUD
    font = pygame.font.SysFont(None, 24, bold=True)


    # Sprite do jogador (opcional)
    player_img = pygame.image.load("imagens/player.png").convert_alpha()

    # Ajustar tamanho das imagens para o tamanho da célula
    floor_img = pygame.transform.scale(floor_img, (TILE_SIZE, TILE_SIZE))
    wall_img = pygame.transform.scale(wall_img, (TILE_SIZE, TILE_SIZE))
    obstacle_img = pygame.transform.scale(obstacle_img, (TILE_SIZE, TILE_SIZE))
    powerup_a_img = pygame.transform.scale(powerup_a_img, (TILE_SIZE, TILE_SIZE))
    powerup_b_img = pygame.transform.scale(powerup_b_img, (TILE_SIZE, TILE_SIZE))
    powerup_c_img = pygame.transform.scale(powerup_c_img, (TILE_SIZE, TILE_SIZE))
    mud_img = pygame.transform.scale(mud_img, (TILE_SIZE, TILE_SIZE))
    dest_img = pygame.transform.scale(dest_img, (TILE_SIZE, TILE_SIZE))
    start_img = pygame.transform.scale(start_img, (TILE_SIZE, TILE_SIZE))
    player_img = pygame.transform.scale(player_img, (TILE_SIZE, TILE_SIZE))

    # Mapeamento de cada valor do labirinto para a imagem correspondente
    tile_images = {
        0: floor_img,
        1: wall_img,
        2: obstacle_img,
        3: powerup_a_img,
        4: powerup_b_img,
        5: powerup_c_img,
        7: dest_img,
        8: start_img,
        9: mud_img
    }
    obstaculos_din_grid = levels[current_level].obstacles

    # [9, 1, 0, 1, moveu_obstaculo] => 
    # [
    #  pos_grid_x_obstaculo, 
    #  pos_grid_y_obstaculo, 
    #  movimentação horizonatal (-1 para esquerda, 1 para direita, 0 para movimentação vertical)
    #  movimentação vertical (-1 para cima, 1 para baixo, 0 para movimentação horizontal)                                                                                   
    # ]                                                                               

    obstaculo_din_target_grid = list(obstaculos_din_grid)

    #garanti que o número de linhas abaixo seja igaul ao número de onstáculos dinâmcos
    # importante garantir a ordem abaixo



    obstaculo_din_pos_px = [
        [obstaculo[0] * TILE_SIZE, obstaculo[1] * TILE_SIZE] for obstaculo in obstaculos_din_grid
    ]

    # Estado de colisão
    collision = False
    collided_obstacle_index = None
    list_collided_obstacle_index = []

    # Estado inicial do jogador
    player_grid = levels[current_level].player_start  # posição em coordenadas de grid (coluna, linha)
    player_pos = [player_grid[0] * TILE_SIZE, player_grid[1] * TILE_SIZE]  # posição em pixels
    target_grid = list(player_grid)
    moving = False

    # Quantidade de cada power-up
    b_count = 0    # power-up B
    jump_count = 0 # power-up C

    # Controle do slow (power-up A)
    time_slow_active = False
    time_slow_end = 0

    # Tempo total e estado do jogo

    total_time = 30
    
    remaining_time = total_time
    game_over = False
    win = False

    # Encontrar a posição do destino (7)
    destination = find_destination(current_maze)

    # Configuração de fonte e velocidade de movimento
    font = pygame.font.SysFont(None, 24)
    SPEED_OBSTACLE = 100
    SPEED_PLAYER = 100

    animation_timer = 0
    colided = False

    global obstacle_animation_timer, obstacle_current_frame

    # Loop principal
    while True:
        # "real_dt" é o tempo real entre frames (usado na física e no movimento)
        real_dt = clock.tick(60) / 1000.0

        # "movement_dt" => usado na movimentação do jogador (não sofre slow)
        # "timer_dt"    => usado na contagem regressiva (pode sofrer slow)
        movement_dt = real_dt
        timer_dt = real_dt

        if not play_drums and remaining_time < 2*(total_time/3):
            play_drums = True
    
        if not play_melody and remaining_time < total_time/3:
            play_melody = True

        if moving:
            animation_timer += movement_dt
            if animation_timer >= animation_delay:
                animation_timer = 0
                current_frame = (current_frame + 1) % len(frames_to_use)
        else:
            current_frame = 0

        # Atualiza a animação dos obstáculos móveis (para todos em sincronia)
        if len(obstaculo_din_pos_px) > 0:
            obstacle_animation_timer += movement_dt
            if obstacle_animation_timer >= obstacle_animation_delay:
                obstacle_animation_timer = 0
                obstacle_current_frame = (obstacle_current_frame + 1) % len(obstacle_frames["down"])  # assume mesmo número de frames para todas as direções


        # Verifica se o slow está ativo e se já acabou
        if time_slow_active:
            # Se chegou ao fim do tempo do slow, desativa
            if pygame.time.get_ticks() / 1000.0 >= time_slow_end:
                time_slow_active = False
            else:
                # Enquanto ativo, reduz apenas a velocidade de passagem do tempo do jogo (timer)
                timer_dt *= 0.5

        # ---------------------------------------------------------------------
        # Processar eventos
        # ---------------------------------------------------------------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

       # if not drums_played and remaining_time > total_time/3:
        
        # Movimentação dos obstáculos dinâmicos - grid
        for index, obstaculo in enumerate(obstaculos_din_grid):
            
            pos_grid_x_obstaculo, pos_grid_y_obstaculo, dx, dy, moveu = obstaculo 

            if moveu == False:

                #Obstaculo irá se mover agora
                obstaculos_din_grid[index][4] = True; 
                obstaculo_din_target_grid[index][4] = True

                new_x_obstaculo = pos_grid_x_obstaculo + dx
                new_y_obstaculo = pos_grid_y_obstaculo + dy
                celll_obstaculo = current_maze[new_y_obstaculo][new_x_obstaculo]

                # Veiricação de colisão entre obstáculos
                for i in range(len(obstaculos_din_grid)):
                    if new_x_obstaculo == obstaculo_din_target_grid[i][0] and new_y_obstaculo == obstaculo_din_target_grid[i][1]:
                        obstaculos_din_grid[index][4] = False
                        obstaculo_din_target_grid[index] = list(obstaculos_din_grid[index])

                if not obstaculos_din_grid[index][4] == False: # Coloquei essa condição por causa da Veiricação de colisão entre obstáculos

                    if new_x_obstaculo == player_grid[0] and new_y_obstaculo == player_grid[1]:
                        print("entra ?")
                        #player_lives -= 1
                        # Reset player to start position after hitting an obstacle
                        #player_grid = [1, 1]
                        #player_pos = [player_grid[0] * TILE_SIZE, player_grid[1] * TILE_SIZE]
                        #colided = True

                        target_grid = list(player_grid)
                        moving = False
                        obstaculos_din_grid[index][4] = False
                        obstaculo_din_target_grid[index] = list(obstaculos_din_grid[index])
                    elif celll_obstaculo == 1:
                        if (dx == 0 and dy == -1):  #UP
                            dy = 1 # Se tava indo pra cima, vai para baixo
                            obstaculo_din_target_grid[index][3] = dy
                        elif (dx == 0 and dy == 1): #DOWN
                            dy = -1 # Se tava indo pra baixo, vai para cima
                            obstaculo_din_target_grid[index][3] = dy
                        elif dx == -1 and dy == 0:  #LEFT
                            dx = 1 # Se tava indo pra esquerda, vai para direita
                            obstaculo_din_target_grid[index][2] = dx
                        elif dx == 1 and dy == 0:   #RIGHT
                            dx = -1 # Se tava indo pra direita, vai para esquerda
                            obstaculo_din_target_grid[index][2] = dx
                    else:

                        #Posição alvo do obstaculo no grid
                        obstaculo_din_target_grid[index][0] = new_x_obstaculo
                        obstaculo_din_target_grid[index][1] = new_y_obstaculo
                    

        # ---------------------------------------------------------------------
        # Início de movimento (se não estiver se movendo agora)
        # ---------------------------------------------------------------------
        if not moving and not game_over and not win:
            keys = pygame.key.get_pressed()
            dx, dy = 0, 0
            global player_direction
            if keys[pygame.K_UP]:
                dx, dy = 0, -1
                player_direction = "up"
            elif keys[pygame.K_DOWN]:
                dx, dy = 0, 1
                player_direction = "down"
            elif keys[pygame.K_LEFT]:
                dx, dy = -1, 0
                player_direction = "left"
            elif keys[pygame.K_RIGHT]:
                dx, dy = 1, 0
                player_direction = "right"
            
                

            if dx != 0 or dy != 0:
                new_x = player_grid[0] + dx
                new_y = player_grid[1] + dy
                if 0 <= new_x < COLS and 0 <= new_y < ROWS:
                    for index_obstaculo in range(len(obstaculo_din_target_grid)):
                        new_x_obstaculo = obstaculo_din_target_grid[index_obstaculo][0]
                        new_y_obstaculo = obstaculo_din_target_grid[index_obstaculo][1]
                        if (new_x == new_x_obstaculo and new_y == new_y_obstaculo):
                            print("if 1")
                            if b_count > 0:
                                target_grid = [new_x, new_y]
                                b_count -= 1
                                use_sound.play()  # Toca o som ao usar o power-up
                                moving = True
                            else: # Joga o boneco para tras
                                print("bug do if 1")
                                new_x = player_grid[0]
                                new_y = player_grid[1]
                                target_grid = [new_x, new_y]
                                moving == True
                        elif (player_grid[0] == new_x_obstaculo and player_grid[1] == new_y_obstaculo):
                            print("if 2")
                            if b_count > 0:
                                target_grid = [new_x, new_y]
                                b_count -= 1
                                use_sound.play()  # Toca o som ao usar o power-up
                                moving = True
                            else: # Joga o boneco para tras
                                print("bug do if 2")
                                new_x = player_grid[0]
                                new_y = player_grid[1] 
                                obstaculos_din_grid[index_obstaculo][4] = False
                                obstaculo_din_target_grid[index_obstaculo] = list(obstaculos_din_grid[index_obstaculo])
                                moving == False
                        else:
                            if (obstaculo_din_target_grid[index_obstaculo][0] == 2):
                                x = 10
                                print("Novo bug Jam")
                                print("Posição Atual Jogador")
                                print(player_grid)
                                print("Posição Target Jogador")
                                var_1 = [new_x,new_y]
                                print(var_1)
                                print("Posição Atual Obstaculos")
                                print(obstaculos_din_grid[index_obstaculo])
                                print("Posição Target Obstaculos")
                                print(obstaculo_din_target_grid[index_obstaculo])
                                



                            
                    cell = current_maze[new_y][new_x]
                    # Caminho livre, power-up ou destino
                    if cell in (0, 8, 3, 4, 5, 7, 9) and moving == False:
                        target_grid = [new_x, new_y]
                        moving = True
                        movement_sound.play() # Toca o som de movimento
                    # Obstáculo transponível (2) com B disponível
                    elif cell == 2 and b_count > 0 and moving == False:
                        target_grid = [new_x, new_y]
                        moving = True
                        b_count -= 1
                        use_sound.play()  # Toca o som ao usar o power-up
                    # Parede (1) => tentar salto (2 células) se tiver C disponível
                    elif cell == 1 and moving == False:
                        jump_x = player_grid[0] + 2 * dx
                        jump_y = player_grid[1] + 2 * dy
                        if jump_count > 0 and 0 <= jump_x < COLS and 0 <= jump_y < ROWS:
                            landing_cell = current_maze[jump_y][jump_x]
                            # Pode pousar em 0, 8, 3, 4, 5, 7 ou 2 (desde que haja B)
                            if landing_cell in (0, 8, 3, 4, 5, 7, 9):
                                target_grid = [jump_x, jump_y]
                                moving = True
                                jump_count -= 1
                                use_sound.play()  # Toca o som ao usar o power-up
                            elif landing_cell == 2 and b_count > 0:
                                target_grid = [jump_x, jump_y]
                                moving = True
                                jump_count -= 1
                                b_count -= 1
                                use_sound.play()  # Toca o som ao usar o power-up
                
        # Movimentação dos obstáculos dinâmicos - pixel
        for index in range(len(obstaculo_din_target_grid)):

            #if not (collision and index in list_collided_obstacle_index):

            _, _, _, _, moveu = obstaculo_din_target_grid[index]

            if moveu == True:

                # Calcular a distância até o destino
                obstaculo_target_px = (obstaculo_din_target_grid[index][0] * TILE_SIZE, obstaculo_din_target_grid[index][1] * TILE_SIZE)
                dx_obstaculo_px = obstaculo_target_px[0] - obstaculo_din_pos_px[index][0]
                dy_obstaculo_px = obstaculo_target_px[1] - obstaculo_din_pos_px[index][1]
                distance_obstaculo = math.hypot(dx_obstaculo_px, dy_obstaculo_px)
                
                # Movimentação suave
                # Distancia a percorrer = Velocidade (px/seg) * Intervalo de tempo (frame)
                move_obstaculo_dist = SPEED_OBSTACLE * movement_dt  

                if distance_obstaculo < 1e-5:
                    # Chegou ao destino em pixels
                    obstaculo_din_pos_px[index][0],  obstaculo_din_pos_px[index][1] = obstaculo_target_px
                    obstaculo_din_target_grid[index][4] = False
                    obstaculos_din_grid[index] = list(obstaculo_din_target_grid[index])

                # Ainda não chegou, avança gradualmente
                elif move_obstaculo_dist < distance_obstaculo:
                    obstaculo_din_pos_px[index][0] += (dx_obstaculo_px / distance_obstaculo) * move_obstaculo_dist 
                    obstaculo_din_pos_px[index][1] += (dy_obstaculo_px / distance_obstaculo) * move_obstaculo_dist
                # Consegue chegar neste frame
                else:
                    obstaculo_din_pos_px[index][0],  obstaculo_din_pos_px[index][1] = obstaculo_target_px
                    obstaculo_din_target_grid[index][4] = False
                    obstaculos_din_grid[index] = list(obstaculo_din_target_grid[index])

        # ---------------------------------------------------------------------
        # Movimentação suave (usando movement_dt)
        # ---------------------------------------------------------------------
        target_pixel = (target_grid[0] * TILE_SIZE, target_grid[1] * TILE_SIZE)
        if moving:
            dx_px = target_pixel[0] - player_pos[0]
            dy_px = target_pixel[1] - player_pos[1]
            distance = math.hypot(dx_px, dy_px)

            if distance < 1e-5:
                # Chegou ao destino em pixels
                
                player_pos[0], player_pos[1] = target_pixel
                player_grid = list(target_grid)
                moving = False

                # Verificar se há power-up ou destino nessa célula
                current_cell = current_maze[player_grid[1]][player_grid[0]]
                if current_cell == 3:
                    # Power-up A => ativa slow
                    time_slow_active = True
                    time_slow_end = pygame.time.get_ticks() / 1000.0 + 10
                    current_maze[player_grid[1]][player_grid[0]] = 0
                elif current_cell == 4:
                    b_count += 1
                    current_maze[player_grid[1]][player_grid[0]] = 0
                elif current_cell == 5:
                    jump_count += 1
                    current_maze[player_grid[1]][player_grid[0]] = 0
                elif current_cell == 7:
                    win = True

            else:
                # Ainda não chegou, avança gradualmente
                move_dist = SPEED_PLAYER * movement_dt
                if move_dist < distance:
                    player_pos[0] += (dx_px / distance) * move_dist
                    player_pos[1] += (dy_px / distance) * move_dist
                else:
                    # Consegue chegar neste frame
                    
                    player_pos[0], player_pos[1] = target_pixel
                    player_grid = list(target_grid)
                    moving = False

                    # Verifica power-up/destino
                    current_cell = current_maze[player_grid[1]][player_grid[0]]
                    if current_cell == 30:
                        time_slow_active = True
                        time_slow_end = pygame.time.get_ticks() / 1000.0 + 10
                        current_maze[player_grid[1]][player_grid[0]] = 0
                        pickup_sound.play()
                    elif current_cell == 3:
                        print("AChoou A ?")
                        remaining_time += 15
                        current_maze[player_grid[1]][player_grid[0]] = 0
                        pickup_sound.play()
                    elif current_cell == 4:
                        b_count += 1
                        current_maze[player_grid[1]][player_grid[0]] = 0
                        pickup_sound.play()
                    elif current_cell == 5:
                        jump_count += 1
                        current_maze[player_grid[1]][player_grid[0]] = 0
                        pickup_sound.play()
                    elif current_cell == 7:
                        win = True
                    elif current_cell == 9:
                        SPEED_PLAYER = 30
                    else:
                        SPEED_PLAYER = 100

        

            


        # ---------------------------------------------------------------------
        # Atualizar tempo (usando timer_dt)
        # ---------------------------------------------------------------------
        if not game_over and not win:
            remaining_time -= timer_dt
            if remaining_time <= 0:
                game_over = True

        # ---------------------------------------------------------------------
        # Verifica distância até o destino via BFS (para mostrar no HUD)
        # ---------------------------------------------------------------------
        path_dist = bfs_distance(current_maze, (player_grid[0], player_grid[1]),
                                 destination, b_count, jump_count)
        
        dist_x = destination[0] - player_grid[0]
        dist_y = destination[1] - player_grid[1]
            
        euclidian_dist = math.hypot(dist_x, dist_y)


        # Atualiza o volume da música com base na distância
        if euclidian_dist is not None:
            max_distance = math.hypot(COLS - 1, ROWS - 1)
            volume = (max_distance - euclidian_dist) / max_distance
            volume = max(0.0, min(1.0, volume))
            pygame.mixer.music.set_volume(volume)
            if play_drums:
                main_drums.set_volume(volume)
            if play_melody:
                main_melody.set_volume(volume)

        # global emocao
        # if  remaining_time < 30 and not emocao:
        #     emocao = True
        #     pygame.mixer.music.stop()
        #     pygame.mixer.music.load("sons/main_music_2.mp3")
        #     pygame.mixer.music.play(loops=0, start=141)


        elif euclidian_dist > 30 and emocao:
            emocao = False  # Corrigido para garantir que a variável volte ao estado correto
            pygame.mixer.music.play(loops=0, start=10)


        # ---------------------------------------------------------------------
        # Desenhar todo o labirinto na world_surface (com as imagens)
        # ---------------------------------------------------------------------
        world_surface.fill((0, 0, 0))
        for row in range(ROWS):
            for col in range(COLS):
                cell = current_maze[row][col]
                x = col * TILE_SIZE
                y = row * TILE_SIZE

                if cell in tile_images:
                    world_surface.blit(tile_images[cell], (x, y))
                else:
                    # Se não estiver no dicionário, desenha chão por padrão
                    world_surface.blit(floor_img, (x, y))

                # Se quiser ainda um contorno:
                # pygame.draw.rect(world_surface, (0, 0, 0), (x, y, TILE_SIZE, TILE_SIZE), 1)

        # Desenha o jogador (imagem em vez de círculo)
        #world_surface.blit(player_img, (player_pos[0], player_pos[1]))
        #world_surface.blit(player_frames[current_frame], (player_pos[0], player_pos[1]))
        # Desenha o jogador com o frame da direção atual
        if b_count > 0:
            frames_to_use = player_frames_B[player_direction]
        else:
            frames_to_use = player_frames[player_direction]

        frame_to_draw = frames_to_use[current_frame].copy()

        if b_count > 0:
            frame_to_draw.set_alpha(128)
 
        world_surface.blit(frame_to_draw, (player_pos[0], player_pos[1]))


         # Desenha os obstáculos móveis com animação direcional
        for i, obstaculo in enumerate(obstaculo_din_pos_px):
            x, y = obstaculo  # Posição atual em pixels
            # Obter a direção com base no vetor de movimento armazenado para o obstáculo
            # Se o obstáculo não estiver se movendo, usamos o último vetor ou um padrão
            dx = obstaculos_din_grid[i][2] if i < len(obstaculos_din_grid) else 0
            dy = obstaculos_din_grid[i][3] if i < len(obstaculos_din_grid) else 0
            direction = get_direction_from_vector(dx, dy)
            frame = obstacle_frames[direction][obstacle_current_frame]
            world_surface.blit(frame, (x, y))
        # global particles
        # # Desenha as partículas na superfície do mundo (world_surface) para que participem do efeito de câmera e zoom:
        # for particle in particles:
        #     particle.draw(world_surface)
        

        # ---------------------------------------------------------------------
        # Câmera (recorte e zoom)
        # ---------------------------------------------------------------------
        view_w = SCREEN_WIDTH // ZOOM
        view_h = SCREEN_HEIGHT // ZOOM
        player_center = (player_pos[0] + TILE_SIZE // 2, player_pos[1] + TILE_SIZE // 2)
        camera_rect = pygame.Rect(0, 0, view_w, view_h)
        camera_rect.center = player_center
        camera_rect = clamp_camera(camera_rect, WIDTH, HEIGHT)

        # Recorta da world_surface e redimensiona para a tela
        camera_surface = world_surface.subsurface(camera_rect).copy()
        scaled_surface = pygame.transform.scale(camera_surface, (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(scaled_surface, (0, 0))

        
        # Dentro do loop principal, antes de atualizar e desenhar:
        # if random.random() < 0.05:
        #     for _ in range(3):
        #         # Cria partículas na parte superior da área visível (ou um pouco acima, para efeito de "caída")
        #         spawn_x = random.randint(camera_rect.left, camera_rect.right)
        #         spawn_y = camera_rect.top - 10  # 10 pixels acima da área visível
        #         new_particle = Particle((spawn_x, spawn_y))
        #         particles.append(new_particle)
        # Atualiza cada partícula
        # for particle in particles:
        #     particle.update(movement_dt)  # 'movement_dt' é o delta time do frame

        # Remove partículas que já expiraram
        # particles = [p for p in particles if not p.is_dead()]

        # ---------------------------------------------------------------------
        # HUD
        # ---------------------------------------------------------------------
        #hud_rect = pygame.Rect(5, 5, 240, 70)
        #pygame.draw.rect(screen, (255, 255, 255), hud_rect)

        # Mostra o tempo
        #timer_color = (255, 165, 0) if time_slow_active else (0, 0, 0)
        #timer_text = font.render(f"Tempo: {int(remaining_time)}", True, timer_color)
        #screen.blit(timer_text, (10, 10))

        # Mostra a distância até o destino
        #if euclidian_dist is not None:
            #distance_text = font.render(f"Distância: {euclidian_dist:.2f}", True, (0, 0, 0))
        #else:
            #distance_text = font.render("Distância: N/A", True, (0, 0, 0))
        #screen.blit(distance_text, (10, 30))

        # Status dos power-ups
        # powerup_text = font.render(
        #     f"Power-ups: B={b_count} | C={jump_count} | Slow={'Ativo' if time_slow_active else 'Off'}",
        #     True, (0, 0, 0)
        # )
        # screen.blit(powerup_text, (10, 50))
        global sound_game_over_played
        global sound_win_played


        if colided:
            colision_image_rect = colision_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(colision_image, colision_image_rect)

        # Mensagens de fim de jogo
        if game_over:
            # Centraliza a imagem de game over na tela
            game_over_rect = game_over_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(game_over_image, game_over_rect)
            pygame.mixer.music.stop()
            if not sound_game_over_played:
                game_over_sound.play()
                sound_game_over_played = True
            if pygame.mixer.get_busy() == False:
                sound_game_over_played = False
                return False
        if win:
            # Centraliza a imagem de vitória na tela
            win_rect = win_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(win_image, win_rect)
            pygame.mixer.music.stop()
            main_drums.stop()
            main_melody.stop()
            if not sound_win_played:
                win_sound.play()
                sound_win_played = True
            print("Lsdasdsadasdassdp")
            if pygame.mixer.get_busy() == False:
                current_level += 1
                sound_win_played = False
                print("Level up")
                return True

        # Define a posição onde a HUD deve aparecer na tela (por exemplo, no topo central)
        hud_rect = hud_background.get_rect()
        hud_rect.center = (SCREEN_WIDTH // 2, 40)  # 40 pode ser ajustado conforme necessário

        # Renderiza o texto do tempo em branco e com a fonte em negrito
        time_text = font.render(f"{int(remaining_time)}", True, (255, 255, 255))

        # Centraliza o texto na imagem do hud
        text_rect = time_text.get_rect(center=hud_background.get_rect().center)

        # Desenha a imagem do HUD na tela
        screen.blit(hud_background, hud_rect)
        # Desenha o texto do tempo em cima da imagem; ajuste a posição com base em hud_rect
        screen.blit(time_text, (hud_rect.left + text_rect.left, hud_rect.top + text_rect.top))

        pygame.display.flip()

if __name__ == "__main__":

    # Add more levels as needed

    if game_level():
        ROWS = len(current_maze)
        COLS = len(current_maze[0])
        game_level()
