from ship import ship_t

SUCCESS = 0
FAILURE = -1
BOT1 = 1
BOT2 = 2
BOT3 = 3
BOT4 = 4

DEBUGING = True

def debug(ship, path):
	ship.set_path(path)
	ship.display_game_board()


def run_simulation(ship, path, heuristic=None, bot=BOT1):
	if not path:
		return FAILURE, []

	if not DEBUGING and ship.is_doomed(path):
		return FAILURE, []

	path.pop(0)
	path_taken = []

	while not ship.is_safe():
		next_position = path.pop(0)

		if ship.can_move(next_position) or bot==BOT1:
			ship.move_to(next_position)
			path_taken.append(next_position)

		# could check if we are done rn if its convinient

		if not ship.is_safe():
			ship.apply_scorch()
			if ship.has_burned_down():
				return FAILURE, path_taken

		if bot != BOT1 and not ship.is_safe():
			path = heuristic()

	return SUCCESS, path_taken

def main(board_size, flamability, info=None):
	ship = ship_t(board_size, flamability)

	shortest_path_1 = ship.calculate_shortest_path()
	status_1, path_1 = run_simulation(ship, shortest_path_1)
	print("Success") if status_1 == SUCCESS else print("Failure")
	debug(ship, path_1)

	ship.refresh()
	shortest_path_2 = ship.calculate_shortest_path()
	status_2, path_2 = run_simulation(ship, shortest_path_2, ship.heuristic_2, BOT2)
	print("Success") if status_2 == SUCCESS else print("Failure")
	debug(ship, path_2)

	if DEBUGING and info:
		print(info)



	# run_simulation(ship, shortest_path, ship.heuristic_1, 2)
	# ship.refresh()
	# run_simulation(ship, shortest_path, ship.heuristic_1, 3)
	# ship.refresh()
	# run_simulation(ship, shortest_path, ship.heuristic_1, 4)

	






if __name__ == '__main__':
	# Open the file for reading
	board_size = None
	flammability = None
	game_info = None
	with open('gameboard_info.txt', 'r') as file:
	    lines = file.readlines()
	    
	    # Processing the simulation info line
	    simulation_info_line = lines[1].strip()  # assuming the second line contains the simulation info
	    board_size, flammability = map(float, simulation_info_line.split(', '))
	    
	    # Processing the rest of the file for game_info
	    game_info = ''.join(lines[3:])  # assuming the game info starts from the fourth line
	    
	main(int(board_size), float(flammability), game_info)
