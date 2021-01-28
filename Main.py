import random
from tkinter import *
from tkinter import messagebox


class Space:
    def __init__(self, master, space_num):
        self.type = random.choice(['empty', 'filled', 'bomb'])
        self.text = StringVar()
        self.text.set(" ")
        self.widget = None
        self.master = master

        self.space_num = space_num

    def find_widget(self, spaces, index):
        # Find the number of bombs around the space, unless this space is a bomb, and it must be empty
        number_of_bombs = 0
        if self.type == 'empty':
            for y in range(index[0] - 1, index[0] + 2):
                for x in range(index[1] - 1, index[1] + 2):
                    if y == -1 or x == -1:
                        continue
                    try:
                        if spaces[y][x].type == 'bomb':
                            number_of_bombs += 1
                    except IndexError:
                        continue

        if number_of_bombs != 0:
            self.text.set(str(number_of_bombs))

        # Determine the widget to be used
        if self.type == 'filled' or self.type == 'bomb':
            self.widget = Button(self.master, textvariable=self.text, width=10, height=5,
                                 command=self.reveal)

        else:
            self.widget = Label(self.master, textvariable=self.text, width=10, height=5)

    def reveal(self):
        Application.reveal(app, space_index=self.space_num)


class Application:
    def __init__(self):
        self.root = Tk()
        self.root.title("Minesweeper")
        self.root.resizable(width=False, height=False)
        self.root.geometry("1200x594")
        self.spaces = []

        self.playing = True
        self.flag = False
        self.flag_state_var = StringVar()
        self.flag_state_var.set("Mining")

        self.toggle_flagging = Button(self.root, text="Toggle flag", width=20, height=30, command=self.toggle_flag)
        self.toggle_flagging.place(x=1000, y=0)

        self.flag_state = Label(self.root, textvariable=self.flag_state_var, width=20, height=5)
        self.flag_state.place(x=1000, y=500)

        self.fill_spaces()

    def fill_spaces(self):
        for y in range(0, 600, 100):
            self.spaces.append([])
            for x in range(0, 1000, 100):
                self.spaces[int(y/100)].append(Space(self.root, [int(y/100), int(x/100)]))

        for y in range(0, len(self.spaces)):
            for x in range(0, len(self.spaces[y])):
                self.spaces[y][x].find_widget(self.spaces, [y, x])

        for y in range(0, 600, 100):
            for x in range(0, 1000, 100):
                self.spaces[int(y/100)][int(x/100)].widget.place(x=x, y=y)

    def reveal(self, space_index):
        if self.playing:
            if self.flag:
                self.spaces[space_index[0]][space_index[1]].text.set("X")
                return

            if self.spaces[space_index[0]][space_index[1]].type == 'bomb':
                messagebox.showinfo("GAME OVER", "You hit a bomb.")
                self.playing = False

            self.spaces[space_index[0]][space_index[1]].widget.forget()
            self.spaces[space_index[0]][space_index[1]] = Space(self.root, space_index)
            self.spaces[space_index[0]][space_index[1]].type = 'empty'
            self.spaces[space_index[0]][space_index[1]].find_widget(self.spaces, space_index)

            for y in range(0, 600, 100):
                for x in range(0, 1000, 100):
                    self.spaces[int(y/100)][int(x/100)].widget.place(x=x, y=y)

    def toggle_flag(self):
        self.flag = not self.flag

        if self.flag:
            self.flag_state_var.set("Flagging")
        else:
            self.flag_state_var.set("Mining")


if __name__ == "__main__":
    app = Application()
    app.root.mainloop()
