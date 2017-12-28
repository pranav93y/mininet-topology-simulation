# Topology-mini
Final Project for CMPE 252 building Clos tree, Jellyfish, and S2 networking topologies.

CMPE 252 Final Project
Implementing a FatTree topology and corresponding routing protocols:

By Justin Lee & Pranav Yerabati

# Instructions to Run

Our project requires two separate shell console windows to run; one for the controller and one for the network topology (mininet). We had issues with the switches connecting with the controller through the same script (as it was in the original mn_ft.py script given), therefore we decided to split and create out own bash scripts to run. Our project requires 4 bash scripts to run; 2 for the controller and 2 for the network topology. 

Controller Bash Scripts:
controller_dij.sh
controller_ecmp.sh

Network Topology (Mininet) Bash Scripts:
run_dij.sh
run_ecmp.sh

#To test Dijkstras:
On one shell windows, run: sudo sh controller_dij.sh
On the other, run: sudo sh run_dij.sh

#To test ECMP
On one shell windows, run: sudo sh controller_ecmp.sh
On the other, run: sudo sh run_ecmp.sh

Iperf was used to generate traffic through the network, and its output will be saved in Topology-mini/mininet_fattree_exp-code_skeleton/results/fattree-{dij/ecmp}/{input-file-name}/data

# Network Topology Plot
We provided a plot we have generated using the python library matplotlib to plot our fat-tree topology. The file is named fattree_topo.png


# Known Issues/Errors

1. Iperf Connection Failed: This is seen some times as the output for the iperf client, however we believe it must be due to how iperf not closing the connection properly. We tested multiple times by opening xterm windows on those hosts, and we were not able to find an error. 

2. We were not able to call the controller in mn_ft.py, as the switches would not connect. Therefore we implemented own own bash scripts to run the controller and mininet in separate shell windows. 

3. We were not able to implement two level routing 


# Project Summary/Description

The goal of this final project was to implement a simulation of a  Fat Tree / Clos topology for a data center network in Mininet with various routing protocols. We build a software defined networking (SDN) network using simulated switches with an SDN controller. The main structure of the code was designed based on Ripl-POX (https://github.com/brandonheller/riplpox, a library for POX). Our public repository for this project can be found at Topology-mini (https://github.com/lejuste/Topology-mini). 

The first part of the project was to contract a fat tree topology with (k=4) fat-tree topology. We built the topology in DCTopo.py based on the fat tree topology in ripl-master (https://github.com/brandonheller/ripl). This was built in mininet.

The second part was to run Dijkstra’s algorithm between two pairs of end hosts. We first built the algorithm that takes in a nested dictionary list that holds all nodes and every connected node to that given node. 

For the third part, we attempted to implement two-level routing algorithms proposed to improve the link bandwidth. However were unable to implement the two flows tables required. 

The fourth step of the project was to implement ECMP which uses a hash function to pick a given path through the fat tree network topology from the k different paths. We implemented this by running dijkstras on a graph object that only had one specific available core switch that is chosen with a hash function which his run by combining any source and destination ip pair. 

Finally, we built a separate script to evaluate each routing scheme using Iperf and the given traffic patterns. 

In conclusion, we spent multiple weeks and countless hours adding functions and modifying the provided skeleton code. We really enjoyed understanding how to create a given topology and use a SDN controller. 

