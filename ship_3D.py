from generate_matrix import get_random
import copy

CLOSED = 0
OPEN = 1
BOT = 2
GOAL = 3
FIRE = 4

# Concider renaming the class
class ship_3D():
	def __init__(self, ship_2D, time_steps):
		self.size = ship_2D.get_size()
		self.game_board = ship_2D.get_grid() # a reference to gameboard
		self.flammability = ship_2D.get_flammability()
		self.time_steps = time_steps
		self.burning_nodes = copy.deepcopy(ship_2D.get_burning_nodes())

		self.simulation = {} # stores the probabilities in [(x, y), average] pairs


	def run_simulation(self, number_of_simulations):
		for sim in range(number_of_simulations):
			# reset the simulation with the current game values
			grid = copy.deepcopy(self.game_board)
			burning_nodes = self.burning_nodes.copy()
			new_nodes_on_fire = set() # simulation list of nodes that catch on fire

			for time_step in range(self.time_steps):
				# 1. apply  scorch - let the fire spread
				self.apply_scorch(grid, burning_nodes, new_nodes_on_fire)


				# 2. in the probability matrix, +=1 on every new cell that caught fire
				for pos in new_nodes_on_fire:
					self.simulation[pos] = self.simulation.get(pos, 0)+1

		for pos, value in self.simulation.items():
			self.simulation[pos] = value/number_of_simulations


		return self.simulation


	def apply_scorch(self, grid, burning_nodes, new_nodes_on_fire):

		might_scorch = {}
		for node in burning_nodes:
			flamable_neighbors = get_neighbors(self.size, grid, node, [OPEN, GOAL, BOT])
			for position in flamable_neighbors:
				if position not in might_scorch:
					might_scorch[position] = self.probability_of_scorching(position, grid)

		for flammable_cell, probability in might_scorch.items():
			if get_random() <= probability:
				grid[flammable_cell[0]][flammable_cell[1]] = FIRE
				burning_nodes.add(flammable_cell)
				new_nodes_on_fire.add(flammable_cell)


	def probability_of_scorching(self, position, grid):
		q = self.flammability
		burning_neighbors = get_neighbors(self.size, grid, position, [FIRE]) #get fire neighbors
		k = len(burning_neighbors)
		return 1 - (1-q)**k



def get_neighbors(size, game_board, position, allowable):
	directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
	valid_neighbors = []

	for d in directions:
		x, y = position[0] + d[0], position[1] + d[1]

		if 0 < x < size - 1 and 0 < y < size - 1: # if it is an interior neighbor
			if game_board[x][y] in allowable:
				valid_neighbors.append((x, y))

	return valid_neighbors

	

		