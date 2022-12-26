import sys, grader, parse
import collections

def bfs_search(problem):
    #Your p2 code here
    #initialize frontier using initial state
    frontier = collections.deque([problem['start_state']])
    exploredSet = []  #actually a list
    while frontier:
        #use popleft instead of pop, because bfs needs queue data structure (FIFO)
        node = frontier.popleft()
        #split each node apart and store them into a list
        node_list = node.split(' ')
        #if reach any of the goal states, then break
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
    #solution = 'Ar B C D\nAr C G'
    return solution

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 2
    grader.grade(problem_id, test_case_id, bfs_search, parse.read_graph_search_problem)