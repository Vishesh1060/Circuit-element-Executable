# -*- coding: utf-8 -*-
"""
Created on Fri Jun  2 23:35:48 2023

@author: vishesh
"""

import json
from jinja2 import Template
from jinja2 import FileSystemLoader as fsl
import jinja2
import os


with open("data.json") as f:
    data = json.load(f)

with open("base/base.vhdl") as f:
    template = Template(f.read())

Jinja=data['Jinja']
entity_name=data['entity_name']
generic_present=data['generic_present']
LRGates=data['LRGates']
Gates=data['Gates']
types=data['Types']
Terminals=data['Terminals']
Link=data['Link']
outterminals=data['outterminals']
core_out,lines,varcounter,varlink='''''',[],-1,[]
Environment=jinja2.Environment(loader=fsl("base/"))  
outfname='e1.vhdl'


def varlinkfinder(inps):
    global varlink
    var=inps
    for tvar in varlink:
        if tvar[0]==inps:
            var=tvar[1]
    return var
    

def linehandler(gatetype,gateref,newvar,indivinput):
    global LRGates,lines
    templine=[]
    _,_=templine.append(str("var%d "%varcounter)),templine.append(str("<="))
    if gatetype=='terminal' or 1==1:
        for indx,inps in enumerate(indivinput):
            if types[gateref]['in']>1:
                if inps.startswith('G'):
                    var=varlinkfinder(inps)
                    templine.append(var)
                else:
                    templine.append(str(inps))
                if indx==len(indivinput)-1:
                    break
                templine.append(str(types[gateref]['type']))
            elif types[gateref]['in']==1:
                templine.append(str(types[gateref]['type']))
                #templine.append(inps)
                if inps.startswith('G'):
                    var=varlinkfinder(inps)
                    templine.append(var)
                    break
                else:
                    templine.append(inps)
                    break
                
        
    lines.append(templine)


def varhandler(gatetype,gateref):
    global varcounter,varlink
    if gatetype=='terminal':
        varcounter+=1
        varlink.append((gateref,'var%d'%varcounter))
        return 'var%d'%varcounter
    
    if gatetype=='partial':
        varcounter+=1
        varlink.append((gateref,'var%d'%varcounter))
        return 'var%d'%varcounter
    
    if gatetype=='interconnected':
        varcounter+=1
        varlink.append((gateref,'var%d'%varcounter))
        return 'var%d'%varcounter
    

def terminalgates(LRGates):
    global Gates,lines,varcounter
    outputs=list(LRGates.keys())
    inputs=[]
    for key in LRGates.keys():
        inputs.append(LRGates[key])
        
    for indx,indivinput in enumerate(inputs):
        flag=1
        for gref in indivinput:
            if not gref.startswith('i'):
                flag=0
                break
        if flag==1:
            print('terminal gate')
            print(outputs[indx])
            newvar=varhandler('terminal',outputs[indx])
            linehandler('terminal',outputs[indx], newvar,indivinput)
            
def terminalcheck(inputs):
    tempjoinstring=''
    for val in inputs:
        tempjoinstring=tempjoinstring+str(val)
    if tempjoinstring.find('G')==-1:
        return True
    else: 
        return False
    
    

def partialcheck(inputs):
    tempjoinstring=''
    for val in inputs:
        tempjoinstring=tempjoinstring+str(val)
    if tempjoinstring.find('i')!=-1 and tempjoinstring.find('G')!=-1:
        return True
    else: 
        return False

def partialterminalgates(LRGates):
    global Gates,lines,varcounter
    outputs=list(LRGates.keys())
    inputs=[]
    for key in LRGates.keys():
        inputs.append(LRGates[key])
    
        
    for indx,indivinput in enumerate(inputs):
        #print(indx,outputs[indx],indivinput)
        if partialcheck(indivinput):
            print('partial')
            print(outputs[indx])
            gatetype,gateref='partial',outputs[indx]
            newvar=varhandler(gatetype, gateref)
            linehandler(gatetype, gateref, newvar,indivinput)

def interconngates(LRGates):
    global Gates,lines,varcounter
    outputs=list(LRGates.keys())
    inputs=[]
    for key in LRGates.keys():
        inputs.append(LRGates[key])
    
    for indx,indivinput in enumerate(inputs):
        if partialcheck(indivinput)==False and terminalcheck(indivinput)==False:    
            print("interconnected")
            print(outputs[indx])
            gatetype,gateref='interconnected',outputs[indx]
            newvar=varhandler(gatetype, gateref)
            linehandler(gatetype, gateref, newvar,indivinput)

def outgenerator():
    global outterminals,lines,core_out
    for out in outterminals:
        templine=[]
        templine.append(out[1])
        templine.append(' <= ')
        for var in varlink:
            if var[0]==out[0]:
                newvar=var[1]
        templine.append(str(newvar))
        print("outline:",templine)
        lines.append(templine)


def conngenerator(lines):
    global core_out
    for lrapper in lines:
        for word in lrapper:
            core_out=core_out+" "+word
        core_out=core_out+'\n'+'\t'



print('LRGates:',LRGates)
terminalgates(LRGates)
partialterminalgates(LRGates) 
interconngates(LRGates)
outgenerator()
conngenerator(lines) 


Jinja['template']=Environment.get_template("base.vhdl")
out=Jinja['template'].render({'Terminals': Terminals,'entity_name': entity_name,'LRGates': LRGates,'Gates': Gates,'types': types,'core_out':core_out})

print(out)

with open(outfname, "w") as file:
    file.write(out)
print(outfname,"generated at",os.getcwd())
    
 #print(varlink)
    
