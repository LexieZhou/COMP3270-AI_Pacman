import sys, grader, parse
import collections

def dfs_search(problem):
    #Your p1 code here
    #initialize frontier using initial state
    frontier = collections.deque([problem['start_state']])
    #create a list to store the explored nodes
    exploredSet = []  
    while frontier:
        node = frontier.pop()
        #split each node apart and store them into a node list
        node_list = node.split(' ')
        #if reach any goal state in the goal states list, then break
        if (node_list[-1] in problem['goal_states']):    
            break
        if (node_list[-1] not in exploredSet):
            #add nodes to exploredSet if node is not in exploredSet
            exploredSet.append(node_list[-1])
            #if the frontier has child (the frontier is in the 'graph' dictionary)
            if node_list[-1] in problem['graph']:
                for child in problem['graph'][node_list[-1]]:
                    #child[-1] is the child node, and add space to split the child node with the previous node
                    frontier.append(node+' '+child[-1])

    #store the exploration order
    order = ' '.join(exploredSet) + '\n'
    #store the solution path
    path = ' '.join(node_list)

    solution = order + path
    #solution = 'Ar D C\nAr C G'
    return solution

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 1
    grader.grade(problem_id, test_case_id, dfs_search, parse.read_graph_search_problem)