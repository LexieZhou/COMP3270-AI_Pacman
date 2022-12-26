import sys, parse, grader
from heapq import heappush, heappop

def ucs_search(problem):
    #Your p3 code here
    #initialize frontier using initial state
    frontier = []
    heappush(frontier, (0, problem['start_state']))
    exploredSet = []  #actually a list
    while frontier:
        #use heappop, because ucs needs priority queue data structure
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
                    #add costs and nodes relatively
                    #add space to split the child node with the previous node
                    heappush(frontier, (node[0]+child[0], node[1]+' '+child[1]))

    order = ' '.join(exploredSet) + "\n"
    path = ' '.join(node_list)
    solution = order + path
    #solution = 'S D B C\nS C G'
    return solution

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 3
    grader.grade(problem_id, test_case_id, ucs_search, parse.read_graph_search_problem)