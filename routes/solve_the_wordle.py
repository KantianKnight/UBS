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
            # guessed_characters[i]["correct"].append(char)
            guessed_characters[i]["correct"] = char
            correct_positions.append(i)
            overall_avail_positions.remove(i)
        elif feedback == 'X':
            if char not in incorrect_positions.keys():
                incorrect_positions[char] = [i]
            else:
                incorrect_positions[char].append(i)
            num_incorrect_positions += 1
            guessed_characters[i]["incorrect"].append(char)
        elif feedback == '-':
            avail_guesses = avail_guesses.replace(char, '')
            
def create_new_guess():
    global avail_guesses, num_incorrect_positions, correct_positions, overall_avail_positions, incorrect_positions
    new_guess = [None] * 5
    
    for i in range(5):
        if i in correct_positions:
            # new_guess[i] = guessed_characters[i]["correct"][0]
            new_guess[i] = guessed_characters[i]["correct"]
            
        for index, guess in enumerate(new_guess):
            if guess is None:
                if num_incorrect_positions > 0:
                    key = next(iter(incorrect_positions)) 
                    wrong_positions = incorrect_positions[key]
                    avail_positions = [pos for pos in range(5) if pos not in wrong_positions]
                    avail_positions = [pos for pos in avail_positions if pos in overall_avail_positions]
                    new_guess[avail_positions[0]] = key
                    overall_avail_positions.remove(avail_positions[0])
                    num_incorrect_positions -= 1
                    incorrect_positions.pop(key)
                else:
                    wrong_guesses_at_pos = guessed_characters[i]["incorrect"]
                    new_avail_guesses = [char for char in avail_guesses if char not in wrong_guesses_at_pos]
                    new_guess[index] = random.choice(new_avail_guesses)
            
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
