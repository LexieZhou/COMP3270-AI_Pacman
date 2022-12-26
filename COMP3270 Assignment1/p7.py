import sys, parse, grader
from p6 import number_of_attacks

def better_board(problem):
    #Your p7 code here
    row_num = problem['row']
    column_num = 8
    queen = problem['queen']

    #function to detect the attack number in row
    def row_detect(q1, q2):
        row_attack = 0
        if q1[1] == q2[1]:
            row_attack += 1
        return row_attack

    #function to detect the attack number in diagonal direction
    def diagonal_detect(q1, q2):
        diagonal_attack = 0
        if abs(q1[0] - q2[0]) == abs(q1[1] - q2[1]):    #in the diagonal direction
            diagonal_attack += 1
        return diagonal_attack

    #function to calculate the sum of attack number for a certain square position
    def square_detect(row, column):
        #build queen_adjust
        #queen_adjust includes current square position and other queens
        #excludes the queen in the same column
        queen_adjust = [[column, row]]
        for i in range(len(queen)):
            #exclude the queen in the same column (already being removed)
            if queen[i][0] != column:
                queen_adjust.append(queen[i])
        
        square_sol = 0
        for m in range(len(queen_adjust)-1):
            #q2 must be in the right of q1 to ensure there is no replicate
            for n in range(m+1, len(queen_adjust)):    
                #add the row_attack
                square_sol += row_detect(queen_adjust[m], queen_adjust[n])
                #add the diagonal_attack
                square_sol += diagonal_detect(queen_adjust[m], queen_adjust[n])
        return square_sol

    #create a list to store the solution for each square of each column
    col_sol_list = []
    for n in range(column_num):
        #create an initialized empty list for each column
        col_sol_list.append([])
        for m in range(row_num):
            #add each square's number of attack
            col_sol_list[n].append(square_detect(m,n))
    
    #create a list to store the min solution value for each column
    min_col_sol = []
    for k in range(column_num):
        for g in range(row_num):
            #find the min cost value for each column
            if col_sol_list[k][g] == min(col_sol_list[k]):
                #store [row number, attack_number] for the min attack number square position in this column
                min_col_sol.append([g, int(col_sol_list[k][g])]) 
                break
    
    #find the min cost value for all the columns
    min_sol_list = []
    for k in range(len(min_col_sol)):
        min_sol_list.append(min_col_sol[k][1])
    min_cost = min(min_sol_list)

    #return the first value from the upper left that has the minimum cost
    for g in range(len(min_col_sol)):
        if min_col_sol[g][1] == min_cost:
            q_later_row = min_col_sol[g][0]
            q_later_column = g
            break
    
    #store the final queen position into the list
    queen_position = [[q_later_column, q_later_row]]
    for i in range(len(queen)):
        #store other queens
        #exclude the queen in the same column (already being removed)
        if queen[i][0] != q_later_column:
            queen_position.append(queen[i])

    #build the final queen board
    solution = ''
    for m in range(row_num):
        row_board = ''
        for n in range(column_num):
            #for the final queen position, add as a 'q'
            if [n, m] in queen_position:
                row_board += 'q '
            else:
                row_board += '. '
        #delete the space in the end and add a new line
        solution += row_board[: -1] + '\n'
    #delete the new line in the end for the last line
    solution = solution[:-1]

#     solution = """. q . . . . . .
# . . . . . . . .
# . . . . . . . .
# . . . q . . . .
# q . . . q . . .
# . . . . . q . q
# . . q . . . q .
# . . . . . . . ."""
    return solution

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 7
    grader.grade(problem_id, test_case_id, better_board, parse.read_8queens_search_problem)