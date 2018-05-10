from Board import Board
import Minimax
from Board import Piece
import Placing

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
        self.placing = Placing.Placing(self.colour, self.board)
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
            self.board.count += 1
            print("not in place" + str(self.board.white_pieces) + "||||||||||||" + str(self.board.black_pieces))
            v = self.placing.placeing_phase()
            self.board.grid[v[0], v[1]] = self.symbol
            piece = Piece(self.symbol, v, self.board)
            self.piece_list.append(piece)
            eliminated_piece = piece.makemove(v)
            if len(eliminated_piece):
                print(str(eliminated_piece))
                for item in eliminated_piece:
                    self.minimax.delete_piece(item.pos[0],item.pos[1])
            #print("aaaaaa" + str(self.piece_list) + "||||||||||||" + str(self.enemy_list))
            return v
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


            self.board.grid[action[0], action[1]] = self.enemy
            piece = Piece(self.enemy, action, self.board)
            self.enemy_list.append(piece)
            eliminated_piece = piece.makemove(action)
            if len(eliminated_piece):
                for item in eliminated_piece:
                    self.minimax.delete_piece(item.pos[0],item.pos[1])


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
