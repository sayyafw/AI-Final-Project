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
        self.actions = []


    def action(self, turns):

        if self.board.count < 24:
            placing_phase()
            """
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
            """
        else:
            self.board.count += 1
            friends = self.minimax.alphabeta_search()
            return self.minimax.alphabeta_search()

    def place(self, (self.i, self.j), self.board):
        """
        place a piece on the board
        """
         piece = Piece(self.symbol, (self.i, self.j), self.board)
         self.piece_list.append(piece)
         return piece


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

##############################################################################

    def placing_phase():
        """ 
        start the simulation for placing phase depending on player's colour
        """
        turn = self.board.count
        a = 1000
        b = -1000
        depth = 0
        if colour == white:
            white_place(self.board, depth, a, b, turn)
        else:
            black_place(self.board, depth, a, b, turn)

    def min(self, state, depth, a, b, turn, colour):
        turn+=1
        depth+=1
        if (depth == 2 or turn >=24):
            return 

    def max(self, state, depth, a, b, turn, colour):
        turn+=1
        depth+=1
        if (depth == 2 or turn >=24):
            return self.minimax.eval_placeing(self.board, colour)
        if (colour == white):
            white_place()
        else:
            black_place()
        
    def white_place(self):
        ystart = 0
        yend = 5
        for x in range(7):
            for y in range(ystart, yend):
                if not self.board.isEmpty(x,y):
                    place_sim(self.board, (x,y))
        return

    def black_place(self, Board, depth, a, b, turn):
        ystart = 2
        yend = 7
   
        return

    def place_sim(self, Board, pos):
    """
    simulate placing a piece on the board
    """
        actions.append(("Place", pos))
        place(pos, self.board)
        eliminated = eliminate_surround(pos)
        if eliminated != []:
            actions.append(("Eliminated", eliminated))
        return
