import numpy as np
import json

def calc_new_gen(weight, adj):
    new_adj = np.zeros((10, 10), dtype=int)
    new_weight = weight

    for i in range(10):
        for j in range(10):
            if adj[i][j] > 0:
                val = int(weight + ((i - j) % 10)) % 10
                # print(val)
                new_adj[i][val] += adj[i][j]
                new_adj[val][j] += adj[i][j]
                new_weight += adj[i][j] * val
    return new_weight, new_adj

def solve(gens, number_str):
    numbers = np.array(list(map(int, number_str)))

    # Create adjacency list for adj[i][j] which counts the number of times i and j are adjacent, where i < j are digits in the colony
    adj = np.zeros((10, 10), dtype=int)
    for i in range(len(number_str) - 1):
        first, second = numbers[i], numbers[i + 1]
        adj[first][second] += 1
    # print(adj)

    weight = np.sum(numbers)
    # first, last = numbers[0], numbers[-1]

    while gens > 0:
        # print(weight, adj)
        weight, adj = calc_new_gen(weight, adj)
        gens -= 1
    return str(int(weight))


# number_str = "123456789"
def solution(request_json):
    requests = request_json
    sols = []
    for request in requests:
        generations = request["generations"]
        number_str = request["colony"]

        sols.append(solve(generations, number_str))
    print(json.dumps(sols))
    return json.dumps(sols)
    # return sols


def main():
    test_dict = [{ "generations": 10, "colony": "1000" },{ "generations": 50, "colony": "1000" }]
    solution(test_dict)

main()