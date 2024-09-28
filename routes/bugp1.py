import json

def find_local_max(graph, times, v):
    return max([find_local_max(graph,times, u) for u in graph[v]] or [0]) + times[v-1]

def solve(times, prerequisites):
    graph = [[] for _ in range(len(times))]
    for v,u in prerequisites:
        graph[u].append(v)
    return max([find_local_max(graph, times, v) for v in range(len(times))])
def solution(data):
    print("HEY")
    sols = []
    for request in data:
        times = request['time']
        prerequisites = [(request['prerequisites'][i][0]-1, request['prerequisites'][i][1]-1)for i in range(len(request['prerequisites']))]
        sols.append(solve(times, prerequisites))
    print("HELLO")
    return json.dumps(sols)
    

        

