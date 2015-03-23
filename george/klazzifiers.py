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
from expts.csvParser import parseCSV, randomPoints
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

def booster(fname, mu=0.525, T=150):

  def updateWeights(classifier, b):
    for p in points:
      predicted = classifier.predict(p.x)
      actual = int(p.y)
      e = 0 if predicted == actual else 1
      p.w *= b**(1-e)

  points = parseCSV(fname)
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
  print("***Boosting Classifier***")
  points = parseCSV(fname)
  strong = booster(fname, T=5)
  stat = ABCD()
  for point in points:
    pred = strong.predict(point.x)
    act = int(point.y)
    stat.update(pred, act)
  print(stat)


def greedy(fname, mu=0.675, T=150):
  points = parseCSV(fname)
  strong = StrongClassifier(mu, T)
  ignores = []
  normalize_points(points)
  for t in range(0, T):
    say(t,' ')
    weak_classifier = best_weak_classifier(points, len(points[0].x), ignores)
    ignores.append(weak_classifier.index)
    error = weak_classifier.trainError()
    beta = error/(1-error)
    if beta == 0:
      strong.T = t
      break
    alpha = math.log(1/beta, 2)
    strong.update(weak_classifier,alpha)
  print('')
  return strong


def _greedy(fname):
  print('***GREEDY CLASSIFIER***')
  points = parseCSV(fname)
  strong = greedy(fname, T=5)
  stat = ABCD()
  for point in points:
    pred = strong.predict(point.x)
    act = int(point.y)
    stat.update(pred, act)
  print(stat)


def transfer(fname, mu=0.5, T=150):
  def craterCount(points):
    count=0
    for point in points:
      if point.y==0: count+=1
    return  count

  def updateWeights(classifier, b, b_t):
    for i, point in enumerate(total):
      predicted = classifier.predict(point.x)
      actual = int(point.y)
      e = 0 if predicted == actual else 1
      if i<len(diff):
        point.w *= b**e
      else:
        point.w *= b_t**-e

  diff = parseCSV(fname)
  same = randomPoints(craters=102, non_craters=153)
  total = diff+same
  craters = craterCount(total)
  non_craters = len(total) - craters
  [p.updateWeight(non_craters, craters) for p in total]
  strong = StrongClassifier(mu, T)
  ignores=[]
  for t in range(0,T):
    say(t,' ')
    normalize_points(total)
    weak_classifier = best_weak_classifier(total[len(diff):], len(total[0].x), ignores)
    ignores.append(weak_classifier.index)
    error = weak_classifier.trainError()
    if error == 0:
      strong.T = t
      break
    beta_t = error/(1-error)
    beta = 1/(1+(2*math.log(len(total)/T))**0.5)
    updateWeights(weak_classifier, beta, beta_t)
    alpha = math.log(1/beta_t)
    strong.update(weak_classifier, alpha)
  print('')
  return strong


def _transfer(fname):
  print('***TL CLASSIFIER***')
  points = parseCSV(fname)
  strong = transfer(fname, T=5)
  stat = ABCD()
  for point in points:
    pred = strong.predict(point.x)
    act = int(point.y)
    stat.update(pred, act)
  print(stat)

if __name__=="__main__":
  #_greedy(config.TRAIN_FILE)
  #_booster(config.TRAIN_FILE)
  _transfer(config.TRAIN_FILE)