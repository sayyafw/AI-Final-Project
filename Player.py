from Board import Board
import Minimax
from Board import Piece


class Player:
    def __init__(self, colour):
        self.colour = colour
        self.board = Board()
        self.i = 0
        self.j = 0
        self.history = []
        self.best = ()
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
            return placeing_phase
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
#############################################################

    def place(self, i , j, symbol):
        """
        place a piece on the board
        """
        piece = Piece(self.symbol, (self.i, self.j), self.board)
        self.piece_list.append(piece)
        #get the pieces that would be eliminated if you place here
        eliminated_piece = piece.makemove((self.i, self.j))
        history.append(eliminated_piece)


    def placeing_phase(self):
        """
        begin a simulation for placing phase, record the best step yet
        """
        turn = self.board.count
        a = -1000
        b = 1000
        depth = 0

        #run it through the minimax function, starts at max
        max(0, turn, a, b)
        
        return best

    def max(self, turn, depth, a, b):
        #check end condition
        if (depth == 2 or turn >=24):
            return self.minimax.eval_placeing(self.board, colour)

        #check for colour, assign variable
        colour = self.colour
        if colour == white:
            ystart = 0
            yend = 5
            col = "W"
        else:
            ystart = 2
            yend = 7
            col = "B"

        value = -10000
        #for each child node
        for x in range(7):
            for y in range(ystart, yend):
                #if the board position is available, try it out
                if not self.board.isEmpty(x,y):
                    #place a piece on the board
                    history.append(("Placing", col, (x,y)))
                    place(x, y, 'O')
                    turn += 1
                    depth += 1
                    #go deeper
                    new_value = min(turn, depth, a, b)

                    #check if better score
                    if new_value > value:
                        value = new_value
                        #if this is the top node, update move
                        if one_placing():
                            self.best=history[0][3]

                    #prune here
                    if new_value >= b:
                        undo_history()
                        turn -=1
                        depth -= 1
                        return value

                    #update alpha
                    if new_value > a:
                        a = new_value

        #go back up the tree
        undo_history()
        turn -=1
        depth -= 1
        return value

    def min(self, turn, depth, a, b):
        turn += 1
        depth += 1
        value = 10000

        if (depth == 2 or turn >=24):
            return self.minimax.eval_placeing(self.board, colour)

        colour = self.colour
        if colour == white:
            ystart = 2
            yend = 7
            col = "B"
        else:
            ystart = 0
            yend = 5
            col = "W"

        for x in range(7):
            for y in range(ystart, yend):
                #if the board position is available, try it out
                if not self.board.isEmpty(x,y):

                    history.append(("Placing", col, (x,y)))
                    place(x, y, 'O')
                    turn += 1
                    depth += 1
                    new_value = max(turn, depth, a, b)

                    #check if better score
                    if new_value < value:
                        value = new_value

                    #prune here
                    if new_value <= a:
                        undo_history()
                        turn -=1
                        depth -= 1
                        return value

                    #update beta
                    if new_value < b:
                        b = new_value

        undo_history()
        turn -=1
        depth -= 1
        return value

    def undo_history(self):
    """
    undo the lastest step performed
    """
        #if there are histories
        if len(history) > 0:
            #if it was a piece was placed
            if history[-1][0] == "Placing":
                self.minimax.delete_piece((self.board(history[-1][2])))
                del history[-1]
                return True
            #if a piece was eliminated, put it back
            else if history[-1][0] == "Eliminated":
                if history[-1][1] == "B":
                    ###############place black at history [-1][2]
                    del history[-1]
                    undo_history()
                    return True
                else:
                    ###############place white
                    del history[-1]
                    undo_history()
                    return True
            else:
                return False
        else:
            return False

    def one_placing(self):
    #check if theres only one placing record in the record
        count = 0
        for item in history:
            if item[0] == "Placing":
                count += 1

        return (count==1)