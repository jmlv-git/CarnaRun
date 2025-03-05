import pygame, sys, math
from collections import deque

# Configurações do mapa
# Valores das células:
# 0: espaço livre
# 1: parede (bloqueada, a menos que o jogador tenha power-up C para pular)
# 2: obstáculo "transponível" (só pode ser cruzado se o jogador tiver power-up B)
# 3: power-up A – desacelera o tempo por 10 segundos (duas cores: vermelho + amarelo)
# 4: power-up B – permite transpor 1 obstáculo transponível (duas cores: verde + vermelho)
# 5: power-up C – permite pular sobre uma parede/obstáculo (duas cores: vermelho + azul escuro)
# 7: destino (chegada) (verde)
# 8: partida (inicial) (azul)
maze = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,8,0,0,0,0,2,0,0,0,0,0,0,0,1],
    [1,0,1,1,1,0,1,1,1,1,1,0,1,0,1],
    [1,0,1,3,1,0,0,0,4,0,1,0,1,0,1],
    [1,0,1,0,1,1,1,0,1,0,1,0,1,0,1],
    [1,0,0,0,0,0,1,0,1,0,1,0,0,0,1],
    [1,1,1,1,1,0,1,0,1,0,1,1,1,0,1],
    [1,0,0,0,1,0,0,0,1,0,0,0,1,0,1],
    [1,0,1,0,1,1,1,1,1,1,1,0,1,0,1],
    [1,0,1,0,0,0,0,0,0,0,1,0,1,0,1],
    [1,0,1,1,1,1,1,1,1,0,1,0,1,0,1],
    [1,0,0,0,0,0,0,0,1,0,0,7,1,5,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
]
ROWS = len(maze)
COLS = len(maze[0])
TILE_SIZE = 40
WIDTH = COLS * TILE_SIZE
HEIGHT = ROWS * TILE_SIZE

# Cores
COLOR_FREE     = (200,200,200)
COLOR_WALL     = (50,50,50)
COLOR_OBSTACLE = (139,69,19)

# Power-ups com duas cores:
# Power-up A: Vermelho + Amarelo
COLOR_PU_A_1 = (255, 0, 0)    # vermelho
COLOR_PU_A_2 = (255, 255, 0)  # amarelo
# Power-up B: Verde + Vermelho
COLOR_PU_B_1 = (0, 255, 0)    # verde
COLOR_PU_B_2 = (255, 0, 0)    # vermelho
# Power-up C: Vermelho + Azul Escuro
COLOR_PU_C_1 = (255, 0, 0)    # vermelho
COLOR_PU_C_2 = (0, 0, 139)    # azul escuro

# Bloco de partida e chegada
COLOR_START = (0, 0, 255)  # azul
COLOR_DEST  = (0, 255, 0)  # verde

def is_traversable(cell, b_count, jump_count):
    if cell in (0, 8, 3, 4, 5, 7):
        return True
    if cell == 2 and b_count > 0:
        return True
    if cell == 1 and jump_count > 0:
        return True
    return False

def bfs_distance(maze, start, end, b_count, jump_count):
    """
    Faz uma busca em largura para verificar se existe um caminho.
    Retorna a distância em passos se houver caminho, ou None se não houver.
    (Podemos manter esse retorno em passos apenas para sabermos se é None ou não.)
    """
    queue = deque()
    visited = set()
    queue.append((start[0], start[1], 0))
    visited.add((start[0], start[1]))
    while queue:
        x, y, d = queue.popleft()
        if (x, y) == end:
            return d  # encontrou caminho
        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < COLS and 0 <= ny < ROWS and (nx, ny) not in visited:
                cell = maze[ny][nx]
                if is_traversable(cell, b_count, jump_count):
                    visited.add((nx, ny))
                    queue.append((nx, ny, d+1))
    return None  # sem caminho

def find_destination(maze):
    for row in range(ROWS):
        for col in range(COLS):
            if maze[row][col] == 7:
                return (col, row)
    return None

def clamp_camera(camera_rect, world_width, world_height):
    if camera_rect.left < 0:
        camera_rect.left = 0
    if camera_rect.top < 0:
        camera_rect.top = 0
    if camera_rect.right > world_width:
        camera_rect.right = world_width
    if camera_rect.bottom > world_height:
        camera_rect.bottom = world_height
    return camera_rect

def main():
    pygame.init()
    SCREEN_WIDTH = 600
    SCREEN_HEIGHT = 520
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Jogo do Labirinto com Câmera e Movimentação Suave")
    clock = pygame.time.Clock()
    ZOOM = 3

    world_surface = pygame.Surface((WIDTH, HEIGHT))

    # Estado inicial do jogador
    player_grid = [1, 1]
    player_pos = [player_grid[0] * TILE_SIZE, player_grid[1] * TILE_SIZE]
    target_grid = list(player_grid)
    moving = False

    b_count = 0     
    jump_count = 0  
    time_slow_active = False
    time_slow_end = 0

    total_time = 120
    remaining_time = total_time

    game_over = False
    win = False

    destination = find_destination(maze)

    font = pygame.font.SysFont(None, 24)
    SPEED = 200

    while True:
        dt = clock.tick(60) / 1000

        # Se o slow estiver ativo, reduz o dt
        if time_slow_active:
            dt *= 0.5
            if pygame.time.get_ticks() / 1000 >= time_slow_end:
                time_slow_active = False

        # Eventos de sair
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # (MUDANÇA 1) -------------------------------------------
        # Agora, checamos continuamente as teclas pressionadas.
        if not moving and not game_over and not win:
            keys = pygame.key.get_pressed()
            dx, dy = 0, 0
            if keys[pygame.K_UP]:
                dx, dy = 0, -1
            elif keys[pygame.K_DOWN]:
                dx, dy = 0, 1
            elif keys[pygame.K_LEFT]:
                dx, dy = -1, 0
            elif keys[pygame.K_RIGHT]:
                dx, dy = 1, 0

            if dx != 0 or dy != 0:
                new_x = player_grid[0] + dx
                new_y = player_grid[1] + dy
                if 0 <= new_x < COLS and 0 <= new_y < ROWS:
                    cell = maze[new_y][new_x]
                    # Checa se pode andar normalmente
                    if cell in (0, 8, 3, 4, 5, 7):
                        target_grid = [new_x, new_y]
                        moving = True
                    elif cell == 2 and b_count > 0:
                        target_grid = [new_x, new_y]
                        moving = True
                        b_count -= 1
                    elif cell == 1:
                        # Verifica salto (pular 2 células)
                        jump_x = player_grid[0] + 2 * dx
                        jump_y = player_grid[1] + 2 * dy
                        if jump_count > 0 and 0 <= jump_x < COLS and 0 <= jump_y < ROWS:
                            landing_cell = maze[jump_y][jump_x]
                            if landing_cell in (0, 8, 3, 4, 5, 7):
                                target_grid = [jump_x, jump_y]
                                moving = True
                                jump_count -= 1
                            elif landing_cell == 2 and b_count > 0:
                                target_grid = [jump_x, jump_y]
                                moving = True
                                jump_count -= 1
                                b_count -= 1
        # (FIM da MUDANÇA 1) ------------------------------------

        # Movimentação suave
        target_pixel = (target_grid[0] * TILE_SIZE, target_grid[1] * TILE_SIZE)
        if moving:
            dx = target_pixel[0] - player_pos[0]
            dy = target_pixel[1] - player_pos[1]
            distance = math.hypot(dx, dy)
            if distance < 1e-5:
                player_pos[0], player_pos[1] = target_pixel
                player_grid = list(target_grid)
                moving = False
                current_cell = maze[player_grid[1]][player_grid[0]]
                if current_cell == 3:
                    time_slow_active = True
                    time_slow_end = pygame.time.get_ticks() / 1000 + 10
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
                move_dist = SPEED * dt
                if move_dist < distance:
                    player_pos[0] += dx / distance * move_dist
                    player_pos[1] += dy / distance * move_dist
                else:
                    # Chegou ao destino
                    player_pos[0], player_pos[1] = target_pixel
                    player_grid = list(target_grid)
                    moving = False
                    current_cell = maze[player_grid[1]][player_grid[0]]
                    if current_cell == 3:
                        time_slow_active = True
                        time_slow_end = pygame.time.get_ticks() / 1000 + 10
                        maze[player_grid[1]][player_grid[0]] = 0
                    elif current_cell == 4:
                        b_count += 1
                        maze[player_grid[1]][player_grid[0]] = 0
                    elif current_cell == 5:
                        jump_count += 1
                        maze[player_grid[1]][player_grid[0]] = 0
                    elif current_cell == 7:
                        win = True

        # Atualiza tempo
        if not game_over and not win:
            remaining_time -= dt
            if remaining_time <= 0:
                game_over = True

        # (MUDANÇA 2) -------------------------------------------
        # Em vez de exibir a distância em passos do BFS,
        # usamos o BFS somente para verificar se *existe* caminho (ou não).
        path_dist = bfs_distance(maze, (player_grid[0], player_grid[1]), destination, b_count, jump_count)
        if path_dist is not None:
            # Calcula distância euclidiana
            dist_x = destination[0] - player_grid[0]
            dist_y = destination[1] - player_grid[1]
            euclidian_dist = math.hypot(dist_x, dist_y)
        else:
            euclidian_dist = None
        # (FIM da MUDANÇA 2) ------------------------------------

        # Desenha o labirinto
        world_surface.fill((0, 0, 0))
        for row in range(ROWS):
            for col in range(COLS):
                cell = maze[row][col]
                rect = pygame.Rect(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                if cell == 1:
                    pygame.draw.rect(world_surface, COLOR_WALL, rect)
                elif cell == 2:
                    pygame.draw.rect(world_surface, COLOR_OBSTACLE, rect)
                elif cell == 3:
                    left_rect = pygame.Rect(col*TILE_SIZE, row*TILE_SIZE, TILE_SIZE//2, TILE_SIZE)
                    right_rect = pygame.Rect(col*TILE_SIZE + TILE_SIZE//2, row*TILE_SIZE, TILE_SIZE - TILE_SIZE//2, TILE_SIZE)
                    pygame.draw.rect(world_surface, COLOR_PU_A_1, left_rect)
                    pygame.draw.rect(world_surface, COLOR_PU_A_2, right_rect)
                elif cell == 4:
                    left_rect = pygame.Rect(col*TILE_SIZE, row*TILE_SIZE, TILE_SIZE//2, TILE_SIZE)
                    right_rect = pygame.Rect(col*TILE_SIZE + TILE_SIZE//2, row*TILE_SIZE, TILE_SIZE - TILE_SIZE//2, TILE_SIZE)
                    pygame.draw.rect(world_surface, COLOR_PU_B_1, left_rect)
                    pygame.draw.rect(world_surface, COLOR_PU_B_2, right_rect)
                elif cell == 5:
                    left_rect = pygame.Rect(col*TILE_SIZE, row*TILE_SIZE, TILE_SIZE//2, TILE_SIZE)
                    right_rect = pygame.Rect(col*TILE_SIZE + TILE_SIZE//2, row*TILE_SIZE, TILE_SIZE - TILE_SIZE//2, TILE_SIZE)
                    pygame.draw.rect(world_surface, COLOR_PU_C_1, left_rect)
                    pygame.draw.rect(world_surface, COLOR_PU_C_2, right_rect)
                elif cell == 7:
                    pygame.draw.rect(world_surface, COLOR_DEST, rect)
                elif cell == 8:
                    pygame.draw.rect(world_surface, COLOR_START, rect)
                else:
                    pygame.draw.rect(world_surface, COLOR_FREE, rect)
                pygame.draw.rect(world_surface, (0, 0, 0), rect, 1)

        # Desenha o jogador (um círculo amarelo)
        player_rect = pygame.Rect(player_pos[0], player_pos[1], TILE_SIZE, TILE_SIZE)
        pygame.draw.ellipse(world_surface, (255, 255, 0), player_rect)

        # Ajusta câmera
        view_w = SCREEN_WIDTH // ZOOM
        view_h = SCREEN_HEIGHT // ZOOM
        player_center = (player_pos[0] + TILE_SIZE // 2, player_pos[1] + TILE_SIZE // 2)
        camera_rect = pygame.Rect(0, 0, view_w, view_h)
        camera_rect.center = player_center
        camera_rect = clamp_camera(camera_rect, WIDTH, HEIGHT)
        camera_surface = world_surface.subsurface(camera_rect).copy()
        scaled_surface = pygame.transform.scale(camera_surface, (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(scaled_surface, (0, 0))

        # HUD
        hud_rect = pygame.Rect(5, 5, 240, 70)
        pygame.draw.rect(screen, (255, 255, 255), hud_rect)
        timer_color = (255, 165, 0) if time_slow_active else (0, 0, 0)
        timer_text = font.render(f"Tempo: {int(remaining_time)}", True, timer_color)
        screen.blit(timer_text, (10, 10))

        # (MUDANÇA 2) Exibindo a distância euclidiana ou N/A
        if euclidian_dist is not None:
            distance_text = font.render(f"Distância: {euclidian_dist:.2f}", True, (0, 0, 0))
        else:
            distance_text = font.render("Distância: N/A", True, (0, 0, 0))
        screen.blit(distance_text, (10, 30))

        powerup_text = font.render(f"Power-ups: B={b_count} | C={jump_count} | Slow={'Ativo' if time_slow_active else 'Off'}", True, (0, 0, 0))
        screen.blit(powerup_text, (10, 50))

        if game_over:
            over_text = font.render("Tempo esgotado! Você perdeu!", True, (255, 0, 0))
            screen.blit(over_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2))
        if win:
            win_text = font.render("Parabéns! Você chegou ao destino!", True, (0, 255, 0))
            screen.blit(win_text, (SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2))

        pygame.display.flip()


if __name__ == "__main__":
    main()
