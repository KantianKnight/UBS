import json

# test = [{"bugseq": [[20,30],[30,150],[110,135],[210,330]]}]

def solution(data):
    solution = []
    for request in data:
        bugs = request['bugseq']
        
    
        bugs.sort(key=lambda x: x[0])
        print(bugs)
        total_time = 0
        completed_tasks = 0
        
        
        for time_needed, expiry_time in bugs:
            if total_time + time_needed <= expiry_time:
                total_time += time_needed
                completed_tasks += 1
    
        solution.append(completed_tasks)
    return json.dumps(solution)
