from generate_matrix import generate_matrix
from generate_matrix import generate_random_coordinate
from generate_matrix import display_image

CLOSED = 0
OPEN = 1
BOT = 2
GOAL = 3
FIRE = 4
PATH = 5

class ship_t():
	"""docstring for Ship_t"""
	def __init__(self, size):
		self.size = size
		self.game_board = generate_matrix(size)
		# self.active_board = [row[:] for row in game_board]
		self.bot = generate_random_coordinate(size)
		self.goal = generate_random_coordinate(size)
		self.initial_fire = generate_random_coordinate(size)

		#update the matrix to have the goal and bot positions
		self.game_board[self.bot] = BOT
		self.game_board[self.goal] = GOAL
		self.game_board[self.initial_fire] = FIRE

		# prob generate a matrix for probabilities

	def calculate_shortest_path(self):
		fringe = []
		fringe.append(self.bot)
		distance = {}
		distance[self.bot] = 0
		parent = {}
		parent[self.bot] = None

		while fringe:
			curr = fringe.pop(0)
			if curr == self.goal:
				print(f"goal: {self.goal} and curr: {curr}")
				return self.build_path(parent, curr)
			neighbors = self.get_neighbors(curr)
			for neighbor in neighbors:
				temp_distance = distance[curr]+1
				if neighbor not in distance or temp_distance < distance[neighbor]:
					distance[neighbor] = temp_distance
					fringe.append(neighbor)
					parent[neighbor] = curr

		return None

	def set_path(self, path):
		for pos in path:
			if pos != self.bot and pos != self.goal:
				self.game_board[pos] = PATH

	def build_path(self, parent, position):
		fringe = []
		fringe.append(position)
		while True:
			curr = parent[fringe[-1]]
			if curr == None:
				return fringe[::-1]

			fringe.append(curr)




	def get_neighbors(self, position):
		directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
		neighbors = [(position[0] + d[0], position[1] + d[1]) for d in directions]
		interior_neighbors = [(x, y) for x, y in neighbors if 0 < x < self.size - 1 and 0 < y < self.size - 1]
		valid_neighbors = [ (x,y) for x,y in interior_neighbors if self.game_board[x][y] in [1,3] ]
		return valid_neighbors

	def display_game_board(self):
		display_image(self.game_board)


		