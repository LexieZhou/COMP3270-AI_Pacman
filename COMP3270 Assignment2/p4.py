import sys, parse
import time, os, copy
import random

def better_play_mulitple_ghosts(problem):
    #Your p4 code here
    Seed = int(problem['Seed'])
    Ppos = problem['Pacman']
    Fpos = problem['Food']
    Gpos = problem['Ghost'] #Ghosts, W, X, Y, Z
    Board = problem['Board']
    Gpos_sequence_all = ['W','X','Y','Z']
    Gpos_sequence = Gpos_sequence_all[:len(Gpos)]

    #define game variables
    ROUND_NUM = 0
    TOTAL_SCORE = 0
    PACMAN_WIN_FLAG = False
    GHOST_WIN_FLAG = False
    solution = ''
    winner = ''

    solution = 'seed: ' + str(Seed) + '\n' + str(ROUND_NUM) + '\n' + printBoard(Board)
    while (PACMAN_WIN_FLAG == False and GHOST_WIN_FLAG == False):
        #return pacman's move direction
        P_direction = P_make_move(Ppos,Fpos, Gpos, Board)
        #update total score
        TOTAL_SCORE = P_check_move(TOTAL_SCORE, Ppos, Fpos, Gpos)
        ROUND_NUM += 1
        #update win flag
        GHOST_WIN_FLAG, PACMAN_WIN_FLAG = win_check(Ppos, Fpos, Gpos, Board, PACMAN_WIN_FLAG, GHOST_WIN_FLAG)
        #print solution
        solution += str(ROUND_NUM) + ': P moving ' + P_direction + '\n'
        solution += printBoard(Board)
        solution += "score: " + str(TOTAL_SCORE) + '\n'
        #check winning situation and print
        if GHOST_WIN_FLAG == True:
            solution += 'WIN: Ghost'
            winner = 'Ghost'
            break
        elif PACMAN_WIN_FLAG == True:
            solution += 'WIN: Pacman'
            winner = 'Pacman'
            break
        else:
            #ghost's turn
            direction = ''
            for G in Gpos_sequence:
                #return ghost's direction
                direction = G_make_move(G, Gpos, Fpos, Board)
                #update total score
                TOTAL_SCORE = G_check_move(TOTAL_SCORE, Ppos, Gpos)
                ROUND_NUM += 1
                #update win flag
                GHOST_WIN_FLAG, PACMAN_WIN_FLAG = win_check(Ppos, Fpos, Gpos, Board, PACMAN_WIN_FLAG, GHOST_WIN_FLAG)
                #print soluton
                solution += str(ROUND_NUM) + ': ' + G + ' moving ' + direction + '\n'
                solution += printBoard(Board)
                solution += "score: " + str(TOTAL_SCORE) + '\n'
                #check win situation and print
                if GHOST_WIN_FLAG == True:
                    solution += 'WIN: Ghost'
                    break
    return solution, winner

#design a evaluation function
def evaluate(Ppos,Fpos,Gpos,Board):
    #use bfs search to find the distance to the closest Ghost
    minGdis = ghost_search(Ppos[0],Ppos[1],Gpos,Board)
    #use bfs search to find the distance to the closest food
    minFdis = food_search(Ppos[0],Ppos[1],Fpos,Board)

    #evaluation function
    #if ghost is at the position
    if minGdis == 0:
        value = -float('inf')
    #if food is close enough and ghost is not a big threat
    elif minFdis == 0 and minGdis > 1:
        value = float('inf')
    #if ghost is a serious threat
    elif minGdis <= 1:
        value = -10/minGdis
    #other cases
    else:
        value = -1/minGdis + 1/minFdis
    return value

#use bfs search to find the closest ghost and return the distance
def ghost_search(start_x,start_y,Gpos,Board):
    Gpos_list = []  #store Ghost positions
    for G in Gpos:
        Gpos_list.append((Gpos[G][0],Gpos[G][1]))
    #initialize frontier using initial state
    #add none to the end of one level to calculate the depth
    frontier = [(start_x,start_y),None]
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

#search for the closest food and return the distance to it
def food_search(Px,Py,Fpos,Board):
    #initialize frontier using initial state
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
            #it means pacman cannot reach the food
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

#store available move choice for Pacman's certain position
def P_check_available_move(row, col, Board):
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

#store available move choice for certain Ghost's position
def G_check_available_move(row, col, Board, Gpos):
    move = []   #list to store available move choice
    if Board[row-1][col] != '%' and Board[row-1][col] not in Gpos:
        move.append('N')
    if Board[row+1][col] != '%'and Board[row+1][col] not in Gpos:
        move.append('S')
    if Board[row][col-1] != '%'and Board[row][col-1] not in Gpos:
        move.append('W')
    if Board[row][col+1] != '%'and Board[row][col+1] not in Gpos:
        move.append('E')
    move.sort()
    return move

#Pacman make move
def P_make_move(Ppos, Fpos, Gpos, Board):
    #make choice about Pacman's best move direction according to the exptimax function
    available_move = P_check_available_move(Ppos[0],Ppos[1],Board)
    #store the moves and relative evaluate values
    expectValue = {}
    direction = ''
    #store the expect value for all avaliable_move and 
    #choose direction which has the largest evaluate value
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
    #set direction to the move that reach the max evaluate value
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
def G_make_move(G,Gpos,Fpos,Board):
    direction = ''
    move_choice = G_check_available_move(Gpos[G][0], Gpos[G][1], Board, Gpos)
    #check if the Ghost is stucked, if not, then move
    if move_choice == []:
        return ''
    else:
        #make choice about Pacman's move direction
        direction = random.choice(move_choice)
        #if the Gposition is orginially a food
        if Gpos[G] in Fpos:
            Board[Gpos[G][0]][Gpos[G][1]] = '.'
        else:
            Board[Gpos[G][0]][Gpos[G][1]] = ' '
        
        #update the pacman position according to the direction
        if direction == 'E':
            Gpos[G][1] += 1
        elif direction == 'W':
            Gpos[G][1] -= 1
        elif direction == 'N':
            Gpos[G][0] -= 1
        elif direction == 'S':
            Gpos[G][0] += 1
        #modify board
        Board[Gpos[G][0]][Gpos[G][1]] = G
    #print(G, direction)
    return direction

#check meet what after Pacman move, and calculate the score accordingly
def P_check_move(TOTAL_SCORE, Ppos, Fpos, Gpos):
    EAT_FOOD_SCORE = 10
    PACMAN_EATEN_SCORE = -500
    PACMAN_WIN_SCORE = 500
    PACMAN_MOVING_SCORE = -1
    MEET_GHOST_FLAG = False
    #check if pacman meets Ghost
    for G in Gpos:
        if Ppos == Gpos[G]:
            TOTAL_SCORE += PACMAN_EATEN_SCORE
            TOTAL_SCORE += PACMAN_MOVING_SCORE
            MEET_GHOST_FLAG = True
    #if not meet ghost, check whether meet food
    if MEET_GHOST_FLAG == False and Ppos in Fpos:
        TOTAL_SCORE += EAT_FOOD_SCORE
        TOTAL_SCORE += PACMAN_MOVING_SCORE
        Fpos.remove(Ppos)
        #check whether Pacman has won
        if Fpos == []:
            TOTAL_SCORE += PACMAN_WIN_SCORE
    #pacman meets empty square
    elif MEET_GHOST_FLAG == False:
        TOTAL_SCORE += PACMAN_MOVING_SCORE
    return TOTAL_SCORE

#check meet what after Ghost move
def G_check_move(TOTAL_SCORE, Ppos, Gpos):
    PACMAN_EATEN_SCORE = -500
    for G in Gpos:
        if Ppos == Gpos[G]:
            TOTAL_SCORE += PACMAN_EATEN_SCORE
            break
    return TOTAL_SCORE

#check who wins
def win_check(Ppos, Fpos, Gpos, Board, PACMAN_WIN_FLAG, GHOST_WIN_FLAG):
    for G in Gpos:
        if Ppos == Gpos[G]:
            GHOST_WIN_FLAG = True
            Board[Ppos[0]][Ppos[1]] = G
    if GHOST_WIN_FLAG == False and Fpos == []:
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
    problem_id = 4
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
        solution, winner = better_play_mulitple_ghosts(copy.deepcopy(problem))
        if winner == 'Pacman':
            win_count += 1
        if verbose:
            print(solution)
    win_p = win_count/num_trials * 100
    end = time.time()
    print('time: ',end - start)
    print('win %',win_p)