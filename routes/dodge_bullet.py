from flask import jsonify
import copy

bullets = {
    'u': [],
    'd': [],
    'l': [],
    'r': []
}

"""
.dd
r*.
...

[   [   ['.'], ['d'], ['d'] ], 
    [   ['r'], ['*'], ['.'] ], 
    [   ['.'], ['.'], ['.'] ]   ]
"""

# def check_bullets_remaining(bullets):
#     for direction in bullets.keys():
#         if len(bullets[direction]) == 0:
#             bullets.pop(direction, None)

def parse_map(text_map):
    return [list(row) for row in text_map.strip().split('\n')]

def get_bullets(game_map):
    for i in range(len(game_map)):
        for j in range(len(game_map[0])):
            # for bullet in game_map[i][j]:
            #     # print(f"[28]\t bullet = {bullet}")
            bullet = game_map[i][j]
            if bullet in bullets.keys():
                bullets[bullet].append((j, i))
                
def find_player(game_map):
    # print(f"\n\n[DEBUG] Enter find_player")
    for i, row in enumerate(game_map):
        for j, cell in enumerate(row):
            if cell[0] == '*':
                return i, j
    # print(f"[DEBUG] Exit find_player\n\n")

def is_valid_move(game_map, x, y):
    return 0 <= y and y < len(game_map) and 0 <= x and x < len(game_map[0])

def completely_safe(game_map, x, y):
    for bullet_direction in bullets:
        if bullet_direction == 'u' or bullet_direction == 'd':
            for bullet_x, bullet_y in bullets[bullet_direction]:
                if bullet_x == x:
                    return False
        elif bullet_direction == 'l' or bullet_direction == 'r':
            for bullet_x, bullet_y in bullets[bullet_direction]:
                if bullet_y == y:
                    return False
                
    return True
            
    

"""
j0 j1 j2 j3 I0
j0 j1 j2 j3 I1
j0 j1 j2 j3 I2
j0 j1 j2 j3 I3
"""


def move_bullets(game_map):
    global bullets
    new_map = copy.deepcopy(game_map)
    # i = y, x = j
    for i in range(len(game_map)):
        for j in range(len(game_map[0])):
            for bullet_direction in game_map[i][j]:
                if bullet_direction == 'u':
                    if is_valid_move(game_map, j, i-1):
                        new_map[i-1][j] += 'u'
                        bullets['u'].append((j, i-1))
                    # new_map[i][j].remove('u')
                    new_map[i][j] = new_map[i][j].replace('u', '')
                    bullets['u'].remove((j, i))
                elif bullet_direction == 'd':
                    # print(f"\n[DEBUG] [D] [BEFORE] bullets = {bullets}")
                    if is_valid_move(game_map, j, i+1):
                        new_map[i+1][j] += 'd'
                        bullets['d'].append((j, i+1))
                    new_map[i][j] = new_map[i][j].replace('d', '')
                    # bullets['d'].remove((i, j))
                    bullets['d'].remove((j, i))
                    # print(f"[DEBUG] [D] [AFTER] bullets = {bullets}\n")
                elif bullet_direction == 'l':
                    if is_valid_move(game_map, j-1, i):
                        new_map[i][j-1] += 'l'
                        bullets['l'].append((j-1, i))
                    # new_map[i][j].remove('l')
                    new_map[i][j] = new_map[i][j].replace('l', '')
                    # bullets['l'].remove((i, j))
                    bullets['l'].remove((j, i))
                elif bullet_direction == 'r':
                    # print(f"\n[DEBUG] [R] [BEFORE] bullets = {bullets}")
                    if is_valid_move(game_map, j+1, i):
                        # new_map[i+1][j].append('r')
                        new_map[i][j+1] += 'r'
                        bullets['r'].append((j+1, i))
                    # new_map[i][j].remove('r')
                    new_map[i][j] = new_map[i][j].replace('r', '')
                    bullets['r'].remove((j, i))
                    # print(f"[DEBUG] [R] [AFTER] bullets = {bullets}\n")
    
    return new_map

def is_safe(game_map, x, y):
    return game_map[y][x] == '.'

def find_safe_path(game_map, start_x, start_y):
    # print(f"\n\n[DEBUG] Enter find_safe_path")
    global bullets
    
    path = []
    cur_x, cur_y = start_x, start_y

    while (len(bullets['u']) > 0 or len(bullets['d']) > 0 or len(bullets['l']) > 0 or len(bullets['r']) > 0) and not completely_safe(game_map, cur_x, cur_y):
        new_map = move_bullets(game_map)
        game_map = new_map
        tmp_path = ''
        
        # print(f"\n\n[DEBUG] game_map = {game_map}")
        
        possible_moves = [(cur_x + 1, cur_y, 'r'), (cur_x - 1, cur_y, 'l'), (cur_x, cur_y + 1, 'd'), (cur_x, cur_y - 1, 'u')]
        has_valid_move = False
        for x, y, direction in possible_moves:
            if is_valid_move(game_map, x, y) and is_safe(game_map, x, y):
                # print(f"\n\n[DEBUG] Move from ({cur_x}, {cur_y}) to ({x}, {y})")
                # print(f"[DEBUG] bullets = {bullets}\n\n")
                tmp_path = direction
                cur_x, cur_y = x, y
                has_valid_move = True
                break
        
        if has_valid_move:
            path.append(tmp_path)
        else:
            # print(f"[DEBUG] Exit find_safe_path because no valid moves\n\n")
            return None
    
    # print(f"[DEBUG] Exit find_safe_path because no more bullets\n\n")
    return path


def solution(request):
    game_map = parse_map(request)
    
    # print(f"\n\n[DEBUG] game_map = {game_map}")
    
    
    get_bullets(game_map)
    
    # print(f"\n\n[DEBUG] bullets = {bullets}")
    player_pos = find_player(game_map)

    start_x, start_y = player_pos
    safe_path = find_safe_path(game_map, start_x, start_y)

    return jsonify({"instructions": safe_path})
    # if safe_path is None:
    #     return jsonify({"instructions": None})
    # else:
    #     return jsonify({"instructions": safe_path})


