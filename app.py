from ship import ship_t

def main(board_size):
	ship = ship_t(board_size)
	ship.display_game_board();

if __name__ == '__main__':
	main(20)