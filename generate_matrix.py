import numpy as np
import random
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

OPEN = 1
CLOSED = 0
FIRE = 4

def display_image(matrix):
    # Define a color map where:
    #  0 is mapped to black
    #  1 is mapped to white
    #  2 is mapped to gold (bot)
    #  3 is mapped to purple (goal)
    #  4 is mapped to red (fire)
    #  5 path (244/255, 196/255, 212/255)

    closed_color = (0, 0, 0)
    open_color = (1, 1, 1)
    original_position = (0, 0.6588, 0.4196)
    goal_color = (0.8,0,0.8)
    fire_color = (1,0.647,0)
    path_color = (0.2, 1, 0.2)
    burning_color = (0, 0.3922, 0)
    og_is_goal_color = (1, 0.8431, 0)
    burned_path_color = (1, 0.4118, 0.3804)
    killed_color = (0.6902, 0.8784, 0.902)
    initial_fire_color = (1, 0, 0)


    colors = [ closed_color, open_color, original_position, goal_color, fire_color, path_color, burning_color, og_is_goal_color, burned_path_color, killed_color, initial_fire_color]  # R, G, B
    cmap_name = 'custom1'
    cm = ListedColormap(colors, name=cmap_name, N=None)
    
    # Display the image
    border_thickness = 0.5
    plt.imshow(matrix, cmap=cm, vmin=0, vmax=10,  # Set vmax to 4
               extent=[-border_thickness, matrix.shape[1] + border_thickness,
                       matrix.shape[0] + border_thickness, -border_thickness])
    plt.axis('off')  # Turn off the axis
    plt.gca().set_xlim([-border_thickness, matrix.shape[1] + border_thickness])
    plt.gca().set_ylim([matrix.shape[0] + border_thickness, -border_thickness])
    
    # Setting a border around the graph using axhline and axvline
    plt.gca().axhline(y=-border_thickness, color='black', linewidth=border_thickness * 2)
    plt.gca().axhline(y=matrix.shape[0] + border_thickness, color='black', linewidth=border_thickness * 2)
    plt.gca().axvline(x=-border_thickness, color='black', linewidth=border_thickness * 2)
    plt.gca().axvline(x=matrix.shape[1] + border_thickness, color='black', linewidth=border_thickness * 2)
    

    plt.gca().invert_yaxis()
    plt.show()

#generates a random number between 0 and 1
def get_random():
    return random.random()


def generate_random_coordinate(n):
    x = random.randint(1, n - 2)
    y = random.randint(1, n - 2)
    return (x, y)

def generate_matrix(n):
    matrix = np.zeros((n, n), dtype=int);
    start = generate_random_coordinate(n);

    fringe = []
    fringe.append(start);
    # generate initial matrix
    while fringe:
        random_index = random.randint(0, len(fringe) - 1)
        curr = fringe.pop(random_index);
        if matrix[curr] == 1 or matrix[curr] == 0:
            matrix[curr] = -1;
            neighbors = get_neighbors(matrix, curr, n);
            for neighbor in neighbors:
                if matrix[neighbor] != -1:
                    matrix[neighbor] += 1
                    fringe.append(neighbor)

    matrix[matrix > 0] = CLOSED
    matrix[matrix == -1] = OPEN

    # open approximately half of the dead ends
    dead_ends = get_dead_ends(matrix, n)
    eliminate_dead_ends(matrix, n, dead_ends)
    return matrix

def eliminate_dead_ends(matrix, n, dead_ends):
    length = len(dead_ends)//2
    #print(f"there are {len(dead_ends)} dead ends and we will remove {length} dead_ends")
    while length < len(dead_ends):
        random_index = random.randint(0, len(dead_ends) - 1)
        position = None
        index = 0;

        for elm in dead_ends:
            if index ==random_index:
                position = elm
                break
            index+=1
            
        matrix[position] = OPEN
        dead_ends.remove(position)



def get_dead_ends(matrix, n):
    fringe = []
    for i in range(1, n-1):
        for j in range(1, n-1):
            #if its an interior posiotion (probably redundant)
            if 0 < i < n - 1 and 0 < j < n - 1:
                position = (i, j)
                if(matrix[position] == OPEN) and is_dead_end(matrix, position, n):
                    neighbors = get_closed_neighbors(matrix, get_neighbors(matrix, position, n))
                    if neighbors:
                        for neighbor in neighbors:
                            fringe.append(neighbor)
    return set(fringe)

def is_dead_end(matrix, position, n):
    neighbors = get_neighbors(matrix, position, n)
    count = 0
    for pos in neighbors:
        if matrix[pos] == OPEN:
            count+=1
    return True if count>1 else False

def get_closed_neighbors(matrix, neighbors):
    closed_neighbors = []
    for neighbor in neighbors:
        if matrix[neighbor] == CLOSED:
            closed_neighbors.append(neighbor)
    return closed_neighbors

def get_neighbors(matrix, start, n):
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    neighbors = [(start[0] + d[0], start[1] + d[1]) for d in directions]
    valid_neighbors = [(x, y) for x, y in neighbors if 0 < x < n - 1 and 0 < y < n - 1]
    return valid_neighbors

def get_flamability_matrix(n):
    return np.random.rand(n, n)

if __name__ == "__main__":

	generate_matrix(10);


