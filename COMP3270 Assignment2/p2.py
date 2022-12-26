import sys, parse
import time, os, copy
import random

def better_play_single_ghosts(problem):
    #Your p2 code here
    #fetch problem detail
    Seed = int(problem['Seed'])
    Ppos = problem['Pacman']
    Fpos = problem['Food']
    Gpos = problem['Ghost']
    Board = problem['Board']

    #define game variables
    ROUND_NUM = 0
    TOTAL_SCORE = 0
    PACMAN_WIN_FLAG = False
    GHOST_WIN_FLAG = False

    solution = 'seed: ' + str(Seed) + '\n' + str(ROUND_NUM) + '\n' + printBoard(Board)
    #while the game not reach the end
    while (PACMAN_WIN_FLAG == False and GHOST_WIN_FLAG == False):
        #get Pacman's move direction
        P_direction = P_make_move(Ppos,Fpos, Gpos, Board)
        #update total score
        TOTAL_SCORE = P_check_move(TOTAL_SCORE, Ppos, Fpos, Gpos)
        ROUND_NUM += 1
        #update winning flag
        GHOST_WIN_FLAG, PACMAN_WIN_FLAG = win_check(Ppos, Fpos, Gpos, Board, PACMAN_WIN_FLAG, GHOST_WIN_FLAG)
        #print solution
        solution += str(ROUND_NUM) + ': P moving ' + P_direction + '\n'
        solution += printBoard(Board)
        solution += "score: " + str(TOTAL_SCORE) + '\n'

        # check and print winning situation
        if GHOST_WIN_FLAG == True:
            solution += 'WIN: Ghost'
            winner = 'Ghost'
            break
        elif PACMAN_WIN_FLAG == True:
            solution += 'WIN: Pacman'
            winner = 'Pacman'
            break
        #ghost's turn
        else:
            #obtain ghost's move direction
            W_direction = G_make_move(Gpos, Fpos, Board)
            #update total score
            TOTAL_SCORE = G_check_move(TOTAL_SCORE, Ppos, Gpos)
            ROUND_NUM += 1
            #update winning flag
            GHOST_WIN_FLAG, PACMAN_WIN_FLAG = win_check(Ppos, Fpos, Gpos, Board, PACMAN_WIN_FLAG, GHOST_WIN_FLAG)
            #print solution
            solution += str(ROUND_NUM) + ': W moving ' + W_direction + '\n'
            solution += printBoard(Board)
            solution += "score: " + str(TOTAL_SCORE) + '\n'
            #check win situation and print
            if GHOST_WIN_FLAG == True:
                solution += 'WIN: Ghost'
                winner = 'Ghost'
                break
    return solution, winner

#design a evaluation function
def evaluate(Ppos,Fpos,Gpos,Board):
    #use bfs search to find the closest Ghost distance
    minGdis = ghost_search(Ppos[0],Ppos[1],Gpos,Board)
    #use bfs search to find the closest food distance
    minFdis = food_search(Ppos[0],Ppos[1],Fpos,Board)

    #evaluation function, if pacman meets ghost
    if minGdis == 0:
        value = -float('inf')
    #food is close enough and ghost is not a big threat
    elif minFdis == 0 and minGdis > 1:
        value = float('inf')
    #ghost is a big threat
    elif minGdis <= 1:
        value = -10/minGdis
    #other cases
    else:
        value = -1/minGdis + 5/minFdis
    return value

#search the closest ghost
def ghost_search(start_x,start_y,Gpos,Board):
    #initialize frontier using initial state
    #add none to the end of one level to calculate the depth
    frontier = [(start_x,start_y),None]
    exploredSet = set()
    dis = 0
    while len(frontier) != 0:
        node = frontier.pop(0)
        #if the node is None, add distance by 1
        if node == None:
            dis += 1
            #add one more None to denote it is the end of one level
            frontier.append(None)
            #encountering two Nones means encountering all the nodes
            #it means pacman cannot reach ghost
            if (len(frontier)!=0 and frontier[0] == None):
                dis = float('inf')
                break

        #if reach any of the goal states, then break
        elif node[0] == Gpos['W'][0] and node[1] == Gpos['W'][1]:
            break
        else:
            if node not in exploredSet:
                #add nodes to exploredSet if node is not in exploredSet
                exploredSet.add(node)
                #add child into frontier
                if Board[node[0]-1][node[1]] != '%':
                    frontier.append((node[0]-1,node[1]))
                if Board[node[0]+1][node[1]] != '%':
                    frontier.append((node[0]+1,node[1]))
                if Board[node[0]][node[1]+1] != '%':
                    frontier.append((node[0],node[1]+1))
                if Board[node[0]][node[1]-1] != '%':
                    frontier.append((node[0],node[1]-1))
    return dis

# use bfs search to find the closest food and return the distance to it
def food_search(Px,Py,Fpos,Board):
    #initialize frontier using initial state
    #add none to the end of one level to calculate the depth
    frontier = [(Px,Py),None]
    exploredSet = set()
    dis = 0
    while len(frontier) != 0:
        node = frontier.pop(0)
        if node == None:
            dis += 1
            #add none to the end of one level
            frontier.append(None)
            #encountering two Nones means encountering all the nodes
            #it means cannot reach food
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
                if Board[node[0]-1][node[1]] != '%':
                    frontier.append((node[0]-1,node[1]))
                if Board[node[0]+1][node[1]] != '%':
                    frontier.append((node[0]+1,node[1]))
                if Board[node[0]][node[1]+1] != '%':
                    frontier.append((node[0],node[1]+1))
                if Board[node[0]][node[1]-1] != '%':
                    frontier.append((node[0],node[1]-1))
    return dis

#store available move choice for certain position
def check_available_move(row, col, Board):
    move = []   #list to store available move choice
    if Board[row-1][col] != '%':
        move.append('N')
    if Board[row+1][col] != '%':
        move.append('S')
    if Board[row][col-1] != '%':
        move.append('W')
    if Board[row][col+1] != '%':
        move.append('E')
    move.sort()
    return move

#Pacman make best move according to the evaluation function
def P_make_move(Ppos, Fpos, Gpos, Board):
    #make choice about Pacman's best move direction according to the exptimax function
    available_move = check_available_move(Ppos[0],Ppos[1],Board)
    expectValue = {} # store the move direction and relative evaluate value after move
    direction = ''
    #store the expect value for all avaliable_move and 
    #choose direction which has the largest expect value
    for move in available_move:
        if move == 'E':
            PchangePos = [Ppos[0], Ppos[1]+1]
        elif move == 'W':
            PchangePos = [Ppos[0], Ppos[1]-1]
        elif move == 'N':
            PchangePos = [Ppos[0]-1, Ppos[1]]
        else:
            PchangePos = [Ppos[0]+1, Ppos[1]]
        move_value = evaluate(PchangePos, Fpos, Gpos,Board)
        expectValue[move] = move_value
    #return the direction with the max evaluate value
    for key in expectValue:
        if expectValue[key] == max(expectValue.values()):
            direction = key
    
    Board[Ppos[0]][Ppos[1]] = ' '
    #update the pacman position according to the direction
    if direction == 'E':
        Ppos[1] += 1
    elif direction == 'W':
        Ppos[1] -= 1
    elif direction == 'N':
        Ppos[0] -= 1
    elif direction == 'S':
        Ppos[0] += 1
    #modify board
    Board[Ppos[0]][Ppos[1]] = 'P'
    return direction

#Ghost make move
def G_make_move(Gpos,Fpos,Board):
    avaliable_move = check_available_move(Gpos['W'][0], Gpos['W'][1], Board)
    #check if ghost is blocked
    if avaliable_move == []:
        return ''
    else:
        #make choice about Pacman's move direction
        direction = random.choice(avaliable_move)
        #if the Gposition is orginially a food
        if Gpos['W'] in Fpos:
            Board[Gpos['W'][0]][Gpos['W'][1]] = '.'
        else:
            Board[Gpos['W'][0]][Gpos['W'][1]] = ' '
        #update the pacman position according to the direction
        if direction == 'E':
            Gpos['W'][1] += 1
        elif direction == 'W':
            Gpos['W'][1] -= 1
        elif direction == 'N':
            Gpos['W'][0] -= 1
        elif direction == 'S':
            Gpos['W'][0] += 1
        #modify board
        Board[Gpos['W'][0]][Gpos['W'][1]] = 'W'
        return direction

#check meet what after Pacman move, and calculate the score accordingly
def P_check_move(TOTAL_SCORE, Ppos, Fpos, Gpos):
    EAT_FOOD_SCORE = 10
    PACMAN_EATEN_SCORE = -500
    PACMAN_WIN_SCORE = 500
    PACMAN_MOVING_SCORE = -1
    #check if pacman meets Ghost
    if Ppos == Gpos['W']:
        TOTAL_SCORE += PACMAN_EATEN_SCORE
        TOTAL_SCORE += PACMAN_MOVING_SCORE
    #check if pacman meets food
    elif Ppos in Fpos:
        TOTAL_SCORE += EAT_FOOD_SCORE
        TOTAL_SCORE += PACMAN_MOVING_SCORE
        Fpos.remove(Ppos)
        #check whether Pacman has won
        if Ppos != Gpos['W'] and Fpos == []:
            TOTAL_SCORE += PACMAN_WIN_SCORE
    #pacman meets empty square
    else:
        TOTAL_SCORE += PACMAN_MOVING_SCORE
    #print(TOTAL_SCORE)
    return TOTAL_SCORE

#check meet what after Ghost move
def G_check_move(TOTAL_SCORE, Ppos, Gpos):
    PACMAN_EATEN_SCORE = -500
    #check if pacman meets food
    if Ppos == Gpos['W']:
        TOTAL_SCORE += PACMAN_EATEN_SCORE
    return TOTAL_SCORE

#check if pacman or ghost has won the game
def win_check(Ppos, Fpos, Gpos, Board, PACMAN_WIN_FLAG, GHOST_WIN_FLAG):
    if Ppos == Gpos['W']:   #ghost win
        GHOST_WIN_FLAG = True
        Board[Ppos[0]][Ppos[1]] = 'W'
        Ppos = [0, 0]
    elif Fpos == []:   #pacman win
        PACMAN_WIN_FLAG = True
    return GHOST_WIN_FLAG, PACMAN_WIN_FLAG

#print the whole board
def printBoard(Board):
    Row = len(Board)
    line = ''
    for i in range(Row):
        line += ''.join(Board[i])
        line += '\n'
    return line

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])    
    problem_id = 2
    file_name_problem = str(test_case_id)+'.prob' 
    file_name_sol = str(test_case_id)+'.sol'
    path = os.path.join('test_cases','p'+str(problem_id)) 
    problem = parse.read_layout_problem(os.path.join(path,file_name_problem))
    num_trials = int(sys.argv[2])
    verbose = bool(int(sys.argv[3]))
    print('test_case_id:',test_case_id)
    print('num_trials:',num_trials)
    print('verbose:',verbose)
    start = time.time()
    win_count = 0
    for i in range(num_trials):
        solution, winner = better_play_single_ghosts(copy.deepcopy(problem))
        if winner == 'Pacman':
            win_count += 1
        if verbose:
            print(solution)
    win_p = win_count/num_trials * 100
    end = time.time()
    print('time: ',end - start)
    print('win %',win_p)