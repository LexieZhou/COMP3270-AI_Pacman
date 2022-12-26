import sys, parse
import time, os, copy
import random

def expecti_max_mulitple_ghosts(problem, k):
    #Your p6 code here
    Seed = int(problem['Seed'])
    Ppos = problem['Pacman']
    Fpos = problem['Food']
    Gpos = problem['Ghost'] #Ghosts, W, X, Y, Z
    Board = problem['Board']
    Gpos_sequence_all = ['W','X','Y','Z']
    Gpos_sequence = Gpos_sequence_all[:len(Gpos)]
    depth = 0
    max_depth = k
    #define game variables
    ROUND_NUM = 0
    TOTAL_SCORE = 0
    PACMAN_WIN_FLAG = False
    GHOST_WIN_FLAG = False
    solution = ''
    winner = ''
    gameState = [Ppos,Fpos,Gpos,PACMAN_WIN_FLAG,GHOST_WIN_FLAG,Board,Gpos_sequence,max_depth,TOTAL_SCORE]

    solution = 'seed: ' + str(Seed) + '\n' + str(ROUND_NUM) + '\n' + printBoard(gameState)
    #if PACMEN_WIN_FLAG == False and GHOST_WIN_FLAG == False
    while (gameState[3] == False and gameState[4] == False):
        #get pacman's moving direction
        P_direction = expectimax(0,depth,gameState)[1]
        #update gameState including positions and total scores
        update(0,P_direction,gameState)
        ROUND_NUM += 1
        TOTAL_SCORE = gameState[8]
        #print solution
        solution += str(ROUND_NUM) + ': P moving ' + P_direction + '\n'
        solution += printBoard(gameState)
        solution += "score: " + str(TOTAL_SCORE) + '\n'
        #check winning situation and print
        if gameState[4] == True:
            solution += 'WIN: Ghost'
            winner = 'Ghost'
            break
        elif gameState[3] == True:
            solution += 'WIN: Pacman'
            winner = 'Pacman'
            break
        else:
            #ghost's turn
            direction = ''
            for G in Gpos_sequence:
                #ghost agent number is 1-4
                agent = Gpos_sequence.index(G) + 1
                legalActions = getLegalActions(agent,gameState)
                if legalActions == []:
                    direction = ''
                else:
                    #get ghost's moving direction by randomly choose one legal actions
                    direction = random.choice(legalActions)
                    #update gameState including positions and total scores
                    update(agent,direction,gameState)
                ROUND_NUM += 1
                TOTAL_SCORE = gameState[8]
                #print solution
                solution += str(ROUND_NUM) + ': ' + G + ' moving ' + direction + '\n'
                solution += printBoard(gameState)
                solution += "score: " + str(TOTAL_SCORE) + '\n'
                #check winning situation and print
                if gameState[4] == True:
                    solution += 'WIN: Ghost'
                    break
    return solution, winner

#minimax recursion function
def expectimax(agent, depth, gameState):
    expectimax_state = copy.deepcopy(gameState)
    Ppos = expectimax_state[0]
    Fpos = expectimax_state[1]
    Gpos = expectimax_state[2]
    Board = expectimax_state[5]
    max_depth = expectimax_state[7]
    max_value = -float('inf')
    #if the game has terminated, return the value of the terminal states
    if win_check_pos(expectimax_state)[0] == True or win_check_pos(expectimax_state)[1] == True or depth == max_depth:
        return evaluate(Ppos, Fpos, Gpos, Board),'STOP'
    #if maximizer's turn (Pacman is the agent 0)
    if agent == 0:
        #store the minimax value and relative action from all legal actions
        expectimax_value = []
        expectimax_action = []
        #store all the actions that can reach the max value in order to random the best move
        max_action = []
        for action in getLegalActions(agent,expectimax_state):
            expectimax_value.append(expectimax(1,depth,generateSuccessor(agent,action,expectimax_state))[0])
            expectimax_action.append(action)
        #maximum value
        max_value = max(expectimax_value)
        for i in range(len(expectimax_value)):
            if (expectimax_value[i] == max_value):
                max_action.append(expectimax_action[i])
        return max_value,random.choice(max_action)

    #if minimizer's turn (ghost is the agent 1-4)
    else:
        nextAgent = agent + 1
        if len(Gpos) == agent:  #all ghosts have moved, then it is Pacman's turn
            nextAgent=0
        if nextAgent==0:  #increase current depth by 1 if all agents have moved
            depth += 1
        #store the expectimax value and relative action from all legal actions
        expecti_value = []
        legal_actions = getLegalActions(agent,expectimax_state)
        if legal_actions == []:
            return expectimax(nextAgent, depth,gameState), ''
        else:
            for action in legal_actions:
                expecti_value.append(evaluate(Ppos,Fpos,Gpos,Board)) 
            #expecti_value is the average of all possible values
            expecti_value = sum(expecti_value)/float(len(expecti_value))
            return expecti_value, ''

#generate successor of the agent in current gameState
def generateSuccessor(agent,action,expectimax_state):
    new_expectimax_state = copy.deepcopy(expectimax_state)
    new_Fpos = expectimax_state[1]
    Gpos_sequence = new_expectimax_state[6]
    #specify the agent and position
    if agent == 0:
        row = new_expectimax_state[0][0]
        col = new_expectimax_state[0][1]
    else:
        ghostName = Gpos_sequence[agent-1]
        row = new_expectimax_state[2][ghostName][0]
        col = new_expectimax_state[2][ghostName][1]
    #generate new position
    if action == 'E':
        new_pos = [row, col+1]
    elif action == 'W':
        new_pos = [row, col-1]
    elif action == 'N':
        new_pos = [row-1, col]
    elif action == 'S':
        new_pos = [row+1, col]
    
    #if food has been eaten by pacmen
    if new_pos in new_Fpos and agent == 0:
        new_Fpos.remove(new_pos)
    new_expectimax_state[1] = new_Fpos
    #change the position in gameState
    if agent == 0:
        new_expectimax_state[0] = new_pos
    else:
        new_expectimax_state[2][ghostName] = new_pos
    return new_expectimax_state

#get legal actions of the agent
def getLegalActions(agent,expectimax_state):
    legal_move = []   #list to store available move choice
    Gpos = expectimax_state[2]
    Gpos_sequence = expectimax_state[6]
    Board = expectimax_state[5]
    if agent == 0:
        row = expectimax_state[0][0]
        col = expectimax_state[0][1]
        if Board[row-1][col] != '%':
            legal_move.append('N')
        if Board[row+1][col] != '%':
            legal_move.append('S')
        if Board[row][col-1] != '%':
            legal_move.append('W')
        if Board[row][col+1] != '%':
            legal_move.append('E')
    else:
        ghostName = Gpos_sequence[agent-1]
        row = expectimax_state[2][ghostName][0]
        col = expectimax_state[2][ghostName][1]
        if Board[row-1][col] != '%' and Board[row-1][col] not in Gpos:
            legal_move.append('N')
        if Board[row+1][col] != '%'and Board[row+1][col] not in Gpos:
            legal_move.append('S')
        if Board[row][col-1] != '%'and Board[row][col-1] not in Gpos:
            legal_move.append('W')
        if Board[row][col+1] != '%'and Board[row][col+1] not in Gpos:
            legal_move.append('E')
    legal_move.sort()
    return legal_move

#design a evaluation function
def evaluate(Ppos,Fpos,Gpos,Board):
    #use bfs search to find the distance to the closest Ghost
    minGdis = ghost_search(Ppos[0],Ppos[1],Gpos,Board)
    #use bfs search to find the distance to the closest food
    minFdis = food_search(Ppos[0],Ppos[1],Fpos,Board)

    #evaluation function
    if minGdis == 0:
        value = -float('inf')
    #food is close enough and ghost is not a big threat
    elif minFdis == 0 and minGdis > 1:
        value = float('inf')
    #ghost is a serious threat
    elif minGdis <= 1:
        value = -10/minGdis
    #other cases
    else:
        value = -1/minGdis + 1/minFdis
    return value

#find the closest ghost and return the distance
def ghost_search(start_x,start_y,Gpos,Board):
    Gpos_list = []  #store Ghost positions
    for G in Gpos:
        Gpos_list.append((Gpos[G][0],Gpos[G][1]))
    #initialize frontier using initial state
    frontier = [(start_x,start_y),None]
    exploredSet = set()
    dis = 0
    while len(frontier) != 0:
        node = frontier.pop(0)
        if node == None:
            dis += 1
            frontier.append(None)
            #encountering two Nones means encountering all the nodes
            if (len(frontier)!=0 and frontier[0] == None):
                dis = float('inf')
                break
        #if reach any of the goal states, then break
        elif node in Gpos_list:
            break
        else:
            if node not in exploredSet:
                #add nodes to exploredSet if node is not in exploredSet
                exploredSet.add(node)
                #if the frontier has child, add child to frontier
                if Board[node[0]-1][node[1]] != '%':
                    frontier.append((node[0]-1,node[1]))
                if Board[node[0]+1][node[1]] != '%':
                    frontier.append((node[0]+1,node[1]))
                if Board[node[0]][node[1]+1] != '%':
                    frontier.append((node[0],node[1]+1))
                if Board[node[0]][node[1]-1] != '%':
                    frontier.append((node[0],node[1]-1))
    return dis

#find the closest food and return the distance
def food_search(Px,Py,Fpos,Board):
    #initialize frontier using initial state
    frontier = [(Px,Py),None]
    exploredSet = set()
    dis = 0
    while len(frontier) != 0:
        node = frontier.pop(0)
        if node == None:
            dis += 1
            frontier.append(None)
            #encountering two Nones means encountering all the nodes
            if (len(frontier)!=0 and frontier[0] == None):
                dis = float('inf')
                break
        #if reach any of the goal states, then break
        elif [node[0],node[1]] in Fpos:
            break
        else:
            if node not in exploredSet:
                #add nodes to exploredSet if node is not in exploredSet
                exploredSet.add(node)
                #if the frontier has child, add child to frontier
                if Board[node[0]-1][node[1]] != '%':
                    frontier.append((node[0]-1,node[1]))
                if Board[node[0]+1][node[1]] != '%':
                    frontier.append((node[0]+1,node[1]))
                if Board[node[0]][node[1]+1] != '%':
                    frontier.append((node[0],node[1]+1))
                if Board[node[0]][node[1]-1] != '%':
                    frontier.append((node[0],node[1]-1))
    return dis

#check who wins in temporary expectimax_gameState, and return the winning flag
def win_check_pos(expectimax_gameState):
    Ppos = expectimax_gameState[0]
    Fpos = expectimax_gameState[1]
    Gpos = expectimax_gameState[2]

    pacman_win_flag = expectimax_gameState[3]
    ghost_win_flag = expectimax_gameState[4]
    for G in Gpos:
        if Ppos == Gpos[G]:
            ghost_win_flag = True
    if ghost_win_flag == False and Fpos == []:
        pacman_win_flag = True
    return ghost_win_flag, pacman_win_flag


#update gameState (all positions and board) with agent and move direction
def update(agent, direction,gameState):
    EAT_FOOD_SCORE = 10
    PACMAN_EATEN_SCORE = -500
    PACMAN_WIN_SCORE = 500
    PACMAN_MOVING_SCORE = -1
    #original position
    Ppos = gameState[0]
    Fpos = gameState[1]
    Gpos = gameState[2]
    PACMAN_WIN_FLAG = gameState[3]
    GHOST_WIN_FLAG = gameState[4]
    Board = gameState[5]
    G = gameState[6][agent-1]
    TOTAL_SCORE = gameState[8]

    #previous position and change relative board position to ' '
    if agent == 0:
        row,col = Ppos[0],Ppos[1]
        Board[Ppos[0]][Ppos[1]] = ' '
    else:
        row,col = Gpos[G][0],Gpos[G][1]

        #if the Gposition is orginially a food
        if Gpos[G] in Fpos:
            Board[Gpos[G][0]][Gpos[G][1]] = '.'
        else:
            Board[Gpos[G][0]][Gpos[G][1]] = ' '
    
    #change position according to action(direction)
    if direction == 'E':
        col = col+1
    elif direction == 'W':
        col = col-1
    elif direction == 'N':
        row = row-1
    elif direction == 'S':
        row = row+1

    #new position
    if agent == 0:
        Ppos = [row,col]
        #check if pacman meets Ghost
        for G in Gpos:
            if Ppos == Gpos[G]:
                TOTAL_SCORE += PACMAN_EATEN_SCORE
                TOTAL_SCORE += PACMAN_MOVING_SCORE
                #modify board
                Board[Ppos[0]][Ppos[1]] = G
                #update ghost_win_flag
                GHOST_WIN_FLAG = True
        #if not meet ghost, check whether meet food
        if GHOST_WIN_FLAG == False and Ppos in Fpos:
            TOTAL_SCORE += EAT_FOOD_SCORE
            TOTAL_SCORE += PACMAN_MOVING_SCORE
            Fpos.remove(Ppos)
            #modify board
            Board[Ppos[0]][Ppos[1]] = 'P'
            #check whether Pacman has won
            if Fpos == []:
                TOTAL_SCORE += PACMAN_WIN_SCORE
                #update pacman_win_flag
                PACMAN_WIN_FLAG = True
        #pacman meets empty square
        elif GHOST_WIN_FLAG == False:
            TOTAL_SCORE += PACMAN_MOVING_SCORE
            Board[Ppos[0]][Ppos[1]] = 'P'
    #ghost 
    else:
        Gpos[G] = [row,col]
        #modify board
        Board[Gpos[G][0]][Gpos[G][1]] = G
        for G in Gpos:
            if Ppos == Gpos[G]:
                TOTAL_SCORE += PACMAN_EATEN_SCORE
                #update ghost_win_flag
                GHOST_WIN_FLAG = True
                break

    #update new gameState
    gameState[0] = Ppos
    gameState[1] = Fpos
    gameState[2] = Gpos
    gameState[3] = PACMAN_WIN_FLAG
    gameState[4] = GHOST_WIN_FLAG
    gameState[5] = Board
    gameState[8] = TOTAL_SCORE

    return

#print the whole board
def printBoard(gameState):
    Board = gameState[5]
    Row = len(Board)
    line = ''
    for i in range(Row):
        line += ''.join(Board[i])
        line += '\n'
    return line

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])    
    problem_id = 6
    file_name_problem = str(test_case_id)+'.prob' 
    file_name_sol = str(test_case_id)+'.sol'
    path = os.path.join('test_cases','p'+str(problem_id)) 
    problem = parse.read_layout_problem(os.path.join(path,file_name_problem))
    k = int(sys.argv[2])
    num_trials = int(sys.argv[3])
    verbose = bool(int(sys.argv[4]))
    print('test_case_id:',test_case_id)
    print('k:',k)
    print('num_trials:',num_trials)
    print('verbose:',verbose)
    start = time.time()
    win_count = 0
    for i in range(num_trials):
        solution, winner = expecti_max_mulitple_ghosts(copy.deepcopy(problem), k)
        if winner == 'Pacman':
            win_count += 1
        if verbose:
            print(solution)
    win_p = win_count/num_trials * 100
    end = time.time()
    print('time: ',end - start)
    print('win %',win_p)