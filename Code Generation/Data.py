# -*- coding: utf-8 -*-
import json
Data={
      'Jinja':{
          'template':''
          },
      'generic_present':False,
      'entity_name':'entity',
      'LRGates':{
          'G1':['i1','i2'],
          'G2':['i3','i4'],
          'G3':['G1','G2'],
          'G4':['G3']
          },
      'Gates':['G1','G2','G3','G4'],
      'types':{
        'G1':{'type':'AND','in':2,'out':1},
        'G2':{'type':'AND','in':2,'out':1},
        'G3':{'type':'OR','in':2,'out':1},
        'G4':{'type':'NOT','in':1,'out':1}, 
        },
    'Terminals':{
        "in":4,
        "out":1,
        },
    'Link':{}
}

flag=0
i=0

# try:
#    with open('data.json','w') as f:
#        json.dump(Data,f,ensure_ascii=False,indent=4)
# except Exception as e:
#        print(e)
#        i+=1
#        with open('data.json','w') as f:
#            json.dump('data%d.json'%i,f,ensure_ascii=False,indent=4)

