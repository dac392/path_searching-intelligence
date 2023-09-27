import numpy as np
import random
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

OPEN = 1
CLOSED = 0

def display_image(matrix):
    # Define a color map where:
    #  0 is mapped to white
    #  1 is mapped to black
    #  2 is mapped to gold ( BOT )
    #  3 is mapped to purple ( GOAL )
    colors = [(0, 0, 0), (1, 1, 1), (0.5, 0, 0.5), (1, 0.84, 0)]  # R, G, B
    n_bins = [4]  # Discretizes the interpolation into bins
    cmap_name = 'custom1'
    cm = ListedColormap(colors, name=cmap_name, N=None)
    
    # Display the image
    border_thickness = 0.5
    plt.imshow(matrix, cmap=cm, vmin=0, vmax=3,
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
    
    plt.show()


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

if __name__ == "__main__":

	generate_matrix(10);


