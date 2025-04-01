import settings

class Level:
        def __init__(self, maze, player_start, obstacles):
            self.maze = maze
            self.player_start = player_start
            self.obstacles = obstacles

levels = []

level_1 = Level(
        maze=settings.maze_phase_1,
        player_start=settings.player_grid_1,
        obstacles=settings.obstacles_moves_1
    )

levels.append(level_1)

level_2 = Level(
        maze=settings.maze_phase_2,
        player_start=settings.player_grid_2,
        obstacles=settings.obstacles_moves_2
    )

levels.append(level_2)    