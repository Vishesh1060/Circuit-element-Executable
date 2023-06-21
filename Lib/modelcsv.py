import csv
def csvparse(csvpath):
    (imgData,i,j)=({},-1,-1)
    file=csv.reader(open(csvpath,'r'))
    for L in file:
        i+=1
        if i==0:
            for key in L:
                if key not in imgData:
                    imgData[key]=[]
        else:
            j=-1        
            kl=list(imgData.keys())
            for value in L:
                j+=1
                if value.isnumeric():
                    imgData[kl[j]].append(int(value))
                elif kl[j]=="rectangle_top_left" or kl[j]=="rectangle_bottom_right":
                    strval=value.strip("()").split(',')
                    inttupval=(int(strval[0]),int(strval[1]))
                    imgData[kl[j]].append(inttupval)
                else:
                    imgData[kl[j]].append(value)
    return imgData