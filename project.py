class IllegalCube(Exception):
    pass

# Since there are ~3.6 million (3,674,160) possible permutations, performance is crucial.
# Best performing Breadth-first search algorithm from https://stackoverflow.com/a/50575971
# Non-recursive since recursion ran slower. The following still keeps track of visited vertices.
def breadthFirst(graph, start, end):
    """
    Breadth-first search algorithm to find the shortest path from the solved cube to the instance.

    :param: graph: cube group where edges are cubes related via a quater turn
    :param: start: solved cube
    :param: end: instance cube
    :returns: smallest list of vertices from the graph (cubes)
    """

    queue = [(start,[start])]
    visited = set()

    print("Performing a Breadth-first search traversal...\n")

    while queue:
        vertex, path = queue.pop(0)
        visited.add(vertex)

        for node in graph[vertex]:
            if node == end: return path + [end]
            elif node not in visited:
                    visited.add(node)
                    queue.append((node, path + [node]))



def solution(instance):
    """
    Generates a Cayley graph starting with the solved cube and stops at the instance. 
    Depends on the 'breadthFirst()' to find the shortest path aka the minimum steps to solve.

    :param instance: the cube to solve
    :returns: list of steps as cubes encoded as strings
    """

    solvedCube = "WWWWGGGGRRRRBBBBOOOOYYYY" # Solved instance
    instance = instance.upper()             # Capitalise to make function case-insensitive

    # The 6 legal quarter turns rather than 12 as half the moves are redundent,
    # this is because we don't care about the orientation of the cube
    legalMoves = [[0,1,7,5,4,20,6,21,10,8,11,9,2,13,3,15,16,17,18,19,14,12,22,23],  # U    up clockwise
        [0,1,12,14,4,3,6,2,9,11,8,10,21,13,20,15,16,17,18,19,5,7,22,23],            # U'   up anti-clockwise
        [0,1,2,3,4,5,18,19,8,9,6,7,12,13,10,11,16,17,14,15,22,20,23,21],            # F    front clockwise
        [0,1,2,3,4,5,10,11,8,9,14,15,12,13,18,19,16,17,6,7,21,23,20,22],            # F'   front anti-clockwise
        [0,9,2,11,4,5,6,7,8,21,10,23,14,12,15,13,3,17,1,19,20,18,22,16],            # R    right clockwise
        [0,18,2,16,4,5,6,7,8,1,10,3,13,15,12,14,23,17,21,19,20,9,22,11]]            # R'   right anti-clockwise

    # Rotating the whole cube in 3D space (each face takes a turn being on top)
    six = [[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23],
        [12,13,14,15,9,11,8,10,21,23,20,22,18,16,19,17,1,0,3,2,7,6,5,4],
        [8,9,10,11,5,7,4,6,20,21,22,23,14,12,15,13,3,2,1,0,19,18,17,16],
        [20,21,22,23,7,6,5,4,19,18,17,16,15,14,13,12,9,8,11,10,0,1,2,3],
        [4,5,6,7,17,19,16,18,22,20,23,21,10,8,11,9,2,0,3,1,15,14,13,12],
        [16,17,18,19,13,15,12,14,23,22,21,20,6,4,7,5,0,1,2,3,11,10,9,8]]

    # Spinning the whole cube keeping the same face down (turn 90degree clockwise four times)
    four = [[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23],
        [2,0,3,1,8,9,10,11,12,13,14,15,16,17,18,19,4,5,6,7,21,23,20,22],
        [3,2,1,0,12,13,14,15,16,17,18,19,4,5,6,7,8,9,10,11,23,22,21,20],
        [1,3,0,2,16,17,18,19,4,5,6,7,8,9,10,11,12,13,14,15,22,20,23,21]]

    # Check early to see if the instance is encoded properly, if not, throw exception
    if not sorted(solvedCube) == sorted(instance): raise IllegalCube(instance)
    
    # Check early to see if the cube is already solved, if so, stop here to save memory
    if solvedCube == instance: return [solvedCube]

    # To allow ultimate flexibility for user inputs, the instance may be in any orientation.
    # Therefore, store all 24 possible orientations of the instance so its position can be ignored
    instancePositions = set()
    for rot in range(0,len(six)):
        newOrientation = ''.join([instance[i] for i in six[rot]])
        [instancePositions.add(''.join([newOrientation[i] for i in four[spin]])) for spin in range(0, len(four))]

    graph = dict()          # Adjacency list (keys are vertices (cubes) and values are edges (cubes related by transforming to one-another with a quarter turn))
    neighbours = list()     # Neighbour cubes for a parent cube, will be added to the graph (dictionary) with the parent cube as the key and the neighbours as the values
    toRotate = {solvedCube} # Queue of parent cubes to rotate (starts off with the solved cube)
    temporary = set()       # New neighbour cubes to be rotated next (as parent cubes)

    print("\nGenerating Pocket cube group graph...\n")

    while not instancePositions.intersection(graph):
        
        for cube in toRotate:
            for move in range(0,len(legalMoves)):
                # Generate neighbours
                newCube = ''.join([cube[i] for i in legalMoves[move]])
                neighbours.append(newCube)
                
            temporary.update(neighbours) # Store neighbours to be rotated next round
            graph[cube] = neighbours     # Add neighbours to the graph
            neighbours = list()          # Reset

            # If any orientation of the instance is found in the graph, do a Breadth-first search
            # to get a list of the cubes (vertices) that forms the shortest path.
            # Return the list as it provides the minimum number of steps to solve the instance.
            for instance in instancePositions:
                if instance in graph:
                    print("Found instance after {:,} permutations\n".format(len(graph)))
                    shortestPath = (breadthFirst(graph, solvedCube, instance)) 
                    return shortestPath

        toRotate = temporary # Transfer the new permutations to be rotated next
        temporary = set()    # Reset for the next set of new permutations



def printSolution(solution):
    """
    Prints the minimum number of steps to solve your cube.

    :param solution: list of steps as cubes encoded as strings
    :returns: message for the minimum number of steps
    """

    steps = len(solution) - 1 # minus 1 as there are no steps to get to the solved cube
    
    print("Steps to solve your cube:\n")

    # Reverse to show steps from instance to solved cube, rather than solved cube to instance
    for step in reversed(solution):
        print("\
    "+step[0]+step[1]+"\n\
    "+step[2]+step[3]+"\n\
"+step[6]+step[7]+" "+step[10]+step[11]+" "+step[14]+step[15]+" "+step[4]+step[5]+"\n\
"+step[8]+step[9]+" "+step[12]+step[13]+" "+step[16]+step[17]+" "+step[18]+step[19]+"\n\
    "+step[20]+step[21]+"\n\
    "+step[22]+step[23]+"\n")
    
    # Check grammar
    grammar = "are {0} steps!\n".format(steps)
    if (steps == 1): grammar = "is 1 step!\n"
    print("Minimum number of steps needed " + grammar)

print("\nRun main.py\n")
