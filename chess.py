def pawn(x, y, board):
    color = board[x][y].color
    moves = []
    if color == "white":
        if board[x + 1][y].color != "white":
            moves.append((x + 1, y))
            if x == 1 and board[x + 2][y].color != "white":
                moves.append((x + 2, y))
        if y < 7 and board[x + 1][y + 1].color == "black":
            moves.append((x + 1, y + 1))
        if y > 0 and board[x + 1][y - 1].color == "black":
            moves.append((x + 1, y - 1))

    if color == "black":
        if board[x - 1][y].color != "black":
            moves.append((x - 1, y))
            if x == 6 and board[x - 2][y].color != "black":
                moves.append((x - 2, y))
        if y < 7 and board[x - 1][y + 1].color == "white":
            moves.append((x - 1, y + 1))
        if y > 0 and board[x - 1][y - 1].color == "white":
            moves.append((x - 1, y - 1))

    return moves


def bishop(x, y, board):
    color = board[x][y].color
    moves = []
    for i in range(1, min(x, y) + 1):
        clr = board[x - i][y - i].color
        if clr is None:
            moves.append((x - i, y - i))
        elif clr != color:
            moves.append((x - i, y - i))
            break
        else:
            break

    for i in range(1, min(x, 8 - y - 1) + 1):
        clr = board[x - i][y + i].color
        if clr is None:
            moves.append((x - i, y + i))
        elif clr != color:
            moves.append((x - i, y + i))
            break
        else:
            break

    for i in range(1, min(8 - x - 1, y) + 1):
        clr = board[x + i][y - i].color
        if clr is None:
            moves.append((x + i, y - i))
        elif clr != color:
            moves.append((x + i, y - i))
            break
        else:
            break

    for i in range(1, min(8 - x - 1, 8 - y - 1) + 1):
        clr = board[x + i][y + i].color
        if clr is None:
            moves.append((x + i, y + i))
        elif clr != color:
            moves.append((x + i, y + i))
            break
        else:
            break

    return moves


def rook(x, y, board):
    color = board[x][y].color
    moves = []
    for i in range(1, x + 1):
        clr = board[x - i][y].color
        if clr is None:
            moves.append((x - i, y))
        elif clr != color:
            moves.append((x - i, y))
            break
        else:
            break

    for i in range(1, 7 - x + 1):
        clr = board[x + i][y].color
        if clr is None:
            moves.append((x + i, y))
        elif clr != color:
            moves.append((x + i, y))
            break
        else:
            break

    for i in range(1, y + 1):
        clr = board[x][y - i].color
        if clr is None:
            moves.append((x, y - i))
        elif clr != color:
            moves.append((x, y - i))
            break
        else:
            break

    for i in range(1, 7 - y + 1):
        clr = board[x][y + i].color
        if clr is None:
            moves.append((x, y + i))
        elif clr != color:
            moves.append((x, y + i))
            break
        else:
            break

    return moves


def knight(x, y, board):
    color = board[x][y].color
    pos_moves = [
        (x - 2, y - 1), (x - 1, y - 2),
        (x + 1, y - 2), (x + 2, y - 1),
        (x - 2, y + 1), (x - 1, y + 2),
        (x + 1, y + 2), (x + 2, y + 1),
    ]
    moves = []

    for i in pos_moves:
        x, y = i[0], i[1]
        if 0 <= i[0] <= 7 and 0 <= i[1] <= 7 and board[x][y].color != color:
            moves.append((x, y))

    return moves


def queen(x, y, board):
    moves = bishop(x, y, board) + rook(x, y, board)

    return moves


def king(x, y, board, enemy_moves):
    moves = []
    color = board[x][y].color
    enemy_moves = set(enemy_moves)
    pos_moves = [
        (x - 1, y - 1), (x - 1, y),
        (x - 1, y + 1), (x, y - 1),
        (x, y + 1), (x + 1, y - 1),
        (x + 1, y), (x + 1, y + 1),
    ]
    for i in pos_moves:
        x, y = i[0], i[1]
        if 0 <= i[0] <= 7 and 0 <= i[1] <= 7 and board[x][y].color != color and (x, y) not in enemy_moves:
            moves.append((x, y))

    return moves


class Chess:

    class Cell:
        def __init__(self, x, y, figure=None, color=None):
            self.figure = figure
            self.color = color
            self.x = x
            self.y = y
            self.moves = []

        def get_moves(self, x, y, figure, board):
            if figure is not None:
                if figure == "pawn":
                    self.moves = pawn(x, y, board)
                if figure == "bishop":
                    self.moves = bishop(x, y, board)
                if figure == "knight":
                    self.moves = knight(x, y, board)
                if figure == "rook":
                    self.moves = rook(x, y, board)
                if figure == "queen":
                    self.moves = queen(x, y, board)
                if figure == "king":
                    enemy_moves = []
                    for x in range(8):
                        for fig in board[x]:
                            if fig.x != x and fig.y != y and fig.color is not None and fig.color != board[x][y].color:
                                enemy_moves += fig.moves
                    self.moves = king(x, y, board, enemy_moves)

            return self.moves

        def correct_kings(self, white, black, board):
            x, y = black[0], black[1]
            fig = board[white[0]][white[1]]
            white_moves = []
            black_moves = {
                (x - 1, y - 1), (x - 1, y),
                (x - 1, y + 1), (x, y - 1),
                (x, y + 1), (x + 1, y - 1),
                (x + 1, y), (x + 1, y + 1),
            }
            for i in fig.moves:
                if i not in black_moves:
                    white_moves.append(i)

            self.moves = white_moves
            return self.moves

    def __init__(self):
        self.board = [[self.Cell(x, y) for y in range(8)] for x in range(8)]

        white_figures = {
            "pawn": [(1, y) for y in range(8)],
            "bishop": [(0, 2), (0, 5)],
            "rook": [(0, 0), (0, 7)],
            "knight": [(0, 1), (0, 6)],
            "queen": [(0, 3)],
            "king": [(0, 4)],
        }
        black_figures = {
            "pawn": [(6, y) for y in range(8)],
            "bishop": [(7, 2), (7, 5)],
            "rook": [(7, 0), (7, 7)],
            "knight": [(7, 1), (7, 6)],
            "queen": [(7, 3)],
            "king": [(7, 4)]
        }

        for fig in white_figures:
            for pos in white_figures[fig]:
                x, y = pos[0], pos[1]
                self.board[x][y] = self.Cell(x, y, fig, 'white')

        for fig in black_figures:
            for pos in black_figures[fig]:
                x, y = pos[0], pos[1]
                self.board[x][y] = self.Cell(x, y, fig, 'black')

        white_moves, black_moves = self.get_possible_moves()

        # for x in range(8):
        #     for fig in self.board[x]:
        #         print(fig.color, fig.figure, fig.x, fig.y)
        #         print(fig.moves)

    def get_possible_moves(self):
        black_moves = []
        white_moves = []
        white_king = ()
        black_king = ()
        for x in range(8):
            for fig in self.board[x]:
                if fig.figure == "king":
                    if fig.color == "white":
                        white_king = (fig.x, fig.y)
                    else:
                        black_king = (fig.x, fig.y)
                    continue

                if fig.figure is not None:
                    x, y = fig.x, fig.y
                    moves = fig.get_moves(x, y, fig.figure, self.board)
                    if fig.color == "white":
                        white_moves += moves
                    else:
                        black_moves += moves

        x, y = white_king[0], white_king[1]
        self.board[x][y].get_moves(x, y, self.board[x][y].figure, self.board)

        x, y = black_king[0], black_king[1]
        black_moves += self.board[x][y].get_moves(x, y, self.board[x][y].figure, self.board)

        white_moves += self.board[x][y].correct_kings(white_king, black_king, self.board)

        return white_moves, black_moves

    def check(self, cnt):
        for x in range(8):
            for fig in self.board[x]:
                for move in fig.moves:
                    figure = self.board[move[0]][move[1]]
                    if figure.figure == "king":
                        if (cnt == 0 and figure.color == "white") or (cnt == 1 and figure.color == "black"):
                            print("INCORRECT")
                            return True

        return False

    def make_move(self, pos1, pos2, cnt):
        x1, y1 = int(pos1[1]) - 1, ord(pos1[0]) - ord('a')
        x2, y2 = int(pos2[1]) - 1, ord(pos2[0]) - ord('a')
        # print(x1, y1, x2, y2)

        fig = Board.board[x1][y1]
        # print(fig.moves, fig.figure, fig.color, fig.x, fig.y)
        # print(cnt)
        # print(cnt == 0, fig.color == "white", (x2, y2) in fig.moves)

        if cnt == 0 and fig.color == "white" and (x2, y2) in fig.moves or \
                cnt == 1 and fig.color == "black" and (x2, y2) in fig.moves:
            figure = fig.figure
            color = fig.color
            old_figure = self.board[x2][y2].figure
            old_color = self.board[x2][y2].color
            self.board[x1][y1] = self.Cell(x1, y1)

            if (x2 == 0 or x2 == 7) and figure == "pawn":
                figure = "queen"

            self.board[x2][y2] = self.Cell(x2, y2, figure, color)

            white_moves, black_moves = self.get_possible_moves()

            if self.check(cnt):
                figure = fig.figure
                color = fig.color
                self.board[x1][y1] = self.Cell(x1, y1, figure, color)
                self.board[x2][y2] = self.Cell(x2, y2, old_figure, old_color)

                white_moves, black_moves = self.get_possible_moves()

                return False

            else:
                # for x in range(8):
                #     for fig1 in self.board[x]:
                #         print(fig1.color, fig1.figure, fig1.x, fig.y)
                #         print(fig1.moves)
                #
                self.print_board()

                return True

        else:
            return False

    def print_board(self):
        for i in range(8):
            for fig in self.board[i]:
                if fig.figure is None:
                    print(" __ ", end=' ')
                else:
                    print(fig.figure[:4], end=' ')
            print()
        print()


if __name__ == "__main__":
    Board = Chess()
    cnt = 0
    while True:
        pos1, pos2 = [i for i in input().split()]
        Board.make_move(pos1, pos2, cnt)
        cnt = (cnt + 1) % 2


"""
e2 e4
e7 e5
d1 h5
g8 f6
h5 e5

e2 e4
e7 e5
f2 f4
d8 h4
g2 g3
h4 g3
h2 g3
e5 f4
h1 h2
f4 g3
h2 h1
g3 g2
a2 a4
g2 h1

e2 e4
e7 e5
f2 f4
d8 h4
g2 g3
h4 g3


"""