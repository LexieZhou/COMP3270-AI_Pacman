import os, sys
def read_graph_search_problem(file_path):
    #Your p1 code here
    #read the file
    with open(file_path) as f:
        lines = f.readlines()
    #delete '\n' in the end
    for i in range(len(lines)-1):
        lines[i] = lines[i][:-1]
    #use dictionary to define problem
    problem={}
    problem['start_state'] = ''
    problem['goal_states'] = []   #create a list to store possibly multiple goal states
    problem['graph'] = {}         #store node neighbours and costs e.g.'D': {(10, 'Ar')}
    problem['heuristics'] = {}    #store heuristics e.g.'A': 30

    for i in range(len(lines)):
        #split the statement in a certain line
        line_elements = lines[i].split(' ')
        #store the start state
        if i == 0:
            problem['start_state'] += line_elements[1]
        #store the goal states
        elif i == 1:
            for k in range(1,len(line_elements)):
                problem['goal_states'].append(line_elements[k])
        else:
            #store the heuristics of each node
            if len(line_elements) == 2:
                problem['heuristics'][line_elements[0]] = float(line_elements[1])
            #store the graph and costs between two nodes
            else:
                startNode = line_elements[0]
                endNode = line_elements[1]
                cost = float(line_elements[2])
                #create a key if the startNode does not exist in 'graph'
                if startNode not in problem['graph']:
                    problem['graph'][startNode] = [(cost, endNode)]
                #add value to the list if the startNode already exists
                else:
                    problem['graph'][startNode].append((cost, endNode))
                
    #close the file
    f.close()
    return problem

def read_8queens_search_problem(file_path):
    #Your p6 code here
    #read the file
    with open(file_path) as prob:
        lines = prob.readlines()
    #delete '\n' in the end
    for i in range(len(lines)-1):
        lines[i] = lines[i][:-1]
    #delete space in the row string
    for i in range(len(lines)):
        lines[i] = lines[i].replace(' ', '')

    #queen is a list denoting the 8 queens' position for each column
    queen = []
    for j in range(8):    #column
        for i in range(len(lines)):    #row
            if lines[i][j] == 'q':
                #store the queen row position for each column into the queen list
                queen.append([j,i])

    #define problem as a dictionary
    problem = {}
    #calculate the row number
    problem['row'] = len(lines)
    #represent the queen position
    problem['queen'] = queen
    #represent the board
    problem['board'] = lines
    return problem

if __name__ == "__main__":
    if len(sys.argv) == 3:
        problem_id, test_case_id = sys.argv[1], sys.argv[2]
        if int(problem_id) <= 5:
            problem = read_graph_search_problem(os.path.join('test_cases','p'+problem_id, test_case_id+'.prob'))
        else:
            problem = read_8queens_search_problem(os.path.join('test_cases','p'+problem_id, test_case_id+'.prob'))
        print(problem)
    else:
        print('Error: I need exactly 2 arguments!')