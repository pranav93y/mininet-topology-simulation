'''algorithm code is taken from http://www.gilles-bertrand.com/2014/03/disjkstra-algorithm-description-shortest-path-pseudo-code-data-structure-example-image.html'''

def dijkstraHelperFunction(topo,src,dst):
    ''' dijkstra's helper function:

    makes link dictionary
    calls dijkstras on it

    '''


    topoG = topo.g

    graphDic = {} #empty dictionary
    for node in topoG.nodes(): # make switch dictionary without links
        graphDic[node] = {}
    for edge in topoG.edges(): # adds each link to each switch
        graphDic[edge[0]][edge[1]] = 1
        graphDic[edge[1]][edge[0]] = 1

    path = dijkstra(graphDic,src,dst,visited=[],distances={},predecessors={})

    dpidPath = []
    for switch in path:
        dpidPath.append(topo.id_gen(name = switch).dpid)

    return path



def dijkstra(graph,src,dest,visited=[],distances={},predecessors={}):
    """ calculates a shortest path tree routed in src
    """    
    # a few sanity checks
    if src not in graph:
        raise TypeError('The root of the shortest path tree cannot be found')
    if dest not in graph:
        raise TypeError('The target of the shortest path cannot be found')    
    # ending condition
    if src == dest: #if source and destination are the same print out shorest path and exit
        # We build the shortest path and display it
        path=[]
        pred=dest
        while pred != None: # create 
            path.append(pred) # append list path to show the prgevious predecessors
            pred=predecessors.get(pred,None) # get next predecessor and if none return none this breaks the next loop
        return tuple(reversed(path))

    else :     
        # if it is the initial  run, initializes the cost
        if not visited: #this sets the source destination to 0 once because visited list
            distances[src]=0
        # visit the neighbors
        for neighbor in graph[src] : #each neighbor for the new starting node
            if neighbor not in visited: # if the neighbor hasnt been visited, check for new better paths
                new_distance = distances[src] + graph[src][neighbor] # create new weight for this new node + weight of source node
                if new_distance < distances.get(neighbor,float('inf')): # if new distance is less than the neightbor weight(if no weight assume infinity)
                    distances[neighbor] = new_distance #set distances of this new neighboring node to the new distance
                    predecessors[neighbor] = src #set the predecessors of this new neighbor to the "current node"
        # mark as visited
        visited.append(src) # add "current node" to visited

        # now that all neighbors have been visited: recurse                         
        # select the non visited node with lowest distance 'x'
        # run Dijskstra with src='x'
        unvisited={} # create unvisited dictionary
        for k in graph: # for each node
            if k not in visited: #if node is not in visited,
                unvisited[k] = distances.get(k,float('inf')) # add the weigths of every unvisited node
        x=0
        x=min(unvisited, key=unvisited.get) # get the lowest weighted node 
        return dijkstra(graph,x,dest,visited,distances,predecessors) # run dijkstra's algorithm on cheapest node
 


'''if __name__ == "__main__":
# testing not possible cause topo object required

    graph = {'s': {'a': 2, 'b': 1},
            'a': {'s': 3, 'b': 4, 'c':8},
            'b': {'s': 4, 'a': 2, 'd': 2},
            'c': {'a': 2, 'd': 7, 't': 4},
            'd': {'b': 1, 'c': 11, 't': 5},
            't': {'c': 3, 'd': 5}}'''

