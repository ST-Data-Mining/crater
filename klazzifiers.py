from __future__ import division,print_function
import sys
import math
sys.dont_write_bytecode = True
from lib import *
from expts.csvParser import parseCSV
import config


def normalize_points(points):
  if not len(points): return
  tot = sum([point.w for point in points])
  for point in points:
    point.w = point.w/tot
  
def best_weak_classifier(points, attrLen):
  best_c = None
  for i in range(0,attrLen):
    say('.')
    classifier = WeakClassifier(points, i)
    if (not best_c) or (classifier.trainError() < best_c.trainError()):
      best_c = classifier
  return best_c

def booster(fname):
  points = parseCSV(fname)
  T = int(math.ceil(len(points)*0.01))
  for t in range(0,T):
    normalize_points(points)
    weak_classifier = best_weak_classifier(points, len(points[0].x))
    # TODO update weights
    # TODO create 'alpha' and 'beta' list
    print(weak_classifier)
    return
  # TODO compute strong classifier

def greedy(fname):
  # TODO implement greedy algorithm
  pass

def transfer(fname):
  # TODO implement transfer learner algorithm
  pass



if __name__=="__main__":
  booster(config.TRAIN_FILE)