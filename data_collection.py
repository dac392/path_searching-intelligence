import threading
import time
import queue
import csv

import app
import uuid

def run_simulation(results_queue, grid_size, flammability):
	# Here, you'd run your bot simulation and gather the data
	# For the sake of example, I'll just return some mock data
	ship_id = str(uuid.uuid4())
	results = app.main(grid_size, flammability, ship_id)
	for result in results:
		result["grid_size"] = grid_size
		result["flammability"] = flammability
		results_queue.put(result)

def data_collector():
	# Define the queue to hold the results
	results_queue = queue.Queue()

	# Create a list to hold all results
	all_results = []
	threads = []

	Iterate over all grid sizes and flammabilities
	for grid_size in range(20, 201+1, 5):  # From 20 to 200 in intervals of 5
		for flammability_increment in range(1, 50):  # 50 intervals
			flammability = flammability_increment * 0.02  # From 0 to 0.98 in increments of 0.02

			t = threading.Thread(target = run_simulation, args=(results_queue, grid_size, flammability))
			t.start()
			
		for t in threads:
			print("joined a thread. woo")
			t.join()

		# Collect results
		while not results_queue.empty():
			all_results.append(results_queue.get())



	return all_results


def write_to_csv(data):
	fieldnames = ["ship_id", "bot_id", "grid_size", "flammability", "result","reason", "path_taken", "length_of_path"]
	with open("simulation_results.csv", "a", newline='') as csv_file:
		writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
		writer.writeheader()
		for row in data:
			writer.writerow(row)


def main():
	for i in range(10):
		print(f"running... {i}")
		data = data_collector()
		write_to_csv(data)

if __name__ == "__main__":
	main()
