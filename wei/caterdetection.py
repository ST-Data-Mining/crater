#__author__ = 'FuWei'
from __future__ import print_function, division
import sys
from os.path import isfile, join
from os import listdir
import pdb
from sklearn.tree import DecisionTreeClassifier
from data import *
import math

class WeakClassifier(object):
  def __init__(i, trainrows, testrows, indep):
    i.x =[ [row.x[indep]]for row in trainrows]
    i.y =[ row.y for row in trainrows]
    i.w =[ row.w for row in trainrows]
    i.test = [[row.x[indep]] for row in testrows]
    i.classifier = None
    i.err = None
    i.indep = indep # index, the selected feature
    i.predict_result = None
    i.fit()
  def fit(i):
    if not i.classifier:
      i.classifier = DecisionTreeClassifier(max_depth = 1,random_state = 1)
      i.classifier.fit(i.x, i.y)
  def predict(i, test= None):
    # pdb.set_trace()
    i.predict_result = i.classifier.predict(test)
    return i.predict_result
  def trainErr(i):
    sumt =0
    i.err = sum(abs(i.w[j]*val - i.y[j]) for j,val in enumerate(i.predict(i.test)))
    for j, val in enumerate(i.predict(i.test)):
      sumt+= i.w[j]*abs(val -i.y[j])
    return sumt
  def __repr__(i):
    return " index = " +str(i.indep) +"training error = " + str(i.err)


class StrongClassifier(object):
  def __init__(i, T = 100, mu = 0.65, weak = None, alpha = None):
    i.weak = weak
    i.alpha = alpha
    i.T = T
    i.mu = mu
  def predict(i,test):
    predicted = []
    for one in test: # here, one is not tested, not sure.
      L = sum([i.alpha[j]* i.weak[j].predict([one.x[i.weak[j].indep]]) for j in range(i.T)])
      R = i.mu * sum(i.alpha)
      if L >= R:
        predicted.append(1)
      else:
        predicted.append(0)
    return predicted

class abcd():
  def __init__(i, region):
    i.TP, i.TN, i.FP, i.FN = 0,0,0,0
    i.pd, i.pf, i.prec, i.F, i.G = 0,0,0,0,0
    i.region = region
  def report(i,predicted,actual):
    for p, a in zip(predicted, actual):
      if a == p ==1: # crater
        i.TP += 1
      elif a == 1 and p == 0:
        i.FN += 1
      elif a == 0 and p == 1:
        i.FP += 1
      elif a == 0 and p == 0:
        i.TN +=1
    i.pd = i.TP/(i.TP +i.FN+0.001)
    i.pf = i.FP/(i.TP +i.FP+0.001)
    i.prec = i.TP/(i.TP+i.FP+0.001)
    i.F = 2*i.pd*i.prec/(i.pd + i.prec + 0.001)
    i.G = 2*i.pd*(1 - i.pf)/(i.pd +1-i.pf + 0.001)
  def __repr__(i):
    out = "="*20+i.region+"="*20 + "\n"
    out += "Total: " + str((i.TP+i.TN+i.FP+i.FN)) + "\n"
    out += "Precision: "+str(i.prec) + "\n"
    out += "Pd: "+str(i.pd) + "\n"
    out += "F: "+str(i.F) +"\n"
    out += "G: "+str(i.G)+"\n"
    return out

    # header = (' {0:4s}  {1:4s} {2:4s} '+ \
    #        '{3:4s}{4:4s} {5:3s} {6:3s} {7:3s} '+ \
    #        '{8:3s} {9:3s}{10:3s}{11:10s}').format(
    #  "n", "TP","TN","FP","FN","acc","pd","pf","prec",
    #   "f","g","class") +"\n"
    # delimit = '-'*80 +"\n"
    # acc = (i.TP+i.TN)*100/(i.TP+i.TN+i.FP+i.FN+0.001)
    # crater = (' {0:4f}  {1:4f} {2:4f} '+ \
    #        '{3:4f} {4:4f} {5:3f} {6:3f} {7:3f} '+ \
    #        '{8:3f} {9:3f} {10:3f} {11:10s}').format(
    #  round(i.TP+i.FN,2), round(i.TP,2),round(i.TN,2),round(i.FP,2),round(i.FN,2),round(acc,2),round(i.pd*100,2),round(i.pf*100,2),round(i.prec*100,2),\
    #  round(i.F*100,2),round(i.G*100,2),"cater") +"\n"
    # pd = (i.TP+i.TN)*100/(i.TP+i.TN+i.FP+i.FN+0.001)
    # pf = (i.TN/(i.TP+i.TN + 0.001))*100
    # prec = (i.FN/(i.TN+i.FN+0.001))*100
    # F = 2* pd*prec/(pd+prec+0.001)
    # G = 2* pd*(1-pf)/(pd+1-pf+0.001)
    # noncrater = (' {0:2f}  {1:4f} {2:4f} '+ \
    #        '{3:4f} {4:4f} {5:3f} {6:3f} {7:3f} '+ \
    #        '{8:3f} {9:3f} {10:3f} {11:10s}').format(
    #  round(i.TN+i.FP,2), round(i.TN,2),round(i.TP,2),round(i.FN,2),round(i.FP,2),round(pd,2),round(pf,2),round(acc,2),\
    #  round(prec,2), round(F,2), round(G,2),"non-crater" )+"\n"
    # return header+delimit+crater+noncrater

def norm(rows):
  if len(rows)== 0: return
  sumW = sum([row.w for row in rows])
  for i, row in enumerate(rows):
    rows[i].w = rows[i].w/sumW

def bestWeaker(rows):
  bestTrainErr = 10^5
  best_classifier = None
  for i in range(len(rows[0])-1):
    classifier = WeakClassifier(rows[:],rows[:],i)
    trainErr = classifier.trainErr()
    if trainErr < bestTrainErr:
      best_classifier = classifier
      bestTrainErr = trainErr
      print(bestTrainErr)
  return best_classifier, classifier.predict_result

def updateWeights(rows, beta, predicted):
  for i, r in enumerate(rows):
    e = 0 if r.y == predicted[i] else 1 # 0: correctly predict 1: wrong
    r.w *= beta**(1-e)

def boost():
  T = 50
  mu = 0.525
  alpha = []
  weak = []
  rows = read(['3_24.csv'])
  for _ in range(T):
    norm(rows)
    best_weak_classifier, predict_result = bestWeaker(rows)
    best_err = best_weak_classifier.trainErr()
    beta = best_err/(1-best_err)
    updateWeights(rows, beta, predict_result)
    alpha.append(math.log(1/beta))
    weak.append(best_weak_classifier)
  strong = StrongClassifier(T,mu,weak,alpha)
  return strong

def booster():
  print('========== #Booster# ========')
  boost_classifier = boost()
  test = {'west':['1_24.csv','1_25.csv'],'central':['2_24.csv','2_25.csv'],'east':['3_24.csv','3_25.csv'],'all':['all.csv']}
  for region,files in test.iteritems():
    rows =read(files)
    # pdb.set_trace()
    predicted = boost_classifier.predict(rows)
    stat = abcd(region)
    actual = [r.y for r in rows] #
    stat.report(predicted, actual)
    print(stat)






if __name__ == "__main__":
  booster()
  # test1 = read()
  # X = WeakClassifier(test1[:-30],test1[-30:],1)
  # print(X.trainErr())
  # Y  =X.predict(test1)
  # print(Y)
