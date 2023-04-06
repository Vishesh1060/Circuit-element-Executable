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
types=data['types']
Terminals=data['Terminals']
Link=data['Link']


try:
    Environment=jinja2.Environment(loader=fsl("base/"))     
    for i in range(len(LRGates)):
        for j in range(len(LRGates[Gates[i]])-1):
            if i!=len(LRGates):
                Link[Gates[i]]="var%d"%i
            print("var%d"%i,"<=", Link[LRGates[Gates[i]][j]] if(LRGates[Gates[i]][j] in LRGates.keys()) else LRGates[Gates[i]][j],types[Gates[i]]['type'],Link[LRGates[Gates[i]][j+1]] if(LRGates[Gates[i]][j+1] in LRGates.keys()) else LRGates[Gates[i]][j+1])
    if(Terminals['out']>len(Link)):
        print('resolution error')
    else:
        for i in range(1,Terminals['out']+1):
            print("o%d"%i,"<=",types[Gates[-1]]['type'],Link[LRGates[Gates[-1]][-1]] if(LRGates[Gates[-1]][-1] in LRGates.keys()) else LRGates[Gates[i]][j])
    # print(Link)
    Jinja['template']=Environment.get_template("base.vhdl")
    out=Jinja['template'].render(Terminals,entity_name,LRGates,Gates,types)
    print(out)
except Exception as e:
    print(e)
print("e1.vhdl","generated at",os.getcwd())
    
 
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
