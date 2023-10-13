# Out of the Frying Pan and Into the Flyer - Bot Navigation Simulation

Navigate a bot through a burning spaceship, aiming to reach a button to suppress the fire.

## Files Description:

### app.py
- **Role:** Main execution file.
- **Functionality:**
  - Sets up the game environment.
  - Calls a driver function to run the game for all four ships.
  - Resets the board in between games, ensuring all 4 bots get to play the game on the same board size each execution.
- **Main Function:** `main(board_size, flammability, ship_id)`

### ship.py
- **Role:** Core data structure.
- **Functionality:**
  - Handles game state and information.
  - Manages fire mechanics.
  - Calls `algorithms.py` when needing to calculate shortest paths.

### ship_3D.py
- **Role:** Despite the name, it's used for handling simulated games.
- **Functionality:** Specifically caters to Bot 4's heuristic.

### algorithms.py
- **Role:** Algorithms storage.
- **Functionality:**
  - Stores A* implementations.
  - Uses A* with Manhattan distance as the primary heuristic.
  - Bot 4 employs a modified version of A* with a different heuristic.

### data_collection.py
- **Role:** Data collection utility.
- **Functionality:**
  - Executes a multi-threaded script.
  - Collates all results into a CSV file.

### gameboard_info.txt
- **Role:** Config file.
- **Functionality:**
  - Can be used when running `app.py` as main to specify game information.
- **Format:**
  ```
  simulation info:
    100, 0.7
  ```

### generate_matrix.py
- **Role:** Board utility functions.
- **Functionality:**
  - Provides some game board specific functions.
  - Generates images displaying the final game state.

## How to Run:
1. Ensure all files are in the same directory.
2. Update `gameboard_info.txt` with the desired simulation parameters.
3. Execute `app.py` to start the simulation.
4. Check the CSV output for results and generated images for visualization.
