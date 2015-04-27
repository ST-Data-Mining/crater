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


def builder(fname=config.TRAIN_FILE):
  models = dict()
  models["svm"] = svm.builder(fname, kernel="poly")
  models["nn"] = nn.builder(fname, hiddens=250)
  return models

def predictor(models, points):
  ones, zeros = 0,0
  results = []
  consolidated = []
  actuals = []
  predicts,actuals = svm.predictor(models["svm"], points)
  results.append(predicts)
  results.append(nn.predictor(models["nn"], points)[0])
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
  points = parseCSV(config.FEATURES_FOLDER+"3_24.csv", False)
  points += parseCSV(config.FEATURES_FOLDER+"3_25.csv", False)
  classifier = builder(config.TRAIN_FILE)
  predicted, actual = predictor(classifier, points)
  stat = ABCD()
  for p,a in zip(predicted,actual):
    stat.update(p, a)
    print(p, a)
  print(stat)

if __name__=="__main__":
  _runner()