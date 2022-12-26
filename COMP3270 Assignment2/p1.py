import sys, random, grader, parse

def random_play_single_ghost(problem):
    #Your p1 code here
    #fetch problem detail
    Seed = int(problem['Seed'])
    Ppos = problem['Pacman']
    Fpos = problem['Food']
    Gpos = problem['Ghost']
    Board = problem['Board']

    #define game variables
    random.seed(Seed, version=1)
    ROUND_NUM = 0
    TOTAL_SCORE = 0
    PACMAN_WIN_FLAG = False
    GHOST_WIN_FLAG = False

    solution = 'seed: ' + str(Seed) + '\n' + str(ROUND_NUM) + '\n' + printBoard(Board)
    #while the game not reach the end
    while (PACMAN_WIN_FLAG == False and GHOST_WIN_FLAG == False):
        #obtain P's move direction
        P_direction = P_make_move(Ppos,Board)
        #update total score
        TOTAL_SCORE = P_check_move(TOTAL_SCORE, Ppos, Fpos, Gpos)
        ROUND_NUM += 1
        #update win flag
        GHOST_WIN_FLAG, PACMAN_WIN_FLAG = win_check(Ppos, Fpos, Gpos, Board, PACMAN_WIN_FLAG, GHOST_WIN_FLAG)
        #print solution
        solution += str(ROUND_NUM) + ': P moving ' + P_direction + '\n'
        solution += printBoard(Board)
        solution += "score: " + str(TOTAL_SCORE) + '\n'
        #print winning situation
        if GHOST_WIN_FLAG == True:
            solution += 'WIN: Ghost'
            break
        elif PACMAN_WIN_FLAG == True:
            solution += 'WIN: Pacman'
            break
        #when it is ghost's turn
        else:
            #obtain ghost's move direction
            W_direction = G_make_move(Gpos, Fpos, Board)
            #update total score
            TOTAL_SCORE = G_check_move(TOTAL_SCORE, Ppos, Gpos)
            ROUND_NUM += 1
            #update winning flag
            GHOST_WIN_FLAG, PACMAN_WIN_FLAG = win_check(Ppos, Fpos, Gpos, Board, PACMAN_WIN_FLAG, GHOST_WIN_FLAG)
            #print
            solution += str(ROUND_NUM) + ': W moving ' + W_direction + '\n'
            solution += printBoard(Board)
            solution += "score: " + str(TOTAL_SCORE) + '\n'
            if GHOST_WIN_FLAG == True:
                solution += 'WIN: Ghost'
                break            
    return solution

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

#Pacman make move
def P_make_move(Ppos, Board):
    #make choice about Pacman's move direction according to the exptimax function
    direction = random.choice(check_available_move(Ppos[0], Ppos[1], Board))
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
    #make choice about Pacman's move direction
    direction = random.choice(check_available_move(Gpos['W'][0], Gpos['W'][1], Board))
    #if the Gposition is orginially a food
    #the board position should print food when ghost moved away
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

#check who wins
def win_check(Ppos, Fpos, Gpos, Board, PACMAN_WIN_FLAG, GHOST_WIN_FLAG):
    if Ppos == Gpos['W']:
        GHOST_WIN_FLAG = True
        Board[Ppos[0]][Ppos[1]] = 'W'
    elif Fpos == []:
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
    problem_id = 1
    grader.grade(problem_id, test_case_id, random_play_single_ghost, parse.read_layout_problem)