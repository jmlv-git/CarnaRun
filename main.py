import pygame
import sys
import math
from collections import deque

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

maze = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,8,0,0,1,0,0,1,0,0,0,0,0,0,1],
    [1,0,0,0,1,0,0,1,0,0,0,0,0,0,1],
    [1,0,0,3,1,0,0,1,1,1,1,2,2,2,1],
    [1,0,0,0,0,0,0,0,4,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,1,1,1,1,1,1,1,0,0,1,1,1],
    [1,0,0,0,1,0,0,0,1,0,0,0,1,0,1],
    [1,0,0,0,1,1,1,1,1,1,0,0,1,0,1],
    [1,0,0,0,0,0,0,0,0,1,0,0,1,0,1],
    [1,1,1,1,1,1,1,1,1,0,0,0,1,0,1],
    [1,0,0,0,0,0,0,0,1,0,0,7,1,5,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
]

pygame.init()
pygame.mixer.init()  # Inicializa o mixer, se ainda não estiver iniciado

# Carrega os efeitos sonoros (substitua os caminhos pelos arquivos corretos)
pickup_sound = pygame.mixer.Sound("sons/pickup_sound.wav")
use_sound = pygame.mixer.Sound("sons/use_sound.wav")
game_over_sound = pygame.mixer.Sound("sons/game_over.mp3")
win_sound = pygame.mixer.Sound("sons/win_sound.wav")

pygame.mixer.music.load("sons/main_music.mp3")
pygame.mixer.music.play(-1)  # -1 para repetir indefinidamente

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 520
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Carrega as imagens para as mensagens de vitória e derrota
win_image = pygame.image.load("imagens/win_image.png").convert_alpha()
game_over_image = pygame.image.load("imagens/game_over_image.png").convert_alpha()

# Opcional: Redimensione as imagens para o tamanho desejado
win_image = pygame.transform.scale(win_image, (300, 200))
game_over_image = pygame.transform.scale(game_over_image, (300, 200))

# Variável global inicial para direção
player_direction = "down"  # valor padrão

ROWS = len(maze)
COLS = len(maze[0])
TILE_SIZE = 16
WIDTH = COLS * TILE_SIZE
HEIGHT = ROWS * TILE_SIZE

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
# Funções de apoio
# ---------------------------------------------------------------
def is_traversable(cell, b_count, jump_count):
    """Verifica se a célula pode ser atravessada dadas as cargas de B e C."""
    if cell in (0, 8, 3, 4, 5, 7):
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

# ---------------------------------------------------------------
# Função principal (main)
# ---------------------------------------------------------------
def main():

    pygame.display.set_caption("Jogo do Labirinto com Câmera e Movimentação Suave")
    clock = pygame.time.Clock()
    ZOOM = 3

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
    dest_img = pygame.transform.scale(dest_img, (TILE_SIZE, TILE_SIZE))
    start_img = pygame.transform.scale(start_img, (TILE_SIZE, TILE_SIZE))
    player_img = pygame.transform.scale(player_img, (TILE_SIZE, TILE_SIZE))

    # Mapeamento de cada valor do labirinto para a imagem correspondente
    tile_images = {
        0: floor_img,
        1: wall_img,
        #2: obstacle_img,
        3: powerup_a_img,
        4: powerup_b_img,
        5: powerup_c_img,
        7: dest_img,
        8: start_img
    }

    # Lista de Obstáculos Dinâmicos
    moveu_obstaculo = False

    obstaculos_fixo_grid = [
        [11, 3], 
        [12, 3],
        [13, 3],
    ]

    obstaculo_fix_pos_px = [
        [obstaculos_fixo_grid[0][0] * TILE_SIZE, obstaculos_fixo_grid[0][1] * TILE_SIZE],
        [obstaculos_fixo_grid[1][0] * TILE_SIZE, obstaculos_fixo_grid[1][1] * TILE_SIZE],
        [obstaculos_fixo_grid[2][0] * TILE_SIZE, obstaculos_fixo_grid[2][1] * TILE_SIZE],
    ]

    obstaculos_din_grid = [
        [9, 1, 0, 1, moveu_obstaculo], 
        [6, 1, 0, 1, moveu_obstaculo],
        [1, 9, 0, -1, moveu_obstaculo],
        [2, 9, 0, -1, moveu_obstaculo],
        [13, 4, -1, 0, moveu_obstaculo]
    ]

    

    obstaculo_din_target_grid = list(obstaculos_din_grid)

    obstaculo_din_pos_px = [
        [obstaculos_din_grid[0][0] * TILE_SIZE, obstaculos_din_grid[0][1] * TILE_SIZE],
        [obstaculos_din_grid[1][0] * TILE_SIZE, obstaculos_din_grid[1][1] * TILE_SIZE],
        [obstaculos_din_grid[2][0] * TILE_SIZE, obstaculos_din_grid[2][1] * TILE_SIZE],
        [obstaculos_din_grid[3][0] * TILE_SIZE, obstaculos_din_grid[3][1] * TILE_SIZE],
        [obstaculos_din_grid[4][0] * TILE_SIZE, obstaculos_din_grid[4][1] * TILE_SIZE]
    ]

    # Estado de colisão
    collision = False
    collided_obstacle_index = None
    list_collided_obstacle_index = []

    # Estado inicial do jogador
    player_grid = [1, 1]  # posição em coordenadas de grid (coluna, linha)
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
    total_time = 20
    remaining_time = total_time
    game_over = False
    win = False

    # Encontrar a posição do destino (7)
    destination = find_destination(maze)

    # Configuração de fonte e velocidade de movimento
    font = pygame.font.SysFont(None, 24)
    SPEED = 100

    animation_timer = 0

    # Loop principal
    while True:
        # "real_dt" é o tempo real entre frames (usado na física e no movimento)
        real_dt = clock.tick(60) / 1000.0

        # "movement_dt" => usado na movimentação do jogador (não sofre slow)
        # "timer_dt"    => usado na contagem regressiva (pode sofrer slow)
        movement_dt = real_dt
        timer_dt = real_dt

        if moving:
            animation_timer += movement_dt
            if animation_timer >= animation_delay:
                animation_timer = 0
                current_frame = (current_frame + 1) % len(player_frames)
        else:
            current_frame = 0

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
            
        # Movimentação dos obstáculos dinâmicos - grid
        for index, obstaculo in enumerate(obstaculos_din_grid):
            
            pos_grid_x_obstaculo, pos_grid_y_obstaculo, dx, dy, moveu = obstaculo 

            if moveu == False:

                #Obstaculo irá se mover agora
                obstaculos_din_grid[index][4] = True; 
                obstaculo_din_target_grid[index][4] = True

                new_x_obstaculo = pos_grid_x_obstaculo + dx
                new_y_obstaculo = pos_grid_y_obstaculo + dy
                celll_obstaculo = maze[new_y_obstaculo][new_x_obstaculo]
                
                if celll_obstaculo == 1:

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
                    cell = maze[new_y][new_x]
                    # Caminho livre, power-up ou destino
                    if cell in (0, 8, 3, 4, 5, 7):
                        target_grid = [new_x, new_y]
                        if collision == True:
                            collision = False
                            for index in list_collided_obstacle_index:
                                maze[obstaculos_din_grid[index][1]][obstaculos_din_grid[index][0]] = 0
                            list_collided_obstacle_index = []
                        moving = True
                    # Obstáculo transponível (2) com B disponível
                    elif cell == 2 and b_count > 0:
                        target_grid = [new_x, new_y]
                        moving = True
                        b_count -= 1
                        use_sound.play()  # Toca o som ao usar o power-up
                    # Parede (1) => tentar salto (2 células) se tiver C disponível
                    elif cell == 1:
                        jump_x = player_grid[0] + 2 * dx
                        jump_y = player_grid[1] + 2 * dy
                        if jump_count > 0 and 0 <= jump_x < COLS and 0 <= jump_y < ROWS:
                            landing_cell = maze[jump_y][jump_x]
                            # Pode pousar em 0, 8, 3, 4, 5, 7 ou 2 (desde que haja B)
                            if landing_cell in (0, 8, 3, 4, 5, 7):
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

            if not (collision and index in list_collided_obstacle_index):

                _, _, _, _, moveu = obstaculo_din_target_grid[index]

                if moveu == True:

                    # Calcular a distância até o destino
                    obstaculo_target_px = (obstaculo_din_target_grid[index][0] * TILE_SIZE, obstaculo_din_target_grid[index][1] * TILE_SIZE)
                    dx_obstaculo_px = obstaculo_target_px[0] - obstaculo_din_pos_px[index][0]
                    dy_obstaculo_px = obstaculo_target_px[1] - obstaculo_din_pos_px[index][1]
                    distance_obstaculo = math.hypot(dx_obstaculo_px, dy_obstaculo_px)
                    
                    # Movimentação suave
                    # Distancia a percorrer = Velocidade (px/seg) * Intervalo de tempo (frame)
                    move_obstaculo_dist = SPEED * movement_dt  

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
                current_cell = maze[player_grid[1]][player_grid[0]]
                if current_cell == 3:
                    # Power-up A => ativa slow
                    time_slow_active = True
                    time_slow_end = pygame.time.get_ticks() / 1000.0 + 10
                    maze[player_grid[1]][player_grid[0]] = 0
                elif current_cell == 4:
                    b_count += 1
                    maze[player_grid[1]][player_grid[0]] = 0
                elif current_cell == 5:
                    jump_count += 1
                    maze[player_grid[1]][player_grid[0]] = 0
                elif current_cell == 7:
                    win = True

            else:
                # Ainda não chegou, avança gradualmente
                move_dist = SPEED * movement_dt
                if move_dist < distance:
                    player_pos[0] += (dx_px / distance) * move_dist
                    player_pos[1] += (dy_px / distance) * move_dist
                else:
                    # Consegue chegar neste frame
                    
                    player_pos[0], player_pos[1] = target_pixel
                    player_grid = list(target_grid)
                    moving = False

                    # Verifica power-up/destino
                    current_cell = maze[player_grid[1]][player_grid[0]]
                    if current_cell == 3:
                        time_slow_active = True
                        time_slow_end = pygame.time.get_ticks() / 1000.0 + 10
                        maze[player_grid[1]][player_grid[0]] = 0
                        pickup_sound.play()
                    elif current_cell == 4:
                        b_count += 1
                        maze[player_grid[1]][player_grid[0]] = 0
                        pickup_sound.play()
                    elif current_cell == 5:
                        jump_count += 1
                        maze[player_grid[1]][player_grid[0]] = 0
                        pickup_sound.play()
                    elif current_cell == 7:
                        win = True

        # Criar retângulo do jogador
        player_rect = pygame.Rect(player_pos[0], player_pos[1], TILE_SIZE, TILE_SIZE)

        # Criar retângulos para cada obstáculo dinâmico e verificar colisão
        for index in range(len(obstaculo_din_pos_px)):

            obstaculo_rect = pygame.Rect(
                obstaculo_din_pos_px[index][0], 
                obstaculo_din_pos_px[index][1], 
                TILE_SIZE, TILE_SIZE
            )
            
            if player_rect.colliderect(obstaculo_rect):
                if not collision:
                    print("Colisão detectada com obstáculo dinâmico!")
                    collision = True
                    collided_obstacle_index = index
                    list_collided_obstacle_index.append(collided_obstacle_index)
                    # Salva a posição do jogador no momento da colisão
                    #saved_player_pos = player_pos.copy()
                    # Salva a posição do obstáculo no momento da colisão
                    saved_obstacle_pos = obstaculo_din_pos_px[index].copy()
                    maze[obstaculos_din_grid[collided_obstacle_index][1]][obstaculos_din_grid[collided_obstacle_index][0]] = 2
        
                else:
                    if index not in list_collided_obstacle_index:
                        list_collided_obstacle_index.append(index) # Colidiu com outro obstaculo.
                        maze[obstaculos_din_grid[index][1]][obstaculos_din_grid[index][0]] = 2
                    
        # Se houver colisão, impede o movimento do obstáculo
        if collision:
            obstaculo_din_pos_px[collided_obstacle_index] = saved_obstacle_pos.copy()


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
        path_dist = bfs_distance(maze, (player_grid[0], player_grid[1]),
                                 destination, b_count, jump_count)
        if path_dist is not None:
            dist_x = destination[0] - player_grid[0]
            dist_y = destination[1] - player_grid[1]
            euclidian_dist = math.hypot(dist_x, dist_y)
        else:
            euclidian_dist = None

        # Atualiza o volume da música com base na distância
        if euclidian_dist is not None:
            max_distance = math.hypot(COLS - 1, ROWS - 1)
            volume = (max_distance - euclidian_dist) / max_distance
            volume = max(0.0, min(1.0, volume))
            pygame.mixer.music.set_volume(volume)

        # ---------------------------------------------------------------------
        # Desenhar todo o labirinto na world_surface (com as imagens)
        # ---------------------------------------------------------------------
        world_surface.fill((0, 0, 0))
        for row in range(ROWS):
            for col in range(COLS):
                cell = maze[row][col]
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
            
        world_surface.blit(frames_to_use[current_frame], (player_pos[0], player_pos[1]))


        #Desenha o obstáculo
        for obstaculo in obstaculo_din_pos_px:
            x, y = obstaculo  # Pegamos a posição do obstáculo
            world_surface.blit(player_img, (x, y))  # Desenha a imagem do obstáculo

        #Desenha o obstáculo fixos
        for obstaculo in obstaculo_fix_pos_px:
            x, y = obstaculo
            world_surface.blit(obstacle_img, (x, y))  # Desenha a imagem do obstáculo


        

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
        # Mensagens de fim de jogo
        if game_over:
            # Centraliza a imagem de game over na tela
            game_over_rect = game_over_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(game_over_image, game_over_rect)
            pygame.mixer.music.stop()
            if not sound_game_over_played:
                game_over_sound.play()
                sound_game_over_played = True
        if win:
            # Centraliza a imagem de vitória na tela
            win_rect = win_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(win_image, win_rect)
            pygame.mixer.music.stop()
            if not sound_win_played:
                win_sound.play()
                sound_win_played = True

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
    main()
