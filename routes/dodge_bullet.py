from flask import jsonify

def solution(request):
    global player_position, max_x, max_y
    game_map = parse_map(request)
    max_x = len(game_map[0])
    max_y = len(game_map)
    
    player_pos = get_bullets_return_player_position(game_map)
    
    start_x, start_y = player_pos
    safe_path = find_safe_path(start_x, start_y)

    return jsonify({"instructions": safe_path})
    # return safe_path

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
    return player_pos

# Use A* algorithm for pathfinding
import heapq

# def find_safe_path(game_map, start_x, start_y):
#     def heuristic(a, b):
#         return abs(a[0] - b[0]) + abs(a[1] - b[1])
    
#     def neighbors(x, y):
#         for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
#             nx, ny = x + dx, y + dy
#             if 0 <= nx < max_x and 0 <= ny < max_y:
#                 yield nx, ny
    
#     goal = (max_x - 1, max_y - 1)
#     open_set = []
#     heapq.heappush(open_set, (0, start_x, start_y))
#     came_from = {}
#     g_score = { (start_x, start_y): 0 }
#     f_score = { (start_x, start_y): heuristic((start_x, start_y), goal) }
    
#     while open_set:
#         _, x, y = heapq.heappop(open_set)
        
#         if (x, y) == goal:
#             path = []
#             while (x, y) in came_from:
#                 path.append((x, y))
#                 x, y = came_from[(x, y)]
#             path.reverse()
#             return path
        
#         for nx, ny in neighbors(x, y):
#             tentative_g_score = g_score[(x, y)] + 1
#             if (nx, ny) not in g_score or tentative_g_score < g_score[(nx, ny)]:
#                 came_from[(nx, ny)] = (x, y)
#                 g_score[(nx, ny)] = tentative_g_score
#                 f_score[(nx, ny)] = tentative_g_score + heuristic((nx, ny), goal)
#                 heapq.heappush(open_set, (f_score[(nx, ny)], nx, ny))
    
#     return []

def find_safe_path(start_x, start_y):
    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
    
    def neighbors(x, y):
        directions = {'u': (0, -1), 'd': (0, 1), 'l': (-1, 0), 'r': (1, 0)}
        for direction, (dx, dy) in directions.items():
            nx, ny = x + dx, y + dy
            if 0 <= nx < max_x and 0 <= ny < max_y:
                yield nx, ny, direction
    
    goal = (max_x - 1, max_y - 1)
    open_set = []
    heapq.heappush(open_set, (0, start_x, start_y))
    came_from = {}
    g_score = { (start_x, start_y): 0 }
    f_score = { (start_x, start_y): heuristic((start_x, start_y), goal) }

    while open_set:
        _, x, y = heapq.heappop(open_set)
        
        if (x, y) == goal:
            path = []
            while (x, y) in came_from:
                x, y, direction = came_from[(x, y)]
                path.append(direction)
            path.reverse()
            return path
        
        for nx, ny, direction in neighbors(x, y):
            tentative_g_score = g_score[(x, y)] + 1
            if (nx, ny) not in g_score or tentative_g_score < g_score[(nx, ny)]:
                came_from[(nx, ny)] = (x, y, direction)
                g_score[(nx, ny)] = tentative_g_score
                f_score[(nx, ny)] = tentative_g_score + heuristic((nx, ny), goal)
                heapq.heappush(open_set, (f_score[(nx, ny)], nx, ny))
    
    return []

# Example usage
if __name__ == "__main__":
    # test_input = ".dd\\nr*.\\n..."
    test_input = "ddd\\n.*.\\n..."
    print(solution(test_input))