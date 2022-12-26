import sys, grader, parse

def policy_evaluation(problem):
    return_value = ''
    iterations = problem[3]
    grid = problem[4]
    k = 0   #store the iteration number

    #initialize the value board with 0.00
    value = [[0]*len(grid[0])]*len(grid)
    return_value += "V^pi_k=" + str(k) + "\n"
    return_value += printStartValue(problem)
    k += 1
    while k < iterations:
        return_value += "V^pi_k=" + str(k) + "\n"
        value = getValue(problem,value)
        return_value += printValue(value)
        k += 1
    #delete the new line sign
    return_value = return_value[:-1]
    return return_value

#get Value at specific position
def getValue(problem, value):
    grid = problem[4]
    policy = problem[5]
    discount = problem[0]
    n = problem[1]   #noise
    livingReward = problem[2]
    new_valueBoard = []

    for i in range(len(value)):
        new_valueBoard.append([])
        for j in range(len(value[0])):
            new_value = 0
            a = policy[i][j]   #intended action
            d = {'N':['N', 'E', 'W'], 'E':['E', 'S', 'N'], 'S':['S', 'W', 'E'], 'W':['W', 'N', 'S']}

            if a == 'exit':
                new_value = round(float(grid[i][j]),2)
            elif a == '#':
                new_value = ' ##### '
            else:
                #get all possible actions
                actions = d[a]
                for action in actions:
                    row, col = i,j
                    delta = 0 #store the change value
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
                        delta = livingReward + discount*value[i][j]
                    #if agent reach another position successfully, update delta and value
                    else:
                        delta = livingReward + discount*value[row][col]

                    #check whether the action is the intended action and update value
                    if action == a:
                        new_value += (1-2*n)*delta
                    else:
                        new_value += n*delta
            new_valueBoard[i].append(new_value)
    return new_valueBoard


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
    policy = problem[5]
    value = [[0]*len(policy[0])]*len(policy)
    valueBoard = ''
    for i in range(len(value)):
        for j in range(len(value[0])):
            if policy[i][j] == '#':
                valueBoard += '|{:7}|'.format(' ##### ')
            else:
                valueBoard += '|{:7.2f}|'.format(value[i][j])
        valueBoard += '\n'
    return valueBoard

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    #test_case_id = -7
    problem_id = 2
    grader.grade(problem_id, test_case_id, policy_evaluation, parse.read_grid_mdp_problem_p2)