from ortools.linear_solver import pywraplp

# Create the integer solver with the SCIP backend
# This is the solver that will be used to solve the problem
solver = pywraplp.Solver.CreateSolver('SCIP')

def run():
    print("Please enter the number of nodes : ")
    num_nodes = int(input())
    print("Please enter the number of edges:")
    num_edges = int(input())
    print("Please enter the edges")
    E = []
    for e in range(num_edges):
        f_node, s_node = list(map(int, input().split()))
        E.append((f_node, s_node))

    # 1. Declaring variables
    A = {}
    C = {}
    num_color = num_nodes

    # 1.1 Declaring the coloring matrix variables
    # A[i][j] = 1 when node i is colored with color j and 0 otherwise
    for node in range(num_nodes):
        for color in range(num_color):
            A[node, color] = solver.IntVar(0, 1, '') 


    # 1.2 Color vector variables
    for color in range(num_color):
        C[color] = solver.IntVar(0, 1, '')

    # 2. Constraints

    # 2.1 One vertex one color
    for node in range(num_nodes):
        solver.Add(solver.Sum([A[node, color] for color in range(num_color)]) == 1)

    # 2.2 Neighboors having different color
    # Similar with a color is never used twice in an edge
    for (f_node, s_node) in E:
        for color in range(num_color):
            solver.Add(A[f_node, color] + A[s_node, color] <= C[color])
            
    # 3. Objective function
    solver.Minimize(solver.Sum([C[color] for color in range(num_color)]))

    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print(f'Total number of color = {solver.Objective().Value()}\n')
        for i in range(num_nodes):
            for j in range(num_color):
                # Test if x[i,j] is 1 (with tolerance for floating point arithmetic).
                if A[i, j].solution_value() == 1:
                    print(f'Node {i} assigned to color {j}')
        

    else:
        print('No solution found.')

if __name__ == "__main__":
    run()