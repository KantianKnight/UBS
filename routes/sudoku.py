import json
import base64
import gzip
import pytesseract
import cv2
import numpy as np
import easyocr
from flask import jsonify
from PIL import Image
import io

def solution(data):
    # parsed_data = json.loads(data)
    parsed_data = data
    id = parsed_data["id"]
    encoded = parsed_data["encoded"]
    img_length = parsed_data["imgLength"]
    empty_cells = parsed_data["emptyCells"]

    compressed_data = base64.b64decode(encoded)
    def run_length_decode(data):
        decoded_bytes = bytearray()
        i = 0
        while i < len(data):
            run_length = data[i]
            i += 1
            value = data[i]
            i += 1
            decoded_bytes.extend([value] * run_length)
        return bytes(decoded_bytes)
    decompressed_data = run_length_decode(compressed_data)

    # Open (decompressed_data + '.jpg') as an image
    sudokuBoard = Image.open(io.BytesIO(decompressed_data))
    # sudokuBoard.show()

    # Image Preprocessing
    gray_image = cv2.cvtColor(np.array(sudokuBoard), cv2.COLOR_BGR2GRAY)
    thresh_image = cv2.adaptiveThreshold(gray_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
    cell_size = gray_image.shape[0] // 4
    sudoku_array = []

    # Loop through each cell in the 4x4 grid
    for row in range(4):
        row_numbers = []
        for col in range(4):
            # Extract the cell from the thresholded image
            margin_top = margin_left = 2  # Adjust the left margin as needed
            cell = thresh_image[row * cell_size + margin_top:(row + 1) * cell_size, col * cell_size + margin_left:(col + 1) * cell_size]

            # Apply morphological operations to enhance the cell image
            kernel = np.ones((3, 3), np.uint8)
            cell = cv2.morphologyEx(cell, cv2.MORPH_CLOSE, kernel, iterations=1)
            cell = cv2.morphologyEx(cell, cv2.MORPH_OPEN, kernel, iterations=1)
            cell = cv2.morphologyEx(cell, cv2.MORPH_CLOSE, kernel, iterations=1)
            cell = cv2.morphologyEx(cell, cv2.MORPH_OPEN, kernel, iterations=1)
            
            # Dilate and erode to make borders more uniform
            cell = cv2.dilate(cell, kernel, iterations=1)
            cell = cv2.erode(cell, kernel, iterations=1)
            cell = cv2.dilate(cell, kernel, iterations=1)
            cell = cv2.erode(cell, kernel, iterations=1)

            # Use pytesseract to extract the number from the cell
            custom_config = r'--oem 3 --psm 10 outputbase digits'
            extracted_text = pytesseract.image_to_string(cell, config=custom_config).strip()
            
            # If the extracted text is empty, check for dots and count them
            if not extracted_text:
                num_dots = 0
                # Find contours in the cell image
                contours, _ = cv2.findContours(cell, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                for contour in contours:
                    if cv2.contourArea(contour) > 10:  # You can adjust the threshold value as needed
                        num_dots += 1
                if 1 <= num_dots <= 9:
                    extracted_text = str(num_dots)
                else:
                    extracted_text = '0'
            
            # Convert the extracted text to an integer, default to 0 if not a digit
            number = int(extracted_text) if extracted_text.isdigit() else 0
            row_numbers.append(number)
        
        sudoku_array.append(row_numbers)

    # Convert to numpy array and ensure it's 4x4
    sudoku_array = np.array(sudoku_array).reshape((4, 4))
    # print(sudoku_array)

    # Now that I have the sudoku board as a 4x4 array, I can solve the puzzle using a backtracking algorithm.
    def is_valid_move(board, row, col, num):
        if num in board[row]:
            return False
        if num in board[:, col]:
            return False
        subgrid = board[row // 2 * 2:row // 2 * 2 + 2, col // 2 * 2:col // 2 * 2 + 2]
        if num in subgrid:
            return False
        return True

    def solve_sudoku(board):
        def solve(row, col):
            if row == 4:
                return True
            next_row = row + 1 if col == 3 else row
            next_col = (col + 1) % 4
            if board[row, col] != 0:
                return solve(next_row, next_col)
            for num in range(1, 5):
                if is_valid_move(board, row, col, num):
                    board[row, col] = num
                    if solve(next_row, next_col):
                        return True
                    board[row, col] = 0
            return False

        solve(0, 0)
        return board

    solved_sudoku = solve_sudoku(sudoku_array)

    # Calculate the Sum of the numbers in empty_cells
    # "emptyCells":[{"x":1,"y":2},{"x":2,"y":0},{"x":3,"y":3},{"x":3,"y":1}]}
    sum = 0
    for empty_cell in empty_cells:
        row = empty_cell["y"]; col = empty_cell["x"]
        sum += solved_sudoku[row][col]
    
    # Convert numpy int64 to Python int before creating the output
    solved_sudoku = solved_sudoku.astype(int)

    # Convert the solved sudoku board to a list of lists with Python int
    solved_sudoku_list = [[int(num) for num in row] for row in solved_sudoku.tolist()]

    # Return the solved sudoku board and the sum
    output = {
        "answer": solved_sudoku_list,
        "sum": int(sum)  # Ensure sum is a Python int
    }
    
    return jsonify(output)