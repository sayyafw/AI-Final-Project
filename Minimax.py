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
        else:
            self.piece_list = self.game.black_pieces


    def alphabeta_search(self):
        value, best_move, best_piece = self.min_max_max(None, self.game, self.depth, self.piece_list[0])
        return_pos = best_piece.pos
        print(best_piece.pos)
        best_piece.makemove(best_move)
        return (return_pos, best_move)



    def min_max_min(self, state, game, depth, oldpiece):

        if self.cut_off(depth):
            return self.eval(game, self.colour), state, oldpiece

        beta = 100000

        for piece in self.piece_list:
            oldpos = piece.pos
            for move in piece.moves():
                elim_pieces = piece.makemove(move)
                value = self.min_max_max(move, game, depth+1, piece)
                piece.undomove(oldpos, elim_pieces)

                if value < beta:
                    beta = value
                    best_move = move
                    best_piece = piece

        return beta, best_move, best_piece

    def min_max_max(self, state, game, depth, oldpiece):

        if self.cut_off(depth):
            return self.eval(game, self.colour), state, oldpiece

        alpha = -100000
        for piece in self.piece_list:
            oldpos = piece.pos
            for move in piece.moves():
                elim_pieces = piece.makemove(move)
                value, we, hello = self.min_max_max(move, game, depth+1, piece)
                piece.undomove(oldpos, elim_pieces)

                if value > alpha:
                    alpha = value
                    best_move = move
                    best_piece = piece

        return alpha, best_move, best_piece

    def cut_off(self, depth):
        if depth > 2:
            return True
        return False

    def eval(self, game, colour):
        return 0.3*self.distance_from_center(game, colour) + 0.7*self.pieces_left(game, colour)

    def eval_placeing(self, game, colour):
        return 10*self.pieces_lefts(game, colour) + 2*self.distance_from_center


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
                    self.eliminate_piece(ENEMIES[colour], adjacent_square, board)
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
                    self.eliminate_piece(colour, pos, board)
                    break

    def step(self, position, direction):
        """
        Take an (x, y) tuple `position` and a `direction` (UP, DOWN, LEFT or RIGHT)
        and combine to produce a new tuple representing a position one 'step' in
        that direction from the original position.
        """
        px, py = position
        dx, dy = direction
        return (px + dx, py + dy)

    def eliminate_surround(colour, pos):
        """
        check the surrounding of a piece, and remove enemies
        """
        e_pieces = []
        for direction in DIRECTIONS:
            adjacent_square = self.step(pos, direction)
            opposite_square = self.step(adjacent_square, direction)
            if opposite_square in board.grid:
                if board.grid[adjacent_square] in ENEMIES[colour] \
                        and board.grid[opposite_square] in FRIENDS[colour]:
                    eliminated_piece = board.find_piece(adjacent_square)
                    self.eliminate_piece(ENEMIES[colour], adjacent_square, board)
                    e_pieces.append(eliminated_piece)
        return e_pieces

    @staticmethod
    def eliminate_piece(colour, position, game):
        if colour == WHITE:
            for item in  game.white_pieces:
                if item == position:
                    game.white_pieces.remove(item)
            game.grid[position] = BLANK

        else:
            for item in  game.black_pieces:
                if item.pos == position:
                    game.black_pieces.remove(item)
            game.grid[position] = BLANK

    def distance_from_center(self, game, colour):

        if colour == WHITE:
            piece_list = game.white_pieces
        else:
            piece_list = game.black_pieces

        distance = 0
        for piece in piece_list:
            distance = fabs(piece.pos[0] - 4 + piece.pos[1] - 4)
        return distance

    def pieces_left(self, game, colour):
        if colour == WHITE:
            return len(game.white_pieces)
        else:
            return len(game.black_pieces)
        







































"""

    def min_max_min(self, game, alpha, beta, depth):

        if self.colour == WHITE:
            piece_list = game.white_pieces
        else:
            piece_list = game.black_pieces

        for piece in piece_list:
            oldpos = piece.pos
            for move in piece.moves():
                piece.makemove(move)
                value = self.max_value(game, alpha, beta, depth+1, piece)
                piece.undomove(oldpos)

            if value < beta:
                beta = value
                best_move = move
                best_piece = piece

            if beta < alpha:
                break
        return beta, best_move, best_piece

    def min_max_max(self, game, alpha, beta, depth):

        if self.colour == WHITE:
            piece_list = game.white_pieces
        else:
            piece_list = game.black_pieces

        for piece in piece_list:
            oldpos = piece.pos
            for move in piece.moves():
                piece.makemove(move)
                value = self.min_max_min(game, alpha, beta, depth+1, piece)
                piece.undomove(oldpos)

                if value > alpha:
                    alpha = value
                    best_move = move
                    best_piece = piece

                if alpha > beta:
                    break

        return alpha, best_move, best_piece

    def min_value(self, move, game, alpha, beta, depth, piece):

        if self.cut_off(depth):
            return self.eval(game, self.colour)
        beta = self.min_max_min(board, alpha, beta, depth+1)

        if beta < alpha:
            return alpha

        return beta, best_move

    def max_value(self, game, alpha, beta, depth, piece):
        if self.cut_off(depth):
            return self.eval(game, self.colour)

            board = copy.deepcopy(game)
            piece.makemove(move, board, self.enemy)
            value = self.min_max_in (game, alpha, beta, depth + 1)

            if value > alpha:
                return alpha, move, piece

            else:
                beta = value
                best_move = move
        return alpha, best_move
        
        """

