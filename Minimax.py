from math import inf, fabs
import copy


WHITE, BLACK, CORNER, BLANK, REMOVED = ['O', '@', 'X', '-', ' ']
ENEMIES = {WHITE: {BLACK, CORNER}, BLACK: {WHITE, CORNER}}
FRIENDS = {WHITE: {WHITE, CORNER}, BLACK: {BLACK, CORNER}}

DIRECTIONS = UP, DOWN, LEFT, RIGHT = (0, -1), (0, 1), (-1, 0), (1, 0)


class alphabeta_search:

    def __init__(self, colour, enemy, game):
        self.depth = 0
        self.colour = colour
        self.enemy = enemy
        self.game = game
        if self.colour == WHITE:
            self.piece_list = self.game.white_pieces
            self.enemy_list = self.game.black_pieces
        else:
            self.piece_list = self.game.black_pieces
            self.enemy_list = self.game.white_pieces


    def alphabeta_search(self):
        value, best_move, best_piece = self.min_max_max(self.game, self.depth, self.piece_list[0], None)
        return_pos = best_piece.pos
        print(best_piece.pos, best_move)
        if (self.colour == WHITE):
            print("hello")
        best_piece.makemove(best_move)
        return (return_pos, best_move)



    def min_max_min(self, game, depth, oldpiece, oldmove):

        if self.cut_off(depth):
            return self.eval(self.colour), oldmove, oldpiece

        beta = 10000

        best_move = None
        best_piece = None
        for piece in self.piece_list:
            if not piece.alive:
                continue
            oldpos = piece.pos
            for move in piece.moves():
                elim_pieces = piece.makemove(move)
                value, we, fun = self.min_max_max(game, depth+1, piece, move)
                piece.undomove(oldpos, elim_pieces)

                if value < beta:
                    beta = value
                    best_move = move
                    best_piece = piece
                else:
                    break
        return beta, best_move, best_piece

    def min_max_max(self, game, depth, oldpiece, oldmove):


        alpha = -10000

        if self.cut_off(depth):
            return self.eval(self.colour), oldmove, oldpiece
        best_move = None
        best_piece = None
        for piece in self.piece_list:
            if not piece.alive:
                continue
            oldpos = piece.pos
            for move in piece.moves():
                elim_pieces = piece.makemove(move)
                value, we, hello = self.min_max_min(game, depth+1, piece, move)
                piece.undomove(oldpos, elim_pieces)

                if value > alpha:
                    alpha = value
                    best_move = move
                    best_piece = piece
                else:
                    break

        return alpha, best_move, best_piece

    def cut_off(self, depth):
        if depth > 3:
            return True
        return False

    def eval(self, colour):
        if colour == self.colour:
            sign = 1
        else:
            sign = -1
        return sign * self.distance_from_center() + self.pieces_left() - 2*self.enemy_pieces_left() + self.piece_distance()

    def makemove(self, coords, board, colour, piece):
        """
        Carry out a move from this piece's current position to the position
        `newpos` (a position from the list returned from the `moves()` method)
        Update the board including eliminating any nearby pieces surrounded as
        a result of this move.

        Return a list of pieces eliminated by this move (to be passed back to
        the `undomove()` method if you want to reverse this move).

        Do not call with method on pieces with `alive = False`.
        """
        # make the move
        oldpos = piece.pos
        pos = coords
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

    def step(self, position, direction):
        """
        Take an (x, y) tuple `position` and a `direction` (UP, DOWN, LEFT or RIGHT)
        and combine to produce a new tuple representing a position one 'step' in
        that direction from the original position.
        """
        px, py = position
        dx, dy = direction
        return (px + dx, py + dy)

    def eliminate_piece(self, piece):

        piece.alive = False
        self.game.grid[piece.pos] = BLANK

    def distance_from_center(self):

        distance = 0
        for piece in self.piece_list:
            distance = fabs(piece.pos[0] - 4 + piece.pos[1] - 4)
        return distance

    def pieces_left(self):
        count = 0
        for piece in self.piece_list:
            if piece.alive:
                count += 1
        return count

    def enemy_pieces_left(self):
        count = 0
        for piece in self.enemy_list:
            if piece.alive:
                count += 1
        return count

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

        return score
