import numpy as np
import heapq
import tkinter as tk
from tkinter import simpledialog, messagebox, Canvas
import time

# Create 60x60 grid with obstacles
grid = np.zeros((60, 60))
np.random.seed(42)
for _ in range(70):
    x, y = np.random.randint(0, 60, 2)
    while grid[x][y] == 1:
        x, y = np.random.randint(0, 60, 2)
    grid[x][y] = 1

# A* algorithm implementation
class Node:
    def __init__(self, x, y, g=float('inf'), h=0):
        self.x = x
        self.y = y
        self.g = g
        self.h = h
        self.f = g + h
        self.parent = None

    def __lt__(self, other):
        return self.f < other.f

def heuristic(x1, y1, x2, y2):
    return max(abs(x1 - x2), abs(y1 - y2))  # Change heuristic to account for diagonal moves

def a_star(grid, start, end):
    start_node = Node(start[0], start[1], g=0, h=heuristic(start[0], start[1], end[0], end[1]))
    end_node = Node(end[0], end[1])
    open_list = [start_node]
    open_set = {(start_node.x, start_node.y)}
    closed_set = set()
    nodes = {(x, y): Node(x, y, h=heuristic(x, y, end[0], end[1])) for x in range(60) for y in range(60)}
    
    while open_list:
        current_node = heapq.heappop(open_list)
        open_set.remove((current_node.x, current_node.y))
        closed_set.add((current_node.x, current_node.y))
        if (current_node.x, current_node.y) == (end_node.x, end_node.y):
            path = []
            while current_node:
                path.append((current_node.x, current_node.y))
                current_node = current_node.parent
            return path[::-1]
        
        # 8-connectivity: Allow for diagonal moves
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                x, y = current_node.x + dx, current_node.y + dy
                if 0 <= x < 60 and 0 <= y < 60 and grid[x][y] == 0 and (x, y) not in closed_set:
                    neighbor = nodes[(x, y)]
                    g_value = current_node.g + 1 if dx == 0 or dy == 0 else current_node.g + 1.414  # 1.414 is the distance for a diagonal move
                    
                    if (x, y) not in open_set:
                        open_set.add((x, y))
                        heapq.heappush(open_list, neighbor)
                    elif g_value >= neighbor.g:
                        continue
                    neighbor.parent = current_node
                    neighbor.g = g_value
                    neighbor.f = neighbor.g + neighbor.h
                    
    return None

def draw_grid_with_path(path, start, end):
    canvas.delete("all")  # Clear previous drawings
    for i in range(60):
        for j in range(60):
            color = 'black' if grid[i][j] == 1 else 'white'
            canvas.create_rectangle(j*10, i*10, (j+1)*10, (i+1)*10, fill=color, outline="gray")
    canvas.create_oval(start[1]*10+1, start[0]*10+1, (start[1]+1)*10-1, (start[0]+1)*10-1, fill='green')
    canvas.create_oval(end[1]*10+1, end[0]*10+1, (end[1]+1)*10-1, (end[0]+1)*10-1, fill='red')
    
    root.update()
    if path:
        for (x, y) in path:
            canvas.create_oval(y*10+3, x*10+3, (y+1)*10-3, (x+1)*10-3, fill='blue')
            root.update()
            time.sleep(0.03)  # Delay for simulation effect

def on_find_path_button_clicked():
    try:
        start = tuple(map(int, start_entry.get().split(',')))
        end = tuple(map(int, end_entry.get().split(',')))
        path = a_star(grid, start, end)
        draw_grid_with_path(path, start, end)
    except:
        messagebox.showerror("Error", "Invalid input. Ensure format is x,y (e.g., 5,6)")


# GUI Setup
root = tk.Tk()
root.title("A* Pathfinding")

left_frame = tk.Frame(root)
left_frame.pack(side=tk.LEFT, padx=20, pady=20)

# Entries for start and end points
start_label = tk.Label(left_frame, text="Start (x,y):")
start_label.pack(pady=10)
start_entry = tk.Entry(left_frame)
start_entry.pack(pady=10)
start_entry.insert(0, "0,0")

end_label = tk.Label(left_frame, text="End (x,y):")
end_label.pack(pady=10)
end_entry = tk.Entry(left_frame)
end_entry.pack(pady=10)
end_entry.insert(0, "59,59")

find_path_button = tk.Button(left_frame, text="Find Path", command=on_find_path_button_clicked)
find_path_button.pack(pady=20)

canvas = Canvas(root, width=600, height=600)
canvas.pack(side=tk.RIGHT)

root.mainloop()
