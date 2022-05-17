# -*- coding: utf-8 -*-
import tkinter as tk


class Chess(object):
    def __init__(self):
        self.IsClicked = False
        self.WhoMoves = "red"
        self.SCALE = 2
        self.letters = ["A", "B", "C", "D", "E", "F", "G", "H"]
        self.letter_to_index = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6, "H": 7}
        # lables = list of lists (8, 8)
        self.desk, self.labels = self.MakeDesk()

    def GetLabel(self, colrow):

        pos = colrow[0] + str(colrow[1])
        i, j = self.GetIndexByPos(pos)
        label = self.labels[i][j]
        return label

    def CanMove(self, step, label, posible_steps):
        distinatination_label = self.GetLabel(step)
        if distinatination_label["text"] != "":
            if distinatination_label["fg"] != label["fg"]:
                posible_steps.append(step)
            return False

        posible_steps.append(step)
        return True

    def Move(self, new_pos, old_pos):
        old_text = self.GetLabel(old_pos)["text"]
        old_fg = self.GetLabel(old_pos)["fg"]
        new_text = self.GetLabel(new_pos)["text"]
        new_fg = self.GetLabel(new_pos)["fg"]
        self.GetLabel(new_pos)["text"] = old_text
        self.GetLabel(new_pos)["fg"] = old_fg
        self.GetLabel(old_pos)["text"] = ""
        self.WhoMoves = "red" if self.WhoMoves == "green" else "green"
        self.last_move1 = (old_pos, old_text, old_fg)
        self.last_move2 = (new_pos, new_text, new_fg)

    def UnMove(self):
        self.GetLabel(self.last_move1[0])["text"] = self.last_move1[1]
        self.GetLabel(self.last_move1[0])["fg"] = self.last_move1[2]
        self.GetLabel(self.last_move2[0])["text"] = self.last_move2[1]
        self.GetLabel(self.last_move2[0])["fg"] = self.last_move2[2]
        self.WhoMoves = "red" if self.WhoMoves == "green" else "green"

    def PosibleSteps(self, row, column):
        posible_steps = []
        pos = column + str(row)
        i, j = self.GetIndexByPos(pos)
        label = self.labels[i][j]
        # inf = (row, column, label["text"], label["fg"])
        if label["text"] == "P":
            column_index = self.letter_to_index[column]
            if label["fg"] == "red":
                kill_step_r = [(chr(ord(column) + 1), row + 1)]
                kill_step_l = [(chr(ord(column) - 1), row + 1)]
                step = [(column, row + 1), (column, row + 2)]
            if label["fg"] == "green":
                kill_step_r = [(chr(ord(column) + 1), row - 1)]
                kill_step_l = [(chr(ord(column) - 1), row - 1)]
                step = [(column, row - 1), (column, row - 2)]
            if kill_step_r[0][0] in {chr(ord("A") - 1), "I"} or self.GetLabel(kill_step_r[0])["text"] == "" or \
                    self.GetLabel(kill_step_r[0])["fg"] == label["fg"]:
                kill_step_r = []
            if kill_step_l[0][0] in {chr(ord("A") - 1), "I"} or self.GetLabel(kill_step_l[0])["text"] == "" or \
                    self.GetLabel(kill_step_l[0])["fg"] == label["fg"]:
                kill_step_l = []
            if self.GetLabel(step[0])["text"] != "":
                step = []
            elif row == 2:
                if self.GetLabel(step[1])["text"] != "":
                    step.pop(1)
            elif row == 7:
                if self.GetLabel(step[1])["text"] != "":
                    step.pop(1)
            else:
                step.pop(1)

            # дописать ходы наискосок
            posible_steps = step + kill_step_l + kill_step_r

        if label["text"] == "R" or label["text"] == "Q":
            for i in range(row - 1, 0, -1):
                step = (column, i)
                if self.CanMove(step, label, posible_steps) == False:
                    break

            for i in range(row + 1, 9):
                step = (column, i)
                if self.CanMove(step, label, posible_steps) == False:
                    break

            column_index = self.letter_to_index[column]
            for i in reversed(self.letters[0: column_index:]):
                step = (i, row)
                if self.CanMove(step, label, posible_steps) == False:
                    break
            for i in self.letters[column_index + 1: 8]:
                step = (i, row)
                if self.CanMove(step, label, posible_steps) == False:
                    break

        if label["text"] == "E" or label["text"] == "Q":
            column_index = self.letter_to_index[column]
            down = 1
            up = 1
            left = 1
            right = 1
            for i in range(row - 1, 0, -1):
                down += 1
            for i in range(row + 1, 9):
                up += 1
            for i in reversed(self.letters[0: column_index:]):
                left += 1
            for i in self.letters[column_index + 1: 8]:
                right += 1
            for i in range(1, min(up, left)):
                step = (self.letters[column_index - i], row + i)
                if self.CanMove(step, label, posible_steps) == False:
                    break
            for i in range(1, min(up, right)):
                step = (self.letters[column_index + i], row + i)
                if self.CanMove(step, label, posible_steps) == False:
                    break
            for i in range(1, min(down, left)):
                step = (self.letters[column_index - i], row - i)
                if self.CanMove(step, label, posible_steps) == False:
                    break
            for i in range(1, min(down, right)):
                step = (self.letters[column_index + i], row - i)
                if self.CanMove(step, label, posible_steps) == False:
                    break

        if label["text"] == "H":
            column_index = self.letter_to_index[column]
            for step in [
                (column_index - 2, row - 1),
                (column_index - 2, row + 1),
                (column_index - 1, row + 2),
                (column_index + 1, row + 2),
                (column_index + 2, row + 1),
                (column_index + 2, row - 1),
                (column_index + 1, row - 2),
                (column_index - 1, row - 2)
            ]:
                if 0 < step[1] <= 8 and 0 <= step[0] <= 7:
                    step = (self.letters[step[0]], step[1])

                    self.CanMove(step, label, posible_steps)

        if label["text"] == "K":
            column_index = self.letter_to_index[column]
            for step in [
                (column_index - 1, row + 1),
                (column_index, row + 1),
                (column_index + 1, row + 1),
                (column_index - 1, row),
                (column_index - 1, row - 1),
                (column_index, row - 1),
                (column_index + 1, row - 1),
                (column_index + 1, row)
            ]:
                if 0 < step[1] <= 8 and 0 <= step[0] <= 7:
                    step = (self.letters[step[0]], step[1])

                    self.CanMove(step, label, posible_steps)
        return posible_steps

    def OnClick(self, row, column):
        new_pos = (column, row)
        if self.IsClicked == False and self.GetLabel(new_pos)["fg"] == self.WhoMoves:
            self.posible_steps = []
            posible_steps_without_cheks = self.PosibleSteps(row, column)
            print('posible_steps_without_cheks', posible_steps_without_cheks)
            for i in posible_steps_without_cheks:
                pos = (column, row)
                self.Move(i, pos)
                all_posible_step = []
                for j in ("A", "B", "C", "D", "E", "F", "G", "H"):
                    for x in range(1, 9):
                        if self.GetLabel((j, x))["fg"] != self.WhoMoves and self.GetLabel((j, x))["text"] == "K":
                            kings_pos = (j, x)
                        if self.GetLabel((j, x))["fg"] == self.WhoMoves:
                            posible_steps = self.PosibleSteps(x, j)
                            all_posible_step += posible_steps
                            if ("E", 8) in posible_steps:
                                print(j, x)
                                print(self.GetLabel((j, x))["text"])
                if kings_pos not in all_posible_step:
                    self.posible_steps.append(i)
                self.UnMove()
            self.old_pos = new_pos
            for i in self.posible_steps:
                self.GetLabel(i)["bg"] = "blue"
            self.IsClicked = True
        elif self.IsClicked == True:
            if (new_pos) in self.posible_steps:
                self.Move(new_pos, self.old_pos)
            else:
                print("походите заново")
            self.IsClicked = False
            for i in range(8):
                for j in range(8):
                    if (j + i) % 2 != 0:
                        col = "black"
                    else:
                        col = "white"
                    label = self.labels[i][j]
                    label["bg"] = col

    def GetIndexByPos(self, pos):
        i = 8 - int(pos[1])
        j = self.letter_to_index[pos[0].upper()]
        return i, j

    def MakeDesk(self):
        desk = tk.Tk()
        frame_num = tk.Frame(desk)
        frame_num.pack(side=tk.LEFT, anchor=tk.NW)
        for i in range(1, 9):
            label = tk.Label(frame_num, text=i, bg="green", width=self.SCALE * 2, height=self.SCALE)
            label.pack(side=tk.BOTTOM)
        frame_let = tk.Frame(desk)
        frame_let.pack(side=tk.BOTTOM, anchor=tk.SE)
        for i in self.letters:
            label = tk.Label(frame_let, text=i, bg="red", width=self.SCALE * 2, height=self.SCALE)
            label.pack(side=tk.LEFT)
        chess_frame = tk.Frame(desk)
        chess_frame.pack()
        labels = []
        for i in range(8):
            labels.append([])
            for j in range(8):
                if (j + i) % 2 != 0:
                    col = "black"
                else:
                    col = "white"
                label = tk.Label(chess_frame, bg=col, width=self.SCALE * 2, height=self.SCALE)
                label.grid(row=i, column=j)
                label.bind("<Button-1>", lambda event, row=8 - i, column=self.letters[j]: self.OnClick(row, column))
                labels[i].append(label)
            # label["text"] = "a"

        return desk, labels

    def PlaceFigureOnBoard(self, pos, figure, color):
        # pos - string ("A2"), figure - string "P", color - string ("W" or "B")
        i, j = self.GetIndexByPos(pos)
        label = self.labels[i][j]  # TODO

        label["text"] = figure
        label["fg"] = "green" if color == "W" else "red"

    def Run(self):
        self.desk.mainloop()


if __name__ == "__main__":
    board = Chess()

    board.PlaceFigureOnBoard("a7", "P", "W")
    board.PlaceFigureOnBoard("b7", "P", "W")
    board.PlaceFigureOnBoard("c7", "P", "W")
    board.PlaceFigureOnBoard("d7", "P", "W")
    board.PlaceFigureOnBoard("e7", "P", "W")
    board.PlaceFigureOnBoard("f7", "P", "W")
    board.PlaceFigureOnBoard("g7", "P", "W")
    board.PlaceFigureOnBoard("h7", "P", "W")
    board.PlaceFigureOnBoard("a8", "R", "W")
    board.PlaceFigureOnBoard("h8", "R", "W")
    board.PlaceFigureOnBoard("b8", "H", "W")
    board.PlaceFigureOnBoard("c8", "E", "W")
    board.PlaceFigureOnBoard("d8", "Q", "W")
    board.PlaceFigureOnBoard("e8", "K", "W")
    board.PlaceFigureOnBoard("g8", "H", "W")
    board.PlaceFigureOnBoard("f8", "E", "W")

    board.PlaceFigureOnBoard("a2", "P", "B")
    board.PlaceFigureOnBoard("b2", "P", "B")
    board.PlaceFigureOnBoard("c2", "P", "B")
    board.PlaceFigureOnBoard("d2", "P", "B")
    board.PlaceFigureOnBoard("e2", "P", "B")
    board.PlaceFigureOnBoard("f2", "P", "B")
    board.PlaceFigureOnBoard("g2", "P", "B")
    board.PlaceFigureOnBoard("h2", "P", "B")
    board.PlaceFigureOnBoard("a1", "R", "B")
    board.PlaceFigureOnBoard("h1", "R", "B")
    board.PlaceFigureOnBoard("b1", "H", "B")
    board.PlaceFigureOnBoard("c1", "E", "B")
    board.PlaceFigureOnBoard("d1", "Q", "B")
    board.PlaceFigureOnBoard("e1", "K", "B")
    board.PlaceFigureOnBoard("g1", "H", "B")
    board.PlaceFigureOnBoard("f1", "E", "B")

    board.Run()