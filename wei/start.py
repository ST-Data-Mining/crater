from __future__ import division
import sys
from os import listdir
from table import *
from os.path import isfile, join
from settings import *
from de import *
from cart_de import * # comment this if using scikitlearn 
from rf_de import *
from sk import *
from time import strftime
import pdb

def myrdiv(d):
  def pre(dist):
    l=dist.items()[0][-1]
    k = dist.items()[0][0]
    return [k].extend(l)
  stat = []
  for key,val in d.iteritems():
    val.insert(0,key)
    stat.append(val)
  return stat

def createfile(objective):
  The.option.resultname = '/Users/WeiFu/Google Drive/myresult'+ strftime("%Y-%m-%d %H:%M:%S")+objective
  f = open(The.option.resultname,'w').close()

def writefile(s):
  # print s
  # pdb.set_trace()
  global The
  f = open(The.option.resultname, 'a')
  f.write(s+'\n')
  f.close()


def start(path="./data/features"):
  def bigt(tbl):
    if isinstance(tbl, list):
      t = tbl[0]
      for i in range(1, len(tbl)):
        t._rows += tbl[i]._rows
    else:
      t = tbl
    return t
  def saveSat(score,dataname):
    class1 = dataname +": N-Def"
    class2 = dataname +": Y-Def"
    name = [pd,pf,prec,F,g]
    for i, s in enumerate(name):
      s[class1]= s.get(class1,[])+[float(score[0][i]/100)]
      s[class2]= s.get(class2,[])+[float(score[1][i]/100)]

  def printresult(dataset):
    print "\n" + "+" * 20 + "\n DataSet: "+dataset + "\n" + "+" * 20
    for i, k in enumerate(["pd", "pf","prec","f","g"]):
        # pdb.set_trace()
        express = "\n"+"*"*10+k+"*"*10
        # print express
        writefile(express)
        rdivDemo(myrdiv(lst[i]))
    writefile("End time :" +strftime("%Y-%m-%d %H:%M:%S"))
    # print "End time :" +strftime("%Y-%m-%d %H:%M:%S")
    writefile("\n"*2)
    print "\n"

  def predicttest(predict, testname):
    for i in xrange(1):
      The.data.predict = predict
      score = main()
      print "one more ~"
      saveSat(score, testname)

  def cart_predicttest(predict, testname):
    for i in xrange(1):
      The.data.predict = predict
      score = cart()
      saveSat(score, testname)
  def tunetest(predict):
    de()
    The.option.tuning = False
    predicttest(predict,"Tuned_WHERE")

  def basetest(predict):
    The.option.baseLine = True
    The.tree.infoPrune = 0.33
    The.option.threshold = 0.5
    The.tree.min = 4
    The.option.minSize  = 0.5    # min leaf size
    The.where.depthMin= 2      # no pruning till this depth
    The.where.depthMax= 10     # max tree depth
    # The.where.wriggle = 0.2    #  set this at init()
    The.where.prune   = False   # pruning enabled?
    The.tree.prune = True
    The.option.tuning = False
    predicttest(predict, "Naive_WHERE")

  def cart_tunetest(predict):
    The.classifier.carttuned = True
    cart_de()
    # The.cart.max_features = 0.01
    # The.cart.min_samples_split = 18
    # The.cart.min_samples_leaf = 3
    # The.option.threshold = 0.83
    # The.cart.max_depth = 1
    The.option.tuning = False
    cart_predicttest(predict,"Tuned_Cart")
    The.classifier.carttuned = False


  def cart_basetest(predict):
    The.classifier.cart = True
    The.cart.criterion = "entropy"
    The.cart.max_features = None
    The.cart.max_depth = None
    The.cart.min_samples_split = 2
    The.cart.min_samples_leaf = 1
    # The.cart.max_leaf_nodes = None
    The.option.threshold = 0.5
    The.cart.random_state = 0
    cart_predicttest(predict, "Naive_Cart")
    The.classifier.cart = False

  def rf_tunetest(predict):
    The.classifier.rftuned = True
    rf_de()
    # The.option.threshold = 0.99
    # The.rf.max_features = 0.18
    # The.rf.min_samples_split = 1
    # The.rf.min_samples_leaf = 3
    # The.rf.n_estimators = 85
    # The.rf.max_leaf_nodes = 24
    The.option.tuning = False
    cart_predicttest(predict,"Tuned_RFst")
    The.classifier.rftuned = False

  def rndfsttest(predict):
    The.classifier.rf = True
    The.option.threshold = 0.5
    The.rf.max_features = "auto"
    The.rf.min_samples_split = 2
    The.rf.min_samples_leaf = 1
    The.rf.max_leaf_nodes = None
    The.rf.n_estimators = 100
    cart_predicttest(predict, "Naive_RFst")
    The.classifier.rf = False


  global The
  The.option.tunedobjective = 3 # 0->pd, 1->pf,2->prec, 3->f, 4->g
  objectives = {0:"pd", 1:"pf", 2:"prec", 3:"f", 4:"g"}
  createfile(objectives[The.option.tunedobjective])
  data = [join(path, f)
          for f in listdir(path) if isfile(join(path, f))]
  pdb.set_trace()
  for i in range(len(data)):
    The.option.actualpredicted = "result_"+data[i][data[i].find("/",10,-1)+1:]
    pdb.set_trace()
    random.seed(1)
    pd, pf, prec,F, g = {},{},{},{},{}
    lst = [pd,pf,prec,F,g]
    try:
      predict = data[i]
      train = [data[4]] # training data set 3_24.csv
    except IndexError, e:
      print " done!"
      break
    The.data.predict = predict
    The.data.train = train
    The.option.baseLine = False
    writefile(objectives[The.option.tunedobjective]+ " as the objective\n"+"Begin time :" + strftime("%Y-%m-%d %H:%M:%S"))
    timeout = time.time()
    basetest(predict)
    writefile("Naive_Where Running Time: " + str(time.time()-timeout))
  #CART
    # timeout = time.time()
    # The.data.predict = tune_predict # chage the tune predict set for cart tuning
    # cart_tunetest(predict)
    # writefile("Tuned_Cart Running Time: " + str(time.time()-timeout))
    # timeout = time.time()
    # cart_basetest(predict)
    # writefile("Naive_Cart Running Time: " + str(time.time()-timeout))
    # timeout = time.time()
    # The.data.predict = tune_predict
    # rf_tunetest(predict)
    # writefile("Tuned_RFst Running Time: " + str(time.time()-timeout))
    # timeout = time.time()
    # rndfsttest(predict)
    # writefile("Naive_RFst Running Time: " + str(time.time()-timeout))
    printresult("data"+str(i))


if __name__ =="__main__":
  eval(cmd())