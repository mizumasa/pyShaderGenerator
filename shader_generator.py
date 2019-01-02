#!/usr/local/bin python
# -*- coding: utf-8 -*-

import sys
import random
import os
import json
import shader_edge as se
import shader_node as sn

DEBUG_ON = False

class Generator:
    def __init__(self):
        self.nodes = []
        self.nodesStable = []
        self.edges = []
        self.nodeProvider = sn.NodeProvider()
        self.edgeProvider = se.EdgeProvider()
        self.nodeProvider.debugOn = DEBUG_ON
        self.edgeProvider.debugOn = DEBUG_ON
        return
    def clear(self):
        self.nodes = []
        self.nodesStable = []
        self.edges = []
        self.nodeProvider.clear()
    def init(self):
        self.clear()
        nodeBuf = sn.Node(4)
        nodeBuf.setValue("gl_FragColor")
        self.nodes.append(nodeBuf)
        return

    def expand(self):
        allStable = True
        for edge in self.edges[::-1]:
            if not edge.isStable():
                allStable = False
                edge.expand(self.nodes, self.nodesStable, self.nodeProvider)
        for node in self.nodes[::-1]:
            if not node.isStable():
                allStable = False
                node.expand(self.edges, self.edgeProvider)
        return allStable

    def extend(self):
        for i in range(4):
            node = random.choice(self.nodes)
            if node.isStable() and (node.dim != 4):
                node.extend(self.nodes, self.nodeProvider,self.edges, self.edgeProvider)

    def alter(self):
        #change partially
        edge =  random.choice(self.edges)
        template = self.edgeProvider.getOtherEdge(edge.dimOut,edge.dimInList)
        if template != None:
            #print "change ",edge.template," -> ",template
            edge.setTemplate(template)

    def expandToEnd(self):
        while 1:
            if self.expand():
                break
        return

    def getPrint(self):
        out = ""
        for i in self.nodes[::-1]:
            if i.type == sn.NTYPE_SYS_OUTPUT:
                buf = i.getValue() + " = " + i.getEdge()+";"
                print( buf )
                out+=buf
            if i.type == sn.NTYPE_VARIABLE:
                buf = getTypeFromDim( i.dim ) +" "+ i.getValue() + " = " + i.getEdge()+";"
                print( buf )
                out+=buf
        return out
    def getTextObj(self,bPrint = False):
        out = ""
        data = ()
        for i in self.nodes[::-1]:
            if i.type == sn.NTYPE_SYS_OUTPUT:
                buf = i.getValue() + " = " + i.getEdge()+";"
                if bPrint:print( buf )
                data += (buf,)
                out += buf
            if i.type == sn.NTYPE_VARIABLE:
                buf = getTypeFromDim( i.dim ) +" "+ i.getValue() + " = " + i.getEdge()+";"
                data += (buf,)
                if bPrint:print( buf )
                out+=buf
        return {"line":out,"data":data,"color":()}
    def printInfo(self):
        print( ">>info")
        for i,j in enumerate(self.nodes):
            j.id = "n"+str(i)
        for i,j in enumerate(self.nodesStable):
            j.id = "s"+str(i)
        for i,j in enumerate(self.edges):
            j.id = "e"+str(i)
        print( len(self.nodes),"Nodes")
        for i in self.nodes:
            i.printOneLine()
        print( len(self.nodesStable),"NodesStable")
        for i in self.nodesStable:
            i.printOneLine()
        print( len(self.edges),"Edges")
        for i in self.edges:
            i.printOneLine()
        print( "info<<")

    def extractObj(self):
        out = {"nodes":[],"nodesStable":[],"edges":[]}
        for i,j in enumerate(self.nodes):
            j.id = "n"+str(i)
        for i,j in enumerate(self.nodesStable):
            j.id = "s"+str(i)
        for i,j in enumerate(self.edges):
            j.id = "e"+str(i)
        #print len(self.nodes),"Nodes"
        for i in self.nodes:
            out["nodes"].append(i.extractObj())
        #print len(self.nodesStable),"NodesStable"
        for i in self.nodesStable:
            out["nodesStable"].append(i.extractObj())
        #print len(self.edges),"Edges"
        for i in self.edges:
            out["edges"].append(i.extractObj())
        return out

    def applyObj(self,extractedObj):
        self.clear()
        for nodeObj in extractedObj["nodes"]:
            nodeBuf = sn.Node(nodeObj["dim"])
            nodeBuf.setObj(nodeObj)
            self.nodes.append(nodeBuf)
        for nodeSObj in extractedObj["nodesStable"]:
            nodeBuf = sn.Node(nodeSObj["dim"])
            nodeBuf.setObj(nodeSObj)
            self.nodesStable.append(nodeBuf)
        for edgeObj in extractedObj["edges"]:
            edgeBuf = se.Edge(edgeObj["dimOut"],edgeObj["dimInList"],self.getNodeFromId(edgeObj["rootNode"]))
            edgeBuf.setObj(edgeObj)
            self.edges.append(edgeBuf)
        for nodeObj in extractedObj["nodes"]:
            node = self.getNodeFromId(nodeObj["id"])
            node.setRootNode(self.getNodeFromId(nodeObj["rootNode"]))
            node.setEdge(self.getEdgeFromId(nodeObj["edge"]))
        for edgeObj in extractedObj["edges"]:
            edge = self.getEdgeFromId(edgeObj["id"])
            inputBuf = []
            for inputId in edgeObj["inList"]:
                inputBuf.append(self.getNodeFromId(inputId))
            edge.setInput(inputBuf)
            if edgeObj.has_key("out"):
                edge.setOutNode(self.getNodeFromId(edgeObj["out"]))
    def getElementByChannel(self,channel):
        nodes = []
        edges = []
        var = []
        for i in self.nodes:
            if i.type == sn.NTYPE_SYS_OUTPUT:
                buf = i.getValue() + " = " + i.getEdge()+";"
                print( buf )
        for i in self.nodes:
            if i.type == sn.NTYPE_VARIABLE:
                if i.getValue() in var:
                    buf = getTypeFromDim( i.dim ) +" "+ i.getValue() + " = " + i.getEdge()+";"
                    print( buf )

    def getEdgeFromId(self,_id):
        for i in self.edges:
            if _id == i.id:
                return i
        print("no such id edge",_id)
        return None

    def getNodeFromId(self,_id):
        for i in self.nodes:
            if _id == i.id:
                return i
        for i in self.nodesStable:
            if _id == i.id:
                return i
        print("no such id node",_id)
        return None

def getTypeFromDim(dim):
    if dim == 1:
        return "float"
    if dim == 2:
        return "vec2"
    if dim == 3:
        return "vec4"
    if dim == 4:
        return "vec4"
    return

def exchangeEdge(generator1,generator2):
    print "exchange start"
    if len(generator1.edges) > 1 and len(generator2.edges) > 1:
        i = random.choice(generator1.edges[1:])
        rIdx = random.randint(1,len(generator2.edges)-1)
        for j in generator2.edges[rIdx:] + generator2.edges[:rIdx]:
            if j.dimOut == i.dimOut and j.dimInList == i.dimInList:
                print "exchange edge",i.template, j.template
                buf = j.template
                j.template = i.template
                i.template = buf
                return
    return

def main():
    pass

if __name__ == '__main__':
    argvs=sys.argv
    print(argvs)
    main()


