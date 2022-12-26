# 1. How to run the game?
#    python p4.py num_of_trials print_policy (1 is print, 0 otherwise)
#    e.g. python p4.py 100 0
# 2. The program will output find count and find number
#    e.g.  find_count/num_trials = 99/100 
#          find % 99.0
# 3. What is problem definition?
#    problem uses the test case 2 of problem 3: 
#    storing information about discount, noise,livingReward, grid, and agent position.
#    problem = [1.0, 0.1, -0.01, [['_', '_', '_', '1'], ['_', '#', '_', '-1'], ['S', '_', '_', '_']], [2, 0]]
# 4. Findings
#    - The learning rate decay and epsilon decay is quite important to 
# reach an optimal policy and would be different in different maps/games. 
# We should try to find an appropriate one.
# Like in this problem, alpha should be reduced more quickly at the beginning,
# while epsilon should be reduced more slowly at first.
#   - With more iteration times, the learning output is better and more accurate.
#   - Instead of decaying learning rate and epsilon, if we increase learning rate 
# and epsilon by time, the learning process will become time consuming and the 
# find rate will be lower (the learning output is not accurate).


import sys
import random,copy

# the main function about how to get optimal policy
def optimal_policy(problem):
    policy = ''
    alpha = 1  # set initial learning rate
    epsilon = 1 # set initial epsilon
    k = 0      # store the iteration times

    # store the initial problem setting, for each episode, need to initialize state back to initial problem setting
    init_problem = copy.deepcopy(problem)
    noise = problem[1] 
    grid = problem[3]
    Qvalue = initQvalue(grid)   #initialize Qvalue, Qvalue stores all Q values in the grid

    # learning process, iteration 1000 times
    while k < 1000:
        k += 1
        alpha = 150.0/(150.0+8*k)       # update alpha
        epsilon = 100.0/(100.0+k/20.0)  # update epsilon for epsilon-greedy
        # initialize the problem settings
        episode_problem = copy.deepcopy(init_problem)
        EPISODE_END_FLAG = False

        # begin one episode from start state to exit position
        while EPISODE_END_FLAG == False:
            Apos = episode_problem[4]  # agent position, keep updating
            # for each step, make action using epsilon greedy
            intended_action = intendAction(Apos[0], Apos[1], epsilon, Qvalue)  # get intended action
            if intended_action == 'exit':
                grid[Apos[0]][Apos[1]] = init_problem[3][Apos[0]][Apos[1]] # set back the initial exit value
                EPISODE_END_FLAG = True
                real_action = "exit"
            else:
                d = {'N':['N', 'E', 'W'], 'E':['E', 'S', 'N'], 'S':['S', 'W', 'E'], 'W':['W', 'N', 'S']}
                real_action = random.choices(population=d[intended_action], weights=[1 - noise*2, noise, noise])[0]

            # update Qvalue
            Qvalue = updateQ(intended_action,real_action,alpha,init_problem, episode_problem, Qvalue)
            # update problem grid
            EPISODE_END_FLAG, episode_problem = updateProb(real_action, episode_problem,EPISODE_END_FLAG)
            # get learnt policy
            policy = printOptimalAction(problem, Qvalue)

    return policy

#initialize the Qvalue table at the beginning of the game
def initQvalue(grid):
    # initialize Qvalue which stores dictionary(action:Qvalue)
    Qvalue = []*len(grid)
    for i in range(len(grid)):
        Qvalue.append([])
        for j in range(len(grid[0])):
            Pdic = {}   # store action-value information of certain position
            # exit position
            if grid[i][j] != '_' and grid[i][j] != 'S' and grid[i][j] != '#':
                Pdic['exit'] = 0.0
            # wall position
            elif grid[i][j] == '#':
                Pdic['#'] = 0.0
            else:
                Pdic['N'] = 0.0
                Pdic['S'] = 0.0
                Pdic['E'] = 0.0
                Pdic['W'] = 0.0
            Qvalue[i].append(Pdic)
    return Qvalue

# use use epsilon greedy (with decay) to force exploit and get intended action
def intendAction(row0, col0, epsilon, Qvalue):
    optimal_a = getOptimalAction(row0,col0,Qvalue)
    # if reach the exit position or a wall
    if optimal_a == 'exit' or optimal_a == '#':
        return optimal_a
    else:
        n = random.uniform(0, 1)
        if n < epsilon:
            # randomly choose one of the directions if n < epsilon
            return random.choice(['N','S','E','W'])
        else:
            # otherwise return optimal action
            return optimal_a

# get optimal action for certain position (with the max Qvalue)
def getOptimalAction(row0, col0, Qvalue):
    # get action-value detail information from Qvalue table
    Pdic = Qvalue[row0][col0]
    # if the position is a wall or an exit position
    if len(Pdic) == 0:
        return list(Pdic.keys())[0]
    else:
        # return the action with the max Qvalue
        return max(Pdic, key=Pdic.get)

# update Qvalue and state position
def updateQ(action, real_action, alpha, init_problem, problem, Qvalue):
    init_grid = init_problem[3]
    discount = problem[0]
    livingReward = problem[2]
    grid = problem[3]
    row0, col0 = problem[4][0],problem[4][1]
    prev_Q = Qvalue[row0][col0][action]
    new_Q = None
    
    if real_action == 'exit':
        new_Q = (1-alpha)*prev_Q + alpha*(livingReward + float(init_grid[row0][col0]))
    else:
        maxNextQ = 0
        row,col = copy.deepcopy(row0),copy.deepcopy(col0)
        # change position according to real action
        if real_action == 'N':
            row -= 1
        elif real_action == 'S':
            row += 1
        elif real_action =='E':
            col += 1
        elif real_action == 'W':
            col -= 1
        #if reach out of boundary or meet wall
        if row < 0 or row >= len(grid) or col < 0 or col >= len(grid[0]) or grid[row][col] == '#':
            maxNextQ = livingReward + discount * max(Qvalue[row0][col0].values())
        #if agent reach another position successfully, update delta and value
        else:
            maxNextQ = livingReward + discount * max(Qvalue[row][col].values())
            
        new_Q = (1-alpha)*prev_Q + alpha*maxNextQ
    
    # update new_Q in Qvalue table
    Qvalue[row0][col0][action] = new_Q

    return Qvalue

#update problem grid and agent position
def updateProb(real_action, problem, EPISODE_END_FLAG):
    grid = problem[3]
    Apos = problem[4]
    
    # check new position according to real action
    row, col = copy.deepcopy(Apos[0]), copy.deepcopy(Apos[1])
    if real_action == 'N':
        row -= 1
    elif real_action == 'S':
        row += 1
    elif real_action =='E':
        col += 1
    elif real_action == 'W':
        col -= 1
    
    # check meet what
    # if walk out of boundary, no need to update
    if row < 0 or row >= len(grid) or col < 0 or col >= len(grid[0]) or grid[row][col] == '#':
        return EPISODE_END_FLAG, problem
    # else, change agent position
    else:
        grid[Apos[0]][Apos[1]] = '_'  #set back the initial position setting
        grid[row][col] = 'P'
        Apos = [row,col]

    #update problem
    problem[3] = grid
    problem[4] = Apos

    return EPISODE_END_FLAG,problem

# print the Qvalue board
def printValue(Qvalue):
    for i in range(len(Qvalue)):
        for j in range(len(Qvalue[0])):
            print(Qvalue[i][j])
    return

# print the grid board
def printGrid(problem):
    grid = problem[3]
    gridBoard = ''
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            gridBoard += '|{:3s}|'.format(grid[i][j])
        gridBoard += '\n'
    return gridBoard

# print the optimal action board
def printOptimalAction(problem, Qvalue):
    grid = problem[3]
    optimalBoard = ''
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            optimalBoard += '|{:5s}|'.format(getOptimalAction(i,j,Qvalue))
        optimalBoard += '\n'
    optimalBoard = optimalBoard[:-1]
    return optimalBoard

if __name__ == "__main__":
    # initialize problem setting
    problem = [1.0, 0.1, -0.01, 
        [['_', '_', '_', '1'], ['_', '#', '_', '-1'], ['S', '_', '_', '_']], 
        [2, 0]]
    # store optimal policy    
    optimal = "|E    ||E    ||E    ||exit |\n|N    ||#    ||W    ||exit |\n|N    ||W    ||W    ||S    |"
    policy = ''
    if len(sys.argv) == 3:
        num_trials = int(sys.argv[1])
        toPrint = int(sys.argv[2])
        print('num_trials:',num_trials)
        find_count = 0
        if toPrint == 1: #print out all policy
            for i in range(num_trials):
                policy = optimal_policy(problem)
                print(policy + '\n')
                if policy == optimal:
                    find_count += 1
        else:
            for i in range(num_trials):
                policy = optimal_policy(problem)
                if policy == optimal:
                    find_count += 1
        find_rate = find_count/num_trials * 100
        print("find_count/num_trials = {}/{}".format(find_count,num_trials))
        print('find %',find_rate)
    else:
        print('Error: I need exactly 3 arguments! \np4.py,num_of_trials,print_policy respectively!')