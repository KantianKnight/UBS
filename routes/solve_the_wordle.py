import random

starting_word_list = ["soare", "roate", "raise"]

global avail_guesses
avail_guesses = "abcdefghijklmnopqrstuvwxyz"

overall_avail_positions = [0, 1, 2, 3, 4]
incorrect_positions = {}
num_incorrect_positions = 0
correct_positions = []
guessed_characters = {
    0 : {
        "correct" : [],
        "incorrect" : []
    },
    1 : {
        "correct" : [],
        "incorrect" : []
    },
    2 : {
        "correct" : [],
        "incorrect" : []
    },
    3 : {
        "correct" : [],
        "incorrect" : []
    },
    4 : {
        "correct" : [],
        "incorrect" : []
    }
}

def update_knowledge(guess, evaluation):
    global avail_guesses, num_incorrect_positions, correct_positions, overall_avail_positions, incorrect_positions
    for i, (char, feedback) in enumerate(zip(guess, evaluation)):
        if feedback == 'O':
            guessed_characters[i]["correct"] = char
            correct_positions.append(i)
            if i in overall_avail_positions:
                # print(f"\n\n[DEBUG] remove {i} from the overall_avail_positions: {overall_avail_positions}\n\n")
                overall_avail_positions.remove(i)
        elif feedback == 'X':
            if char not in incorrect_positions.keys():
                incorrect_positions[char] = [i]
                # print(f"\n\n[DEBUG] initialize {i} to the incorrect_positions of {char}\n\n")
            else:
                incorrect_positions[char].append(i)
                # print(f"\n\n[DEBUG] adding {i} to the incorrect_positions of {char}\n\n")
            num_incorrect_positions += 1
            # print(f"\n\n[DEBUG] increment num_incorrect_positions to {num_incorrect_positions}\n\n")
            guessed_characters[i]["incorrect"].append(char)
        elif feedback == '-':
            avail_guesses = avail_guesses.replace(char, '')
            
def create_new_guess():
    global avail_guesses, num_incorrect_positions, correct_positions, overall_avail_positions, incorrect_positions
    new_guess = [None] * 5
    
    num_to_be_guessed = 5 - len(correct_positions)
    
    for i in range(5):
        if i in correct_positions:
            new_guess[i] = guessed_characters[i]["correct"]
            num_to_be_guessed -= 1
            print(f"\n\n[DEBUG] new_guess[{i}] = {guessed_characters[i]['correct']}\n\n")
            if guessed_characters[i]["correct"] in incorrect_positions.keys():
                incorrect_positions.pop(guessed_characters[i]["correct"])
                # print(f"\n\n[DEBUG] remove {guessed_characters[i]['correct']} from incorrect_positions {incorrect_positions}\n\n")
    
    while (num_to_be_guessed > 0):
        if num_incorrect_positions > 0 and incorrect_positions:
            avail_positions = [0, 1, 2, 3, 4]
            key, _ = list(incorrect_positions.items())[0]
            wrong_positions = incorrect_positions[key]
            avail_positions = [pos for pos in range(5) if pos not in wrong_positions]
            avail_positions = [pos for pos in avail_positions if pos in overall_avail_positions]
            
            incorrect_positions.pop(key, None)
            while len(avail_positions) < 1:
                if not incorrect_positions or num_incorrect_positions <= 0:
                    wrong_guesses_at_pos = guessed_characters[i]["incorrect"]
                    new_avail_guesses = [char for char in avail_guesses if char not in wrong_guesses_at_pos]
                    new_guess[index] = random.choice(new_avail_guesses)
                    print(f"\n\n[DEBUG] [IF_WHILE] new_guess[{index}] = {new_guess[index]}\n\n")
                    break
                
                key, _ = list(incorrect_positions.items())[0]
                wrong_positions = incorrect_positions[key]
                avail_positions = [pos for pos in range(5) if pos not in wrong_positions]
                avail_positions = [pos for pos in avail_positions if pos in overall_avail_positions]
                incorrect_positions.pop(key, None)
            
            new_guess[avail_positions[0]] = key
            print(f"\n\n[DEBUG] [IF-END] new_guess[{avail_positions[0]}] = {key}\n\n")
            overall_avail_positions.remove(avail_positions[0])
            num_incorrect_positions -= 1
            # print(f"\n\n[DEBUG] decrement num_incorrect_positions to {num_incorrect_positions}\n\n")
            incorrect_positions.pop(key, None)
            
    # print(f"\n\n[DEBUG] new_guess: {new_guess}\n\n")
    # for index, guess in enumerate(new_guess):
    #     if guess is not None:
    #         continue
        
    #     if num_incorrect_positions > 0 and incorrect_positions:
    #         avail_positions = [0, 1, 2, 3, 4]
    #         key, _ = list(incorrect_positions.items())[0]
    #         wrong_positions = incorrect_positions[key]
    #         avail_positions = [pos for pos in range(5) if pos not in wrong_positions]
    #         avail_positions = [pos for pos in avail_positions if pos in overall_avail_positions]
            
    #         incorrect_positions.pop(key, None)
    #         while len(avail_positions) < 1:
    #             if not incorrect_positions or num_incorrect_positions <= 0:
    #                 wrong_guesses_at_pos = guessed_characters[i]["incorrect"]
    #                 new_avail_guesses = [char for char in avail_guesses if char not in wrong_guesses_at_pos]
    #                 new_guess[index] = random.choice(new_avail_guesses)
    #                 print(f"\n\n[DEBUG] [IF_WHILE] new_guess[{index}] = {new_guess[index]}\n\n")
    #                 break
                
    #             key, _ = list(incorrect_positions.items())[0]
    #             wrong_positions = incorrect_positions[key]
    #             avail_positions = [pos for pos in range(5) if pos not in wrong_positions]
    #             avail_positions = [pos for pos in avail_positions if pos in overall_avail_positions]
    #             incorrect_positions.pop(key, None)
            
    #         new_guess[avail_positions[0]] = key
    #         print(f"\n\n[DEBUG] [IF-END] new_guess[{avail_positions[0]}] = {key}\n\n")
    #         overall_avail_positions.remove(avail_positions[0])
    #         num_incorrect_positions -= 1
    #         # print(f"\n\n[DEBUG] decrement num_incorrect_positions to {num_incorrect_positions}\n\n")
    #         incorrect_positions.pop(key, None)
    #         # print(f"\n\n[DEBUG] remove {key} from incorrect_positions {incorrect_positions}\n\n")
    #     else:
    #         wrong_guesses_at_pos = guessed_characters[i]["incorrect"]
    #         new_avail_guesses = [char for char in avail_guesses if char not in wrong_guesses_at_pos]
    #         new_guess[index] = random.choice(new_avail_guesses)
    #         print(f"\n\n[DEBUG] [ELSE] new_guess[{index}] = {new_guess[index]}\n\n")
    
    
    for index, guess in enumerate(new_guess):
        if guess is None:
            wrong_guesses_at_pos = guessed_characters[i]["incorrect"]
            new_avail_guesses = [char for char in avail_guesses if char not in wrong_guesses_at_pos]
            new_guess[index] = random.choice(new_avail_guesses)
            print(f"\n\n[DEBUG] [ELSE] new_guess[{index}] = {new_guess[index]}\n\n")
            
    print(f"\n\n[DEBUG] new_guess: {new_guess}\n\n")
    return ''.join(new_guess)

def make_guess(data):
    guess_history = data.get('guessHistory', [])
    evaluation_history = data.get('evaluationHistory', [])
    
    if not guess_history:
        return random.choice(starting_word_list)

    for guess, evaluation in zip(guess_history, evaluation_history):
        update_knowledge(guess, evaluation)

    new_guess = create_new_guess()
    return new_guess
