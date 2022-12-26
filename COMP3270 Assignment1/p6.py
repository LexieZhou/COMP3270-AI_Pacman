import sys, parse, grader

def number_of_attacks(problem):
    #Your p6 code here
    row_num = problem['row']
    column_num = 8
    queen = problem['queen']

    #function to detect whether there is attack in the row
    def row_detect(q1, q2):
        row_attack = 0
        if q1[1] == q2[1]:   #has the same row number
            row_attack += 1
        return row_attack

    #function to detect whether there is attack in the diagonal direction
    def diagonal_detect(q1, q2):
        diagonal_attack = 0
        if abs(q1[0] - q2[0]) == abs(q1[1] - q2[1]):   #in the diagonal direction
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


    solution = ''
    row_sol_list = []
    for i in range(row_num):
        row_sol = ''
        #for a certain row, detect the attack number column by column
        for j in range(column_num):
            #add the square_attack number and add a space
            if len(str(square_detect(i, j))) == 1:
                #normalize the format to two characters if the attack number has only 1 digit
                square_sol = ' '+str(square_detect(i, j))
            else:
                square_sol = str(square_detect(i,j))
            row_sol += square_sol + ' '
        row_sol_list.append(row_sol)
    
    for k in range(len(row_sol_list)-1):
        solution += row_sol_list[k][:-1] + '\n'
    #add the last line
    solution += row_sol_list[-1][:-1]

#     solution = """18 12 14 13 13 12 14 14
# 14 16 13 15 12 14 12 16
# 14 12 18 13 15 12 14 14
# 15 14 14 17 13 16 13 16
# 17 14 17 15 17 14 16 16
# 17 17 16 18 15 17 15 17
# 18 14 17 15 15 14 17 16
# 14 14 13 17 12 14 12 18"""
    return solution

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 6
    grader.grade(problem_id, test_case_id, number_of_attacks, parse.read_8queens_search_problem)