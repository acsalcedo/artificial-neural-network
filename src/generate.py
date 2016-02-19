import random
import sys

dataFolder = "../data/circle/"

def main(argv):

    if len(argv) != 2:
        print "python generate.py <outputfile> <datasetSize>"
        sys.exit()

    fileName = argv[0]
    setSize = int(argv[1])
    flag = 1
    f = open(dataFolder+fileName,'w')
    i = 0
    while i < setSize:
        x = random.random()*20
        y = random.random()*20

        target = 0

        inCircle = (x-10)**2 + (y-10)**2 <= 49

        if inCircle and flag:
            
            target = -1
            flag = not flag

        elif not(inCircle or flag):
            
            target = 1
            flag = not flag
        
        else:
            continue

        f.write("%s %s %s\n" %(x,y,target))
        i += 1

    f.close()

def generatePoints():

    f = open(dataFolder+"testSet.txt",'w')
    y = 0

    while y <= 20:
        x = 0
        while x <= 20:
            f.write("%s %s %s\n" %(x,y,-9))
            x += 0.2
        y += 0.2
        
    f.close()