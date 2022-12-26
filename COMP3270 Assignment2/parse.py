import os, sys
def read_layout_problem(file_path):
    #Your p1 code here
    #problem = ''
    #define problem as a dictionary to store the seed num, position of pacman, food, ghosts
    problem = {}
    problem['Food'] = []
    problem['Ghost'] = {}

    #read the problem line by line
    with open(file_path) as f:
        lines = f.readlines()
    #obtain the seed number and deleting the new line sign
    seed = lines[0].split(' ')[-1][:-1]     #seed type is str
    problem['Seed'] = seed

    #obtain other positions
    for i in range(1,len(lines)-1):
        for j in range(len(lines[-1])):  #the length of one line
            if lines[i][j] == 'P':
                problem['Pacman'] = [i-1, j]
            elif lines[i][j] == '.':
                problem['Food'].append([i-1, j])
            elif lines[i][j] == 'W':
                problem['Ghost']['W'] = [i-1, j]
            elif lines[i][j] == 'X':
                problem['Ghost']['X'] = [i-1, j]
            elif lines[i][j] == 'Y':
                problem['Ghost']['Y'] = [i-1, j]
            elif lines[i][j] == 'Z':
                problem['Ghost']['Z'] = [i-1, j]

    problem['Board'] = []
    #delete the last new line sign
    for i in range(1, len(lines)-1):
        lines[i] = lines[i][:-1].strip()
        problem['Board'].append(list(lines[i]))
    problem['Board'].append(list(lines[len(lines)-1]))
    
    return problem

if __name__ == "__main__":
    if len(sys.argv) == 3:
        problem_id, test_case_id = sys.argv[1], sys.argv[2]
        problem = read_layout_problem(os.path.join('test_cases','p'+problem_id, test_case_id+'.prob'))
        print(problem)
    else:
        print('Error: I need exactly 2 arguments!')