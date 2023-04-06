# -*- coding: utf-8 -*-
"""
Created on Tue Nov  1 15:07:29 2022

@author: vishesh
"""

import xml.etree.ElementTree as ElementTree
from os import mkdir,listdir
from shutil import copy as copy

c=1
# file directory
d="../"
# Output directory
Output="../classified"

L1=listdir(d)

File=[]

def eval(Elements):
    gates=["and","nand","or","nor","xor","xnor"]
    for e in Elements:
        for g in gates:
            if(e==g):
                print(c,". \"",g,"\" found",end=" ")
                return 1
    return 0

def parser(File,Elements):
    tree = ElementTree.parse(File)    
    for child in tree.getroot():
        if(child.tag=="object"):
            for child2 in child:
                if(child2.tag=="name"):
                    Elements.append(child2.text)

for l in L1:
    if(l.endswith("xml")):
        File.append(d+l)

for f in File:
    Elements=[]
    parser(f,Elements)
    if(eval(Elements)):
        try:
            mkdir(Output)
        except Exception:
            pass
        copy(f,Output)
        copy(f.replace("xml","jpg"),Output)
        c=c+1
        print(" ok")

print(len(File)," files processed")
print(c-1," successful matches found")
