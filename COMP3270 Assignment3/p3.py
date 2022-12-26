import sys, grader, parse

def value_iteration(problem):
    return_value = ''
    iterations = problem[3]
    grid = problem[4]
    k = 0   #store the iteration number

    #initialize the value board with 0.00
    value = [[0]*len(grid[0])]*len(grid)
    return_value += "V_k=" + str(k) + "\n"
    return_value += printStartValue(problem)
    k += 1
    while k < iterations:
        return_value += "V_k=" + str(k) + "\n"
        value, action = getValueAction(problem,value)
        return_value += printValue(value)
        return_value += "pi_k=" + str(k) + "\n"
        return_value += printAction(action)
        k += 1
    #delete the new line sign
    return_value = return_value[:-1]
    return return_value

#get Value and Action at specific position
def getValueAction(problem, value):
    grid = problem[4]
    new_valueBoard = []
    new_actionBoard = []

    for i in range(len(value)):
        new_valueBoard.append([])
        new_actionBoard.append([])
        for j in range(len(value[0])):
            new_value = 0
            new_action = ''

            #if it is an exit position
            if grid[i][j] != '_' and grid[i][j] != '#' and grid[i][j] != 'S':
                new_value = round(float(grid[i][j]),2)
                new_action = 'x'
            #if it is a wall position
            elif grid[i][j] == '#':
                new_value = ' ##### '
                new_action = '#'
            else:
                new_value, new_action = getMaxValueAction(i,j,problem,value)
                        
            new_valueBoard[i].append(new_value)
            new_actionBoard[i].append(new_action)

    return new_valueBoard, new_actionBoard

#get the max value and relative action
def getMaxValueAction(row0,col0,problem,value):
    discount = problem[0]
    n = problem[1]   #noise
    livingReward = problem[2]
    grid = problem[4]
    d = {'N':['N', 'E', 'W'], 'E':['E', 'S', 'N'], 'S':['S', 'W', 'E'], 'W':['W', 'N', 'S']}
    values = []    #store all possible values
    actions = []   #store all relative actions
    max_value = None
    max_action = ''

    #calculate every situation for all possible actions N/E/S/W at position [row0,col0]
    for a in d:
        supposed_value = 0
        for action in d[a]:
            delta = 0 #store the change value
            row,col = row0,col0
            #get supposed position according to certain action
            if action == 'N':
                row -= 1
            elif action == 'S':
                row += 1
            elif action == 'E':
                col += 1
            elif action == 'W':
                col -= 1
            
            #check what agent meet
            #if walk out of boundary or meet wall, then the agent doesn't move, delta value is the current value
            if row < 0 or row >= len(grid) or col < 0 or col >= len(grid[0]) or grid[row][col] =='#':
                delta = livingReward + discount*value[row0][col0]
            #if agent reach another position successfully, update delta and value
            else:
                delta = livingReward + discount*value[row][col]

            #check whether the action is the intended action and update value
            if action == a:
                supposed_value += (1-2*n)*delta
            else:
                supposed_value += n*delta
        values.append(supposed_value)
        actions.append(a)

    max_value = max(values)
    #return the max value and first action that reaches the max value
    for i in range(len(actions)):
        if values[i] == max_value:
            max_action = actions[i]
            break
    return max_value,max_action

#print the action board
def printAction(action):
    actionBoard = ''
    for i in range(len(action)):
        for j in range(len(action[0])):
            actionBoard += '|{:3}|'.format(' '+action[i][j]+' ')
        actionBoard += '\n'
    return actionBoard

#print the value board
def printValue(value):
    valueBoard = ''
    for i in range(len(value)):
        for j in range(len(value[0])):
            if type(value[i][j]) == str:
                valueBoard += '|{:7}|'.format(value[i][j])
            else:
                valueBoard += '|{:7.2f}|'.format(value[i][j])
        valueBoard += '\n'
    return valueBoard

#print the start value board
def printStartValue(problem):
    grid = problem[4]
    value = [[0]*len(grid[0])]*len(grid)
    valueBoard = ''
    for i in range(len(value)):
        for j in range(len(value[0])):
            if grid[i][j] == '#':
                valueBoard += '|{:7}|'.format(' ##### ')
            else:
                valueBoard += '|{:7.2f}|'.format(value[i][j])
        valueBoard += '\n'
    return valueBoard

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    #test_case_id = -4
    problem_id = 3
    grader.grade(problem_id, test_case_id, value_iteration, parse.read_grid_mdp_problem_p3)