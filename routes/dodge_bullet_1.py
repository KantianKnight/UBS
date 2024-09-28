from flask import jsonify
import copy

bullets = {
    'u': [],
    'd': [],
    'l': [],
    'r': []
}
# player_position = (0, 0)

"""
.dd
r*.
...
"""


def parse_map(text_map):
    return [list(row) for row in text_map.strip().split('\\n')]

def get_bullets_return_player_position(game_map):
    player_position= (0, 0)
    for i in range(len(game_map)):
        for j in range(len(game_map[0])):
            bullet = game_map[i][j]
            if bullet in bullets.keys():
                bullets[bullet].append((j, i))
            elif bullet == '*':
                player_position = (j, i)
    
    return player_position

def is_valid_move(game_map, x, y):
    return 0 <= y and y < len(game_map) and 0 <= x and x < len(game_map[0])

def completely_safe(x, y):
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
                    new_map[i][j] = new_map[i][j].replace('u', '')
                    bullets['u'].remove((j, i))
                elif bullet_direction == 'd':
                    if is_valid_move(game_map, j, i+1):
                        new_map[i+1][j] += 'd'
                        bullets['d'].append((j, i+1))
                    new_map[i][j] = new_map[i][j].replace('d', '')
                    bullets['d'].remove((j, i))
                elif bullet_direction == 'l':
                    if is_valid_move(game_map, j-1, i):
                        new_map[i][j-1] += 'l'
                        bullets['l'].append((j-1, i))
                    new_map[i][j] = new_map[i][j].replace('l', '')
                    bullets['l'].remove((j, i))
                elif bullet_direction == 'r':
                    if is_valid_move(game_map, j+1, i):
                        new_map[i][j+1] += 'r'
                        bullets['r'].append((j+1, i))
                    # new_map[i][j].remove('r')
                    new_map[i][j] = new_map[i][j].replace('r', '')
                    bullets['r'].remove((j, i))
    
    return new_map

def is_safe(game_map, x, y):
    return game_map[y][x] == '.'

def find_safe_path(game_map, start_x, start_y):
    global bullets
    
    path = []
    cur_x, cur_y = start_x, start_y

    while (len(bullets['u']) > 0 or len(bullets['d']) > 0 or len(bullets['l']) > 0 or len(bullets['r']) > 0) and not completely_safe(cur_x, cur_y):
        new_map = move_bullets(game_map)
        game_map = new_map
        tmp_path = ''
        
        possible_moves = [(cur_x + 1, cur_y, 'r'), (cur_x - 1, cur_y, 'l'), (cur_x, cur_y + 1, 'd'), (cur_x, cur_y - 1, 'u')]
        has_valid_move = False
        for x, y, direction in possible_moves:
            if is_valid_move(game_map, x, y) and is_safe(game_map, x, y):
                tmp_path = direction
                cur_x, cur_y = x, y
                has_valid_move = True
                break
        
        if has_valid_move:
            path.append(tmp_path)
        else:
            return None
    
    return path


def solution(request):
    global player_position
    game_map = parse_map(request)
    
    player_pos = get_bullets_return_player_position(game_map)
    
    start_x, start_y = player_pos
    safe_path = find_safe_path(game_map, start_x, start_y)

    # return jsonify({"instructions": safe_path})
    return safe_path

if __name__ == "__main__":
    # test_input = "....\\n.r*.\\n...."
    test_input = ".dd\\nr*.\\n..."
    print(solution(test_input))


