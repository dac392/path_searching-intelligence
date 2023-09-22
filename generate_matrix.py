import numpy as np
import random
import matplotlib.pyplot as plt

def display_image(matrix):
    # Map the 0s and 1s in the matrix to the color values for white and black respectively
    img = np.array(matrix) * 255
    
    # Display the image
    border_thickness = 0.5
    plt.imshow(img, cmap='gray', vmin=0, vmax=255, extent=[-border_thickness, img.shape[1] + border_thickness,
                                                           img.shape[0] + border_thickness, -border_thickness])
    plt.axis('off')  # Turn off the axis
    plt.gca().set_xlim([-border_thickness, img.shape[1] + border_thickness])
    plt.gca().set_ylim([img.shape[0] + border_thickness, -border_thickness])
    
    # Setting a border around the graph using axhline and axvline
    plt.gca().axhline(y=-border_thickness, color='black', linewidth=border_thickness*2)
    plt.gca().axhline(y=img.shape[0] + border_thickness, color='black', linewidth=border_thickness*2)
    plt.gca().axvline(x=-border_thickness, color='black', linewidth=border_thickness*2)
    plt.gca().axvline(x=img.shape[1] + border_thickness, color='black', linewidth=border_thickness*2)
    
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

    # print(start);
    # print(matrix);
    matrix[matrix > 0] = 0
    matrix[matrix == -1] = 1
    display_image(matrix);




def get_neighbors(matrix, start, n):
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    neighbors = [(start[0] + d[0], start[1] + d[1]) for d in directions]
    valid_neighbors = [(x, y) for x, y in neighbors if 0 < x < n - 1 and 0 < y < n - 1]
    return valid_neighbors

if __name__ == "__main__":

	generate_matrix(10);


