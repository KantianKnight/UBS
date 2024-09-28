import logging
import socket
from flask import request

from routes import app, digital_colony, kazuma, solve_the_wordle
from flask import Flask, request, jsonify


logger = logging.getLogger(__name__)

@app.route('/', methods=['GET'])
def default_route():
    return 'Python da'

@app.route('/wordle-game', methods=['POST'])
def wordle_game():
    # data = request.json()
    # print(data)
    data = request.json
    print(data)
    guess = solve_the_wordle.make_guess(data)
    return jsonify({"guess": guess})

@app.route('/digital-colony', methods=['POST'])
def give_result():
    data = request.get_json()
    return digital_colony.solution(data)

@app.route('/efficient-hunter-kazuma', methods=['POST'])
def give_kazuma_result():
    data = request.get_json()
    return kazuma.solution(data)
    # return jsonify(result)

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
