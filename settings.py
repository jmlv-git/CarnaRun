maze_phase_1 = [
   [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
   [1,8,0,0,0,0,0,0,0,0,0,0,1,4,0,0,0,1,1,0,0,0,0,0,0,0,1,0,0,1],
   [1,8,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,1,0,0,0,0,0,0,0,1,0,0,1],
   [1,1,1,1,1,1,1,0,9,1,0,0,1,1,1,1,0,1,1,0,1,1,1,1,1,1,1,0,0,1],
   [1,2,2,4,0,4,1,0,9,1,0,0,0,0,0,0,0,1,1,0,0,0,0,1,0,0,0,0,0,1],
   [1,0,2,0,2,4,1,0,9,1,0,0,0,2,0,0,0,1,1,0,0,0,0,1,0,0,0,0,0,1],
   [1,0,2,1,1,1,1,0,9,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,0,0,1],
   [1,0,0,0,0,0,0,0,9,1,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,1],
   [1,2,0,0,0,0,0,0,9,1,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,1],
   [1,1,1,1,0,0,1,1,1,1,0,0,1,1,1,1,1,1,1,2,1,1,1,1,1,1,1,1,1,1],
   [1,3,0,1,0,0,0,0,0,1,0,0,9,2,9,0,0,0,0,0,1,0,0,0,0,0,1,0,0,1],
   [1,0,0,1,0,0,0,0,0,1,0,0,9,9,9,9,0,0,0,0,1,0,0,0,0,0,1,0,0,1],
   [1,0,0,1,1,1,1,0,0,1,0,0,1,1,1,1,0,1,1,1,1,1,1,1,0,0,1,0,0,1],
   [1,0,0,1,0,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,1],
   [1,0,0,1,0,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,1],
   [1,0,0,1,0,0,1,1,1,1,0,0,1,0,0,1,1,1,1,1,1,1,0,1,1,1,1,0,0,1],
   [1,0,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,1],
   [1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1],
   [1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1],
   [1,0,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
   [1,2,0,1,1,1,1,0,0,1,1,1,1,0,1,1,0,1,1,1,1,0,0,1,0,0,1,1,1,1],
   [1,0,0,1,1,1,1,0,0,1,1,1,1,0,1,1,2,1,1,1,1,0,0,1,0,0,1,1,1,1],
   [1,0,2,1,0,0,1,0,0,0,0,0,0,0,1,1,0,1,1,0,0,0,0,1,0,2,0,0,0,1],
   [1,0,0,1,0,0,1,1,1,1,1,1,1,1,1,1,2,1,1,1,1,1,1,1,1,1,1,0,2,1],
   [1,2,0,1,0,0,0,0,0,1,0,0,0,0,1,1,0,2,2,0,0,0,0,0,0,0,0,0,0,1],
   [1,0,0,1,0,0,0,0,0,1,0,0,0,0,1,1,0,2,0,0,0,0,0,0,0,0,0,0,0,1],
   [1,0,2,1,1,1,1,0,0,1,0,0,1,0,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1],
   [1,0,0,2,0,4,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
   [1,2,0,0,0,2,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,7,1],
   [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
]

obstacles_moves_1 = [ 
        [2, 2, -1, 0, False], 
        [7, 2, 0, 1, False],
    ]

player_grid_1 = [1, 1]

maze_phase_2 = [
   [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
   [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,1],
   [1,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1],
   [1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,1],
   [1,2,1,0,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,2,4,1],
   [1,4,1,0,0,0,0,0,0,0,0,0,0,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,4,1],
   [1,4,1,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,2,2,0,0,0,0,0,0,0,1,4,1],
   [1,4,1,0,0,0,0,1,1,1,0,1,2,1,0,1,0,0,2,2,2,0,0,0,0,0,0,1,2,1],
   [1,2,1,0,0,0,0,1,0,1,0,1,0,0,0,0,0,2,2,0,0,0,2,0,0,2,0,1,4,1],
   [1,2,1,0,0,0,0,1,0,1,1,1,1,1,1,1,0,0,0,2,2,0,0,0,0,0,0,1,4,1],
   [1,4,1,0,0,0,0,1,0,1,1,1,4,1,1,1,0,2,2,2,1,0,2,0,2,0,0,1,4,1],
   [1,4,1,0,0,0,0,1,0,1,1,1,0,1,1,1,1,0,2,2,2,0,0,0,0,2,2,1,4,1],
   [1,4,1,0,1,1,1,1,0,1,1,1,0,1,1,1,0,2,0,2,0,2,2,0,0,0,0,1,2,1],
   [1,1,1,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,2,0,2,2,0,2,2,0,0,4,1],
   [1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
   [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
   [1,1,1,1,1,1,1,1,1,1,1,1,0,1,2,1,1,1,1,1,1,1,1,2,1,1,1,1,1,1],
   [1,0,0,0,0,0,0,0,0,0,0,2,0,0,2,1,0,0,0,0,0,0,1,0,1,1,0,1,4,1],
   [1,0,0,0,0,0,0,0,0,0,0,2,0,0,2,1,0,1,1,1,1,0,1,0,1,1,0,1,4,1],
   [1,0,1,1,1,1,1,1,1,2,1,1,1,1,2,1,0,1,0,2,0,0,1,0,1,1,0,1,4,1],
   [1,0,1,1,1,1,1,1,1,4,1,1,0,1,0,1,0,1,4,4,0,2,1,0,1,1,0,1,4,1],
   [1,0,1,0,0,0,0,0,1,4,1,1,0,1,0,1,0,1,4,2,0,0,1,0,1,1,0,1,4,1],
   [1,0,1,0,1,1,1,0,1,4,1,1,0,1,0,1,0,1,0,1,1,1,1,0,1,1,0,1,4,1],
   [1,0,1,0,1,7,1,0,1,4,1,1,0,1,0,1,0,1,0,2,4,4,1,0,1,1,0,1,4,1],
   [1,0,1,0,1,0,1,0,1,4,1,1,0,1,0,1,0,1,1,1,1,2,1,0,1,1,0,1,1,1],
   [1,0,1,0,1,0,1,0,1,0,1,1,0,1,0,1,0,0,0,0,0,0,1,0,1,1,0,1,1,1],
   [1,0,1,0,1,0,1,0,0,0,1,1,0,1,0,1,0,1,1,1,1,1,1,0,1,1,0,1,1,1],
   [1,0,1,0,1,2,1,1,1,1,1,1,0,1,0,1,0,1,1,1,1,1,1,0,1,1,0,1,1,1],
   [1,0,0,0,1,2,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,1,1],
   [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
]
obstacles_moves_2 = [
            [2, 2, -1, 0, False], 
            [12, 16, 0, 1, False],
            [16, 5, 0, 1, False],
        ]

player_grid_2 = [14, 15]
