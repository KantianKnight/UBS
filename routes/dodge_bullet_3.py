import heapq
from collections import defaultdict

def parse_map(text_map):
    return [list(row) for row in text_map.strip().split('\n')]

def get_initial_state(game_map):
    bullets = defaultdict(set)
    player_position = None
    for y, row in enumerate(game_map):
        for x, cell in enumerate(row):
            if cell in 'udlr':
                bullets[cell].add((x, y))
            elif cell == '*':
                player_position = (x, y)
    return bullets, player_position

def calculate_danger_zones(bullets, max_x, max_y):
    danger_zones = set()
    for direction, positions in bullets.items():
        for x, y in positions:
            if direction in 'ud':
                danger_zones.update((x, i) for i in range(max_y))
            else:
                danger_zones.update((i, y) for i in range(max_x))
    return danger_zones

def is_safe(position, danger_zones):
    return position not in danger_zones

def find_safe_path(start, danger_zones, max_x, max_y):
    queue = [(0, start, [])]
    visited = set()
    moves = [('r', 1, 0), ('l', -1, 0), ('d', 0, 1), ('u', 0, -1)]

    while queue:
        _, (x, y), path = heapq.heappop(queue)
        
        if (x, y) in visited:
            continue
        visited.add((x, y))

        if is_safe((x, y), danger_zones):
            return path

        for direction, dx, dy in moves:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < max_x and 0 <= new_y < max_y:
                new_path = path + [direction]
                priority = len(new_path)
                heapq.heappush(queue, (priority, (new_x, new_y), new_path))

    return None

def solution(request):
    game_map = parse_map(request)
    max_y, max_x = len(game_map), len(game_map[0])
    bullets, player_position = get_initial_state(game_map)
    danger_zones = calculate_danger_zones(bullets, max_x, max_y)
    safe_path = find_safe_path(player_position, danger_zones, max_x, max_y)
    # return {"instructions": safe_path}
    return safe_path
    
    
if __name__ == "__main__":
    # test_input = "....\\n.r*.\\n...."
    test_input = ".dd\\nr*.\\n..."
    print(solution(test_input))