from __future__ import division,print_function
from os import environ
import sys
HOME=environ['HOME']
PROJECT_ROOT=HOME+'/Panzer/NCSU/Spatial and Temporal/crater'
EXPTS = PROJECT_ROOT+'/expts'
sys.path.extend([PROJECT_ROOT,EXPTS])
sys.dont_write_bytecode = True
from george.lib import *
from expts.csvParser import parseCSV, randomPoints
import config


def normalize_points(points):
  if not len(points): return
  tot = sum([point.w for point in points])
  for point in points:
    point.w = point.w/tot
  
def best_weak_classifier(points, attrLen, ignores=None, start=0):
  best_c = None
  if not ignores: ignores = []
  for i in range(0,attrLen):
    if i in ignores:
      continue
    classifier = WeakClassifier(points, i)
    if (not best_c) or (classifier.trainError(start) < best_c.trainError(start)):
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
    say(t+1, ' ')
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


def _booster(fname, T=150):
  print('***BOOSTER CLASSIFIER***')
  boost_classifier = booster(fname, T=T)
  #print(boost_classifier)
  for region,test_files in [('west',['1_24.csv','1_25.csv']), ('center',['2_24.csv','2_25.csv']),
                            ('east',['3_24.csv','3_25.csv']), ('all',['all.csv']) ]:
    points = parseCSV(config.FEATURES_FOLDER+test_files[0], False)
    if len(test_files) > 1:
      points += parseCSV(config.FEATURES_FOLDER+test_files[1], False)

    stat = ABCD()
    for point in points:
      pred = boost_classifier.predict(point.x)
      act = int(point.y)
      stat.update(pred, act)
    print('\n'+region)
    print(stat)


def greedy(fname, mu=0.675, T=150):
  points = parseCSV(fname)
  strong = StrongClassifier(mu, T)
  ignores = []
  normalize_points(points)
  for t in range(0, T):
    say(t+1,' ')
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


def _greedy(fname, T=150):
  print('***GREEDY CLASSIFIER***')
  greedy_classifier = greedy(fname, T=T)
  #print(greedy_classifier)
  for region,test_files in [('west',['1_24.csv','1_25.csv']), ('center',['2_24.csv','2_25.csv']),
                            ('east',['3_24.csv','3_25.csv']), ('all',['all.csv']) ]:
    points = parseCSV(config.FEATURES_FOLDER+test_files[0], False)
    if len(test_files) > 1:
      points += parseCSV(config.FEATURES_FOLDER+test_files[1], False)

    stat = ABCD()
    for point in points:
      pred = greedy_classifier.predict(point.x)
      act = int(point.y)
      stat.update(pred, act)
    print('\n'+region)
    print(stat)


def transfer(fname, sameFiles, mu=0.5, T=150):
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

  diff = parseCSV(fname, False)
  same = randomPoints(sameFiles, craters=102, non_craters=153)
  total = diff+same
  craters = craterCount(total)
  non_craters = len(total) - craters
  [p.updateWeight(non_craters, craters) for p in total]
  strong = StrongClassifier(mu, T)
  ignores=[]
  for t in range(0,T):
    say(t+1,' ')
    normalize_points(total)
    weak_classifier = best_weak_classifier(total, len(total[0].x), ignores, len(diff))
    ignores.append(weak_classifier.index)
    error = weak_classifier.trainError(start=len(diff))
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


def _transfer(fname, T=150):
  print('***TRANSFER CLASSIFIER***')

  #print(tl_classifier)
  for region,test_files in [('west',['1_24.csv','1_25.csv']), ('center',['2_24.csv','2_25.csv']),
                            ('east',['3_24.csv','3_25.csv']), ('all',['all.csv']) ]:
    tl_classifier = transfer(fname, test_files, T=T)
    points = parseCSV(config.FEATURES_FOLDER+test_files[0], True)
    if  len(test_files) > 1:
      points += parseCSV(config.FEATURES_FOLDER+test_files[1], True)

    stat = ABCD()
    for point in points:
      pred = tl_classifier.predict(point.x, True)
      act = int(point.y)
      stat.update(pred, act)
    print('\n'+region)
    print(stat)

def _runner(T=150):
  train = config.TRAIN_FILE
  _booster(train,T)
  _greedy(train,T)
  _transfer(train,T)


if __name__=="__main__":
  _runner()
