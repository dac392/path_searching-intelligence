from generate_matrix import generate_matrix
from generate_matrix import generate_random_coordinate
from generate_matrix import display_image
from generate_matrix import get_flamability_matrix
from generate_matrix import get_random

CLOSED = 0
OPEN = 1
BOT = 2
GOAL = 3
FIRE = 4
PATH = 5
BURNING = 6
OG_IS_GOAL = 7
BURNED_PATH = 8
KILLED = 9
INITIAL_FIRE = 10


class ship_t():
	"""docstring for Ship_t"""
	def __init__(self, size, flamability):
		self.size = size
		self.flamability = flamability
		self.game_board = generate_matrix(size)
		# self.active_board = [row[:] for row in game_board]
		self.original_position = generate_random_coordinate(size)
		self.bot = self.original_position
		self.goal = generate_random_coordinate(size)
		self.initial_fire = generate_random_coordinate(size)

		# probability matrix
		self.burning_nodes = set()

		#update the matrix to have the goal and bot positions
		self.game_board[self.original_position] = BOT
		self.game_board[self.goal] = GOAL
		self.game_board[self.initial_fire] = FIRE

		# add initial fire to the fire set
		self.burning_nodes.add(self.initial_fire)



	def apply_scorch(self):

		might_scorch = {}
		# go through the list of burning nodes and get their neighbors
		for node in self.burning_nodes:
			flamable_neighbors = self.get_neighbors(node, FIRE)
			for position in flamable_neighbors:
				if position not in might_scorch:
					might_scorch[position] = self.probability_of_scorching(position)

		for flamable_cell, probability in might_scorch.items():
			if get_random() <= probability:
				self.game_board[flamable_cell] = FIRE
				self.burning_nodes.add(flamable_cell)

	def probability_of_scorching(self, position):
		q = self.flamability
		burning_neighbors = self.get_neighbors(position, BURNING) #get fire neighbors
		k = len(burning_neighbors)
		return 1 - (1-q)**k

	def has_burned_down(self):
		if self.bot in self.burning_nodes or self.goal in self.burning_nodes:
			return True

		return False

	def can_move(self, position):
		if self.game_board[position] == OPEN:
			return True
		return False

	def move_to(self, position):
		self.bot = position

	def is_safe(self):
		return self.bot == self.goal



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
				return self.build_path(parent, curr)
			neighbors = self.get_neighbors(curr, BOT)
			for neighbor in neighbors:
				temp_distance = distance[curr]+1
				if neighbor not in distance or temp_distance < distance[neighbor]:
					distance[neighbor] = temp_distance
					fringe.append(neighbor)
					parent[neighbor] = curr

		return None

	def set_path(self, path):

		if self.game_board[self.initial_fire] != INITIAL_FIRE:
			self.game_board[self.initial_fire] = INITIAL_FIRE
		if self.game_board[self.original_position] != BOT:
			self.game_board[self.original_position] = BURNING
		if self.game_board[self.goal] != GOAL:
			self.game_board[self.goal] = BURNING
		if self.original_position == self.goal:
			self.game_board[self.goal] = OG_IS_GOAL
		if self.bot in self.burning_nodes:
			self.game_board[self.bot] = KILLED



		for pos in path:
			if pos != self.bot and pos != self.goal: 
				if pos not in self.burning_nodes:
					self.game_board[pos] = PATH
				else:
					self.game_board[pos] = BURNED_PATH

	def build_path(self, parent, position):
		fringe = []
		fringe.append(position)
		while True:
			curr = parent[fringe[-1]]
			if curr == None:
				return fringe[::-1]

			fringe.append(curr)



	def get_neighbors(self, position, mode):
		directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
		neighbors = [(position[0] + d[0], position[1] + d[1]) for d in directions]
		interior_neighbors = [(x, y) for x, y in neighbors if 0 < x < self.size - 1 and 0 < y < self.size - 1]
		valid_neighbors = None

		if mode == BOT:
			valid_neighbors = [ (x,y) for x,y in interior_neighbors if self.game_board[x][y] in [OPEN,GOAL] ]
		elif mode == BURNING:
			valid_neighbors = [ (x,y) for x,y in interior_neighbors if self.game_board[x][y] in [FIRE] ]
		else: # FIRE
			valid_neighbors = [ (x,y) for x,y in interior_neighbors if self.game_board[x][y] in [OPEN, GOAL, BOT, PATH] ]

		return valid_neighbors

	def display_game_board(self):
		with open("gameboard_info.txt", "r") as file:
			content = file.read()
			print(content)

		display_image(self.game_board)


		