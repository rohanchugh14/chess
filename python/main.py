from chess import Chess
from tkinter import *

def main():
    root = Tk()
    root.geometry("500x500")
    root.title("Chess")
    canv = Canvas(root, width = 401, height = 401, highlightthickness=0)
    canv.pack()
    for i in range(8):
        for j in range(8):
            x1 = j * 50
            y1 = i * 50
            x2 = x1 + 50
            y2 = y1 + 50
            fill = "white" if (i+j) % 2 == 0 else "black"
            canv.create_rectangle(x1, y1, x2, y2, fill=fill)
    root.mainloop()
    board = Chess("r1bk3r/p2pBpNp/n4n2/1p1NP2P/6P1/3P4/P1P1K3/q5b1")
    print(board)


if __name__ == '__main__':
    main()