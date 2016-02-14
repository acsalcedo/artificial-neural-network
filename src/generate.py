import random
import sys

dataFolder = "../data/circle/"

def main(argv):

    if len(argv) != 2:
        print "python generate.py <outputfile> <datasetSize>"
        sys.exit()

    fileName = argv[0]
    setSize = int(argv[1])

    f = open(dataFolder+fileName,'w')

    for i in range(setSize):
        x = random.random()*20
        y = random.random()*20

        target = 1

        if ((x-10)**2 + (y-10)**2) <= 49:
            target = -1

        f.write("%s %s %s\n" %(x,y,target))

    f.close()

if __name__ == '__main__':
    main(sys.argv[1:])