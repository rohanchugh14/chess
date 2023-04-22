from chess import Chess
from tkinter import *
from tkinter import ttk
from piece import Piece
from board import Board
import os


def main():
    root = Tk()
    root.geometry("500x500")
    root.title("Chess")
    canv = Canvas(root, width = 401, height = 401, highlightthickness=0)
    canv.pack()
    draw_board(canv)
    board = Board()
    # img = PhotoImage(file="../img/white_pawn.png")
    # itm = canv.create_image(100,100, image=img, anchor="nw")
    # canv.tag_bind(itm, "<Button-1>", lambda event: canv.move(itm, 50, 0))
    draw_pieces(canv, board)
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

def draw_pieces(canv, board):
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
                                select_piece(board, piece, canv))
                
                # canv.tag_bind(itm, "<Button-1>", lambda event, \
                #               piece=piece: temp_move_piece(canv, piece))

def temp_move_piece(canv, piece):
    canv.move(piece.get_img(), 0, 50)

def select_piece(board, piece, canv):
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
                            make_move(board, move, canv))

def make_move(board, move, canv):
    captured_piece, discarded, discarded_two = board.make_move(move)
    canv.coords(move.piece.get_img(), move.new_pos[1] * 50, \
                move.new_pos[0] * 50)
    if(captured_piece != None):
        canv.delete(captured_piece.get_img())
    # draw_pieces(canv, board)
    for move in board.shown_moves:
        canv.delete(move.img)
    board.selected_piece = None
    board.update()
    if(board.in_checkmate):
        if(board.in_check):
            print("Checkmate")
        else:
            print("Stalemate")

if __name__ == '__main__':
    main()