#__author__ = 'FuWei'
from __future__ import print_function, division
import sys
import pdb
from os import listdir
from os.path import isfile, join
# from table import *

class o(object):
 def __init__(i, **filed):
   i.__dict__.update(filed)
   return i

class Row(object):
  def __init__(i,data):
    i.x = data[:-1]
    i.y = data[-1]
    i.w = 0
  def __len__(i): return len(i.x)+1
  def weights(i,l,m):
    if i.y == 1:
      i.w = 1/(2*l) # Y, crater
    else:
      i.w = 1/(2*m) # N, non-crater



def read(files):
  Y, N = 0,0
  rows = []
  path = "../data/features"
  # datafiles = [ join(path,f) for f in listdir(path) if isfile(join(path,f))]
  for data in [join(path,f) for f in files]:
    print(data)
    with open(data,"r") as f:
      line = f.readline() #header, ski\
      for line in f.readlines():
        line = map(float, line.split(","))
        if line[-1] == 1:
          Y +=1
        else:
          N +=1
        rows.append(Row(line))
      map(lambda x:x.weights(Y,N),rows)
  return rows

def changeHeader(f = "./data/features"):
  all_files = [ (join(f,path)) for path in listdir(f) if isfile(join(f,path))]
  for one in all_files:
    content = None
    with open(one,"r") as f:
      pdb.set_trace()
      content = f.readlines()
      header = content[0].split(",")
      newheader = []
      for item in header[:-1]:
        newheader +=["$"+item]
      newheader += ["<"+header[-1]]
      content[0] = ",".join(newheader)

    for row in content:
      with open(one+".csv","a") as f:
        f.write(row)
    # pdb.set_trace()







if __name__ == "__main__":
    changeHeader()