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

        #Variables used to judge map shrink
        self.shorten1 = 127
        self.shorten2 = 128
        self.shortened = 0

    """
    Makes moves for the player
    """
    def action(self, turns):

        #Placing Phase
        if self.board.count < 24:
            if self.i < 6:
                self.i += 2
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
        #Moving Phase
        else:
            #Checks if board needs to be shrunk
            if turns == self.shorten1:
                self.decrease_board()
            #Checks if no moves are availabe. Turn must be forfeit
            if not self.check_moves():
                return None
            self.board.count += 1
            #Get best possible move for player and make the move
            move = self.minimax.alphabeta_search()
            return move

    """
    Updates our game state with the enemies action
    """
    def update(self, action):

        self.board.count += 1
        #Placing phase action
        if self.board.count < 25:
            piece = Piece(self.enemy, action, self.board)
            self.enemy_list.append(piece)
            piece.makemove(action)

        #Moving phase action
        else:
            if self.board.count - 24 == self.shorten2:
                self.decrease_board()
            piece = self.board.find_piece(action[0])
            self.minimax.makemove(action[1], self.board, self.enemy, piece)

    """
    Shrinks the game state board by the rules of the game
    """
    def decrease_board(self):
        buf = self.shortened
        #Identifies the corners of the shrunk board
        corners = [(buf+1, buf+1), (buf+1, 6-buf), (6-buf, buf+1), (6-buf, 6-buf)]

        #Checks the board for disqualified pieces 4 squares at a time
        for i in range(buf, 7 - buf):
            for square in [(i, buf), (buf, i), (i, 7-buf), (7-buf, i)]:
                piece = self.board.find_piece(square)
                if piece:
                    piece.alive = False
                self.board.grid[square] = ' '
        self.shortened += 1

        #Reassigns the corners of the new shrunk board
        for square in corners:
            self.board.grid[square] = "X"
            piece = self.board.find_piece(square)
            #Kills piece if located on the edge
            if piece:
                piece.alive = False
        if self.shorten1 < 190:
            self.shorten1 += 64
            self.shorten2 += 64

    """
    Returns a list of total available moves to the player    
    """
    def check_moves(self):
        list = []
        for piece in self.piece_list:
            list.append(piece.moves())
        if len(list) == 0:
            return False
        return True
