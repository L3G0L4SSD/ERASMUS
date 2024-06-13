def is_bipartite(graph, n):
    color = [-1] * n
    stack = []

    for start in range(n):
        if color[start] == -1:  
            stack.append(start)
            color[start] = 0 

            while stack:
                node = stack.pop()
                current_color = color[node]
                print(stack)
                for neighbor in graph[node]:
                    print(color, neighbor)
                    if color[neighbor] == -1:  
                        
                        color[neighbor] = 1 - current_color
                        stack.append(neighbor)
                    elif color[neighbor] == current_color:  
                        return False, []
    # print(color)
    return True, color

def sitting_scheme(guests, animosities):
    n = len(guests)
    graph = [[] for _ in range(n)]
    guest_index = {guest: idx for idx, guest in enumerate(guests)}
 

    for g1, g2 in animosities:
        graph[guest_index[g1]].append(guest_index[g2])
        graph[guest_index[g2]].append(guest_index[g1])
    print(graph, n)

    bipartite, color = is_bipartite(graph, n)

    if not bipartite:
        print("It is not possible to arrange the guests into two tables without conflicts.")
    else:
        table1 = [guests[i] for i in range(n) if color[i] == 0]
        table2 = [guests[i] for i in range(n) if color[i] == 1]

        print("Table 1:", table1)
        print("Table 2:", table2)

# Example usage:
guests = ["Alice", "Bob", "Charlie", "David", "Eve", "Ole"]
animosities = [("Alice", "Bob"), ("Charlie", "David"), ("Eve", "Alice"), ("Bob", "Charlie"), ("Ole", "Charlie")]

print(sitting_scheme(guests, animosities))