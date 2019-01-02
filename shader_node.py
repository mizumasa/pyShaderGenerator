#!/usr/local/bin python
# -*- coding: utf-8 -*-

import sys
import random

VARIABLE_PREFIX = "a_"

NTYPE_SYS_OUTPUT = 0
NTYPE_SYS_INPUT = 1
NTYPE_VARIABLE = 2
NTYPE_VALUE = 3
NTYPE_NONE = 4

NO_WEIGHT =True

class Node:
    def __init__(self,dim):
        self.id = None
        self.dim = dim
        self.end = False
        self.stable = False
        self.start = False
        self.value = ""
        self.rootNode = self
        self.edge = None
        self.type = NTYPE_NONE
        self.w = int(random.random()*1000)/100.
        self.b = int(random.random()*1000)/100.
        return
    def printOneLine(self):
        buf = str(self.id)+","
        buf += "dim:"+str(self.dim)+","
        buf += "type:"+str(self.type)+","
        buf += "v:"+self.value+","
        if self.edge != None:
            buf += "edge-id:"+str(self.edge.id)+","
        buf += "root-id:"+str(self.rootNode.id)+","
        buf = buf.replace("\n","").replace(" ","")
        print buf
    def extractObj(self):
        buf = {}
        buf["id"] = self.id
        buf["dim"] = self.dim
        buf["end"] = self.end
        buf["stable"] = self.stable
        buf["start"] = self.start
        buf["value"] = self.value
        buf["rootNode"] = self.rootNode.id
        if self.edge != None:
            buf["edge"] = self.edge.id
        buf["type"] = self.type
        buf["w"] = self.w
        buf["b"] = self.b
        return buf

    def setObj(self,extractedObj):
        self.id = extractedObj["id"]
        self.end = extractedObj["end"]
        self.stable = extractedObj["stable"]
        self.start = extractedObj["start"]
        self.value = extractedObj["value"]
        #buf["rootNode"]self.rootNode.id
        #buf["edge"]self.edge.id
        self.type = extractedObj["type"]
        self.w = extractedObj["w"]
        self.b = extractedObj["b"]

    def setRootNode(self,node):
        self.rootNode = node

    def setEdge(self,edge):
        self.edge = edge

    def setValue(self, value):
        if value.replace(".","").isdigit():
            self.value = value
            self.end = True
            self.stable = True
            self.type = NTYPE_VALUE
        else:
            self.value = value
            self.type = NTYPE_VARIABLE
            if isSystemInputValue(value):
                self.end = True
                self.stable = True
                self.type = NTYPE_SYS_INPUT
            if isSystemOutputValue(value):
                self.start = True
                self.type = NTYPE_SYS_OUTPUT
        return

    def setStable(self):
        self.stable = True

    def isStable(self):
        return self.stable

    def getValue(self):
        if self.type == NTYPE_NONE:
            return self.getEdge()
        else:
            return self.value

    def getEdge(self):
        if self.type == NTYPE_NONE and (not NO_WEIGHT):
            return addWB(self.edge.getValue(),self.w,self.b)
        else:
            return self.edge.getValue()

    def expand(self,edges,provider,select = -1):
        rootNode = None
        if self.type in [NTYPE_SYS_INPUT,NTYPE_VARIABLE]:
            rootNode = self
        else:
            rootNode = self.rootNode
        buf = provider.new(self.dim,rootNode,output = (self.value == "gl_FragColor"), select = select)
        self.edge = buf
        self.stable = True
        edges.append(buf)
        return

    def extend(self,nodes,node_provider,edges,edge_provider):
        node = node_provider.newDummy(self.dim,self.rootNode)
        node.setStable()
        edge = edge_provider.newPipe(self.dim, self.rootNode)
        node.edge = self.edge
        edge.setInput([node])
        nodes.append(node)
        edges.append(edge)
        self.edge = edge
        return

class NodeProvider:
    def __init__(self):
        self.load()
        self.clear()
        self.debugOn = False
        return
    def clear(self):
        self.variable_idx = 0
        self.variables = []
        return
    def new(self,dim,rootNode,select=-1):
        if dim == 1 and select >= 0:
            buf = Node(1)
            buf.setRootNode(rootNode)
            if select < len(SYS_INPUT["1"]):
                buf.setValue(SYS_INPUT["1"][select])
            else:
                pass
            if self.debugOn:
                print( "new node with ",buf.value )
            return buf
        if dim == 1:
            buf = Node(1)
            buf.setRootNode(rootNode)
            if random.random() > 0.5:
                buf.setValue(random.choice(SYS_INPUT["1"]) )
            elif random.random() > 0.8:
                buf.setValue(str(int(random.random()*1000)/100.))
                #buf.setValue("1.")
            elif random.random() > 0.7:
                variable_name = VARIABLE_PREFIX + str(self.variable_idx)
                buf.setValue(variable_name)
                self.variables.append(variable_name)
                self.variable_idx += 1
            elif random.random() > 0.5 and len(self.variables) > 0:
                variableNameUsable = getVariableNameUsable(self.variables,rootNode)
                if len(variableNameUsable) > 0:
                    buf.setValue( random.choice( variableNameUsable ) )
                    buf.setStable()
            else:
                pass
            if self.debugOn:
                print( "new node with ",buf.value )
            return buf
        else:
            buf = Node(dim)
            buf.setRootNode(rootNode)
            if random.random() > 0.5:
                buf.setValue(random.choice(SYS_INPUT[str(dim)]) )
            if self.debugOn:
                print( "new node with ",buf.value )
            return buf
    def newDummy(self,dim,rootNode):
        buf = Node(1)
        buf.setRootNode(rootNode)
        if self.debugOn:
            print( "new node dummy with ",buf.value )
        return buf

    def load(self):
        return

def addWB(edgeValue,w,b):
    return  " ".join(['(',edgeValue,'*',str(w),'+',str(b),')'])

def variableName2Idx(variable_name):
    return int( variable_name.replace(VARIABLE_PREFIX,"") )

def getVariableNameUsable(variables,rootNode):
    if rootNode.type == NTYPE_SYS_OUTPUT:
        return variables
    rootVariableIdx = variableName2Idx(rootNode.value)
    out = []
    for i in variables:
        if variableName2Idx(i) > rootVariableIdx:
            out.append(i)
    return out

def isSystemInputValue(name):
    if name in SYS_INPUT_ALL:
        return True
    else:
        return False

def isSystemOutputValue(name):
    if name in ["gl_FragColor"]:
        return True
    else:
        return False

def main():
    pass

if __name__ == '__main__':
    argvs=sys.argv
    main()


SYS_INPUT = {
    "1":[
        "sin( time * 4.)",
        "cos( time * 3.)",
        "tan( time * 2.)",
        "cos( time * 5.)",
        "uv.x * time - floor(uv.x * time)",
        "uv.y * time - floor(uv.y * time)",
        "uv.x * 10. - floor(uv.x * 10.)",
        "uv.y * 10. - floor(uv.y * 10.)",
        "uv.x",
        "uv.y",
        "uv.x + time",
        "uv.y + time"
    ],
    "2":[
        "uv",
        "uv.xx",
        "uv.yx",
        "uv.yy",
    ],
    "3":[
        "uv.xxy",
        "uv.xyx",
        "uv.yxx"
    ],
    "4":[
        "uv.xxyy",
        "uv.xyxy",
        "uv.yxyx"
    ]
}
SYS_INPUT_ALL = []
for i in SYS_INPUT.values():
    SYS_INPUT_ALL += i