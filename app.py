import logging
import socket
from flask import request

from routes import app, math_colony, kazuma, solve_the_wordle, klotski, bugp2, sudoku
from flask import Flask, request, jsonify


logger = logging.getLogger(__name__)

@app.route('/', methods=['GET'])
def default_route():
    return 'Python Template'

@app.route('/wordle-game', methods=['POST'])
def wordle_game():
    data = request.json
    print(data)
    guess = solve_the_wordle.make_guess(data)
    return jsonify({"guess": guess})

@app.route('/digital-colony', methods=['POST'])
def give_result():
    data = request.get_json()
    return math_colony.solution(data)

@app.route('/efficient-hunter-kazuma', methods=['POST'])
def give_kazuma_result():
    data = request.get_json()
    result = kazuma.solution(data)
    # print(result)
    return jsonify(result)

@app.route('/sudoku', methods=['POST'])
def solve_sudoku():
    data = request.get_json()
    return sudoku.solution(data)

@app.route('/klotski', methods=['POST'])
def get_result():
    data = request.get_json()
    return klotski.solution(data)

@app.route('/bugfixer/p2', methods=['POST'])
def bug_p2_result():
    data = request.get_json()
    return bugp2.solution(data)

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
