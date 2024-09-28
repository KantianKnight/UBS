import logging
import socket
from flask import request

# from routes import math_colony, solve_the_wordle, klotski, bugp2, bugp1, kazuma
from routes import app, clumsy, sudoku#, dodge_bullet
from flask import Flask, request, jsonify

logger = logging.getLogger(__name__)

@app.route('/', methods=['GET'])
def default_route():
    return 'Python Template'

# @app.route('/wordle-game', methods=['POST'])
# def wordle_game():
#     data = request.json
#     print(data)
#     guess = solve_the_wordle.make_guess(data)
#     return jsonify({"guess": guess})

# @app.route('/digital-colony', methods=['POST'])
# def give_result():
#     data = request.get_json()
#     return math_colony.solution(data)

# @app.route('/efficient-hunter-kazuma', methods=['POST'])
# def give_kazuma_result():
#     data = request.get_json()
#     result = kazuma.solution(data)
#     # print(result)
#     return jsonify(result)

@app.route('/sudoku', methods=['POST'])
def solve_sudoku():
    data = request.get_json()
    return 1
    # return sudoku.solution(data)
    # return jsonify(sudoku.solution(data))
    # return sudoku.solution(data)

# @app.route('/klotski', methods=['POST'])
# def get_result():
#     data = request.get_json()
#     return klotski.solution(data)

# @app.route('/bugfixer/p1', methods=['POST'])
# def bug_p1_result():
#     data = request.get_json()
#     return bugp1.solution(data)

# @app.route('/bugfixer/p2', methods=['POST'])
# def bug_p2_result():
#     data = request.get_json()
#     return bugp2.solution(data)

# @app.route('/dodge', methods=['POST'])
# def dodge():
#     data = str(request.data).split('\'')[1]
#     return dodge_bullet.solution(data)

@app.route('/the-clumsy-programmer', methods=['POST'])
def clumsy_result():
    data = request.get_json()
    return clumsy.solution(data)

logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter(
    '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

if __name__ == "__main__":
    logging.info("Starting application ...")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('localhost', 8080))
    port = sock.getsockname()[1]
    sock.close()
    app.run(port=port)
