from __future__ import division,print_function
from os import environ
import sys
HOME=environ['HOME']
PROJECT_ROOT=HOME+'/Panzer/NCSU/Spatial and Temporal/crater'
EXPTS = PROJECT_ROOT+'/expts'
sys.path.extend([PROJECT_ROOT,EXPTS])
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
  
def best_weak_classifier(points, attrLen, ignores=[]):
  best_c = None
  for i in range(0,attrLen):
    if i in ignores:
      continue
    classifier = WeakClassifier(points, i)
    if (not best_c) or (classifier.trainError() < best_c.trainError()):
      best_c = classifier
  return best_c

def booster(fname, mu=0.525, sample=50):

  def updateWeights(classifier, b):
    for p in points:
      predicted = classifier.predict(p.x)
      actual = int(p.y)
      e = 0 if predicted == actual else 1
      p.w *= b**(1-e)

  points = parseCSV(fname)
  #T = int(math.ceil(len(points)*sample))
  T=sample
  strong = StrongClassifier(mu, T)
  ignores = []
  for t in range(0,T):
    say(t, ' ')
    normalize_points(points)
    weak_classifier = best_weak_classifier(points, len(points[0].x), ignores)
    ignores.append(weak_classifier.index)
    error = weak_classifier.trainError()
    beta = error/(1-error)
    if beta == 0:
      strong.T = t
      break
    updateWeights(weak_classifier, beta)
    alpha = math.log(1/beta, 2)
    strong.update(weak_classifier,alpha)
  print('')
  return strong


def _booster(fname):
  points = parseCSV(fname)
  strong = booster(fname, sample=5)
  stat = ABCD()
  for point in points:
    pred = strong.predict(point.x)
    act = int(point.y)
    stat.update(pred, act)
  print(stat)

def greedy(fname):
  # TODO implement greedy algorithm
  pass

def transfer(fname):
  # TODO implement transfer learner algorithm
  pass

if __name__=="__main__":
  _booster(config.TRAIN_FILE)