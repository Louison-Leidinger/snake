import tkinter as tk
import random

square_size = 100
rows = 10
cols = 10
speed = 100  # Vitesse de déplacement du serpent, en millisecondes

def generate_matrix(rows, cols):
    matrix = [[0 for _ in range(cols)] for _ in range(rows)]
    def place_block():
        while True:
            start_row = random.randint(0, rows - 1)
            start_col = random.randint(0, cols - 1)
            direction = random.choice(['horizontal', 'vertical'])
            if direction == 'horizontal' and start_col <= cols - 3:
                if all(matrix[start_row][start_col + i] == 0 for i in range(3)):
                    for i in range(3):
                        matrix[start_row][start_col + i] = 1
                    return [(start_row, start_col + i) for i in range(3)]
            elif direction == 'vertical' and start_row <= rows - 3:
                if all(matrix[start_row + i][start_col] == 0 for i in range(3)):
                    for i in range(3):
                        matrix[start_row + i][start_col] = 1
                    return [(start_row + i, start_col) for i in range(3)]
    return matrix, place_block()

matrix, current_positions = generate_matrix(rows, cols)

root = tk.Tk()
root.title("Snake")
canvas_width = cols * square_size
canvas_height = rows * square_size
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
canvas.pack()

def draw_matrix():
    canvas.delete("all")
    for i in range(rows):
        for j in range(cols):
            x0 = j * square_size
            y0 = i * square_size
            x1 = x0 + square_size
            y1 = y0 + square_size
            color = 'red' if matrix[i][j] == 1 else 'black'
            canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline='red')

current_direction = 'Right'

def move():
    global current_positions, current_direction
    head_x, head_y = current_positions[0]
    direction_moves = {
        "Up": ((head_x - 1) % rows, head_y),
        "Down": ((head_x + 1) % rows, head_y),
        "Left": (head_x, (head_y - 1) % cols),
        "Right": (head_x, (head_y + 1) % cols)
    }
    new_head_pos = direction_moves[current_direction]
    if matrix[new_head_pos[0]][new_head_pos[1]] == 0 or new_head_pos in current_positions:
        for i in range(len(current_positions) - 1, 0, -1):
            current_positions[i] = current_positions[i - 1]
        current_positions[0] = new_head_pos
        for i in range(rows):
            for j in range(cols):
                matrix[i][j] = 0
        for pos in current_positions:
            matrix[pos[0]][pos[1]] = 1
        draw_matrix()
    root.after(speed, move)

def change_dir(new_direction):
    global current_direction
    opposite_directions = {'Up': 'Down', 'Down': 'Up', 'Left': 'Right', 'Right': 'Left'}
    if new_direction != opposite_directions.get(current_direction):
        current_direction = new_direction

root.bind("<Up>", lambda e: change_dir('Up'))
root.bind("<Down>", lambda e: change_dir('Down'))
root.bind("<Left>", lambda e: change_dir('Left'))
root.bind("<Right>", lambda e: change_dir('Right'))

draw_matrix()
move()

root.mainloop()
