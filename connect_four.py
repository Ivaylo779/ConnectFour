class ColumnOutOfRangeError(Exception):
    pass


class ColumnIsFullError(Exception):
    pass


def create_matrix(rows, cols):
    return [[0 for _ in range(cols)] for _ in range(rows)]


def print_matrix(mtrx):
    for r in mtrx:
        print(r)


def is_valid(column, max_index):
    if not (0 <= column < max_index):
        raise ColumnOutOfRangeError


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


max_slots = 4
row_count = 6
col_count = 7

matrix = create_matrix(row_count, col_count)

print_matrix(matrix)

player = 1

counter = 0

while True:
    try:
        column_num = int(input(f"Player {player}, please choose a column: ")) - 1
        is_valid(column_num, col_count)
        row, col = place_choice(matrix, column_num, player)
        print_matrix(matrix)
    except ValueError:
        print("This is not a number! Please, choose a valid number.")
        continue
    except ColumnOutOfRangeError:
        print("Please, choose a column in range [1-7].")
        continue
    except ColumnIsFullError:
        print("This column is full. Please, select another column.")
        continue

    if is_winner(matrix, row, col, player, max_slots):
        print(f"The winner is player {player}!")
        break

    counter += 1
    if row_count * col_count == counter:
        print("The game ended in a draw!")
        break

    player = 2 if player == 1 else 1
