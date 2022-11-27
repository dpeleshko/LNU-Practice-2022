from random import randint

# Board for holding ship locations
HIDDEN_BOARD = [[" "] * 10 for x in range(10)]
# Board for displaying hits and misses
GUESS_BOARD = [[" "] * 10 for i in range(10)]


def print_board(board):
    print("    А  Б  В  Г  Д  Е  Є  Ж  З  И  ")
    row_number = 0
    for row in board:
        print("%d | %s|" % (row_number, "| ".join(row)))
        row_number += 1


letters_to_numbers = {
    'А': 0,
    'Б': 1,
    'В': 2,
    'Г': 3,
    'Д': 4,
    'Е': 5,
    'Є': 6,
    'Ж': 7,
    'З': 8,
    'И': 9
}

def create_ships(board):
    for ship in range(15):
        ship_row, ship_column = randint(0, 9), randint(0, 9)
        while board[ship_row][ship_column] == "X":
            ship_row, ship_column = get_ship_location()
        board[ship_row][ship_column] = "X"


def get_ship_location():

    row = input("Введіть цифру рядка: ").upper()
    while row not in "0123456789":
        print('Ви ввели некоректне значення, спробуйте ще раз')
        row = input("Введіть рядок: ").upper()
    column = input("Введіть стовпчик: ").upper()
    while column not in "АБВГДЕЄЖЗИ":
        print('Ви ввели некоректне значення, спробуйте ще раз')
        column = input("Введіть букву стовпчика: ").upper()
    return int(row) , letters_to_numbers[column]


def count_hit_ships(board):
    count = 0
    for row in board:
        for column in row:
            if column == "X":
                count += 1
    return count


if __name__ == "__main__":
    create_ships(HIDDEN_BOARD)
    turns = 10
    while turns > 0:
        print('Вгадайте місце розташування корабля ')
        print_board(GUESS_BOARD)
        row, column = get_ship_location()
        if GUESS_BOARD[row][column] == "-":
            print("Ви вже стріляли сюди ")
        elif HIDDEN_BOARD[row][column] == "X":
            print("Влучив!")
            GUESS_BOARD[row][column] = "X"
            turns -= 1  
        else:
            print("Промазав!")
            GUESS_BOARD[row][column] = "-"
            turns -= 1     
        if count_hit_ships(GUESS_BOARD) == 5:
            print("Ви виграли!")
            break
        print("У Вас залишилось " + str(turns) + " пострілів")
        if turns == 0:
            print("Постріли закінчилися..")