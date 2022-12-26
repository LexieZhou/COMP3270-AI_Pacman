import sys, grader, parse
import random
import copy

def play_episode(problem):
    experience = ''
    #fetch problem details
    init_problem = copy.deepcopy(problem)
    seed = problem[0]
    livingReward = problem[2]
    cumulativeReward = 0.0
    GameEnd = False
    if seed != -1:
        random.seed(seed, version=1)

    #print start state
    experience += "Start state:\n" + printBoard(problem) + "Cumulative reward sum: " + str(cumulativeReward) + "\n-------------------------------------------- \n"
    #process
    while GameEnd == False:
        a,real_a = makeMove(problem)   #get intended action and real action
        experience += "Taking action: {} (intended: {})\n".format(real_a,a)
        GameEnd, problem = update(init_problem,problem,real_a,GameEnd)
        experience += "Reward received: {}\nNew state:\n".format(livingReward)
        cumulativeReward = round(cumulativeReward + livingReward,2)  #round number to 2 decimal places

        experience += printBoard(problem) + "Cumulative reward sum: {}".format(cumulativeReward) + "\n-------------------------------------------- \n"
    #exit
    endApos = problem[5]
    # get reward from initial grid at end agent position (exit position)
    exitReward = float(init_problem[3][endApos[0]][endApos[1]])
    cumulativeReward = round(cumulativeReward + exitReward,2)
    experience += "Taking action: exit (intended: exit)\nReward received: {}\nNew state:\n".format(exitReward)
    experience += printEndBoard(init_problem)
    experience += "Cumulative reward sum: {}".format(cumulativeReward)

    return experience

#agent make move, return intended action and real action
def makeMove(problem):
    policy = problem[4]
    Apos = problem[5]
    n = problem[1]   #noise
    a = policy[Apos[0]][Apos[1]]   #intended action
    d = {'N':['N', 'E', 'W'], 'E':['E', 'S', 'N'], 'S':['S', 'W', 'E'], 'W':['W', 'N', 'S']}
    #if the agent is at exit position
    if policy[Apos[0]][Apos[1]] == 'exit':
        return 'exit','exit'
    else:
        real_a = random.choices(population=d[a], weights=[1 - n*2, n, n])[0]
        return a,real_a

#update the game situation before exit
#first check whether reach the exit,reward recieved, whether reach the wall, then update the problem setting
def update(init_problem, problem, real_a, GameEnd):
    init_grid = init_problem[3]
    grid = problem[3]
    policy = problem[4]
    Apos = problem[5]
    row, col = Apos[0], Apos[1]    #used to store the supposed Apos

    #update supposed agent position and check what agent met
    if real_a == 'N':
        row -= 1
    elif real_a == 'S':
        row += 1
    elif real_a == 'E':
        col += 1
    elif real_a == 'W':
        col -= 1
 
    #if walk out of boundary or reach the wall, no need to update
    if row < 0 or row >= len(grid) or col < 0 or col >= len(grid[0]) or grid[row][col] =='#':
        return GameEnd, problem
    #if agent met exit position, update grid
    elif policy[row][col] == 'exit':
        grid[Apos[0]][Apos[1]] = init_grid[Apos[0]][Apos[1]]  #set back the initial position setting
        grid[row][col] = 'P'
        Apos = [row,col]
        GameEnd = True
    #if agent reach _, update grid and Agent position
    else:
        grid[Apos[0]][Apos[1]] = init_grid[Apos[0]][Apos[1]]  #set back the initial position setting
        grid[row][col] = 'P'
        Apos = [row,col]

    #update new problem
    problem[3] = grid
    problem[5] = Apos

    return GameEnd, problem

#print the grid board
def printBoard(problem):
    new_grid = copy.deepcopy(problem[3])
    Apos = problem[5]
    board = ''
    #if agent at the start state, replace S by P
    if new_grid[Apos[0]][Apos[1]] == 'S':
        new_grid[Apos[0]][Apos[1]] = 'P'
    #print out the grid board
    for i in range(len(new_grid)):
        for j in range(len(new_grid[i])):
            position = '{0: >5}'.format(new_grid[i][j])   #set position printing width
            board += position
        board += '\n' 
    return board

#print end grid board
def printEndBoard(init_problem):
    grid = init_problem[3]
    board = ''
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            position = '{0: >5}'.format(grid[i][j])   #set position printing width
            board += position
        board += '\n' 
    return board

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    #test_case_id = 1
    problem_id = 1
    grader.grade(problem_id, test_case_id, play_episode, parse.read_grid_mdp_problem_p1)