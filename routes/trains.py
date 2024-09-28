from collections import defaultdict
import heapq

subway_stations = {
    "Tokyo Metro Ginza Line": [
        "Asakusa", "Tawaramachi", "Inaricho", "Ueno", "Ueno-hirokoji", "Suehirocho",
        "Kanda", "Mitsukoshimae", "Nihombashi", "Kyobashi", "Ginza", "Shimbashi",
        "Toranomon", "Tameike-sanno", "Akasaka-mitsuke", "Nagatacho", "Aoyama-itchome",
        "Gaiemmae", "Omotesando", "Shibuya"
    ],
    "Tokyo Metro Marunouchi Line": [
        "Ogikubo", "Minami-asagaya", "Shin-koenji", "Higashi-koenji", "Shin-nakano",
        "Nakano-sakaue", "Nishi-shinjuku", "Shinjuku", "Shinjuku-sanchome", "Shin-ochanomizu",
        "Ochanomizu", "Awajicho", "Otemachi", "Tokyo", "Ginza", "Kasumigaseki", "Kokkai-gijidomae",
        "Akasaka-mitsuke", "Yotsuya", "Yotsuya-sanchome", "Shinjuku-gyoemmae", "Nishi-shinjuku-gochome",
        "Nakano-fujimicho", "Nakano-shimbashi", "Nakano-sakaue", "Shinjuku-sanchome", "Kokkai-gijidomae",
        "Kasumigaseki", "Ginza", "Tokyo", "Otemachi", "Awajicho", "Shin-ochanomizu", "Ochanomizu"
    ],
    "Tokyo Metro Hibiya Line": [
        "Naka-meguro", "Ebisu", "Hiroo", "Roppongi", "Kamiyacho", "Kasumigaseki", "Hibiya",
        "Ginza", "Higashi-ginza", "Tsukiji", "Hatchobori", "Kayabacho", "Nihombashi",
        "Kodemmacho", "Akihabara", "Naka-okachimachi", "Ueno", "Iriya", "Minowa",
        "Minami-senju", "Kita-senju"
    ],
    "Tokyo Metro Tozai Line": [
        "Nakano", "Ochiai", "Takadanobaba", "Waseda", "Kagurazaka", "Iidabashi", "Kudanshita",
        "Takebashi", "Otemachi", "Nihombashi", "Kayabacho", "Monzen-nakacho", "Kiba",
        "Toyosu", "Minami-sunamachi", "Nishi-kasai", "Kasai", "Urayasu", "Minami-gyotoku",
        "Gyotoku", "Myoden", "Baraki-nakayama", "Nishi-funabashi"
    ],
    "Tokyo Metro Chiyoda Line": [
        "Yoyogi-uehara", "Yoyogi-koen", "Meiji-jingumae", "Omotesando", "Nogizaka", "Akasaka",
        "Kokkai-gijidomae", "Kasumigaseki", "Hibiya", "Nijubashimae", "Otemachi",
        "Shin-ochanomizu", "Yushima", "Nezu", "Sendagi", "Nishi-nippori", "Machiya",
        "Kita-senju", "Ayase", "Kita-ayase"
    ],
    "Tokyo Metro Yurakucho Line": [
        "Wakoshi", "Chikatetsu-narimasu", "Chikatetsu-akatsuka", "Heiwadai", "Hikawadai",
        "Kotake-mukaihara", "Senkawa", "Kanamecho", "Ikebukuro", "Higashi-ikebukuro",
        "Gokokuji", "Edogawabashi", "Iidabashi", "Ichigaya", "Kojimachi", "Nagatacho",
        "Sakuradamon", "Yurakucho", "Ginza-itchome", "Shintomicho", "Toyocho",
        "Kiba", "Toyosu", "Tsukishima", "Shintomicho", "Tatsumi", "Shinonome", "Ariake"
    ],
    "Tokyo Metro Hanzomon Line": [
        "Shibuya", "Omotesando", "Aoyama-itchome", "Nagatacho", "Hanzomon", "Kudanshita",
        "Jimbocho", "Otemachi", "Mitsukoshimae", "Suitengumae", "Kiyosumi-shirakawa",
        "Sumiyoshi", "Kinshicho", "Oshiage"
    ],
    "Tokyo Metro Namboku Line": [
        "Meguro", "Shirokanedai", "Shirokane-takanawa", "Azabu-juban", "Roppongi-itchome",
        "Tameike-sanno", "Nagatacho", "Yotsuya", "Ichigaya", "Iidabashi", "Korakuen",
        "Todaimae", "Hon-komagome", "Komagome", "Nishigahara", "Oji", "Oji-kamiya",
        "Shimo", "Akabane-iwabuchi"
    ],
    "Tokyo Metro Fukutoshin Line": [
        "Wakoshi", "Chikatetsu-narimasu", "Chikatetsu-akatsuka", "Narimasu", "Shimo-akatsuka",
        "Heiwadai", "Hikawadai", "Kotake-mukaihara", "Senkawa", "Kanamecho", "Ikebukuro",
        "Zoshigaya", "Nishi-waseda", "Higashi-shinjuku", "Shinjuku-sanchome", "Kita-sando",
        "Meiji-jingumae", "Shibuya"
    ],
    "Toei Asakusa Line": [
        "Nishi-magome", "Magome", "Nakanobu", "Togoshi", "Gotanda", "Takanawadai",
        "Sengakuji", "Mita", "Shiba-koen", "Daimon", "Shimbashi", "Higashi-ginza",
        "Takaracho", "Nihombashi", "Ningyocho", "Higashi-nihombashi", "Asakusabashi",
        "Kuramae", "Asakusa", "Honjo-azumabashi", "Oshiage"
    ],
    "Toei Mita Line": [
        "Meguro", "Shirokanedai", "Shirokane-takanawa", "Mita", "Shiba-koen", "Onarimon",
        "Uchisaiwaicho", "Hibiya", "Otemachi", "Jimbocho", "Suidobashi", "Kasuga",
        "Hakusan", "Sengoku", "Sugamo", "Nishi-sugamo", "Shin-itabashi", "Itabashi-kuyakushomae",
        "Itabashi-honcho", "Motohasunuma", "Shin-takashimadaira", "Nishidai", "Hasune",
        "Takashimadaira", "Shimura-sakaue", "Shimura-sanchome", "Nishidai"
    ],
    "Toei Shinjuku Line": [
        "Shinjuku", "Shinjuku-sanchome", "Akebonobashi", "Ichigaya", "Kudanshita",
        "Jimbocho", "Ogawamachi", "Iwamotocho", "Bakuro-yokoyama", "Hamacho",
        "Morishita", "Kikukawa", "Sumiyoshi", "Nishi-ojima", "Ojima", "Higashi-ojima",
        "Funabori", "Ichinoe", "Mizue", "Shinozaki", "Motoyawata"
    ],
    "Toei Oedo Line": [
        "Hikarigaoka", "Nerima-kasugacho", "Toshimaen", "Nerima", "Nerima-sakamachi",
        "Shin-egota", "Ochiai-minami-nagasaki", "Nakai", "Higashi-nakano", "Nakano-sakaue",
        "Nishi-shinjuku-gochome", "Tochomae", "Shinjuku-nishiguchi", "Higashi-shinjuku",
        "Wakamatsu-kawada", "Ushigome-yanagicho", "Ushigome-kagurazaka", "Iidabashi",
        "Kasuga", "Hongosanchome", "Ueno-okachimachi", "Shin-okachimachi", "Kuramae",
        "Ryogoku", "Morishita", "Kiyosumi-shirakawa", "Monzen-nakacho", "Tsukishima",
        "Kachidoki", "Shiodome", "Daimon", "Akasaka-mitsuke", "Roppongi", "Aoyama-itchome",
        "Shinjuku", "Tochomae", "Shinjuku", "Shinjuku-sanchome", "Higashi-shinjuku",
        "Wakamatsu-kawada", "Ushigome-yanagicho", "Ushigome-kagurazaka", "Iidabashi",
        "Kasuga", "Hongosanchome", "Ueno-okachimachi", "Shin-okachimachi", "Kuramae",
        "Ryogoku", "Morishita", "Kiyosumi-shirakawa", "Monzen-nakacho", "Tsukishima",
        "Kachidoki", "Shiodome", "Daimon", "Shiodome", "Tsukishima"
    ]
}

times = {
    "Tokyo Metro Ginza Line": 2,
    "Tokyo Metro Marunouchi Line": 3,
    "Tokyo Metro Hibiya Line": 2.5,
    "Tokyo Metro Tozai Line": 4,
    "Tokyo Metro Chiyoda Line": 1.5,
    "Tokyo Metro Yurakucho Line": 2,
    "Tokyo Metro Hanzomon Line": 2,
    "Tokyo Metro Namboku Line" : 1,
    "Tokyo Metro Fukutoshin Line": 3,
    "Toei Asakusa Line": 3.5,
    "Toei Mita Line": 4,
    "Toei Shinjuku Line": 1.5,
    "Toei Oedo Line": 1
}

# I want to create a graph with the stations as nodes and the time taken between them as the edge weight
# For every liine in times, I want to iterate through the stations and add the edge between the current station and the next station
# I will use the times dictionary to get the time taken between the stations
# Create the graph below
graph = defaultdict(list)

for line, stations in subway_stations.items():
    time = times[line]
    for i in range(len(stations) - 1):
        graph[stations[i]].append((stations[i + 1], time))
        graph[stations[i + 1]].append((stations[i], time))

# # Example of how to print the graph
# for station, connections in graph.items():
#     print(f"{station}: {connections}")

# Use an all-pairs shortest path algorithm between stations and save them in a dictionary
# I will use the graph created above to find the shortest path between two stations
# I will use the heapq module to implement the priority queue
def dijkstra(graph, start):
    queue = [(0, start)]
    distances = {start: 0}
    while queue:
        current_distance, current_station = heapq.heappop(queue)
        if current_distance > distances[current_station]:
            continue
        for neighbor, weight in graph[current_station]:
            distance = current_distance + weight
            if distance < distances.get(neighbor, float('inf')):
                distances[neighbor] = distance
                heapq.heappush(queue, (distance, neighbor))
    return distances

# Create a 2D array to store all the shortest path values
stations = list(graph.keys())
num_stations = len(stations)
shortest_paths_matrix = [[float('inf')] * num_stations for _ in range(num_stations)]

# Create a mapping from station name to index
station_index = {station: idx for idx, station in enumerate(stations)}

# Fill the 2D array with the shortest path values
for i, station in enumerate(stations):
    distances = dijkstra(graph, station)
    for destination, distance in distances.items():
        j = station_index[destination]
        shortest_paths_matrix[i][j] = distance

# Convert the 2D array to a dictionary with station names as keys
shortest_paths_dict = {
    station: {stations[j]: shortest_paths_matrix[i][j] for j in range(num_stations)}
    for i, station in enumerate(stations)
}

# # Example of how to print the shortest paths
# for station, paths in shortest_paths_dict.items():
#     print(f"From {station}:")
#     for destination, distance in paths.items():
#         print(f"  to {destination}: {distance} minutes")

# # Print the distance between 2 stations
# print(shortest_paths_dict["Shibuya"]["Shinjuku-sanchome"])

# Each station has a point value associated with it
# I will create a dictionary with the station names as keys and the point values as values
# I start at a given station and I need to end at that station
# I have a given amount of time to travel between the stations
# I will use dynamic programming to find the maximum points I can get
# I will create a 2D array to store the maximum points at each station and time
# I will iterate through the stations and times and calculate the maximum points
# I will use the shortest_paths_dict to get the time taken between the stations
# I will use the points dictionary to get the points at each station
points = {
    "Shibuya": 10, "Shinjuku-sanchome": 8, "Ginza": 7, "Tokyo": 9, "Ueno": 6,
    "Asakusa": 5, "Ikebukuro": 4, "Roppongi": 3, "Meguro": 2, "Otemachi": 1
}

def max_points(start_station, total_time):
    # Initialize DP table
    dp = [[0] * (total_time + 1) for _ in range(num_stations)]
    start_idx = station_index[start_station]

    # Base case: starting station at time 0
    for t in range(total_time + 1):
        dp[start_idx][t] = points.get(start_station, 0)

    # Fill DP table
    for t in range(1, total_time + 1):
        for i in range(num_stations):
            current_station = stations[i]
            current_points = points.get(current_station, 0)
            for neighbor, travel_time in graph[current_station]:
                neighbor_idx = station_index[neighbor]
                if t >= travel_time:
                    dp[neighbor_idx][t] = max(dp[neighbor_idx][t], dp[i][t - travel_time] + current_points)

    # Find the maximum points we can get ending at the start station
    max_points = 0
    for t in range(total_time + 1):
        max_points = max(max_points, dp[start_idx][t])

    return max_points

# Example usage
start_station = "Shibuya"
total_time = 10
print(f"Maximum points starting and ending at {start_station} with {total_time} minutes: {max_points(start_station, total_time)}")