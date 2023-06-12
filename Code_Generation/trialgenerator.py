# Import the modules
import json
from jinja2 import Template

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
Link,tempLink=data['Link'],[]
core_out,lines='''''',[]

#vhdl_code = template.render(data)
#print(data)
templink,internalcheck=[],[]
varcounter=0


    

def replacer(newinp,originalinp,val):
    print("-----",newinp)
    if newinp==[]:
        newinp=[]
        for orgnalval in originalinp:
            if orgnalval==val[0]:
                newinp.append(val[1])
            else:
                newinp.append(orgnalval)
        return newinp
    else:
        for indx,orgnalval in enumerate(originalinp):
            if orgnalval==val[0]:
                
                newinp[indx]=val[1]
                print(newinp)
            else:
                pass
        return newinp

def terminalgates(LRGates):
    global internalcheck,tempLink,lines,varcounter
    internalline=[]
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
            internalcheck.append(outputs[indx])
            tempLink.append((outputs[indx],LRGates[outputs[indx]]))
            #print("var%d"%varcounter,"<=",end='')
            internalline.append(str("var%d "%varcounter))
            internalline.append(str("<="))
            varcounter+=1
            for indx1,inps in enumerate(LRGates[outputs[indx]]):
                internalline.append(inps)
                if indx1!=len(LRGates[outputs[indx]])-1: 
                    internalline.append(types[outputs[indx]]['type'])
    lines.append((internalline))
    print(templink)
    return lines

def partialterminalgates(LRGates):
    global internalcheck,tempLink,varcounter,GateVarLink
    internalline=[]
    outputs=list(LRGates.keys())
    inputs=[]
    for key in LRGates.keys():
        inputs.append(LRGates[key])
    newinputs=[]
    for indx,indivinput in enumerate(inputs):
        flagi,flagni=0,0
        for inpref in indivinput:
            if inpref.startswith('i')and not (outputs[indx] in internalcheck):
                flag=1 
                break
        if flag==1:
            print('partial terminal gate')
            print(outputs[indx])
            #add output of gate to variable linker
            internalcheck.append(outputs[indx])
    
    print(tempLink)
                
def interconngates(LRGates):
    global internalcheck,tempLink,varcounter,GateVarLink
    outputs=list(LRGates.keys())
    inputs=[]
    for key in LRGates.keys():
        inputs.append(LRGates[key])
    
    for indx,indivinput in enumerate(inputs):
        flag=0
        for gref in indivinput:
            if not (outputs[indx] in internalcheck):
                flag=1 
                break
        if flag==1:
            print('interconnected gate')
            print(outputs[indx])
            internalcheck.append(outputs[indx])
            tempLink.append((outputs[indx],LRGates[outputs[indx]]))
    print(tempLink)    
    
for i in range(len(LRGates)):
    for j in range(len(LRGates[Gates[i]])-1):
        pass

print(LRGates)
terminalgates(LRGates)


#partialterminalgates(LRGates)
interconngates(LRGates)

for line in tempLink:
    print(line)


#loop old section
        # if i!=len(LRGates):
        #     Link[Gates[i]]="var%d"%i
        # core_out= core_out+'\n'+str("\t\tvar%d "%i+"<= ")+str(Link[LRGates[Gates[i]][j]] if(LRGates[Gates[i]][j] in LRGates.keys()) else LRGates[Gates[i]][j]) +" "+ str(types[Gates[i]]['type']) +" "+ str(Link[LRGates[Gates[i]][j+1]] if(LRGates[Gates[i]][j+1] in LRGates.keys()) else LRGates[Gates[i]][j+1])+'\n'


'''
with open("output.vhdl", "w") as f:
    f.write(vhdl_code)
'''