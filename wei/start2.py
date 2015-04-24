# __author__ = 'WeiFu'
from __future__ import division
from settings import *
from os import listdir
from main import *
from time import strftime
from sk import *
from de import *
from cart_de import *
from rf_de import *


class Learner(object):
  def __init__(i, learner, dataname, train, tune, test):
    i.learner = learner
    i.dataname = dataname
    i.train = train
    i.tune = tune
    i.test = test
    # i.pd = {}
    # i.pf = {}
    # i.prec = {}
    # i.f = {}
    # i.g = {}
    # i.stat = [i.pd, i.pf, i.prec, i.f, i.g]

  def untuned(i):
    The.data.predict = i.test
    The.data.train = i.train
    i.default()
    score = i.call()
    return score
    # i.keep(score)

  def tuned(i):
    The.data.predict = i.tune
    The.data.train = i.train
    The.option.tunning = True
    i.optimizer()
    The.option.tunning = False
    The.data.predict = i.test
    score = i.call()
    return score
    # i.keep(score)

  def call(i):
    raise NotImplementedError

  def optimizer(i):
    raise NotImplementedError

  def default(i):
    raise NotImplementedError


class Where(Learner):
  global The

  def default(i):
    The.option.baseLine = True
    The.tree.infoPrune = 0.33
    The.option.threshold = 0.5
    The.tree.min = 4
    The.option.minSize = 0.5  # min leaf size
    The.where.depthMin = 2  # no pruning till this depth
    The.where.depthMax = 10  # max tree depth
    # The.where.wriggle = 0.2    #  set this at init()
    The.where.prune = False  # pruning enabled?
    The.tree.prune = True

  def call(i): return main()

  def optimizer(i): de()


class CART(Learner):
  global The

  def default(i):
    # The.classifier.cart = True
    The.cart.criterion = "entropy"
    The.cart.max_features = 0.76
    The.cart.max_depth = 11
    The.cart.min_samples_split = 2
    The.cart.min_samples_leaf = 20
    The.option.threshold = 1

  # The.cart.random_state = 0
  def call(i): return cart()

  def optimizer(i): cart_de()


class RF(Learner):
  global The

  def default(i):
    # The.classifier.rf = True
    The.option.threshold = 0.8
    The.rf.max_features = 0.52
    The.rf.min_samples_split = 5
    The.rf.min_samples_leaf = 4
    The.rf.max_leaf_nodes = 16
    The.rf.n_estimators = 129

  def call(i): return rf()

  def optimizer(i): rf_de()





def start(path="./data"):
  def keep(learner, score):  # keep stats from run
    NDef = learner + ": N-Def"
    YDef = learner + ": Y-Def"
    for j, s in enumerate(lst):
      s[NDef] = s.get(NDef, []) + [(float(score[0][j] / 100))]
      s[YDef] = s.get(YDef, []) + [(float(score[1][j] / 100))]  # [YDef] will void to use myrdiv.

  def printResult(dataname):
    def myrdiv(d):
      stat = []
      for key, val in d.iteritems():
        val.insert(0, key)
        stat.append(val)
      return stat
    print "\n" + "+" * 20 + "\n DataSet: " + dataname + "\n" + "+" * 20
    for j, k in enumerate(["pd", "pf", "prec", "f", "g"]):
      print "\n" + "*" * 10 + k + "*" * 10
      rdivDemo(myrdiv(lst[j]))
    print "End time :" + strftime("%Y-%m-%d %H:%M:%S") + "\n" * 2

  random.seed(10)
  global The
  The.option.tunedobjective = 3  # 0->pd, 1->pf,2->prec, 3->f, 4->g
  objectives = {0: "pd", 1: "pf", 2: "prec", 3: "f", 4: "g"}
  folders = [f for f in listdir(path) if not isfile(join(path, f))]
  for folder in folders[2:3]:
    nextpath = join(path, folder)
    data = [join(nextpath, f) for f in listdir(nextpath) if isfile(join(nextpath, f))]
    for i in range(len(data)):
      pd, pf, prec,F, g = {},{},{},{},{}
      lst = [pd,pf,prec,F,g]
      expname = folder + "V" + str(i)
      try:
        predict = data[i + 2]
        tune = data[i + 1]
        train = [data[i]]
      except IndexError, e:
        print folder + " done!"
        break
      print objectives[The.option.tunedobjective] + " as the objective\n" + "Begin time :" + strftime(
        "%Y-%m-%d %H:%M:%S")
      # ##WHERE
      for model in [Where, CART, RF]:
        timeout = time.time()
        name = "Tuned_" + model.__name__
        thislearner = model(name, folder, train, tune, predict)
        keep(name,thislearner.tuned())
        print "Tuned_" + model.__name__ + "Running Time:" + str(time.time() - timeout)
        timeout = time.time()
        name = "Naive_" + model.__name__
        keep(name,thislearner.untuned())
        print "Naive_" + model.__name__ + "Running Time:" + str(time.time() - timeout)
      printResult(expname)
      # pdb.set_trace()


if __name__ == "__main__":
  eval(cmd())