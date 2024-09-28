
import json
def create_board(board, moves):
    board_cords = {}
    board_moves = {}
    for i in range(0, 5):
        for j in range(0, 4):
            board_cords[board[i*4+j]] = []
            board_moves[board[i*4+j]] = [0,0]
    
    
    for i in range(0, 5):
        for j in range(0, 4):
            board_cords[board[i*4+j]].append([i, j])

    for i in range(0,len(moves),2):
        letter = moves[i]
        direction = moves[i+1]
        if direction == 'N':
            board_moves[letter][0] -= 1
        elif direction == 'S':
            board_moves[letter][0] += 1
        elif direction == 'E':
            board_moves[letter][1] += 1
        elif direction == 'W':
            board_moves[letter][1] -= 1
    
    final_board = [["@" for i in range(4)]for j in range(5) ] 
    for key in board_cords:
        if key == '@':
            continue
        for cord in board_cords[key]:
            final_board[cord[0]+board_moves[key][0]][cord[1]+board_moves[key][1]] = key

    final_string = ""
    for line in final_board:
        final_string+= "".join(line)
    return final_string
    
    

# test = '''
# [
#   {
#     "board": "BCDEBCFGAAFGAAHHI@@J",
#     "moves": "IEIEASBSCSDWDWEWEWFNGNHNINIEAE"
#   },
#   {
#     "board": "BBAACCAADDE@FGG@HIJJ",
#     "moves": "EEDEFNGEHNINJWJWGSESIEHEFSDWASBEBECNDNFNHNJNGWGWESISASDEDEFNHNJNGNIWIWEWEWASJEJEGNENEWAW"
#   },
#   {
#     "board": "BAACDAAE@FF@GHIJGHIJ",
#     "moves": "DSBSFEDEBSAWEWENFNDEDEBEBEASEWEWCWCWFNDNDWJNJNIEBSBSDSDSAEGNGNHWDWDSASCSCEEEESFWGNHNDWJNINBEAS"
#   }
# ]
# '''
def solution(request_json):
    requests = request_json
    #requests = json.loads(request_json)
    sols = []
    for request in requests:
        board = request["board"]
        moves = request["moves"]
        sols.append(create_board(board, moves))
    
    return json.dumps(sols)
    #return json.dumps(sols)

