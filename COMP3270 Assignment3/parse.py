#debug code
import os, sys

def read_grid_mdp_problem_p1(file_path):
    #Your p1 code here
    problem = []
    with open(file_path) as f:
        lines = f.readlines()
    #obtain the seed,noise and livingReward
    seed = lines[0].split(' ')[-1][:-1]
    noise = lines[1].split(' ')[-1][:-1]
    livingReward = lines[2].split(' ')[-1][:-1]
    problem.append(int(seed))
    problem.append(float(noise))
    problem.append(float(livingReward))

    #obtain grid and policy
    grid = []
    policy = []
    line_num = 4
    while lines[line_num][:-1] != "policy:":
        grid.append(lines[line_num].strip().split())
        line_num += 1
    line_num += 1
    while line_num < len(lines):
        policy.append(lines[line_num].strip().split())
        line_num += 1
    problem.append(grid)
    problem.append(policy)

    #obtain initial agent position
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == 'S':
                problem.append([i,j])

    return problem

def read_grid_mdp_problem_p2(file_path):
    #Your p2 code here
    problem = ''
    problem = []
    with open(file_path) as f:
        lines = f.readlines()
    #obtain the discount,noiss, livingReward, and iterations
    discount = lines[0].split(' ')[-1][:-1]
    noise = lines[1].split(' ')[-1][:-1]
    livingReward = lines[2].split(' ')[-1][:-1]
    iterations = lines[3].split(' ')[-1][:-1]
    problem.append(float(discount))
    problem.append(float(noise))
    problem.append(float(livingReward))
    problem.append(int(iterations))

    #obtain grid and policy
    grid = []
    policy = []
    line_num = 5
    while lines[line_num][:-1] != "policy:":
        grid.append(lines[line_num].strip().split())
        line_num += 1
    line_num += 1
    while line_num < len(lines):
        policy.append(lines[line_num].strip().split())
        line_num += 1
    problem.append(grid)
    problem.append(policy)

    #obtain initial agent position
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == 'S':
                problem.append([i,j])

    return problem

def read_grid_mdp_problem_p3(file_path):
    #Your p3 code here
    problem = ''
    problem = []
    with open(file_path) as f:
        lines = f.readlines()
    #obtain the discount,noiss, livingReward, and iterations
    discount = lines[0].split(' ')[-1][:-1]
    noise = lines[1].split(' ')[-1][:-1]
    livingReward = lines[2].split(' ')[-1][:-1]
    iterations = lines[3].split(' ')[-1][:-1]
    problem.append(float(discount))
    problem.append(float(noise))
    problem.append(float(livingReward))
    problem.append(int(iterations))

    #obtain grid and policy
    grid = []
    line_num = 5
    while line_num < len(lines):
        grid.append(lines[line_num].strip().split())
        line_num += 1
    problem.append(grid)

    #obtain initial agent position
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == 'S':
                problem.append([i,j])

    return problem

#debug code
if __name__ == "__main__":
    if len(sys.argv) == 3:
        problem_id, test_case_id = sys.argv[1], sys.argv[2]
        problem = read_grid_mdp_problem_p3(os.path.join('test_cases','p'+problem_id, test_case_id+'.prob'))
        print(problem)
    else:
        print('Error: I need exactly 2 arguments!')