from collections import deque
import matplotlib.pyplot as plt
import numpy as np

def bfs(labyrinth, start, exit):
    rows, cols = len(labyrinth), len(labyrinth[0])
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    
    queue = deque([(start, [start])])
    distances = {start: 0}
    paths = {start: [start]}
    
    while queue:
        (x, y), path = queue.popleft()
        
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            
            if 0 <= nx < rows and 0 <= ny < cols and labyrinth[nx][ny] == 1 and (nx, ny) not in distances:
                queue.append(((nx, ny), path + [(nx, ny)]))
                distances[(nx, ny)] = distances[(x, y)] + 1
                paths[(nx, ny)] = path + [(nx, ny)]
                
                if (nx, ny) == exit:
                    return distances[(nx, ny)], paths[(nx, ny)]
    
    return float('inf'), []  # If the exit is not reachable

def determine_winner(labyrinth, wizards, exit):
    results = []
    
    for wizard in wizards:
        start, speed = wizard['start'], wizard['speed']
        distance, path = bfs(labyrinth, start, exit)
        if distance == float('inf'):
            time = float('inf')  # Wizard can't reach the exit
        else:
            time = distance / speed
        results.append({'name': wizard['name'], 'time': time, 'path': path})
    
    # Determine the wizard with the minimum time
    winner = min(results, key=lambda x: x['time'])
    
    return winner, results

# Modified labyrinth (1 represents corridor, 0 represents wall)
labyrinth = [
    [1, 1, 0, 1, 1, 0, 1],
    [0, 1, 1, 1, 0, 1, 1],
    [1, 1, 0, 1, 1, 1, 0],
    [0, 0, 0, 1, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1, 0, 0],
    [1, 1, 1, 1, 1, 1, 1]
]

# Example wizards with their starting positions and speeds
wizards = [
    {'name': 'Wizard A', 'start': (0, 0), 'speed': 1.0},
    {'name': 'Wizard B', 'start': (2, 0), 'speed': 0.5},
    {'name': 'Wizard C', 'start': (6, 6), 'speed': 1.2}
]

exit = (6, 0)

winner, results = determine_winner(labyrinth, wizards, exit)

print(f"The winner is {winner['name']} with a time of {winner['time']:.2f} minutes.")
print("\nAll paths and times:")

for result in results:
    print(f"{result['name']}: Time = {result['time']:.2f} minutes, Path = {result['path']}")

# Display labyrinth map and paths
plt.imshow(labyrinth, cmap='binary')
plt.title("Labyrinth Map (0: Wall, 1: Corridor)")
plt.xlabel("Columns")
plt.ylabel("Rows")
plt.xticks(range(len(labyrinth[0])))
plt.yticks(range(len(labyrinth)))
plt.colorbar(label="0: Wall, 1: Corridor")
plt.grid(color='gray', linestyle='-', linewidth=0.5)

# Highlight exit
plt.scatter(exit[1], exit[0], color='red', s=100, label='Exit')

# Highlight paths of wizards
colors = ['blue', 'green', 'purple']
for i, result in enumerate(results):
    path = np.array(result['path'])
    plt.plot(path[:, 1], path[:, 0], color=colors[i], marker='o', label=f"{result['name']}'s Path")

plt.legend()
plt.show()
