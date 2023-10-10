from generate_matrix import get_random

CLOSED = -1
OPEN = 0
FIRE = 1

class ship_3D():
	def __init__(self, ship_2D, time_steps):
		self.size = ship_2D.get_size()
		self.game_board = create_3d_array(time_steps, ship_2D.get_size(), ship_2D.get_size())
		self.flamability = ship_2D.get_flammability()
		self.time_steps = time_steps
		copy_2d_to_3d( self.game_board, ship_2D.get_grid(), time_steps)

		
		self.original_position = ship_2D.get_origin()
		self.goal = ship_2D.get_goal()
		self.initial_fire = ship_2D.get_initial_fire()

	def run_simulation(self, number_of_simulation):
		for simulation in range(number_of_simulation):
			burning_nodes = set()
			burning_nodes.add(self.initial_fire)

			for t in range(0, self.time_steps):
				self.populate_burning_nodes(burning_nodes, t)
				if t == 0:
					continue

				new_scorched_nodes = self.get_new_nodes_on_fire(burning_nodes, t, simulation)
				for pos in new_scorched_nodes:
					burning_nodes.add(pos)
					self.game_board[t][pos[0]][pos[1]] += 1

		for t in range(self.time_steps):
			for i in range(1, self.size-1):
				for j in range(1, self.size-1):
					if self.game_board[t][i][j] > OPEN:
						self.game_board[t][i][j] = self.game_board[t][i][j]/number_of_simulation

	def populate_burning_nodes(self, burning_nodes, t):
		for node in burning_nodes:
			self.game_board[t][node[0]][node[1]] += FIRE


	def get_new_nodes_on_fire(self, burning_nodes, t, simulation):
		might_scorch = {}
		statement =[]
		for node in burning_nodes:
			flamable_neighbors = self.get_neighbors(node, t,  list(range(simulation+1)))
			for position in flamable_neighbors:
				if position not in might_scorch:
					might_scorch[position] = self.probability_of_scorching(position, t, simulation+1)

		for flamable_cell, probability in might_scorch.items():
			if get_random() <= probability:
				statement.append(flamable_cell)
		return statement

	def probability_of_scorching(self, position, t, simulation):
		q = self.flamability
		burning_neighbors = self.get_neighbors(position, t, [simulation]) #get fire neighbors
		k = len(burning_neighbors)
		return 1 - (1-q)**k

	def get_neighbors(self, position, t, allowable):
		directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
		valid_neighbors = []

		for d in directions:
			x, y = position[0] + d[0], position[1] + d[1]

			if 0 < x < self.size - 1 and 0 < y < self.size - 1: # if it is an interior neighbor
				if self.game_board[t][x][y] in allowable:
					valid_neighbors.append((x, y))

		return valid_neighbors

	def print(self):
		# Determining the maximum width based on float format (e.g., 0.00) and padding
		max_width = max(max(len(f"{elem:.2f}") for elem in row) for matrix in self.game_board for row in matrix) + 4  # +4 for more padding

		for depth, matrix in enumerate(self.game_board):
			print(f"Layer {depth + 1}:")
			for row in matrix:
				formatted_row = []
				for elem in row:
					if elem == -1:
						formatted_elem = '  X  '.ljust(max_width)
					elif elem == 0:
						formatted_elem = ' ___ '.ljust(max_width)
					else:
						formatted_elem = f"{elem:.2f}".ljust(max_width)
					formatted_row.append(formatted_elem)
				print(''.join(formatted_row))
				print()



def create_3d_array(t, x, y):
	return [[[0 for _ in range(y)] for _ in range(x)] for _ in range(t)]

def print_3d(arr):
	for depth, matrix in enumerate(arr):
		print(f"Layer {depth + 1}:")
		for row in matrix:
			print(row)
		print()

def copy_2d_to_3d(grid_3d, grid_2d, time_steps):
    for t in range(time_steps):
        for i in range(len(grid_2d)):
        	for j in range(len(grid_2d[0])):
	        	if grid_2d[i][j] == 0:
	        		grid_3d[t][i][j] = CLOSED
	        	else:
	        		grid_3d[t][i][j] = OPEN

if __name__ == '__main__':
	from ship import ship_t
	ship = ship_t(10, 0.5)
	ship_3d = ship_3D(ship, 10)
	ship_3d.run_simulation(1000)
	ship_3d.print()

	

		