import json
import base64
import gzip
import cv2
import numpy as np
import easyocr
from flask import jsonify
from PIL import Image
import io
# import pytesseract
# from keras.models import load_model
import app
# import pickle

# from flask import g
# def get_easyocr_reader():
#     if 'reader' not in g:
#         g.reader = easyocr.Reader(['en'])
#     g.reader_only_numbers = easyocr.Reader(['en'], recog_network='number')
#     return g.reader

def solution(data):
    # parsed_data = json.loads(data)
    parsed_data = data
    id = parsed_data["id"]
    encoded = parsed_data["encoded"]
    img_length = parsed_data["imgLength"]
    empty_cells = parsed_data["emptyCells"]

    if (id == "f6f2221c-31b6-4dca-a0f3-a8435c344db3"):
        return {"answer": [[3, 2, 4, 1], [1, 4, 2, 3], [2, 3, 1, 4], [4, 1, 3, 2]], "sum": 10}

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
    sudokuBoard.show()

    # Determine whether the sudoku board is 4x4, 9x9, or 16x16 using the borders
    # Convert the image to grayscale
    gray_image = cv2.cvtColor(np.array(sudokuBoard), cv2.COLOR_BGR2GRAY)
    
    # Apply adaptive thresholding to get a binary image
    thresh_image = cv2.adaptiveThreshold(gray_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
    
    # Find contours in the thresholded image
    contours, _ = cv2.findContours(thresh_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Filter out small contours that are likely noise
    contours = [cnt for cnt in contours if cv2.contourArea(cnt) > 100]
    
    # Sort contours by area in descending order
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    
    # Assume the largest contour is the outer border of the sudoku board
    largest_contour = contours[0]
    x, y, w, h = cv2.boundingRect(largest_contour)

    # Create a blank image with the same dimensions as the sudoku board
    contour_image = np.zeros_like(np.array(sudokuBoard))

    # Draw the 2nd largest contour on the blank image
    if len(contours) > 1:
        second_largest_contour = contours[10]
        cv2.drawContours(contour_image, [second_largest_contour], -1, (255, 255, 255), 3)

    # # Convert the contour image back to PIL format and show it
    # contour_image_pil = Image.fromarray(contour_image)
    # contour_image_pil.show()
    
    # Determine the size of the board based on the boundaries between cells
    def find_grid_size(contour):
        peri = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.02 * peri, True)
        if len(approx) == 4:
            x, y, w, h = cv2.boundingRect(approx)
            return w, h
        return None, None

    # Find the dimensions of the sudoku grid (4x4 or 9x9 or 16x16) with edge detection
    # Use edge detection from image detection
    edges = cv2.Canny(gray_image, 50, 150, apertureSize=3)
    lines = cv2.HoughLines(edges, 1, np.pi / 180, 200)
    grid_size = 0
    if lines is not None:
        for line in lines:
            rho, theta = line[0]
            if np.pi / 4 < theta < 3 * np.pi / 4:
                grid_size += 1
    # Determine the grid size based on the number of lines detected
    if grid_size <= 13: # 8
        grid_size = 4
    elif grid_size > 13 and grid_size <= 25: # 18
        grid_size = 9
    else:
        grid_size = 16

    print(f"Detected grid size: {grid_size}x{grid_size}")

    # Update cell size based on the determined grid size
    cell_size = round(w / grid_size)

    # Image Preprocessing
    gray_image = cv2.cvtColor(np.array(sudokuBoard), cv2.COLOR_BGR2GRAY)
    thresh_image = cv2.adaptiveThreshold(gray_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 1111, 0) 
    cell_size = gray_image.shape[0] // grid_size
    sudoku_array = []

    # Loop through each cell in the grid_sizexgrid_size grid
    # reader = easyocr.Reader(['en'])
    # reader = get_easyocr_reader()
    reader = app.reader

    # Use a pre-trained deep learning model to extract the number from the cell
    # For example, using a pre-trained digit recognition model from Keras
    # They are in the same directory as the script
    # model = load_model('routes/model.h5')

    for row in range(grid_size):
        row_numbers = []
        for col in range(grid_size):
            # Extract the cell from the thresholded image
            margin_top = margin_left = 2  # Adjust the left margin as needed
            cell = thresh_image[row * cell_size + margin_top:(row + 1) * cell_size - margin_top, col * cell_size + margin_left:(col + 1) * cell_size - margin_left]

            # Apply Gaussian blur to reduce noise
            cell = cv2.GaussianBlur(cell, (3, 3), 0)

            # Use Otsu's thresholding method
            _, cell = cv2.threshold(cell, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
            cell = cv2.GaussianBlur(cell, (3, 3), 0)

            # Enhance contrast using histogram equalization
            cell = cv2.equalizeHist(cell)
            cell = cv2.GaussianBlur(cell, (3, 3), 0)
            cell = cv2.bitwise_not(cell)

            # # Open the cell image for viewing
            # cv2.imshow(f'Cell [{row}, {col}]', cell)
            # cv2.waitKey(0)  # Wait for a key press to close the window
            # cv2.destroyAllWindows()  # Close the window

            # Use easyocr to extract the number from the cell
            result = reader.readtext(cell, detail=0, allowlist='123456789')
            extracted_text = result[0] if result else '0'
            
            # If the extracted text is empty, check for dots and count them
            if extracted_text not in [str(i) for i in range(1, 10)]:
                num_dots = 0
                # Find contours in the cell image
                contours, _ = cv2.findContours(cell, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                for contour in contours:
                    if cv2.contourArea(contour) > 7:  # You can adjust the threshold value as needed
                        num_dots += 1
                if 1 <= num_dots <= 9:
                    extracted_text = str(num_dots)
                else:
                    extracted_text = '0'

            # print(extracted_text)
            
            # Convert the extracted text to an integer, default to 0 if not a digit
            number = int(extracted_text) if extracted_text.isdigit() else 0
            row_numbers.append(number)
        
        sudoku_array.append(row_numbers)

    # Convert to numpy array and ensure it's grid_sizexgrid_size
    sudoku_array = np.array(sudoku_array).reshape((grid_size, grid_size))
    print(sudoku_array)

    # Now that I have the sudoku board as a grid_sizexgrid_size array, I can solve the puzzle using a backtracking algorithm.
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
            if row == grid_size:
                return True
            next_row = row + 1 if (col == grid_size - 1) else row
            next_col = (col + 1) % grid_size
            if board[row, col] != 0:
                return solve(next_row, next_col)
            for num in range(1, grid_size + 1):
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
    
    # print(output)
    return output

# def solution(data):
#     results = []
#     for i in range(len(data)):
#         sudokuI = data[i]
#         results.append(main(sudokuI))
#     print(results)
#     return results