''' 
 based on riplpox 
'''

import logging
from copy import copy
from Dijkstras import dijkstraHelperFunction
from Hashed import HashHelperFunction

class Routing(object):
    '''Base class for data center network routing.

    Routing engines must implement the get_route() method.
    '''

    def __init__(self, topo):
        '''Create Routing object.

        @param topo Topo object from Net parent
        '''
        self.topo = topo
        

    def get_route(self, src, dst):
        '''Return flow path.

        @param src source host
        @param dst destination host

        @return flow_path list of DPIDs to traverse (including hosts)
        '''

        raise NotImplementedError

class HashedRouting(Routing):
    ''' Hashed routing '''

    def __init__(self, topo):
        self.topo = topo


    def get_route(self, src, dst):
        ''' Return flow path. '''
        return HashHelperFunction(self.topo,src,dst)

        

class DijkstraRouting(Routing):
    ''' Dijkstra routing '''

    def __init__(self, topo):
        self.topo = topo
        self.count = 0;

    def get_route(self, src, dst):
        ''' Return flow path. '''
        return dijkstraHelperFunction(self.topo,src,dst)

        
