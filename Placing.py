from Board import Board
import Minimax
from Board import Piece

class Placing:
    def __init__(self, colour):
        self.colour = colour
        self.board = Board()
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

    def place(self, i , j, symbol):
        """
        place a piece on the board
        """
        piece = Piece(symbol, (i, j), self.board)
        self.piece_list.append(piece)
        #get the pieces that would be eliminated if you place here
        
        eliminated_piece = piece.makemove((i, j))
        if len(eliminated_piece):
            for item in eliminated_piece:
                if item.player == "@":
                    
                    self.history.append(("Eliminated","B" ,item.pos))
                else:
                    
                    self.history.append(("Eliminated","W" ,item.pos))

    def placeing_phase(self):
        """
        begin a simulation for placing phase, record the best step yet
        """
        turn = self.board.count
        a = -1000
        b = 1000
        depth = 0

        #run it through the minimax function, starts at max
        self.max(turn, 0, a, b)
        self.place(self.best[0], self.best[1], self.symbol)
        print(str(self.symbol) + str(self.best))
        return (self.best)

    def max(self, turn, depth, a, b):
        #check end condition
        if (depth >= 3):
            return self.minimax.eval_placeing(self.colour)
        #check for colour, assign variable
        colour = self.colour
        if colour == "white":
            ystart = 0
            yend = 6
            col = "W"
            symbol = "O"
        else:
            ystart = 2
            yend = 8
            col = "B"
            symbol = "@"

        value = -10000
        #for each child node
        for y in range(ystart, yend):
            for x in range(8):
                #if the board position is available, try it out
                if self.board.isEmpty(x,y):
                    #place a piece on the board
                    self.history.append(("Placing", col, (x,y)))
                    self.place(x, y, symbol)
                    #go deeper
                    new_value = self.min(turn+1, depth+1, a, b)
                    self.undo_history()
                    #check if better score
                    if new_value > value:
                        value = new_value
                        #if this is the top node, update move
                        if self.one_placing():
                            self.best=self.history[0][2]


                    #prune here
                    if new_value >= b:
                        #self.undo_history()
                        return value

                    #update alpha
                    if new_value > a:
                        a = new_value
            


        #go back up the tree
        #self.undo_history()
        return value

    def min(self, turn, depth, a, b):

        value = 10000

        if (depth >= 3):
            return self.minimax.eval_placeing(self.colour)
        colour = self.colour
        if colour == "white":
            ystart = 2
            yend = 8
            col = "B"
            symbol = "@"
        else:
            ystart = 0
            yend = 6
            col = "W"
            symbol = "O"

        for y in range(ystart, yend):
            for x in range(8):
                #if the board position is available, try it out
                if self.board.isEmpty(x,y):
                    
                    self.history.append(("Placing", col, (x,y)))
                    #print("append in min " + str(self.history))
                    self.place(x, y, symbol)

                    new_value = self.max(turn+1, depth+1, a, b)
                    self.undo_history()
                    #check if better score
                    if new_value < value:
                        value = new_value

                    #prune here
                    if new_value <= a:
                        #self.undo_history()
                        return value

                    #update beta
                    if new_value < b:
                        b = new_value   
        self.undo_history()
        return value

    def undo_history(self):
        """
        undo a record of steps
        """
        #if the record isn't empty
        if (len(self.history) > 0):
            #if it was a piece was placed
            if self.history[-1][0] == "Placing":
                cord = self.history[-1][2] 
                self.minimax.delete_piece(cord[0], cord[1])
                self.board.grid[cord[0], cord[1]] = '-' 
                del self.history[-1]
                return
            #if a piece was eliminated, put it back
            elif self.history[-1][0] == "Eliminated":
                if self.history[-1][1] == "B":
                    ###############place black at history [-1][2]
                    del self.history[-1]
                    self.undo_history()
                    return True
                else:
                    ###############place white
                    del self.history[-1]
                    self.undo_history()
                    return
            else:
                return
        else:
            return

    def one_placing(self):
    #check if theres only one placing record in the record
        count = 0
        for item in self.history:
            if item[0] == "Placing":
                count += 1
        return (count==1 or count==2)