#!/usr/local/bin python
# -*- coding: utf-8 -*-

import os
import json
import sys
import random

class Edge:
    def __init__(self,dimOut,dimInList,rootNode):
        self.id = None
        self.dimInList = dimInList
        self.dimOut = dimOut
        self.inList = []
        self.out = None
        self.rootNode = rootNode
        self.template = "vec4( _0_ , _1_ , _2_ , _3_ )"
        return
    def printOneLine(self):
        buf = str(self.id)+","
        buf += "dimIn:"+str(self.dimInList)+","
        buf += "dimOut:"+str(self.dimOut)+","
        buf += "t:"+self.template+","
        buf += "inList:"
        for i in self.inList:
            buf += str(i.id)+" "
        buf += ",root-id:"+str(self.rootNode.id)+","
        buf = buf.replace("\n","").replace(" ","")
        print buf

    def extractObj(self):
        buf = {}
        buf["id"] = self.id
        buf["dimInList"] = self.dimInList
        buf["dimOut"] = self.dimOut
        buf["inList"] = []
        for i in self.inList:
            buf["inList"].append(i.id)
        if self.out != None:
            buf["out"] = self.out.id
        buf["rootNode"] = self.rootNode.id
        buf["template"] = self.template
        return buf

    def setObj(self,extractedObj):
        self.id = extractedObj["id"]
        self.inList = []
        #extractedObj["inList"][]
        #extractedObj["out"]self.out.id
        #extractedObj["rootNode"]self.rootNode.id
        self.template = extractedObj["template"]
        return


    def setTemplate(self,template):
        self.template = template
        return

    def setInput(self,nodeList):
        for i in nodeList:
            self.inList.append(i)
        return

    def setOutNode(self,outNode):
        self.out = outNode
        return

    def setRootNode(self,rootNode):
        self.rootNode = rootNode
        return

    def getValue(self):
        return replaceTemplate(self.template, self.inList)

    def isStable(self):
        if len(self.dimInList) == len(self.inList):
            Flag = True
            for i in range(len(self.dimInList)):
                if self.inList[i].dim != self.dimInList[i]:
                    Flag = False
            return Flag
        else:
            return False

    def expand(self,nodes,nodesStable,provider,select = -1):
        for i in range(len(self.dimInList)):
            if select != -1:
                buf = provider.new(self.dimInList[i],self.rootNode,select = select[i])
            else:
                buf = provider.new(self.dimInList[i],self.rootNode)
            self.inList.append(buf)
            if not buf.isStable():
                nodes.append(buf)
            else:
                nodesStable.append(buf)
        return

class EdgeProvider:
    def __init__(self):
        self.load()
        self.setupSearcherWithDim()
        self.debugOn = False
        return
    def new(self,dim,rootNode,output = False,select = -1):
        if output:
            #buf = Edge(4,[1,1,1],rootNode)
            #buf.setTemplate("clamp( abs( vec4(\n     _0_ ,\n     _1_ ,\n     _2_ ,\n     1. ) ),0.,1.)")
            #buf = Edge(4,[2,1],rootNode)
            #buf.setTemplate("clamp( abs( vec4(\n     _0_ ,\n     _1_ ,\n     1. ) ),0.,1.)")
            edgeSelected = random.choice(self.dataOutput[str(dim)])
            outDim = edgeSelected[0]
            inDimList = edgeSelected[1]
            template = edgeSelected[2]
            buf = Edge(outDim,inDimList,rootNode)
            buf.setTemplate(template)
            if self.debugOn:
                print( "new edge (output)",dim)
            return buf
        if dim in [1,2,3,4]:
            edgeSelected = random.choice(self.data[str(dim)])
            outDim = edgeSelected[0]
            inDimList = edgeSelected[1]
            template = edgeSelected[2]
            #template = "sin( _0_ )"
            buf = Edge(outDim,inDimList,rootNode)
            buf.setTemplate(template)
            if self.debugOn:
                print( "new edge",dim, edgeSelected )
            return buf

    def newPipe(self,dim,rootNode):
        #return edge which has same dim input and output
        randIdx = int((len(self.data[str(dim)]) - 1 ) * random.random())
        edgeSelected = None
        while 1:
            edgeSelected = self.data[str(dim)][randIdx]
            outDim = edgeSelected[0]
            inDimList = edgeSelected[1]
            if len(inDimList) == 1:
                if inDimList[0] == outDim:
                    break
            randIdx = ( randIdx + 1 ) % len(self.data[str(dim)])
        buf = Edge(dim,[dim],rootNode)
        buf.setTemplate(edgeSelected[2])
        if self.debugOn:
            print( "new edge (pipe)",dim, edgeSelected )
        return buf

    def getOtherEdge(self, outDim, inDimList):
        key = str(outDim) + "-" + '_'.join(map(str, inDimList)) 
        if key in self.searcher.keys():
            return random.choice( self.searcher[key] )
        else:
            return None

    def load(self):
        self.dataOutput,self.data = loadEdgeData()
        return

    def setupSearcherWithDim(self):
        self.searcher = {}
        for outDim in self.data.keys():
            for i in self.data[outDim]:
                key = outDim+"-"+'_'.join(map(str, i[1]))
                if key not in self.searcher.keys():
                    self.searcher[key]=[]
                self.searcher[key].append(i[2])




def loadEdgeData():
    f = open("edge.json")
    data = {}
    dataOutput = {}
    buf = json.load(f)
    for outDim in buf["dataOutput"].keys():
        if outDim.isdigit():
            dataOutput[outDim] = []
            outDimInt = int(outDim)
            for inDim in buf["dataOutput"][outDim].keys():
                inDimList = inDim.split('_')
                inDimEachFirst = inDimList[0]
                if inDimEachFirst.isdigit():
                    inDimListInt = []
                    for inDimEach in inDimList:
                        inDimListInt.append(int(inDimEach))
                    for edge in buf["dataOutput"][outDim][inDim]:
                        dataOutput[outDim].append([outDimInt,inDimListInt, edge["t"]])

    outDims = buf["data"].keys()
    outDims.sort()
    for outDim in outDims:
        if outDim.isdigit():
            data[outDim] = []
            outDimInt = int(outDim)
            for inDim in buf["data"][outDim].keys():
                inDimList = inDim.split('_')
                inDimEachFirst = inDimList[0]
                if inDimEachFirst.isdigit():
                    inDimListInt = []
                    for inDimEach in inDimList:
                        inDimListInt.append(int(inDimEach))
                    for edge in buf["data"][outDim][inDim]:
                        data[outDim].append([outDimInt,inDimListInt, edge["t"]])
                elif inDimEachFirst == "n":
                    for nBuf in range(1,5):
                        inDimList = [nBuf]*len(inDimList)
                        inDimListInt = []
                        for inDimEach in inDimList:
                            inDimListInt.append(int(inDimEach))
                        for edge in buf["data"][outDim][inDim]:
                            data[outDim].append([outDimInt,inDimListInt, edge["t"]])

        elif outDim == "n":
            for nBuf in range(1,5):
                for inDim in buf["data"][outDim].keys():
                    inDimList = inDim.split('_')
                    inDimEachFirst = inDimList[0]
                    if inDimEachFirst.isdigit():
                        inDimListInt = []
                        for inDimEach in inDimList:
                            inDimListInt.append(int(inDimEach))
                        for edge in buf["data"][outDim][inDim]:
                            data[str(nBuf)].append([nBuf,inDimListInt, edge["t"]])
                    elif inDimEachFirst == "n":
                        inDimList = [nBuf]*len(inDimList)
                        inDimListInt = []
                        for inDimEach in inDimList:
                            inDimListInt.append(int(inDimEach))
                        for edge in buf["data"][outDim][inDim]:
                            data[str(nBuf)].append([nBuf,inDimListInt, edge["t"]])
    return dataOutput,data

def replaceTemplate(template,inList):
    buf = template
    for i in range(len(inList)):
        buf = buf.replace( "_"+str(i)+"_", inList[i].getValue() )
    return buf

def main():
    pass

if __name__ == '__main__':
    argvs=sys.argv
    main()
