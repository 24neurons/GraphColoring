from ortools.linear_solver import pywraplp
import networkx as nx
import matplotlib.pyplot as plt
# Create the integer solver with the SCIP backend
# This is the solver that will be used to solve the problem
solver = pywraplp.Solver.CreateSolver('SCIP')
import time

num_nodes = 0
num_colors = 0
E = []
COLOR = [('paleturquoise1', '#BBFFFF'), ('palevioletred', '#DB7093'), ('peachpuff1', '#FFDAB9'), ('pink','#FFC0CB'), 
         ('purple', '#800080'), ('red4', '#8B0000'), ('royalblue', '#4169E1'), ('salmon', '#FA8072'), ('seagreen2', '#4EEE94'),
         ('sgiolivedrab', '#8E8E38'), ('sgislateblue',	'#7171C6'), ('skyblue', '#87CEEB'), ('teal','#008080'),
         ('thistle', '#D8BFD8'), ('tomato1','#FF6347'), ('violet', '#EE82EE'), ('yellow3','#CDCD00')]

def Input():
    print("Please enter the number of nodes : ")
    num_nodes = int(input())
    print("Please enter the number of edges:")
    num_edges = int(input())
    print("Please enter the edges")
    for _ in range(num_edges):
        f_node, s_node = list(map(int, input().split()))
        E.append((f_node, s_node))
    return num_nodes, E
def run():

    # 0. Reading the input
    num_nodes, E = Input()

    # 1. Declaring variables
    A, C, NODE_COLOR = {}, {}, []
    num_colors = num_nodes

    # 1.1 Declaring the coloring matrix variables
    # A[i][j] = 1 when node i is colored with color j and 0 otherwise
    for node in range(num_nodes):
        for color in range(num_colors):
            A[node, color] = solver.IntVar(0, 1, '') 

    # 1.2 Color variables
    for color in range(num_colors):
        C[color] = solver.IntVar(0, 1, '')

    # 2. Constraints

    # 2.1 One vertex one color
    for node in range(num_nodes):
        solver.Add(solver.Sum([A[node, color] for color in range(num_colors)]) == 1)

    # 2.2 Neighboors having different color
    # Similar with a color is never used twice in an edge
    for (f_node, s_node) in E:
        for color in range(num_colors):
            solver.Add(A[f_node, color] + A[s_node, color] <= C[color])
            
    # 3. Objective function
    solver.Minimize(solver.Sum([C[color] for color in range(num_colors)]))
    start = time.time()
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print(f'Total number of color = {int(solver.Objective().Value())}\n')
        for i in range(num_nodes):
            for j in range(num_colors):
                # Test if x[i,j] is 1 (with tolerance for floating point arithmetic).
                if A[i, j].solution_value() == 1:
                    print(f'Node {i} assigned to color {COLOR[j][0]}')
                    NODE_COLOR.append(COLOR[j][1])

    else:
        print('No solution found.')
    
    end = time.time()

    print(f"Time to solve: {end - start} seconds")
    graph_display(NODE_COLOR, E)
def graph_display(NODE_COLOR, E):
    num_nodes = len(NODE_COLOR)
    if num_nodes >= 30:
        print("Can not display the visualization for graphs with more than 30 nodes")
    else:
        # Creating the graph
        G = nx.Graph()
        #collecting colorss
        for node in range(num_nodes):
            G.add_node(node)
        for e in E:
            G.add_edge(*e)
        
        # Draw the original
        fig, ax = plt.subplots(1, 2)
        nx.draw(G, node_color = '#FFFFFF', edge_color = '#000000', with_labels = True, ax = ax[0])
        ax[0].set_title("Original graph")

        # Draw the colored graph
        nx.draw(G, node_color=NODE_COLOR, with_labels=True, ax = ax[1])
        ax[1].set_title("Colored graph")
        plt.show()


if __name__ == "__main__":
    run()