Data={
    'Jinja':{
        'template':''
    },
    'generic_present':False,
    'entity_name':'',
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

# for i in range(len(LRGates)):
#         for j in range(len(LRGates[Gates[i]])-1):
#             if i!=len(LRGates):
#                 Link[Gates[i]]="var%d"%i
#             print("var%d"%i,"<=", Link[LRGates[Gates[i]][j]] if(LRGates[Gates[i]][j] in LRGates.keys()) else LRGates[Gates[i]][j],types[Gates[i]]['type'],Link[LRGates[Gates[i]][j+1]] if(LRGates[Gates[i]][j+1] in LRGates.keys()) else LRGates[Gates[i]][j+1])
# if(Terminals['out']>len(Link)):
#     print('resolution error')
# else:
#     for i in range(1,Terminals['out']+1):
#         print("o%d"%i,"<=",types[Gates[-1]]['type'],Link[LRGates[Gates[-1]][-1]] if(LRGates[Gates[-1]][-1] in LRGates.keys()) else LRGates[Gates[i]][j])
# print(Link)

