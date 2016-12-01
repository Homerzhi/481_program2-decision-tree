
import csv
import os
import math

def get_data():
    """Get data, from csv."""
    if os.path.exists("Cars.csv"):
        data=[]
        with open('Cars.csv') as rfile:
            readfile=csv.reader(rfile, delimiter=', ')
            for row in readfile:
                data.append(row)
    return data


class Node:
    def __init__(self,data,attributes,level,parent,parentEntropy,condition,rootname='',entropy=-1,ex=-1,decideValue='',children=dict() ):        
        self.data=data
        self.attributes=attributes
        self.level=level
        self.parent=parent
        self.parentEntropy=parentEntropy
        self.condition=condition
        self.entropy=entropy
        self.ex=ex
        self.rootname=rootname
        self.decideValue=decideValue
        self.children=children
        def entropy(self):return self.entropy
        def data(self):return self.data
        def attributs(self):return self.attributes
        def level(self):return self.level
        def children(self):return self.children
        def rootname(self):return self.rootname
        def decideValue(self):return self.decideValue
        def parent(self):return self.parent
        def ex(self):return self.ex
        def parentEntropy(self):return self.parentEntropy
        def condition(self):return condition
        def setcondition(self,condition):self.condition=condition
        def setparentEntropy(self,En):self.parentEntropy=En
        def setex(self,ex):self.ex=ex
        def setparent(self,parent):self.parent=parent
        def setentropy(self,entropy):self.entropy=entropy
        def setdata(self,data):self.data=data
        def setattributs(self,attributes):
            self.attributes=attributes
        def setlevel(self,level):
            self.level=level
        def setchildren(self,children):
            self.children=children
        def setrootname(self,rootname):
            self.rootname=rootname
        def setdecideValue(self,decideValue):
            self.decideValue=decideValue
def calculateEntropy(data):
    #seperate each column
    dataclass=[];dataAlis=dict()
    for d in data:
        dataclass.append(d[-1])   #last column is rating
    dataset=list(set(dataclass))
    for i in dataset:
        dataAlis[i]=dataclass.count(i)
    total=len(data)
    E=0
    for i in dataset:
        E-=(dataAlis[i]/total)*math.log2(dataAlis[i]/total) 
    return E  
def findRoot(node): #find most gain, return dict[condition: data]
    data=node.data

    datasep=[];dataset=[]
    for i in range(len(data[0])):
        datasep.append(list())
        #dataset.append(list())
    for row in data:        #seperate each column
        for i in range(len(row)):
            datasep[i].append(row[i])
    for i in range(len(datasep)):   #get the unique value of each column
        dataset.append(list(set(datasep[i])))
    dataAlis=[] # calculate number of each unique value in an attribute
    
    for i in range(len(dataset)-1):
        tempdict=dict()
        for a in dataset[i]:
            tempdict[a]=datasep[i].count(a)
        dataAlis.append(tempdict)
    dividedata=[] # seperate data according to attribut value, attribute[value]=list of data has the same value
    for i in range(len(dataset)-1): 
        tempdict=dict()
        for a in dataset[i]:
            tempdict[a]=list()
        for row in data:
            for a in dataset[i]:
                if row[i]==a:
                    tempdict[a].append(row)
        dividedata.append(tempdict)
    Expect=[]
    for i in range(len(dataAlis)):
        ex=0
        for key in dataAlis[i]:
            ex+=(dataAlis[i][key]/len(data))*calculateEntropy(dividedata[i][key])
        Expect.append(ex)
    Entropy=node.entropy;gain=Entropy;gainIndex=-1;
    for i in range(len(Expect)):
        if Expect[i]<gain:
            gain=Expect[i]
            gainIndex=i
    for k in dividedata[gainIndex]:
        for row in dividedata[gainIndex][k]:
            row.pop(gainIndex)
    node.rootname+=node.attributes[gainIndex]
    return gain,dividedata[gainIndex]

if __name__ == '__main__':  
    attributs=['CarPrice','maintCost','NumDoors','NumPersons','TrunkSize','Safety','Rating']   
    initdata= get_data()

    datasets=[];tree=[];
    initnode=Node(initdata,attributs,0,0,0,'0')
    datasets.append(initnode)

    ''' repeat '''
    while(len(datasets)>0):
        node=datasets.pop(0)
        node.entropy=calculateEntropy(node.data)
        #node.children=
        if(node.entropy!=0):
            node.ex,node.children=findRoot(node)
            tree.append(node)
            #print(node.rootname,'   ',len(node.attributes),'<<<',len(tree))
            tempattr=node.attributes.copy()
            tempattr.pop(node.attributes.index(node.rootname))
            
            if(len(node.children)!=0):
                for k in node.children:
                    datasets.append(Node(node.children[k],tempattr,node.level+1,node.rootname,node.entropy,k))
        else:
            node.decideValue=node.data[0][-1]
          
            tree.append(node)
        #print(len(datasets))
    print('len of tree:',len(tree),len(set(tree)))

    
 
      

    
    def allzero(tree):
        for n in tree:
            if n.entropy!=0:
                return True
        return False
    output=[]
    while(allzero(tree)):
        node=tree.pop(0)
        level=node.level
        #if(node.entropy==0):print('level:',node.level)
        string=node.rootname+node.condition+str(level)
        tem='    '+string+'[label="'+string+'\\nentropy='+str(node.entropy)+'\\nparent Entropy='+str(node.parentEntropy)+'\\nexpect='+str(node.ex) +'"]\n'
        output.append(tem)
        children=node.children
        for k in children:
            data=children[k]
            i=0
            while(i<len(tree)):
                
                if(tree[i].data==data) and tree[i].level==level+1 and tree[i].parent==node.rootname and tree[i].parentEntropy==node.entropy:
                    if(tree[i].entropy!=0):
                        
                        tempstring='    '+string+'->'+tree[i].rootname+tree[i].condition+str(level+1)+'[label="'+k+'"] '+ string+' entropy:'+str(node.entropy)+' condition:'+str(node.condition)+tree[i].rootname+' parent en:'+str(tree[i].parentEntropy)+tree[i].rootname+' en:'+str(tree[i].entropy)+'\n'
                    else:
                        #string=node.node.rootname
                        tempstring='    '+string+'->'+tree[i].decideValue+str(level+1)+'[label="'+k+'"] '+string+' entropy:'+str(node.entropy)+' condition:'+str(node.condition)+tree[i].rootname+' parent en:'+str(tree[i].parentEntropy)+tree[i].rootname+' en:'+str(tree[i].entropy)+'\n'
                    
                        tree.pop(i)
                        i-=1
                        
                    output.append(tempstring)
                i+=1
        

        
    with open("decition.dot",'w') as ps:
        pass
    output.sort()
    output=list(set(output))
    output.sort()
    with open("decition.dot",'a') as ps:
        ps.write("digraph G{\n")
        for d in output:
            ps.write(d)
        ps.write("}")


    mo=[]
    with open("decition.dot",'r') as ps:
        readfile=ps.readlines()
        for row in readfile:
            if(']'in row):
                row=row[:row.index(']')+1]
                mo.append(row+'\n')
    mo=list(set(mo))
    mo.sort()
    with open("decition.dot",'w') as ps:  
        ps.write("digraph G{\n")          
        for d in mo:
            ps.write(d)
        ps.write("}")
        
        
                
        

