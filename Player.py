from Board import Board
import Minimax
from Board import Piece


class Player:
    def __init__(self, colour):
        self.colour = colour
        self.board = Board()
        self.i = 0
        self.j = 0
        if colour == 'white':
            self.symbol = 'O'
            self.piece_list = self.board.white_pieces
            self.enemy_list = self.board.black_pieces
            self.enemy = '@'
        else:
            self.j = 7
            self.symbol = '@'
            self.enemy = 'O'
            self.piece_list = self.board.black_pieces
            self.enemy_list = self.board.white_pieces
        self.minimax = Minimax.alphabeta_search(self.symbol, self.enemy, self.board)
        self.moving = False


    def action(self, turns):

        if self.board.count < 24:
            if self.i < 6:
                self.i+=2
            else:
                self.i = 0
                if self.colour == 'white':
                    self.j += 1
                else:
                    self.j -= 1
            piece = Piece(self.symbol, (self.i, self.j), self.board)
            self.piece_list.append(piece)
            piece.makemove((self.i, self.j))
            self.board.count += 1
            return (self.i, self.j)
        else:
            self.board.count += 1
            friends = self.minimax.alphabeta_search()
            return self.minimax.alphabeta_search()


    def update(self, action):
        self.board.count += 1
        if self.board.count < 25:
            piece = Piece(self.enemy, action, self.board)
            self.enemy_list.append(piece)
            piece.makemove(action)

        else:
            piece = self.board.find_piece(action[0])
            self.minimax.makemove(action[1], self.board, self.enemy, piece)
            self.board.count += 1
