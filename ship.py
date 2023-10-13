from generate_matrix import generate_matrix
from generate_matrix import generate_random_coordinate
from generate_matrix import display_image
from generate_matrix import get_flamability_matrix
from generate_matrix import get_random

from algorithms import a_star
from algorithms import great_value_monte_carlo
from ship_3D import ship_3D

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

PADDING = True
BOT3 = 35


class ship_t():
	"""docstring for Ship_t"""
	def __init__(self, size, flamability):
		self.size = size
		self.flamability = flamability
		self.game_board = generate_matrix(size)
		self.original_position = generate_random_coordinate(size)
		self.bot = self.original_position
		self.goal = generate_random_coordinate(size)
		self.initial_fire = generate_random_coordinate(size)

		# fire sets
		self.burning_nodes = set()
		self.radiance = set()

		#update the matrix to have the goal and bot positions
		self.game_board[self.original_position] = BOT
		self.game_board[self.goal] = GOAL
		self.game_board[self.initial_fire] = FIRE

		# add initial fire to the fire set
		self.burning_nodes.add(self.initial_fire)
		self.simulation = None


	def heuristic_2(self):
		path = self.get_shortest_path(self.bot, self.goal)
		if path is None:
			# print("I couldn't find a path and I'm freaking out")
			return []

		return path

	def heuristic_3(self):
		self.update_radiance()
		path = self.get_shortest_path( self.bot, self.goal, PADDING , self.radiance)
		if path is None:
			return self.heuristic_2()
		return path

	def heuristic_4(self):
		sim_ship = ship_3D(self, 3)
		self.simulation = sim_ship.run_simulation(15)
		path = self.get_simulated_path()
		if path is None:
			return []
		return path





# < SCORCH AND FIRE METHODS >

	# takes care of applying burn mechanic onto the board
	def apply_scorch(self):

		might_scorch = {}
		for node in self.burning_nodes:
			flamable_neighbors = self.get_neighbors(node, [OPEN, GOAL, BOT, PATH])
			for position in flamable_neighbors:
				if position not in might_scorch:
					might_scorch[position] = self.probability_of_scorching(position)

		for flamable_cell, probability in might_scorch.items():
			if get_random() <= probability:
				self.game_board[flamable_cell] = FIRE
				self.burning_nodes.add(flamable_cell)

	# calculated the probability of a position on the board burning
	def probability_of_scorching(self, position):
		q = self.flamability
		burning_neighbors = self.get_neighbors(position, [FIRE]) #get fire neighbors
		k = len(burning_neighbors)
		return 1 - (1-q)**k

	# used primarily for bot 3. updates which nodes are on the perimeter of the currently burning nodes
	def update_radiance(self):
		self.radiance.clear()

		for ember in self.burning_nodes:
			neighbors = self.get_neighbors(ember, [OPEN]) # get the nodes around the fire < excludes the goal >
			for neighbor in neighbors:
				if neighbor not in self.burning_nodes and neighbor not in self.radiance:
					self.radiance.add(neighbor)



# GETTERS
	def get_neighbors(self, position, allowable):
		directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
		valid_neighbors = []

		for d in directions:
			x, y = position[0] + d[0], position[1] + d[1]

			if 0 < x < self.size - 1 and 0 < y < self.size - 1: # if it is an interior neighbor
				if self.game_board[x][y] in allowable:
					valid_neighbors.append((x, y))

		return valid_neighbors

	
	# calculates shortest path using A*
	def get_shortest_path(self, start, goal, modified=False, radiance=None):
		path = a_star(self.game_board, start, goal, modified, radiance)
		if path:
			path.pop(0)
		return path

	# calculates shortest path from bot to goal using shortest paths while running simulated games
	def get_simulated_path(self):
		path = great_value_monte_carlo(self.bot, self.goal, self.game_board, self.simulation, self.flamability)
		if path:
			path.pop(0)
		return path

	def get_initial_fire(self):
		return self.initial_fire

	def get_goal(self):
		return self.goal

	def get_origin(self):
		return self.original_position

	def get_flammability(self):
		return self.flamability

	def get_size(self):
		return self.size

	def get_grid(self):
		return self.game_board

	def get_burning_nodes(self):
		return self.burning_nodes


# SETTERS
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


# UTILITY

	def has_burned_down(self):
		if self.bot in self.burning_nodes:
			return True, "bot on fire"
		if self.goal in self.burning_nodes:
			return True, "goal on fire"

		return False, None

	def can_move(self, position):
		if self.game_board[position] == OPEN  or self.game_board[position] == GOAL:
			return True

		return False

	def move_to(self, position):
		self.bot = position

	def is_safe(self):
		return self.bot == self.goal

	def build_path(self, parent, position):
		fringe = []
		fringe.append(position)
		while True:
			curr = parent[fringe[-1]]
			if curr == None:
				return fringe[::-1]

			fringe.append(curr)


	def display_game_board(self):
		display_image(self.game_board)

	def refresh(self):
		for i in range(self.size):
			for j in range(self.size):
				if self.game_board[i][j] not in (0, 1):
					self.game_board[i][j] = OPEN

		self.bot = self.original_position
		self.game_board[self.original_position] = BOT
		self.game_board[self.goal] = GOAL
		self.game_board[self.initial_fire] = FIRE

		self.burning_nodes.clear()
		self.burning_nodes.add(self.initial_fire)

	def freak_out(self):
		variables = {}
		variables["size"] = self.size
		variables["flamability"] = self.flamability
		variables["original_position"] = self.original_position
		variables["goal"] = self.goal 
		variables["initial_fire"] = self.initial_fire

		with open('meta_data.txt', 'w') as file:

			for key, value in variables.items():
				file.write(f"{key}: {value}\n")
			file.write(f"Gameboard:\n")
			for row in self.game_board:
				line = ','.join(map(str, row))
				file.write(line+'\n')


#	 an attempt to speed up games by  getting rid of uninteresting and one sided games
	def is_doomed(self, bot_path):
		fire_path =  self.get_shortest_path(self.initial_fire, self.goal)
		bot_path =  self.get_shortest_path(self.original_position, self.goal)

		if len(bot_path)*3 < len(fire_path) or len(bot_path) < 0.0025*(self.size-1)*(self.size-1):
			#print("bot is quite close to the goal")
			return False , bot_path, "probably activated fire suppression"
		if bot_path is None:
			#print("no bot path found")
			return True, [], "could not find path to goal"
		if len(fire_path)/self.flamability < len(bot_path):
			#print("Fire is much closer to  button than the bot is")
			return True , [], "proably goal is on fire"
		if self.initial_fire == self.goal:
			#print("Initial Fire spawned on the Goal")
			return True , [], "initial fire spawned on the goal"
		if self.initial_fire == self.original_position:
			#print("Initial Fire spawned on the Bot")
			return True , [], "initial fire spawned on the bot"

		return False, None, None


		