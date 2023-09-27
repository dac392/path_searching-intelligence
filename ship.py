from generate_matrix import generate_matrix
from generate_matrix import generate_random_coordinate
from generate_matrix import display_image

class ship_t():
	"""docstring for Ship_t"""
	def __init__(self, size):
		# super(ship_t, self).__init__()
		self.size = size
		self.game_board = generate_matrix(size)
		# self.active_board = [row[:] for row in game_board]
		self.bot = generate_random_coordinate(size)
		self.button = generate_random_coordinate(size)
		# prob generate a matrix for probabilities

	def display_game_board(self):
		self.game_board[self.bot] = 2
		self.game_board[self.button] = 3
		print(self.game_board)
		display_image(self.game_board)


		