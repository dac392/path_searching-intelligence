import heapq

CLOSED = 0
class Node:
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.g = float('inf') # Distance to start node
		self.h = 0 # Heuristic distance to goal node
		self.f = 0 # Total cost
		self.parent = None

	def __eq__(self, other):
		return self.x == other.x and self.y == other.y

	def __lt__(self, other):
		return self.f < other.f

	def get_neighbors(self, grid):
		neighbors = []
		for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
			x, y = self.x + dx, self.y + dy
			if 0 < x < len(grid) -1 and 0 < y < len(grid) -1 and grid[x][y] != CLOSED:
				neighbors.append((x, y))
		return neighbors
		
	def get_exclusive_neighbors(self, grid, simulation):
		neighbors = []
		for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
			x, y = self.x + dx, self.y + dy
			if 0 < x < len(grid) -1 and 0 < y < len(grid) -1 and grid[x][y] != CLOSED:
				if simulation[x][y] <= 0.4:
					neighbors.append((x, y))
		return neighbors

	def get_position(self):
		return (self.x, self.y)




def heuristic(node, goal):
	# Using Manhattan distance as heuristic
	return abs(node.x - goal.x) + abs(node.y - goal.y)

def a_star(grid, start, goal, modified=False, radiance=None):
	start_node = Node(*start)
	goal_node = Node(*goal)
	start_node.g = 0
	start_node.h = heuristic(start_node, goal_node)
	start_node.f = start_node.h

	open_list = [start_node]
	closed_list = []

	while open_list:
		current_node = heapq.heappop(open_list)

		if current_node == goal_node:
			path = []
			while current_node:
				path.append((current_node.x, current_node.y))
				current_node = current_node.parent
			return path[::-1]  # Return reversed path

		closed_list.append(current_node)

		# neighbor shenanigans
		neighbors = current_node.get_neighbors(grid)
		for pos in neighbors:
			neighbor = Node(pos[0], pos[1])

			if neighbor in closed_list:
				continue

			if modified and pos in radiance:
				continue

			neighbor.g = current_node.g + 1
			neighbor.h = heuristic(neighbor, goal_node)
			neighbor.f = neighbor.g + neighbor.h
			neighbor.parent = current_node

			if neighbor not in open_list:
				heapq.heappush(open_list, neighbor)


	return None  # No path found

def walmart_brand_monte_carlo(start, goal, grid, simulation):
	start_node = Node(*start)
	goal_node = Node(*goal)
	start_node.g = 0
	start_node.h = heuristic(start_node, goal_node)
	start_node.f = start_node.h

	open_list = [start_node]
	closed_list = []

	while open_list:
		current_node = heapq.heappop(open_list)
		if current_node == goal_node:
			path = []
			while current_node:
				path.append((current_node.x, current_node.y))
				current_node = current_node.parent
			return path[::-1]  # Return reversed path

		# neighbor shenanigans
		neighbors = current_node.get_exclusive_neighbors(grid, simulation)
		for pos in neighbors:
			neighbor = Node(pos[0], pos[1])

			if neighbor in closed_list:
				continue

			neighbor.g = current_node.g + 1
			neighbor.h = heuristic(neighbor, goal_node)
			neighbor.f = neighbor.g + neighbor.h
			neighbor.parent = current_node

			if neighbor not in open_list:
				heapq.heappush(open_list, neighbor)


	return None  # No path found



