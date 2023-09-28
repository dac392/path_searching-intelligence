from ship import ship_t

SUCCESS = 0
FAILURE = -1

def debug(ship, path):
	ship.set_path(path)
	ship.display_game_board()


def run_simulation(ship, path, heuristic=None, mode=1):
	if not path:
		return FAILURE, []
	path.pop(0)
	path_taken = []

	while not ship.is_safe():
		next_position = path.pop(0)

		if ship.can_move(next_position) or mode==1:
			ship.move_to(next_position)
			path_taken.append(next_position)
		# else:
		# 	heuristic(path, next_position)

		# could check if we are done rn if its convinient

		if not ship.is_safe():
			ship.apply_scorch()
			if ship.has_burned_down():
				return FAILURE, path_taken

	return SUCCESS, path_taken

def main(board_size, flamability):
	ship = ship_t(board_size, flamability)
	shortest_path = ship.calculate_shortest_path()


	status, path = run_simulation(ship, shortest_path)
	print("Success") if status == SUCCESS else print("Failure")
	debug(ship, path)
	# ship.refresh()


	# run_simulation(ship, shortest_path, ship.heuristic_1, 2)
	# ship.refresh()
	# run_simulation(ship, shortest_path, ship.heuristic_1, 3)
	# ship.refresh()
	# run_simulation(ship, shortest_path, ship.heuristic_1, 4)






if __name__ == '__main__':
	main(10, 0.3)