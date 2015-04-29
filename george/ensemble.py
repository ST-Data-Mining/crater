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
import svm
import nn
import random
import klazzifiers


def builder(fname=config.TRAIN_FILE, test_files=None):
  models = dict()
  models["svm"] = svm.builder(fname, kernel="poly")
  models["nn"] = nn.builder(fname, hiddens=250)
  models["greedy"] = klazzifiers.greedy(fname)
  models["boost"] = klazzifiers.booster(fname)
  models["transfer"] = klazzifiers.transfer(fname, test_files)
  return models

def predictor(models, points):
  results = []
  consolidated = []
  actuals = []
  predicts,actuals = svm.predictor(models["svm"], points)
  results.append(predicts)
  results.append(nn.predictor(models["nn"], points)[0])
  results.append([models["greedy"].predict(point.x) for point in points])
  results.append([models["boost"].predict(point.x) for point in points])
  results.append([models["transfer"].predict(point.x) for point in points])
  for i in range(len(results[0])):
    ones, zeros = 0,0
    for j in range(len(results)):
      if (results[j][i] == 0):
        zeros +=1
      elif (results[j][i] == 1):
        ones +=1
    if zeros > ones:
      consolidated.append(0)
    elif ones > zeros:
      consolidated.append(1)
    else:
      consolidated.append(random.choice([0,1]))
  return consolidated, actuals

def _runner():
  test_files=['all.csv']
  points = parseCSV(config.FEATURES_FOLDER+test_files[0], False)
  #points += parseCSV(config.FEATURES_FOLDER+test_files[1], False)
  classifier = builder(config.TRAIN_FILE, test_files)
  predicted, actual = predictor(classifier, points)
  stat = ABCD()
  for p,a in zip(predicted,actual):
    stat.update(p, a)
    print(p, a)
  print(stat)

if __name__=="__main__":
  _runner()