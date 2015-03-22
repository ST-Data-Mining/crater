from __future__ import division,print_function
import sys
sys.dont_write_bytecode = True
sys.path.append('..')
from lib import *
import config 

def writecsv():
  f = open('/home/george/Panzer/NCSU/Spatial and Temporal/crater/data/features/all.csv','r+')
  for i, name in enumerate(['1_24.csv','2_24.csv','3_24.csv','1_25.csv','2_25.csv','3_25.csv']):
    readcsv(name, toWrite=f, cnt=i)
  f.close()

def readcsv(fileName, base="/home/george/Panzer/NCSU/Spatial and Temporal/crater/data/features/", toWrite=None, cnt=0):
  with open(base+fileName,'rb') as csvfile:
    line = csvfile.readline()
    i=0
    if cnt == 0 and toWrite != None:
      toWrite.write(line)
      i+=1
    for line in csvfile.readlines():
      if toWrite != None:
        toWrite.write(line)
      i+=1
    print(i)

#readcsv('all.csv')

def parseCSV(fileName):
  pos=0;neg=0
  points = []
  with open(fileName, 'rb') as csvfile:
    line = csvfile.readline()
    for line in csvfile.readlines():
      datarow =  map(float, line.split(','))
      if datarow[-1] == 1:
        pos += 1
      else:
        neg += 1
      points.append(Point(datarow))
  [point.updateWeight(pos, neg) for point in points]
  return points

if __name__=="__main__":
  parseCSV(config.TRAIN_FILE)