from tkinter import *
from piece import Piece
from board import Board

"""
Name: Rohan Chugh
UTEID: rkc797

On my honor, Rohan Chugh, this programming assignment is my own work
and I have not provided this code to any other student.
Complete the following:
1. What is the purpose of your program?

The purpose of my program is to simulate a local game of Chess using a GUI.

2. List the major features of your program:

The major features of program are:
    - A GUI that displays the current state of the board
    - A reset button that resets the board to the starting position
    - A label that displays the current turn and check/checkmate status
    - A label that displays the instructions for the game
    - Images that appear to represent the pieces
    - Images that appear to represent the legal moves of a piece when it is
    - selected
    - A class for each piece that contains methods for generating legal moves
    - A class for the board that contains methods for updating the board's
    - state and making moves
    - A class for moves that contains the piece that is moving and the new
    - position of the piece

3. What 3rd party modules must be installed for the program to work?
(Must be clear and explicit here or we won't be able to test your program.)

The only 3rd party module that must be installed for the program to work is
Tkinter.

4. List the things your learned while doing this program. Python features,
techniques, third party modules, etc.

I learned how to use Tkinter to create a GUI and how to use the Canvas widget
to draw the board and pieces. I learned a lot about the PhotoImage class, like
how to read in images from the file system with the path and how to use them
in the Canvas. I also learned how to bind mouse events to Canvas objects like
the photo images, and I learned how to do all of this programatically instead
of hard-coding the UI like a lot of the Wordle assignment was. 



5. What was the most difficult thing you had to overcome or learn
to get this program to work?

The most difficult thing I had to overcome was the initial phase of how to
approach creating a board-game and GUI. It would be easy to do something like
create the pieces as images and put them on a UI or to create the chess board
as an image and put it on a UI, but it was much harder to try to figure out
what the best way of creating pieces was, i.e. as objects or images or buttons,
and what the best way to allow the movement of those pieces. I also had a big
time sink in trying to figure out some obscure bugs with how Tkinter's Canvas
photos work, as there is some stuff that is hidden in Python's abstraction in
its garbage collector that I had to learn about to figure out why my images
weren't showing up on the Canvas. It boiled down to the PhotoImage objects 
getting garbage collected before being displayed on the Canvas because tkinter
doesn't save them in memory, which only happens when making an image in a
function since those variables are local to the function (making it a nightmare
to debug since my go-to step was recreate it in a testing file, which worked
perfectly since I didn't recreate it in a test file function). I also had a
hard time figuring out how to make the pieces move, as I had to figure out
how to make the pieces move to the correct position on the board and how to
generate true legal moves, taking into things like not allowing you to put 
yourself in check. Figuring out the best approach to this structure of Chess
was very difficult, and I went through a lot of struggle with how to represent
it using python's OOP features.

6. What features would you add next?
The next features I would add are some things that would allow for more
advanced chess, such as castling, en passant, pawn promotion, and
all the obscure checks for stalemate (with some being 
relatively simple like making the same moveset 3 times in a row) and the
ability to choose what piece  you want to promote your pawn to. There would also
be a lot of very simple nice-to-have features like a timer for each player or
more information on the UI like the number of pieces each player has taken and
what the past moves were. I would also like to add a feature that allows you
to save the full state of the game, as currently you can manually change the
initial state the board is loaded in by adding a parameter to the Board() call,
but it only recreates the piece positions and not the logic like whose turn it 
is or check/checkmate status, which FEN strings have support for. 
"""

def main():
    root = Tk()
    root.geometry("500x550")
    root.title("Chess")
    canv = Canvas(root, width = 401, height = 401, highlightthickness=0)
    canv.pack()
    draw_board(canv)
    # make a general label that will go under the canvas and display the
    # current turn and check/checkmate status
    txt = StringVar()
    txt.set("White's turn\nInstructions: Click on a piece to" + \
                " select it and see its legal moves. Click on one of the" + \
                " legal moves to make that move. ")
    lbl = Label(root, textvariable=txt, font=("Arial", 12), \
                    justify=CENTER)
    lbl.config(wraplength=400)
    lbl.pack()
    reset_btn = Button(root, text="Reset", font=("Arial", 12), command=lambda: \
                       reset(canv, txt, root))
    reset_btn.pack()
    board = Board()
    # img = PhotoImage(file="../img/white_pawn.png")
    # itm = canv.create_image(100,100, image=img, anchor="nw")
    # canv.tag_bind(itm, "<Button-1>", lambda event: canv.move(itm, 50, 0))
    draw_pieces(canv, board, txt, root)
    root.mainloop()

def draw_board(canv):
    for i in range(8):
        for j in range(8):
            x1 = j * 50
            y1 = i * 50
            x2 = x1 + 50
            y2 = y1 + 50
            fill = "white" if (i+j) % 2 == 0 else "black"
            canv.create_rectangle(x1, y1, x2, y2, fill=fill)

def draw_pieces(canv, board, txt, root):
    for i in range(8):
        for j in range(8):
            piece_str = board.get_piece_str(i, j)
            if(piece_str != ' '):
                color = 0 if piece_str.isupper() else 1
                piece_img = Piece.images[color][piece_str.lower()]
                itm = canv.create_image(j * 50, i * 50, image=piece_img,\
                                         anchor="nw")
                piece = board.get_piece(i, j)
                piece.set_img(itm)
                canv.tag_bind(itm, "<Button-1>", lambda event, \
                              piece=piece, canv=canv: \
                                select_piece(board, piece, canv, txt, root))
                
                # canv.tag_bind(itm, "<Button-1>", lambda event, \
                #               piece=piece: temp_move_piece(canv, piece))

def temp_move_piece(canv, piece):
    canv.move(piece.get_img(), 0, 50)

def select_piece(board, piece, canv, txt, root):
    # return early if the wrong piece is trying to be selected
    if(piece.color != board.turn):
        return
    # if a piece is already selected, remove the shown moves
    if(board.selected_piece != None):
        for move in board.shown_moves:
            canv.delete(move.img)
    # select the piece and get the legal moves
    moves = board.select_piece(piece)
    # draw the legal moves
    for i in range(len(moves)):
        move = moves[i]
        itm = canv.create_image(move.new_pos[1] * 50, move.new_pos[0] * 50, \
                                image=Piece.DOT_IMAGE, anchor="nw")
        move.set_img(itm)
        # bind a make move to the on click
        canv.tag_bind(itm, "<Button-1>", lambda event, \
                        move=move, board=board, canv=canv: \
                            make_move(board, move, canv, txt, root))

def make_move(board, move, canv, txt, root):
    # cool way to discard the return values of a function :)
    # returns the old row and col of the piece that was moved
    # to allow using the same method for temp moves for pruning,
    # but not necessary for actual moves since the piece doesn't
    # need to go back to its original position
    captured_piece, _, _ = board.make_move(move)
    canv.coords(move.piece.get_img(), move.new_pos[1] * 50, \
                move.new_pos[0] * 50)
    if(captured_piece != None):
        canv.delete(captured_piece.get_img())
    # draw_pieces(canv, board)
    for move in board.shown_moves:
        canv.delete(move.img)
    board.selected_piece = None
    board.update()
    # no legal moves left, check for checkmate or stalemate
    if(board.in_checkmate):
        if(board.in_check):
            color = "White" if board.turn == 1 else "Black"
            txt.set("Checkmate! " + color + " wins!")
        else:
            txt.set("It's a stalemate! Draw!")
        
    elif(board.in_check):
        color = "White" if board.turn == 0 else "Black"
        txt.set(color + " is in check!")
        # ask to reset board
        # create button to reset board
        
    else:            
        txt.set("White's turn" if board.turn == 0 else "Black's turn")

def reset(canv, txt, root):
    # clear the canvas
    canv.delete("all")
    # draw the board
    draw_board(canv)
    # create a new board
    board = Board()
    # draw the pieces
    draw_pieces(canv, board, txt, root)
    txt.set("White's turn\nInstructions: Click on a piece to" + \
                " select it and see its legal moves. Click on one of the" + \
                " legal moves to make that move. ")
    # board.update()

if __name__ == '__main__':
    main()