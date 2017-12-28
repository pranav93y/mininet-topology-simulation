'''algorithm code is taken from http://www.gilles-bertrand.com/2014/03/disjkstra-algorithm-description-shortest-path-pseudo-code-data-structure-example-image.html'''

def HashHelperFunction(topo,src,dst):
    ''' hash's helper function:

    makes link dictionary without the certain core switches
    calls dijkstras on it

    make a new graph that blocks all 

    '''
    #print 'src: ' + src
    #print 'dst: ' + dst
    topoG = topo.g
    k = topo.k

    # create list of core switches
    core_switch_list = []
    for node in topoG.nodes():
        if(node[0]=='4'):
        	core_switch_list.append(node)
    
    # finds bucket for given src,dst pair
    flowHash = hash(src+dst)
    bucket_num = flowHash%4
    #print 'bucket_num: ' + str(bucket_num)

    graphDic = {} #empty dictionary
    for node in topoG.nodes(): # make empty switch dictionary without unwanted core switches
        if(node[0] =='4'):
            if(node == core_switch_list[bucket_num]):
                graphDic[node] = {}
        else:
            graphDic[node] = {}
    # print graphDic
    for edge in topoG.edges(): # adds each link to each switch
        if(edge[1] in core_switch_list): #found out all core links list coreswitch as second switch in link tuple
            if(edge[1] == core_switch_list[bucket_num]):
                graphDic[edge[0]][edge[1]] = 1
                graphDic[edge[1]][edge[0]] = 1
        else:
            graphDic[edge[0]][edge[1]] = 1
            graphDic[edge[1]][edge[0]] = 1

    # print 'linkDictionary: '
    # print graphDic
    path = HashedDijkstra(graphDic,src,dst,visited=[],distances={},predecessors={})
    #print path
    if path == 0:
        graphDic = {} #empty dictionary
        for node in topoG.nodes(): # make switch dictionary without links
            graphDic[node] = {}
        for edge in topoG.edges(): # adds each link to each switch
            graphDic[edge[0]][edge[1]] = 1
            graphDic[edge[1]][edge[0]] = 1
        path = HashedDijkstra(graphDic,src,dst,visited=[],distances={},predecessors={})
           
    # make dpid list
    dpidPath = []
    for switch in path:
        dpidPath.append(topo.id_gen(name = switch).dpid)
    #print dpidPath

    return path



def HashedDijkstra(graph,src,dest,visited=[],distances={},predecessors={}):
    """ calculates a shortest path tree routed in src
    """    
    # a few sanity checks
    if src not in graph:
        print src
        print graph
        return 0
    if dest not in graph:
        print dest
        print graph
        return 0
    # ending condition

    if src == dest: #if source and destination are the same print out shorest path and exit
        # We build the shortest path and display it
        path=[]
        pred=dest
        while pred != None: # create 
            path.append(pred) # append list path to show the prgevious predecessors
            pred=predecessors.get(pred,None) # get next predecessor and if none return none this breaks the next loop
        #print('shortest path: '+str(tuple(reversed(path)))+" cost="+str(distances[dest])) #print out the path and distances
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
        x=min(unvisited, key=unvisited.get) # get the lowest weighted node 
        return HashedDijkstra(graph,x,dest,visited,distances,predecessors) # run dijkstra's algorithm on cheapest node
                


'''if _name_ == "_main_":
    # testing not possible cause topo object required

    graph = {'s': {'a': 2, 'b': 1},
            'a': {'s': 3, 'b': 4, 'c':8},
            'b': {'s': 4, 'a': 2, 'd': 2},
            'c': {'a': 2, 'd': 7, 't': 4},
            'd': {'b': 1, 'c': 11, 't': 5},
            't': {'c': 3, 'd': 5}}'''


