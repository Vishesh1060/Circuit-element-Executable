# -*- coding: utf-8 -*-

import jinja2
import os
from json import load 
from jinja2 import FileSystemLoader as fsl

data = load(open('data.json'))

Jinja=data['Jinja']
entity_name=data['entity_name']
generic_present=data['generic_present']
LRGates=data['LRGates']
Gates=data['Gates']
types=data['Types']
Terminals=data['Terminals']
Link=data['Link']
core_out=''''''
outfname='e1.vhdl'

Environment=jinja2.Environment(loader=fsl("base/"))   

for i in range(len(LRGates)):
    for j in range(len(LRGates[Gates[i]])-1):
        if i!=len(LRGates):
            Link[Gates[i]]="var%d"%i

    
for i in range(len(LRGates)):
    for j in range(len(LRGates[Gates[i]])-1):
        if i!=len(LRGates):
            Link[Gates[i]]="var%d"%i
        print(Gates[i],LRGates)
        try:
            core_out= core_out+'\n'+str("\t\tvar%d "%i+"<= ")+str(Link[LRGates[Gates[i]][j]] if(LRGates[Gates[i]][j] in LRGates.keys()) else LRGates[Gates[i]][j]) +" "+ str(types[Gates[i]]['type']) +" "+ str(Link[LRGates[Gates[i]][j+1]] if(LRGates[Gates[i]][j+1] in LRGates.keys()) else LRGates[Gates[i]][j+1])+'\n'
        except Exception as e:
            print("Error=",e.args)
                   
if(Terminals['out']>len(Link)):
    print('resolution error')

else:
    for i in range(1,Terminals['out']+1):
        #legacy solution:
        #core_out=core_out+'\n'+str("\t\to%d "%i+"<= ")+str(types[Gates[-1]]['type'])+" "+str(Link[LRGates[Gates[-1]][-1]] if(LRGates[Gates[-1]][-1] in LRGates.keys()) else LRGates[Gates[i]][j])+'\n'
        core_out=core_out+'\n'+str("\t\to%d "%i+"<= ")+" "+str(Link[Gates[i]] if(LRGates[Gates[-1]][-1] in LRGates.keys()) else LRGates[Gates[i]][j])+'\n'

print(core_out)
print(Link)
print(LRGates[Gates[i]][j])

Jinja['template']=Environment.get_template("base.vhdl")
out=Jinja['template'].render({'Terminals': Terminals,'entity_name': entity_name,'LRGates': LRGates,'Gates': Gates,'types': types,'core_out':core_out})



with open(outfname, "w") as file:
    file.write(out)
print(outfname,"generated at",os.getcwd())
    
 
# Data sample
# entity_name (generate as e{{i]} if empty)
# LRGates={
#     'Gate{{i}}':[(port data)],
# }
# Gates=[(Gate label)]
# types={
#        'Gate{{i}}':[(type and behaviour)],
# }
# Terminals={
#  (generate as in{{i}} if empty)
#  (generate as out{{i}} if empty)  
# }
# Link={} (always empty to be generated)
# generic_present=(True or False)
