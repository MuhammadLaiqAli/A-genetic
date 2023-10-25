import tkinter as tk
import random
import numpy as np

GRID_SIZE = 40
OBSTACLES = 20
MOVES = ['U', 'D', 'L', 'R']

def create_grid_with_obstacles():
    grid = np.zeros((GRID_SIZE, GRID_SIZE))
    for _ in range(OBSTACLES):
        x, y = random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1)
        grid[y, x] = 1
    return grid

def objective(path, grid, start, end):
    x, y = start
    obstacles_encountered = 0
    for move in path:
        if move == 'U' and y > 0: y -= 1
        if move == 'D' and y < GRID_SIZE - 1: y += 1
        if move == 'L' and x > 0: x -= 1
        if move == 'R' and x < GRID_SIZE - 1: x += 1
        if grid[y, x] == 1:
            obstacles_encountered += 1
    distance_to_goal = abs(end[0] - x) + abs(end[1] - y)
    return distance_to_goal + obstacles_encountered * GRID_SIZE

def crossover(p1, p2):
    if len(p1) < 2 or len(p2) < 2:
        return [p1, p2]
    index = random.randint(1, min(len(p1), len(p2)) - 1)
    return [p1[:index] + p2[index:], p2[:index] + p1[index:]]

def mutation(path):
    index = random.randint(0, len(path) - 1)
    path[index] = random.choice(MOVES)
    return path

def genetic_algorithm(grid, start, end, n_iter, n_pop, r_cross, r_mut):
    pop = [random.choices(MOVES, k=2 * GRID_SIZE) for _ in range(n_pop)]
    best, best_eval = None, float('inf')
    for gen in range(n_iter):
        scores = [objective(p, grid, start, end) for p in pop]
        for i, score in enumerate(scores):
            if score < best_eval:
                best, best_eval = pop[i], score
                print("Gen %d, new best score: %f" % (gen, best_eval))
        selected = [min(random.sample(pop, 3), key=lambda x: objective(x, grid, start, end)) for _ in range(n_pop)]
        children = []
        for i in range(0, n_pop, 2):
            p1, p2 = selected[i], selected[i+1]
            for c in crossover(p1, p2):
                if random.random() < r_mut:
                    c = mutation(c)
                children.append(c)
        pop = children
    return best, best_eval

def find_shortest_path():
    global start_point, end_point

    start_input = start_entry.get().split(',')
    end_input = end_entry.get().split(',')

    try:
        start_x = int(start_input[0])
        start_y = int(start_input[1])
        end_x = int(end_input[0])
        end_y = int(end_input[1])

        start_point = (start_x, start_y)
        end_point = (end_x, end_y)

        grid = create_grid_with_obstacles()
        best_path, score = genetic_algorithm(grid, start_point, end_point, 100, 100, 0.9, 0.2)

        # Clear existing path
        canvas.delete("path")

        x, y = start_point
        for move in best_path:
            if move == 'U': y -= 1
            if move == 'D': y += 1
            if move == 'L': x -= 1
            if move == 'R': x += 1
            canvas.create_oval(x*10, y*10, (x+1)*10, (y+1)*10, fill="red", tags="path")

    except ValueError:
        print("Invalid input format. Please enter start and end points as 'x,y'.")


# Create the main GUI window
root = tk.Tk()
root.title("Genetic Algorithm Pathfinding")

# Create input fields for start and end points
start_label = tk.Label(root, text="Start Point (x, y):")
start_label.pack()
start_entry = tk.Entry(root)
start_entry.pack()

end_label = tk.Label(root, text="End Point (x, y):")
end_label.pack()
end_entry = tk.Entry(root)
end_entry.pack()

# Button to trigger pathfinding
find_button = tk.Button(root, text="Find Shortest Path", command=find_shortest_path)
find_button.pack()

# Canvas for grid visualization
canvas = tk.Canvas(root, width=GRID_SIZE*10, height=GRID_SIZE*10)
canvas.pack()

# Create the grid with obstacles
grid = create_grid_with_obstacles()
for y in range(GRID_SIZE):
    for x in range(GRID_SIZE):
        color = "black" if grid[y, x] == 1 else "white"
        canvas.create_rectangle(x*10, y*10, (x+1)*10, (y+1)*10, fill=color)

# Global variables for start and end points
start_point = (0, 0)
end_point = (GRID_SIZE - 1, GRID_SIZE - 1)

# Start the tkinter main loop
root.mainloop()
