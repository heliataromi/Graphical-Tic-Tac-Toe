import random
import tkinter as tk


class Player:

    def __init__(self, marker="X", is_human=True, colour='#8E44AD'):
        self.marker = marker
        self.is_human = is_human
        self.colour = colour

    def get_computer_move(self, board: list, other_player):
        move = None

        # First situation: There exists a single move such that the computer can win the game.
        if move is None:
            move = find_winning_move(self, board)

        # Second situation: There exists a single move for the player that will cause the computer to lose the game.
        if move is None:
            move = find_winning_move(other_player, board)
            print(f'{move = }')

        # Third situation: At least one of the corner positions (positions 0, 2, 6, or 8) is free.
        if move is None:
            for position in (0, 2, 6, 8):
                if board[position // 3][position % 3] not in ('X', 'O'):
                    move = position
                    break

        # Fourth situation: The center position (position 4) is free.
        if move is None:
            if board[1][1] not in ('X', 'O'):
                move = 4

        # Fifth situation: At least of the side pieces (positions 1, 3, 5, or 7) is free.
        if move is None:
            for position in (1, 3, 5, 7):
                if board[position // 3][position % 3] not in ('X', 'O'):
                    move = position
                    break

        return move


class Board:
    turn = random.randint(0, 1)

    def __init__(self, players: list[Player], root):
        self.game_board = [[0, 1, 2],
                           [3, 4, 5],
                           [6, 7, 8]]
        self.players = players
        self.root = root
        self.root.title("Tic-Tac-Toe")
        self.create_board(root)

        current_player = self.players[Board.turn]
        if not current_player.is_human:
            move = current_player.get_computer_move(self.game_board, self.players[0])
            self.make_move(move, current_player)
        else:
            self.gamestatus.config(text='Game has started.\nIt\'s your turn.')

    def create_board(self, root):
        root.configure(bg='white')
        self.buttons = self.create_buttons(root)
        self.gamestatus = tk.Label(master=self.root,
                                   text='It\'s your turn.',
                                   font=('Calibri', 14, 'bold'),
                                   background='white')
        self.gamestatus.grid(row=3, columnspan=3)
        self.movestatus = tk.Label(master=self.root,
                                   text='',
                                   font=('Calibri', 14, 'bold'),
                                   background='white')
        self.movestatus.grid(row=5, columnspan=3)

    def create_buttons(self, root):
        buttons = list()

        for i in range(3):
            buttons.append([])
            for j in range(3):
                buttons[i].append(tk.Button(master=root,
                                            width=5,
                                            height=3,
                                            bg='white',
                                            text=f'{i * 3 + j}',
                                            font=('Courier', 15, 'bold'),
                                            command=(lambda i=i, j=j: self.pressed(i * 3 + j))))
                buttons[i][j].grid(row=i, column=j)

        return buttons

    def print_board(self):
        # print game_board
        for row in self.game_board:
            print('|'.join(map(str, row)))

    def make_move(self, position: int, player: Player):
        if not player.is_human:
            self.movestatus.config(text=f'Computer\'s move is {position}.')

        self.game_board[position // 3][position % 3] = player.marker
        self.buttons[position // 3][position % 3].config(text=player.marker,
                                                         fg=player.colour,
                                                         activeforeground=player.colour)

        self.print_board()

        if self.is_winner(self.players[0]):
            self.gamestatus.config(text='You won!', fg='#28B463')
            return
        if self.is_winner(self.players[1]):
            self.gamestatus.config(text='You lost!', fg='#CB4335')
            return
        if self.is_tie():
            self.gamestatus.config(text='Game ended with a tie.', fg='#E67E22')
            return

        if player == self.players[1]:
            Board.turn = 0
            print('It\'s your turn.')

        elif player == self.players[0]:
            Board.turn = 1
            print('It\'s computer\'s turn.')

    def is_position_valid(self, position: int):
        # check the position is available
        return self.game_board[position // 3][position % 3] not in ('X', 'O') and 0 <= position <= 8

    def is_winner(self, player: Player):
        # check if player is winning
        mark = player.marker

        # Horizontal states
        for i in range(3):
            if self.game_board[i][0] == mark:
                if self.game_board[i][1] == mark and self.game_board[i][2] == mark:
                    return True

        # Vertical states
        for i in range(3):
            if self.game_board[0][i] == mark:
                if self.game_board[1][i] == mark and self.game_board[2][i] == mark:
                    return True

        # Diagonal states
        if self.game_board[0][0] == mark:
            if self.game_board[1][1] == mark and self.game_board[2][2] == mark:
                return True

        if self.game_board[0][2] == mark:
            if self.game_board[1][1] == mark and self.game_board[2][0] == mark:
                return True

        # Player hasn't won
        return False

    def is_tie(self):
        return all([x in ('X', 'O') for row in self.game_board for x in row])

    def game_has_ended(self):
        for player in self.players:
            if self.is_winner(player):
                return True

        if self.is_tie():
            return True

        return False

    def pressed(self, position: int):
        if not self.game_has_ended():
            if self.is_position_valid(position):
                self.make_move(position, self.players[0])

                if not self.game_has_ended():
                    if Board.turn == 1:
                        self.gamestatus.config(text='It\'s computer\'s turn.')
                        move = self.players[1].get_computer_move(self.game_board, self.players[0])
                        self.make_move(move, players[1])

                        if not self.game_has_ended():
                            self.gamestatus.config(text='It\'s your turn.')


def find_winning_move(player: Player, board: list[list]) -> int:
    '''
    This function will find which move should a player make to win. It will help the computer
    decide how to win or how to prevent the player from winning.
    '''

    mark = player.marker
    other_mark = ''
    if mark == 'X':
        other_mark = 'O'
    if mark == 'O':
        other_mark = 'X'

    # Horizontal states
    for i in range(3):
        if board[i][0] == mark:
            if board[i][1] == mark and board[i][2] != other_mark:
                return i * 3 + 2
            if board[i][2] == mark and board[i][1] != other_mark:
                return i * 3 + 1
        if board[i][0] != other_mark:
            if board[i][1] == mark and board[i][2] == mark:
                return i * 3

    # Vertical states
    for i in range(3):
        if board[0][i] == mark:
            if board[1][i] == mark and board[2][i] != other_mark:
                return i + 6
            if board[2][i] == mark and board[1][i] != other_mark:
                return i + 3
        if board[0][i] != other_mark:
            if board[1][i] == mark and board[2][i] == mark:
                return i

    # Diagonal states
    if board[0][0] == mark:
        if board[1][1] == mark and board[2][2] != other_mark:
            return 8
        if board[2][2] == mark and board[1][1] != other_mark:
            return 4
    if board[0][0] != other_mark:
        if board[1][1] == mark and board[2][2] == mark:
            return 0

    # Diagonal states
    if board[0][2] == mark:
        if board[1][1] == mark and board[2][0] != other_mark:
            return 6
        if board[2][0] == mark and board[1][1] != other_mark:
            return 4
    if board[0][2] != other_mark:
        if board[1][1] == mark and board[2][0] == mark:
            return 2


if __name__ == '__main__':
    root = tk.Tk()

    # Create players
    human = Player('X', True, '#8E44AD')
    computer = Player('O', False, '#3498DB')

    # Create game board
    players = [human, computer]
    board = Board(players, root)

    root.mainloop()
