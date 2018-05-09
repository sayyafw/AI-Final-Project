from math import fabs, pow

WHITE, BLACK, CORNER, BLANK, REMOVED = ['O', '@', 'X', '-', ' ']
ENEMIES = {WHITE: {BLACK, CORNER}, BLACK: {WHITE, CORNER}}
FRIENDS = {WHITE: {WHITE, CORNER}, BLACK: {BLACK, CORNER}}

DIRECTIONS = UP, DOWN, LEFT, RIGHT = (0, -1), (0, 1), (-1, 0), (1, 0)


"""
Class to Perform MiniMax Search. 
"""

class alphabeta_search:

    """
    Initialises the search class, using the player colour
    enemy and board (game = board)
    """
    def __init__(self, colour, enemy, game):
        self.depth = 0
        self.colour = colour
        self.enemy = enemy
        self.game = game
        if self.colour == WHITE:
            self.piece_list = self.game.white_pieces #Creates a list of pieces belonging to the player
            self.enemy_list = self.game.black_pieces#Creates a list of enemy pieces
        else:
            self.piece_list = self.game.black_pieces
            self.enemy_list = self.game.white_pieces


    """ 
    Performs the actual minimax search, returning the pieces initial position and best move
    """
    def alphabeta_search(self):
        value, best_move, best_piece = self.min_max_max(self.game, self.depth)
        return_pos = best_piece.pos
        best_piece.makemove(best_move) #Perform move for personal record
        return (return_pos, best_move)


    """
    Return the best possible move for the enemy, without exceeding max depth
    """
    def min_max_min(self, game, depth):
        beta = 1000000
        best_move = None
        best_piece = None

        #Checks if max depth or terminal state reached
        if self.cut_off(depth):
            return self.eval(self.colour), best_move, best_piece

        #Checks every move for every alive piece
        for piece in self.piece_list:
            if not piece.alive:
                continue
            # Stores the position of the piece before the move
            oldpos = piece.pos
            for move in piece.moves():
                elim_pieces = piece.makemove(move)
                #Receive the value of the best possible move for the player
                value = self.min_max_max(game, depth+1)
                #Undo move on the same board. Allows board reuse without copying
                piece.undomove(oldpos, elim_pieces)

                #Checks if this is the best possible move
                if value[0] < beta:
                    beta = value[0]
                    best_move = move
                    best_piece = piece
                else:
                    break
        return beta, best_move, best_piece

    """
    Return the best possible move for the enemy, without exceeding max depth
    """
    def min_max_max(self, game, depth):

        alpha = -1000000
        best_move = None
        best_piece = None
        # Checks if max depth or terminal state reached
        if self.cut_off(depth):
            return self.eval(self.colour), best_move, best_piece

        # Checks every move for every alive piece
        for piece in self.piece_list:
            if not piece.alive:
                continue
            oldpos = piece.pos
            for move in piece.moves():
                elim_pieces = piece.makemove(move)
                value = self.min_max_min(game, depth+1)
                piece.undomove(oldpos, elim_pieces)

                #Checks if best possible move
                if value[0] > alpha:
                    alpha = value[0]
                    best_move = move
                    best_piece = piece
                else:
                    break
        return alpha, best_move, best_piece

    """
    Checks if max allowable depth reached
    """
    def cut_off(self, depth):
        if depth > 2:
            return True
        return False

    """
    Using different heuristic functions, attempts to place a value on a game state that is incomplete
    """
    def eval(self, colour):
        if colour == self.colour:
            sign = 1
        else:
            sign = -1
        return sign * (self.pieces_left() - 5*self.enemy_pieces_left()**2 + self.piece_distance())

    def eval_placeing(self, colour):
        """
        calculate the difference between number of living pieces,
        reward slightly for being away from the center
        """
        dist = self.distance_from_center()
        return 5*(self.pieces_left() - self.enemy_pieces_left()) + 2*dist


    def makemove(self, newpos, board, colour, piece):
        """
        Carry out a move from a given pieces position to the position
        `newpos` (a position from the list returned from the `moves()` method)
        Update the board including eliminating any nearby pieces surrounded as
        a result of this move.

        Return a list of pieces eliminated by this move (to be passed back to
        the `undomove()` method if you want to reverse this move).

        Do not call with method on pieces with `alive = False`.
        """
        # make the move
        oldpos = piece.pos
        pos = newpos
        piece.oldpos = piece.pos
        piece.pos = pos
        board.grid[oldpos] = BLANK
        board.grid[pos] = colour

        # eliminate any newly surrounded pieces
        eliminated_pieces = []

        # check adjacent squares: did this move elimminate anyone?
        for direction in DIRECTIONS:
            adjacent_square = self.step(pos, direction)
            opposite_square = self.step(adjacent_square, direction)
            if opposite_square in board.grid:
                if board.grid[adjacent_square] in ENEMIES[colour] \
                        and board.grid[opposite_square] in FRIENDS[colour]:
                    eliminated_piece = board.find_piece(adjacent_square)
                    self.eliminate_piece(eliminated_piece)
                    eliminated_pieces.append(eliminated_piece)

        # check horizontally and vertically: does the piece itself get
        # eliminated?
        for forward, backward in [(UP, DOWN), (LEFT, RIGHT)]:
            front_square = self.step(pos, forward)
            back_square = self.step(pos, backward)
            if front_square in board.grid \
                    and back_square in board.grid:
                if board.grid[front_square] in ENEMIES[colour] \
                        and board.grid[back_square] in ENEMIES[colour]:
                    self.eliminate_piece(piece)
                    break
        return eliminated_pieces

    def check_surround(self, pos,colour):
        # eliminate any newly surrounded pieces
        eliminated_pieces = []

        if colour == "white":
            symbol = "W"
            enemy = "B"
        else:
            symbol = "B"
            enemy = "W"

        # check adjacent squares: did this move elimminate anyone?
        for direction in DIRECTIONS:
            adjacent_square = self.step(pos, direction)
            opposite_square = self.step(adjacent_square, direction)
            if opposite_square in board.grid:
                if board.grid[adjacent_square] in ENEMIES[colour] \
                        and board.grid[opposite_square] in FRIENDS[colour]:
                    eliminated_piece = board.find_piece(adjacent_square)
                    self.eliminate_piece(eliminated_piece)
                    eliminated_pieces.append(("Eliminated", enemy, adjacent_square))

        # check horizontally and vertically: does the piece itself get
        # eliminated?
        for forward, backward in [(UP, DOWN), (LEFT, RIGHT)]:
            front_square = self.step(pos, forward)
            back_square = self.step(pos, backward)
            if front_square in board.grid \
                    and back_square in board.grid:
                if board.grid[front_square] in ENEMIES[colour] \
                        and board.grid[back_square] in ENEMIES[colour]:
                    self.eliminate_piece(piece)
                    eliminated_pieces.append(("Eliminated", symbol, pos))
                    break
        return eliminated_pieces

    def step(self, position, direction):
        """
        Take an (x, y) tuple `position` and a `direction` (UP, DOWN, LEFT or RIGHT)
        and combine to produce a new tuple representing a position one 'step' in
        that direction from the original position.
        """
        px, py = position
        dx, dy = direction
        return (px + dx, py + dy)

    """
    Eliminates a given piece by setting piece.alive to False
    """
    def eliminate_piece(self, piece):

        piece.alive = False
        self.game.grid[piece.pos] = BLANK


    def delete_piece(self, x, y):
        for piece in self.piece_list:
            if (piece.pos == (x,y)):
                self.piece_list.remove(piece)
                break


    """
    Evaluates the distance from center of the entire set
    """
    def distance_from_center(self):

        distance = 0
        for piece in self.piece_list:
            distance += (piece.pos[0] - 3.5)**2 + (piece.pos[1] - 3.5)**2
        return distance

    """
    Checks number of pieces left for player
    """
    def pieces_left(self):
        count = 0
        for piece in self.piece_list:
            if piece.alive:
                count += 1
        return count

    """
    Checks number of pieces left for player
    """
    def enemy_pieces_left(self):
        count = 0
        for piece in self.enemy_list:
            if piece.alive:
                count += 1
        return count

    """
    Calculates average distance between each piece in a list. Attemps to keep pieces close together
    in defensive formation
    """
    def piece_distance(self):
        distance = 0
        for piece1 in self.piece_list:
            for piece2 in self.piece_list:
                if piece1 == piece2:
                    continue
                dx = abs(piece1.pos[0] - piece2.pos[0])
                dy = abs(piece1.pos[1] - piece2.pos[1])
                distance += dx ** 2 + dy ** 2
        distance /= len(self.piece_list)
        score = 1.0 / distance
        return distance

    
