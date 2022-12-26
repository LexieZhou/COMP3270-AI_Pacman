import sys, parse, grader
from heapq import heappush, heappop

def greedy_search(problem):
    #Your p4 code here
    #initialize frontier using initial state
    frontier = []
    start_state = problem['start_state']
    heappush(frontier, (problem['heuristics'][start_state], start_state))
    exploredSet = []  #actually a list
    while frontier:
        #use heappop, because greedy search needs priority queue data structure
        node = heappop(frontier)
        #split each node apart and store them into a list
        node_list = node[-1].split(' ')
        #if reach any of the goal states, then break
        if (node_list[-1] in problem['goal_states']):
            break
        if (node_list[-1] not in exploredSet):
            #add nodes to exploredSet if node is not in exploredSet
            exploredSet.append(node_list[-1])
            #if the frontier has child (the frontier is in the 'graph' dictionary)
            if node_list[-1] in problem['graph']:
                for child in problem['graph'][node_list[-1]]:
                    #add heuristics and nodes relatively
                    #add space to split the child node with the previous node
                    heappush(frontier, (problem['heuristics'][child[1]], node[1]+' '+child[1]))

    order = ' '.join(exploredSet) + "\n"
    path = ' '.join(node_list)
    solution = order + path
    #solution = 'S B D C\nS C G'
    return solution

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 4
    grader.grade(problem_id, test_case_id, greedy_search, parse.read_graph_search_problem)