import heapq
from flask import jsonify

def solution(request):
    global player_position, max_x, max_y
    game_map = parse_map(request)
    max_x = len(game_map[0])
    max_y = len(game_map)
    
    player_pos = get_bullets_return_player_position(game_map)
    
    start_x, start_y = player_pos
    safe_path = find_safe_path(game_map, start_x, start_y)

    # return jsonify({"instructions": safe_path})
    return safe_path

# Efficient parsing of the game map
def parse_map(request):
    return [list(line) for line in request.split('\\n')]

# Efficiently get bullets and player position
def get_bullets_return_player_position(game_map):
    bullets = {'u': [], 'd': [], 'l': [], 'r': []}
    player_pos = None
    for y, row in enumerate(game_map):
        for x, cell in enumerate(row):
            if cell == 'r':
                bullets['r'].append((x, y))
            elif cell == 'l':
                bullets['l'].append((x, y))
            elif cell == 'u':
                bullets['u'].append((x, y))
            elif cell == 'd':
                bullets['d'].append((x, y))
            elif cell == '*':
                player_pos = (x, y)
    return player_pos, bullets

# Use A* algorithm for pathfinding
def find_safe_path(game_map, start_x, start_y):
    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
    
    def neighbors(x, y):
        directions = {'u': (0, -1), 'd': (0, 1), 'l': (-1, 0), 'r': (1, 0)}
        for direction, (dx, dy) in directions.items():
            nx, ny = x + dx, y + dy
            if 0 <= nx < max_x and 0 <= ny < max_y:
                yield nx, ny, direction
    
    def move_bullets(bullets):
        new_bullets = {'u': [], 'd': [], 'l': [], 'r': []}
        for direction, positions in bullets.items():
            for x, y in positions:
                if direction == 'u' and y > 0:
                    new_bullets['u'].append((x, y - 1))
                elif direction == 'd' and y < max_y - 1:
                    new_bullets['d'].append((x, y + 1))
                elif direction == 'l' and x > 0:
                    new_bullets['l'].append((x - 1, y))
                elif direction == 'r' and x < max_x - 1:
                    new_bullets['r'].append((x + 1, y))
        return new_bullets
    
    def is_safe(x, y, bullets):
        for direction, positions in bullets.items():
            if (x, y) in positions:
                return False
        return True
    
    open_set = []
    heapq.heappush(open_set, (0, start_x, start_y))
    came_from = {}
    g_score = { (start_x, start_y): 0 }
    f_score = { (start_x, start_y): 0 }
    directions_from_start = {}
    bullets = get_bullets_return_player_position(game_map)[1]

    while open_set:
        _, x, y = heapq.heappop(open_set)
        
        if is_safe(x, y, bullets):
            path = []
            while (x, y) in came_from:
                x, y, direction = came_from[(x, y)]
                path.append(direction)
            path.reverse()
            return path
        
        for nx, ny, direction in neighbors(x, y):
            if is_safe(nx, ny, bullets):
                tentative_g_score = g_score[(x, y)] + 1
                if (nx, ny) not in g_score or tentative_g_score < g_score[(nx, ny)]:
                    came_from[(nx, ny)] = (x, y, direction)
                    g_score[(nx, ny)] = tentative_g_score
                    f_score[(nx, ny)] = tentative_g_score
                    heapq.heappush(open_set, (f_score[(nx, ny)], nx, ny))
        
        bullets = move_bullets(bullets)
    
    return []

# Example usage
if __name__ == "__main__":
    test_input = ".dd\\nr*.\\n..."
    print(solution(test_input))