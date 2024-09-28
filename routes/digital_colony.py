import numpy as np
import json

def generate_new_gen(number_list):
    
    weight = sum(number_list)
    signatures = np.full(len(number_list)-1, weight)
    for i in range(len(number_list)-1):
        signatures[i] += (number_list[i]- number_list[i+1])%10
    signatures = signatures % 10
    
    merged_array = np.empty((number_list.size + signatures.size,), dtype=signatures.dtype)
    merged_array[0::2] = number_list
    merged_array[1::2] = signatures
    return merged_array


def solve(gens, number_str):
    numbers = list(number_str)
    numbers = list(map(int, numbers))
    numbers = np.array(numbers)
    while gens > 0:
        numbers = generate_new_gen(numbers)
        gens -= 1
    return (np.sum(numbers)).item()


#number_str = "123456789"
def solution(request_json):
    requests = request_json
    sols = []
    for request in requests:
        generations = request["generations"]
        number_str = request["colony"]
        sols.append(solve(generations, number_str))
    return json.dumps(sols)


# def main():
#     test_dict = '[{ "generations": 5, "colony": "1000" },{ "generations": 10, "colony": "1000" }]'
    
    
    

#     print(solution(test_dict))

