from __future__ import division,print_function
import sys
sys.dont_write_bytecode = True
from sklearn.linear_model import LinearRegression

class Point:
  def __init__(i, features, pos=None, neg=None):
    i.x = features[:-1]
    i.y = features[-1]
    if pos and neg:
      i.w = 0.5/pos if i.y == 1 else 0.5/neg
    else :
      i.w = 0
  def updateWeight(i, pos, neg):
    if i.y == 1:
      i.w = 0.5/pos
    else:
      i.w = 0.5/neg
      
class WeakClassifier:
  def __init__(i, points, index):
    i.x = [[point.x[index]] for point in points]
    i.y = [point.y for point in points]
    i.w = [point.w for point in points]
    i.index = index
    i.size = len(points)
    i.error = None
    i._classifier = None
    i.train()
  def train(i):
    if not i._classifier:
      i._classifier = LinearRegression()
      i._classifier.fit(i.x, i.y)
  def trainError(i):
    if not i.error:
      i.error = sum([i.w[j]*abs(i.predict(i.x[j])- i.y[j]) for j in range(0,i.size)])
    return i.error
  def predict(i, inp):
    attr = inp if (len(inp) == 1) else [inp[i.index]]
    return round(i._classifier.predict(attr))
  def __repr__(i):
    return "Single Node Decision Tree" + "\n\t Index = " + str(i.index) + "\n\t Training Error = " + str(i.trainError())
  
  
def say(*lst): 
  print(*lst,end="")
  sys.stdout.flush()