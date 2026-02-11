import tkinter as tk
from tkinter import messagebox

class ColumnIsFullError(Exception):
    pass


def create_matrix(rows, cols):
    return [[0 for _ in range(cols)] for _ in range(rows)]


def place_choice(mtrx, c, player_num):
    for r in range(len(mtrx) - 1, -1, -1):
        if mtrx[r][c] == 0:
            mtrx[r][c] = player_num
            return r, c
    raise ColumnIsFullError


def is_player_num(mtrx, r, c, player_num):
    try:
        return mtrx[r][c] == player_num
    except IndexError:
        return False


def is_vertical_win(mtrx, r, c, player_num, slots):
    return all(is_player_num(mtrx, r + idx, c, player_num) for idx in range(slots))


def is_horizontal_win(mtrx, r, c, player_num, slots):
    filled = 1
    for idx in range(1, slots):
        if is_player_num(mtrx, r, c + idx, player_num):
            filled += 1
        else:
            break

    for idx in range(1, slots):
        if is_player_num(mtrx, r, c - idx, player_num):
            filled += 1
        else:
            break

    return filled >= slots


def is_primary_diagonal_win(mtrx, r, c, player_num, slots):
    filled = 1
    for idx in range(1, slots):
        if is_player_num(mtrx, r + idx, c + idx, player_num):
            filled += 1
        else:
            break

    for idx in range(1, slots):
        if is_player_num(mtrx, r - idx, c - idx, player_num):
            filled += 1
        else:
            break

    return filled >= slots


def is_secondary_diagonal_win(mtrx, r, c, player_num, slots):
    filled = 1
    for idx in range(1, slots):
        if is_player_num(mtrx, r - idx, c + idx, player_num):
            filled += 1
        else:
            break

    for idx in range(1, slots):
        if is_player_num(mtrx, r + idx, c - idx, player_num):
            filled += 1
        else:
            break

    return filled >= slots


def is_winner(mtrx, r, c, player_num, slots):
    return (
            is_vertical_win(mtrx, r, c, player_num, slots) or
            is_horizontal_win(mtrx, r, c, player_num, slots) or
            is_primary_diagonal_win(mtrx, r, c, player_num, slots) or
            is_secondary_diagonal_win(mtrx, r, c, player_num, slots)
    )

def update_ui(labels, row, col, player_num):
    color = "red" if player_num == 1 else "blue"
    labels[row][col].config(bg=color)

def reset_game(mtrx, labels):
    for r in range(len(mtrx)):
        for c in range(len(mtrx[0])):
            mtrx[r][c] = 0
            labels[r][c].config(bg="white")

def handle_column_clicks(mtrx, labels, column_num, player_num, counter, rows, cols, slots):
    try:
        row, column_num = place_choice(mtrx, column_num, player_num)
        update_ui(labels, row, column_num, player_num)
        if is_winner(mtrx, row, column_num, player_num, slots):
            messagebox.showinfo("Game Over", f"the winner is player {player_num}!")
            return 1, 0

        counter += 1
        if counter == rows * cols:
            messagebox.showinfo("Game Over", "The game is a draw!")
            return 1, 0

        return 2 if player_num == 1 else 1, counter
    except ColumnIsFullError:
        messagebox.showerror("Invalid move!" "This column is full! Please choose another column!")

    return player_num, counter

def create_ui(root, rows, cols, slots_to_win):
    matrix = create_matrix(rows, cols)
    labels = [[tk.Label(
        root,
        text=' ',
        width=4,
        height=2,
        bg='white',
        relief='solid',
    ) for _ in range(cols)] for _ in range(rows)]
    for r in range(rows):
        for c in range(cols):
            labels[r][c].grid(row=r, column=c)

    player_state = {"player_number": 1, "counter": 0}

    def button_click(column_num, p_state):
        p_state["player_number"], p_state["counter"] = handle_column_clicks(
            matrix,
            labels,
            column_num,
            player_state["player_number"],
            p_state["counter"],
            rows,
            cols,
            slots_to_win)

    buttons = [tk.Button(
        root,
        text='↓',
        width=4,
        height=2,
        bg='yellow',
        command=lambda c_idx=col: button_click(c_idx, player_state)
    ) for col in range(cols)]

    for col, button in enumerate(buttons):
        button.grid(row=0, column=col)

def start_game():
    root = tk.Tk()
    root.title("Connect Four")

    rows, cols, slots_to_win = 6, 7 ,4
    create_ui(root, rows, cols, slots_to_win)

    root.mainloop()

start_game()