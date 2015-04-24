from __future__ import division,print_function
from os import environ
import sys
HOME=environ['HOME']
PROJECT_ROOT=HOME+'/Panzer/NCSU/Spatial and Temporal/crater'
EXPTS = PROJECT_ROOT+'/expts'
sys.path.extend([PROJECT_ROOT,EXPTS])
sys.dont_write_bytecode = True

from sklearn.neural_network import BernoulliRBM
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from george.lib import *
from expts.csvParser import parseCSV, randomPoints
import config

def builder(fname = config.TRAIN_FILE, hiddens=256, learn_rate=0.01):
  points = parseCSV(fname, False)
  rbm = BernoulliRBM(n_components=hiddens,learning_rate=learn_rate,n_iter=30,random_state=1)
  logistic = LogisticRegression(C=20)
  clf = Pipeline(steps=[('rbm', rbm), ('logistic',logistic)])
  X, y = [], []
  for point in points:
    X.append(normalize(point.x))
    y.append(point.y)
  clf.fit(X,y)
  return clf

def predictor(classifier, points):
  X,actuals = [], []
  for point in points:
    X.append(normalize(point.x))
    actuals.append(point.y)
  predicts = classifier.predict(X)
  return predicts, actuals

def _runner():
  hiddens = 250
  learn_rate = 0.01
  points = parseCSV(config.FEATURES_FOLDER+"all.csv", False)
  #points += parseCSV(config.FEATURES_FOLDER+"1_25.csv", False)
  classifier = builder(config.TRAIN_FILE, hiddens, learn_rate)
  predicted, actual = predictor(classifier, points)
  stat = ABCD()
  for p,a in zip(predicted,actual):
    stat.update(p, a)
    print(p, a)
  print(stat)

if __name__=="__main__":
  _runner()