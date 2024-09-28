from flask import jsonify
import json

bullets = {
    'u': [],
    'd': [],
    'l': [],
    'r': []
}
max_x = 0
max_y = 0

"""
.dd
r*.
...
"""

"""
j0 j1 j2 j3 I0
j0 j1 j2 j3 I1
j0 j1 j2 j3 I2
j0 j1 j2 j3 I3
"""

def parse_map(text_map):
    return [list(row) for row in text_map.strip().split('\\n')]

def get_bullets_return_player_position(game_map):
    player_position= (0, 0)
    # print(f"\n\n[DEBUG] max_y = {max_y}, max_x = {max_x}\n\n")
    for i in range(max_y):
        for j in range(max_x):
            # print(f"\n\n[DEBUG] i = {i}, j = {j}\n\n")
            bullet = game_map[i][j]
            # if bullet in bullets.keys():
            if bullet == 'u' or bullet == 'd' or bullet == 'l' or bullet == 'r':
                bullets[bullet].append((j, i))
            elif bullet == '*':
                player_position = (j, i)
    
    return player_position

def is_valid_move(x, y):
    return 0 <= y and y < max_y and 0 <= x and x < max_x

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
            

def move_bullets():
    global bullets
    
    # Initialize a new map with empty strings
    new_map = [['.' for _ in range(max_x)] for _ in range(max_y)]
    new_bullets = {'u': [], 'd': [], 'l': [], 'r': []}
    
    # Iterate through each bullet direction and its positions
    for direction, positions in bullets.items():
        for bullet_x, bullet_y in positions:
            if direction == 'u' and 0 <= bullet_y - 1:
                # print(f"\n\n[DEBUG] [U] bullet_x = {bullet_x}, bullet_y - 1= {bullet_y-1}, max_x = {max_x}, max_y = {max_y}\n\n")
                new_map[bullet_y - 1][bullet_x] = new_map[bullet_y - 1][bullet_x].replace('.', '')
                new_map[bullet_y - 1][bullet_x] += 'u'
                new_bullets['u'].append((bullet_x, bullet_y - 1))
            elif direction == 'd' and bullet_y + 1 < max_y:
                # print(f"\n\n[DEBUG] [D] bullet_x = {bullet_x}, bullet_y + 1 = {bullet_y+1}, max_x = {max_x}, max_y = {max_y}\n\n")
                new_map[bullet_y + 1][bullet_x] = new_map[bullet_y + 1][bullet_x].replace('.', '')
                new_map[bullet_y + 1][bullet_x] += 'd'
                new_bullets['d'].append((bullet_x, bullet_y + 1))
            elif direction == 'l' and 0 <= bullet_x - 1:
                # print(f"\n\n[DEBUG] [L] bullet_x - 1 = {bullet_x-1}, bullet_y = {bullet_y}, max_x = {max_x}, max_y = {max_y}\n\n")
                new_map[bullet_y][bullet_x - 1] = new_map[bullet_y][bullet_x - 1].replace('.', '')
                new_map[bullet_y][bullet_x - 1] += 'l'
                new_bullets['l'].append((bullet_x - 1, bullet_y))
            elif direction == 'r' and bullet_x + 1 < max_x:
                # print(f"\n\n[DEBUG] [R] bullet_x + 1 = {bullet_x+1}, bullet_y = {bullet_y}, max_x = {max_x}, max_y = {max_y}\n\n")
                new_map[bullet_y][bullet_x + 1] = new_map[bullet_y][bullet_x + 1].replace('.', '')
                new_map[bullet_y][bullet_x + 1] += 'r'
                new_bullets['r'].append((bullet_x + 1, bullet_y))
    
    bullets = new_bullets

    return new_map

def find_safe_path(game_map, start_x, start_y):
    print(f"\n[DEBUG] Enter find path\n")
    global bullets
    
    path = []
    cur_x, cur_y = start_x, start_y

    while (len(bullets['u']) > 0 or len(bullets['d']) > 0 or len(bullets['l']) > 0 or len(bullets['r']) > 0) and not completely_safe(cur_x, cur_y):
        possible_moves = [(cur_x + 1, cur_y, 'r'), (cur_x - 1, cur_y, 'l'), (cur_x, cur_y + 1, 'd'), (cur_x, cur_y - 1, 'u')]
        possible_moves = [(x, y, direction) for x, y, direction in possible_moves if is_valid_move(x, y) and game_map[y][x] == '.']
        new_map = move_bullets()
        game_map = new_map
        tmp_path = ''
        
        has_valid_move = False
        for x, y, direction in possible_moves:
            if 0 <= x < max_x and 0 <= y < max_y and game_map[y][x] == '.':
                tmp_path = direction
                cur_x, cur_y = x, y
                has_valid_move = True
                break
        
        if has_valid_move:
            path.append(tmp_path)
        else:
            print(f"\n[DEBUG] Exit find path as NONE\n")
            return None
    
    print(f"\n[DEBUG] Exit find path\n")
    return path


def solution(request):
    global player_position, max_x, max_y
    game_map = parse_map(request)
    max_x = len(game_map[0])
    max_y = len(game_map)
    
    player_pos = get_bullets_return_player_position(game_map)
    
    start_x, start_y = player_pos
    safe_path = find_safe_path(game_map, start_x, start_y)

    # return jsonify({"instructions": safe_path})
    print("\n[ANSWER]")
    print({"instructions": safe_path})
    return json.dumps({"instructions": safe_path})
    # return safe_path

# if __name__ == "__main__":
#     # test_input = "....\\n.r*.\\n...."
#     # test_input = "ddd\\nr*.\\n..."
#     test_input = "d.d\\n.r*\\n.d."
#     print(solution(test_input))
    
    
    
    