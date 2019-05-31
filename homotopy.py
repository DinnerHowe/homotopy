#!/usr/bin/python
# coding: UTF-8

import numpy as np


from collections import defaultdict
from heapq import *
import matplotlib.pyplot as plt       
import copy
import matplotlib.pyplot as plt 
from  calculateHSignature import calculateHSignature 

colorlist = ['#1f77b4','#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2','#7f7f7f', '#bcbd22', '#17becf']

direct = []
direct.append((-1,-1))
direct.append((-1,0))
direct.append((-1,1))
direct.append((0,-1))
direct.append((0,1))
direct.append((1,-1))
direct.append((1,0))
direct.append((1,+1))

def drawnode(nodes):
    for node in nodes:
        for d in direct:
            connect_node = (node[0] + d[0] , node[1] + d[1])
            if connect_node in nodes:
                cost = np.sqrt(float(d[0])**2 + float(d[1])**2)
                edges.append( (node, connect_node, cost ))
                ax.plot((node[0], connect_node[0]), (node[1], connect_node[1]), c='b', alpha = 0.1)

def drawobsts(obsts):
    for obst in obsts:
        ax.add_patch(plt.Circle((obst[0], obst[1]), 0.5, color='r', alpha=0.4))

def drawpath(path, color, width):
    for i in range(1, len(path)):
        a = path[i-1]
        b = path[i]
        ax.plot((a [0], b[0]), (a[1], b[1]), c=color, linewidth = width )

class Dijkstra:
    def __init__(self, nodes, edges, obsts):
        self.max_homotopy = 60
        self.nodes = nodes
        self.edges = edges
        self.obsts = obsts
        self.homotopy = []
        self.cnt = 0

    def find(self, f, t):
        self.f = f
        self.t = t
        g = defaultdict(list)
        for l,r,c in self.edges:
            g[l].append((c,r))

        q, seen, mins = [(0,f,())], set(), {f: 0}
        while q:
            (cost,v1,path) = heappop(q)
            if v1 not in seen:
                seen.add(v1)
                path = (v1, path)
                if v1 == t: 
                    self.mins = mins
                    return path

                for c, v2 in g.get(v1, ()):
                    if v2 in seen: 
                        continue
                    if v2 in self.obsts: 
                        continue
                    prev = mins.get(v2, None)
                    next = cost + c
                    if prev is None or next < prev:
                        mins[v2] = next
                        heappush(q, (next, v2, path))

    def check_is_homotopy(self, l):
        for h in self.homotopy:
            if np.abs(h - l) <  0.1:
                return True
        return False

    def pathfinder(self, paths, path ,node):
        if len(self.homotopy) > self.max_homotopy:
            return
        path.append(node)
        if node == self.f:
            self.cnt += 1
            l = calculateHSignature(path, self.obsts)
            if not self.check_is_homotopy(l):
                paths.append(copy.copy(path))
                self.homotopy.append(l)
                drawpath (path, colorlist[ len(self.homotopy) % len(colorlist)], 10. / len(self.homotopy) )

                plt.pause(0.5)

            return
        for d in direct:
            connect_node = (node[0] + d[0] , node[1] + d[1])
            if (connect_node in self.mins) and self.mins[connect_node] < self.mins[node]:
                self.pathfinder(paths, path, connect_node)
                if len(self.homotopy) > self.max_homotopy:
                    return
                path.pop()

    def allpath(self):
        paths = []
        path = []
        self.pathfinder(paths, path, self.t)
        return paths




        
win_size = 8

fig, ax = plt.subplots()
ax.set_xlim([-1,win_size ])
ax.set_ylim([-1,win_size ])

if __name__ == "__main__":
    nodes = []
    edges = []
    obsts = []
    for i in range(win_size):
        for j in range(win_size):
            nodes.append((i,j))

    obsts.append((1,1))
    obsts.append((5,5))
    obsts.append((3,3))
    obsts.append((2,6))
    obsts.append((6,2))

    direct = []
    direct.append((-1,-1))
    direct.append((-1,0))
    direct.append((-1,1))

    direct.append((0,-1))
    direct.append((0,1))

    direct.append((1,-1))
    direct.append((1,0))
    direct.append((1,+1))

    drawobsts(obsts)
    drawnode(nodes)
    
    dijkstra = Dijkstra(nodes, edges, obsts)
    path = dijkstra.find((0,0), (7,7))

    paths = dijkstra.allpath()
    print len(paths)

    for path in paths:
        print path
        for i in range(1, len(path)):
            a = path[i-1]
            b = path[i]
            ax.plot((a [0], b[0]), (a[1], b[1]), c='g', linewidth = 5.0 )
        plt.pause(0.5)
        
        plt.cla()
        ax.set_xlim([-1,win_size ])
        ax.set_ylim([-1,win_size ])

        drawnode(nodes)
        drawobsts(obsts)
    plt.show()
    
