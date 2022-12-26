import sys, grader, parse
import random

def random_play_multiple_ghosts(problem):
    #Your p3 code here
    #fetch problem detail
    Seed = int(problem['Seed'])
    Ppos = problem['Pacman']
    Fpos = problem['Food']
    Gpos = problem['Ghost'] #Ghosts, W, X, Y, Z
    Board = problem['Board']
    Gpos_sequence_all = ['W','X','Y','Z']
    Gpos_sequence = Gpos_sequence_all[:len(Gpos)]   #store all the ghost in current problem


    #define game variables
    random.seed(Seed, version=1)
    ROUND_NUM = 0
    TOTAL_SCORE = 0
    PACMAN_WIN_FLAG = False
    GHOST_WIN_FLAG = False

    solution = 'seed: ' + str(Seed) + '\n' + str(ROUND_NUM) + '\n' + printBoard(Board)
    while (PACMAN_WIN_FLAG == False and GHOST_WIN_FLAG == False):
        #return the pacman's move direction
        P_direction = P_make_move(Ppos,Board)
        #update total score
        TOTAL_SCORE = P_check_move(TOTAL_SCORE, Ppos, Fpos, Gpos)
        ROUND_NUM += 1
        #update win flag
        GHOST_WIN_FLAG, PACMAN_WIN_FLAG = win_check(Ppos, Fpos, Gpos, Board, PACMAN_WIN_FLAG, GHOST_WIN_FLAG)
        #print
        solution += str(ROUND_NUM) + ': P moving ' + P_direction + '\n'
        solution += printBoard(Board)
        solution += "score: " + str(TOTAL_SCORE) + '\n'
        #check winning situation
        if GHOST_WIN_FLAG == True:
            solution += 'WIN: Ghost'
            break
        elif PACMAN_WIN_FLAG == True:
            solution += 'WIN: Pacman'
            break
        else:
            direction = ''
            for G in Gpos_sequence:
                #return ghost move direction
                direction = G_make_move(G, Gpos, Fpos, Board)
                #update total score
                TOTAL_SCORE = G_check_move(TOTAL_SCORE, Ppos, Gpos)
                ROUND_NUM += 1
                #update win flag
                GHOST_WIN_FLAG, PACMAN_WIN_FLAG = win_check(Ppos, Fpos, Gpos, Board, PACMAN_WIN_FLAG, GHOST_WIN_FLAG)
                #print solution
                solution += str(ROUND_NUM) + ': ' + G + ' moving ' + direction + '\n'
                solution += printBoard(Board)
                solution += "score: " + str(TOTAL_SCORE) + '\n'
                #check winning situation and print
                if GHOST_WIN_FLAG == True:
                    solution += 'WIN: Ghost'
                    break
    #solution = ''
    return solution

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
def P_make_move(Ppos, Board):
    #make choice about Pacman's move direction according to the exptimax function
    direction = random.choice(P_check_available_move(Ppos[0], Ppos[1], Board))
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
    if move_choice != []:
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
    for G in Gpos:     #if ghost win
        if Ppos == Gpos[G]:
            GHOST_WIN_FLAG = True
            Board[Ppos[0]][Ppos[1]] = G
    if GHOST_WIN_FLAG == False and Fpos == []:   #if pacman win
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
    problem_id = 3
    grader.grade(problem_id, test_case_id, random_play_multiple_ghosts, parse.read_layout_problem)