import json

def solution():
    # data = json.dumps([
    #     {
    #     "monsters": [1,100,340,210,1,4,530]
    #     }
    # ])

    data = input("Input: ")
    parsed_data = json.loads(data)
    monsters_array = parsed_data[0]["monsters"]

    # MAIN
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
            while (dp[j-1][2] == dp[j-2][2] and j > 1):
                j -= 1
            # v1 = max(dp[j-1][2], dp[j-1][2] + m[i] - m[j-1])
            v1 = dp[j-1][2] + m[i] - m[j-1]
            v1 = max(v1, dp[j-1][2] + m[i] - query_tree(tree, 1, 0, n-1, j, i))

            v2 = dp[i-1][2]
            dp.append((v1, v2, max(v1, v2)))

        # print(dp)
        return dp[-1][2]

    # Process the monsters array
    efficiency = main(monsters_array)

    # Output the efficiency
    output_data = json.dumps([
        {
        "efficiency": efficiency
        }
    ])
    print(output_data)

solution()