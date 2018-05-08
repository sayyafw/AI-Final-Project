from Board import Board
import Minimax
from Board import Piece
import Player
class Placing:
	
	def __init__(self, colour):
		"""
		initialize the colour of the player and the board.
		"""
		self.colour = colour
		self.board = Board()
		self.actions = []
		self.turn = self.board.count
		if colour == 'white':
           self.symbol = 'O'
           self.enemy = '@'
        else:
           self.symbol = '@'
           self.enemy = 'O'

	def minimax(self, x, y):
		
		depth = 0;
		a = 1000
		b = -1000
		min(Board, depth, a, b, turn)
		return

	def min(self, state, depth, a, b, turn):
		turn+=1
		depth+=1
		if (depth == 4 or turn >=24):
			return 

	def max(self, state, depth, a, b, turn):
		turn+=1
		depth+=1
		if (depth == 4 or turn >=24):
			return
		
	def white_place(self, Board, depth, a, b, turn):
		ystart = 0
		yend = 5
		for x in range(7):
			for y in range(ystart, yend):
				if board.isEmpty(x,y):
					print("is epmpty!")

					black_place(Board)
		return

	def black_place(self, Board, depth, a, b, turn):
		ystart = 2
		yend = 7
		for x in range(7):
			for y in range(ystart, yend):
				if board.isEmpty(x,y):
					print("is epmpty!")
					white_place(Board)
		return

	def place(self, Board, pos):
	"""
	simulate placing a piece on the board
	"""
		actions.append(("Place", pos))
		Player.place(pos, Board)
		eliminated = eliminate_surround(pos)
		if eliminated != []:
			actions.append(("Eliminated", eliminated))
		return


