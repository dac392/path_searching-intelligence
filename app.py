from ship import ship_t

SUCCESS = 0
FAILURE = -1
BOT1 = 1
BOT2 = 2
BOT3 = 3
BOT4 = 4

DEBUGING = False

def debug(ship, path):
	ship.set_path(path)
	ship.display_game_board()


def run_simulation(ship, path, heuristic=None, bot=BOT1):
	if not path:
		return FAILURE, []

	is_doomed, bot_path, reason = ship.is_doomed(path)
	if is_doomed:
		return FAILURE, [], reason # the ones with empy  paths are likely uninteresting
	elif not is_doomed and bot_path:
		return SUCCESS, bot_path, reason

	if bot == BOT4:
		path = heuristic()

	path_taken = []

	while not ship.is_safe():
		next_position = path.pop(0)

		if ship.can_move(next_position) or bot==BOT1:
			ship.move_to(next_position)
			path_taken.append(next_position)

		if not ship.is_safe():
			ship.apply_scorch()
			has_burned_down, reason = ship.has_burned_down()
			if has_burned_down:
				return FAILURE, path_taken, reason

		if bot != BOT1 and not ship.is_safe():
			path = heuristic()
			if not path:
				return FAILURE, path_taken, "could not find path to goal"

	return SUCCESS, path_taken, "activated fire supression"

def driver(ship, heuristic, bot, ship_id):
	shortest_path = ship.get_shortest_path(ship.get_origin(), ship.get_goal()) if bot != BOT3 else heuristic()

	status, path, reason = run_simulation(ship, shortest_path, heuristic, bot)
	if DEBUGING:
		print("Success") if status == SUCCESS else print("Failure")
		debug(ship, path)

	ship.refresh()
	data = {
		"ship_id": ship_id,
		"bot_id": bot,
		"result": "Success" if status == SUCCESS else "Failure",
		"reason": reason, 
		"path_taken": path,
		"length_of_path": len(path)
	}
	return data


def main(board_size, flamability, ship_id,  info=None):
	ship = ship_t(board_size, flamability)

	bot_1_results = driver(ship, None, BOT1, ship_id)
	bot_2_results = driver(ship, ship.heuristic_2, BOT2, ship_id)
	bot_3_results = driver(ship, ship.heuristic_3, BOT3, ship_id)
	bot_4_results = driver(ship, ship.heuristic_4, BOT4, ship_id)
	if DEBUGING and info:
		print(info)

	return bot_1_results, bot_2_results, bot_3_results, bot_4_results




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
	    
	main(int(board_size), float(flammability), 1 ,game_info)
