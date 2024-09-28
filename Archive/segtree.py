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

# Example array
m = [2, 5, 7, 4, 9, 3]
n = len(m)
tree = [0] * (4 * n)
build_tree(m, tree, 1, 0, n-1)

# Example usage of the segment tree to find the minimum value in the range [1, 3]
min_value = query_tree(tree, 1, 0, n-1, 2, 4)
print(f"Minimum value in the range [1, 3]: {min_value}")