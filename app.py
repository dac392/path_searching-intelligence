from ship import ship_t

def main(board_size):
	ship = ship_t(board_size)
	shortest_path = ship.calculate_shortest_path()
	ship.set_path(shortest_path)
	print(shortest_path)
	ship.display_game_board();


if __name__ == '__main__':
	main(20)