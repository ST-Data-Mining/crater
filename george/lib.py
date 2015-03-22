from __future__ import division,print_function
import sys
sys.dont_write_bytecode = True
from sklearn.linear_model import LinearRegression

class o():
  def __init__(i,**fields):
    i.override(fields)
  def override(i, d):
    i.__dict__.update(d)
    return i
  def __getattr__(i, field):
    return i.__dict__[field]
  def __setattr__(i, field, value):
    i.__dict__[field] = value
  def __repr__(i):
    d = i.__dict__
    name = i.__class__.__name__
    return name+'{'+' '.join([':%s %s' % (k, pretty(d[k]))
                              for k in i.show()]) + '}'

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
  
class StrongClassifier:
  def __init__(i, mu, T, weaks=[], alphas=[]):
    i.mu, i.T, i.weaks, i.alphas = mu, T, weaks, alphas
  def update(i, weak, alpha):
    i.weaks.append(weak)
    i.alphas.append(alpha)
  def __repr__(i):
    rep ="****Strong Classifier****\n"
    rep += "=========================\n"
    for t in range(i.T):
      rep += str(t+1)+ ") alpha = " + str(i.alphas[t])+"\n"
      rep += i.weaks[t].__repr__()
      rep += "\n\n"
    return rep
  def predict(i, inp):
    LHS = sum([i.alphas[t] * i.weaks[t].predict(inp) for t in range(0,i.T)])
    RHS = i.mu * sum(i.alphas)
    if LHS > RHS:
      return  1
    return 0

class ABCD:
  def __init__(i):
    i.TP, i.FP, i.FN, i.TN = 0, 0, 0, 0
  def __repr__(i):
    rep = "**** Statistics ****\n"
    rep += "True  Non-Crater : " + str(i.TP) + "\n"
    rep += "False Non-Crater : " + str(i.FP) + "\n"
    rep += "False Crater     : " + str(i.FN) + "\n"
    rep += "True  Crater     : " + str(i.TN) + "\n"
    return rep
  def update(i, pred, act):
    if pred == 1 and act == 1:
      i.TP += 1
    elif pred == 1 and act == 0:
      i.FP += 1
    elif pred == 0 and act == 1:
      i.FN += 1
    elif pred == 0 and act == 0:
      i.TN += 1

def say(*lst): 
  print(*lst,end="")
  sys.stdout.flush()