import json
from flask import jsonify

def solution(data):
    def main(m):
        # Implement segment tree to find minimum value in a range
        def build_tree(arr, tree, node, start, end):
            if start == end:
                tree[node] = arr[start]
            else:
                mid = (start + end) // 2
                build_tree(arr, tree, 2*node, start, mid)
                build_tree(arr, tree, 2*node+1, mid+1, end)
                tree[node] = min(tree[2*node], tree[2*node+1])
                
        def query_tree(tree, node, start, end, L, R):
            if R < start or end < L:
                return float('inf')
            if L <= start and end <= R:
                return tree[node]
            mid = (start + end) // 2
            left_query = query_tree(tree, 2*node, start, mid, L, R)
            right_query = query_tree(tree, 2*node+1, mid+1, end, L, R)
            return min(left_query, right_query)

        # Segtree for monsters array
        n = len(m)
        tree = [0] * (4 * n)
        build_tree(m, tree, 1, 0, n-1)
        ## i-j Query
        ## query_tree(tree, 1, 0, n-1, i, j)

        # Tuples (max efficiency w/ current monster, max efficiency w/o current monster, max efficiency)
        dp = []; dp.append((0, 0, 0))
        for i in range(1, n):
            j = i
            while (dp[j-1][2] == dp[j-2][2]) and j > 1:
                j -= 1
            if dp[j-1][2] == 0:
                v1 = m[i] - query_tree(tree, 1, 0, n-1, 0, i-1)
            else:
                if j > i-2:
                    k = j-1
                    while (dp[k-1][2] == dp[k-2][2]) and k > 1:
                        k -= 1
                    v1 = max(dp[j-1][0] + m[i] - m[j-1],
                            dp[k-1][0] + m[i] - query_tree(tree, 1, 0, n-1, k+1, i-1))
                else:
                    v1 = max(dp[j-1][0] + m[i] - m[j-1], 
                            dp[j-1][0] + m[i] - query_tree(tree, 1, 0, n-1, j+1, i-1))

            v2 = dp[i-1][2]
            dp.append((v1, v2, max(v1, v2)))

        print(dp)
        return dp[-1][2]
    
    results = []
    for i in range(len(data)):
        monsters_array = data[i]["monsters"]
        efficiency = main(monsters_array)
        results.append({"efficiency": efficiency})

    # output_data = jsonify(results)
    # print(output_data)
    return results

# Example Usage
data = [
    {
      "monsters": [1,100,340,210,1,4,530]
    },
    {
      "monsters": [15, 14, 7, 16, 19, 3, 12, 8, 5, 11, 13, 9, 2, 4, 6, 1, 18, 20, 17, 10]
    }
]
solution(data)