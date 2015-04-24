from __future__ import division,print_function
from os import environ
import sys
HOME=environ['HOME']
PROJECT_ROOT=HOME+'/Panzer/NCSU/Spatial and Temporal/crater'
EXPTS = PROJECT_ROOT+'/expts'
sys.path.extend([PROJECT_ROOT,EXPTS])
sys.dont_write_bytecode = True
from sklearn.svm import SVC
from george.lib import *
from expts.csvParser import parseCSV, randomPoints
import config


def builder(fname = config.TRAIN_FILE, kernel="rbf"):
  points = parseCSV(fname, False)
  clf = SVC(kernel=kernel)
  X, y = [], []
  for point in points:
    X.append(point.x)
    y.append(point.y)
  clf.fit(X,y)
  return clf

def predictor(classifier, points):
  X,actuals = [], []
  for point in points:
    X.append(point.x)
    actuals.append(point.y)
  predicts = classifier.predict(X)
  return predicts, actuals


def _runner():
  kernel = "poly"
  points = parseCSV(config.FEATURES_FOLDER+"all.csv", False)
  #points += parseCSV(config.FEATURES_FOLDER+"1_25.csv", False)
  classifier = builder(config.TRAIN_FILE, kernel)
  predicted, actual = predictor(classifier, points)
  stat = ABCD()
  for p,a in zip(predicted,actual):
    stat.update(p, a)
    print(p, a)
  print(stat)

if __name__=="__main__":
  _runner()