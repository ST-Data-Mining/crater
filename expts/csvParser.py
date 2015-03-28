from __future__ import division,print_function
import sys
sys.dont_write_bytecode = True
sys.path.append('..')
from george.lib import *
import config
import random

'''
In the csv files craters are represented as '0'
and non craters are represented as '1'
'''

def writecsv():
  f = open('/home/george/Panzer/NCSU/Spatial and Temporal/crater/data/features/all.csv','r+')
  for i, name in enumerate(['1_24.csv','2_24.csv','3_24.csv','1_25.csv','2_25.csv','3_25.csv']):
    readcsv(name, toWrite=f, cnt=i)
  f.close()

def readcsv(fileName, base="/home/george/Panzer/NCSU/Spatial and Temporal/crater/data/features/", toWrite=None, cnt=0):
  with open(base+fileName,'rb') as csvfile:
    line = csvfile.readline()
    i=0
    if cnt == 0 and not toWrite:
      toWrite.write(line)
      i+=1
    for line in csvfile.readlines():
      if not toWrite:
        toWrite.write(line)
      i+=1
    print(i)
  csvfile.close()

#readcsv('all.csv')

def parseCSV(fileName, update_weight=True):
  pos=0;neg=0
  points = []
  with open(fileName, 'rb') as csvfile:
    csvfile.readline()
    for line in csvfile.readlines():
      datarow =  map(float, line.split(','))
      if datarow[-1] == 1:
        pos += 1
      else:
        neg += 1
      points.append(Point(datarow))
  if update_weight:
    [point.updateWeight(pos, neg) for point in points]
  return points


def randomPoints(fileNames=None, craters=100, non_craters=100):
  points = []
  if not fileNames: fileNames=[config.ALL_FILE]
  for fileName in fileNames:
    points += parseCSV(config.FEATURES_FOLDER+fileName, False)
  random.seed(1)
  randPoints = []
  c, nc = 0,0
  while c<craters or nc<non_craters:
    point = random.choice(points)
    if point in randPoints: continue
    if (point.y == 0 and c==craters) or (point.y==1 and nc== non_craters):
      continue
    if point.y==0: c+=1
    else: nc+=1
    randPoints.append(point)
  [point.updateWeight(non_craters, craters) for point in randPoints]
  return randPoints


if __name__=="__main__":
  pts = parseCSV(config.TRAIN_FILE)
  cl =  WeakClassifier(pts, 45)
  for pt in pts:
    print(cl.predict(pt.x),pt.y)