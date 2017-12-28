#!/usr/bin/python

'''
Fat tree topology for data center networking

 based on riplpox 
'''

from mininet.topo import Topo


class FatTreeNode(object):
    def __init__(self, pod = 0, sw = 0, host = 0, dpid = None, name = None):
        '''Create FatTreeNodeID object from custom params.

        Either (pod, sw, host) or dpid must be passed in.

        @param pod pod ID
        @param sw switch ID
        @param host host ID
        @param dpid optional dpid
        @param name optional name
        '''
        if dpid:
            self.pod = (dpid & 0xff0000) >> 16
            self.sw = (dpid & 0xff00) >> 8
            self.host = (dpid & 0xff)
            self.dpid = dpid
        elif name:
            pod, sw, host = [int(s) for s in name.split('_')]
            self.pod = pod
            self.sw = sw
            self.host = host
            self.dpid = (pod << 16) + (sw << 8) + host
        else:
            self.pod = pod
            self.sw = sw
            self.host = host
            self.dpid = (pod << 16) + (sw << 8) + host

    def __str__(self):
        return "(%i, %i, %i)" % (self.pod, self.sw, self.host)

    def name_str(self):
        '''Return name string'''
        return "%i_%i_%i" % (self.pod, self.sw, self.host)

    def mac_str(self):
        '''Return MAC string'''
        return "00:00:00:%02x:%02x:%02x" % (self.pod, self.sw, self.host)

    def ip_str(self):
        '''Return IP string'''
        return "10.%i.%i.%i" % (self.pod, self.sw, self.host)

class FatTreeTopo(Topo):    
    LAYER_CORE = 0
    LAYER_AGG = 1
    LAYER_EDGE = 2
    LAYER_HOST = 3



    def def_nopts(self, layer, name = None):
        '''Return default dict for a FatTree topo.

        @param layer layer of node
        @param name name of node
        @return d dict with layer key/val pair, plus anything else (later)
        '''
        d = {'layer': layer}
        if name:
            id = self.id_gen(name = name)
            # For hosts only, set the IP
            if layer == self.LAYER_HOST:
                d.update({'ip': id.ip_str()})
                d.update({'mac': id.mac_str()})
            d.update({'dpid': "%016x" % id.dpid})
        # print d
        return d 

    def __init__(self, k = 4, speed = 1.0):
        super(FatTreeTopo, self).__init__()

        self.k = k
        self.id_gen = FatTreeNode
        self.numPods = k
        self.aggPerPod = k / 2

        self.hostList = []
        self.edgeList = []
        self.aggList = []
        self.coreList = []

        pods = range(0, k)
        core_sws = range(1, k / 2 + 1)
        agg_sws = range(k / 2, k)
        edge_sws = range(0, k / 2)
        hosts = range(2, k / 2 + 2)

        host_port = 1
        
        
      
        for p in pods:
            agg_port = 1
            for e in edge_sws:
                edge_port = 1
                edge_id = self.id_gen(p, e, 1).name_str()
                edge_opts = self.def_nopts(self.LAYER_EDGE, edge_id)
                self.edgeList.append(edge_id)
                self.addSwitch(edge_id, **edge_opts)
                
                for h in hosts:
                    host_id = self.id_gen(p, e, h).name_str()
                    host_opts = self.def_nopts(self.LAYER_HOST, host_id)
                    self.hostList.append(host_id)
                    self.addHost(host_id, **host_opts)
                    self.addLink(host_id, edge_id, host_port, edge_port)
                    
                    edge_port += 1
                
                edge_port = 3        

                for a in agg_sws:
                    agg_id = self.id_gen(p, a, 1).name_str()
                    agg_opts = self.def_nopts(self.LAYER_AGG, agg_id)
                    self.aggList.append(agg_id)
                    self.addSwitch(agg_id, **agg_opts)
                    self.addLink(edge_id, agg_id, edge_port, agg_port)
                    edge_port += 1
                agg_port += 1

            
            print("")
            for a in agg_sws:
                agg_port = 3
                agg_id = self.id_gen(p, a, 1).name_str()
                c_index = a - k / 2 + 1
                for c in core_sws:
                    core_id = self.id_gen(k, c_index, c).name_str()
                    core_opts = self.def_nopts(self.LAYER_CORE, core_id)
                    self.coreList.append(core_id)
                    self.addSwitch(core_id, **core_opts)
                    self.addLink(core_id, agg_id, p+1, agg_port)
                    agg_port += 1

    def layer_nodes(self, layer):
    #return list of node names in specified layer
        if(layer == self.LAYER_CORE):
            return self.coreList
        if(layer == self.LAYER_AGG):
            return self.aggList
        if(layer == self.LAYER_EDGE):
            return self.edgeList
        if(layer == self.LAYER_HOST):
            return self.hostList
    
    def port(self, src, dst):
        '''Get port number (optional)

        Note that the topological significance of DPIDs in FatTreeTopo enables
        this function to be implemented statelessly.

        @param src source switch name
        @param dst destination switch name
        @return tuple (src_port, dst_port):
            src_port: port on source switch leading to the destination switch
            dst_port: port on destination switch leading to the source switch
        '''
        #src_layer = self.layer(src)
        #dst_layer = self.layer(dst)

        #src_id = self.id_gen(name = src)
        #dst_id = self.id_gen(name = dst)

        LAYER_CORE = 0
        LAYER_AGG = 1
        LAYER_EDGE = 2
        LAYER_HOST = 3

        src_layer = 6
        if src in self.coreList:
            src_layer = LAYER_CORE
        if src in self.aggList:
            src_layer = LAYER_AGG
        if src in self.edgeList:
            src_layer = LAYER_EDGE
        if src in self.hostList:
            src_layer = LAYER_HOST

        dst_layer = 6
        if dst in self.coreList:
            dst_layer = LAYER_CORE
        if dst in self.aggList:
            dst_layer = LAYER_AGG
        if dst in self.edgeList:
            dst_layer = LAYER_EDGE
        if dst in self.hostList:
            dst_layer = LAYER_HOST


        src_id = self.id_gen(name = src)
        dst_id = self.id_gen(name = dst)

        if src_layer == LAYER_HOST and dst_layer == LAYER_EDGE:
            src_port = 1
            dst_port = int(src[4])-1
        elif src_layer == LAYER_EDGE and dst_layer == LAYER_HOST:
            src_port = int(dst[4])-1
            dst_port = 1

        elif src_layer == LAYER_EDGE and dst_layer == LAYER_AGG:
            src_port = int(dst[2])+1
            dst_port = int(src[2])+1
        elif src_layer == LAYER_AGG and dst_layer == LAYER_EDGE:
            src_port = int(dst[2])+1
            dst_port = int(src[2])+1

        elif src_layer == LAYER_AGG and dst_layer == LAYER_CORE:
            src_port = int(dst[4])+2
            dst_port = int(src[0])+1
        elif src_layer == LAYER_CORE and dst_layer == LAYER_AGG:
            src_port = int(dst[0])+1
            dst_port = int(src[4])+2

        else:
            raise Exception("Could not find port leading to given dst switch")


        return (src_port, dst_port)
    
  
topos = {"ft" : ( lambda: FatTreeTopo() )}
