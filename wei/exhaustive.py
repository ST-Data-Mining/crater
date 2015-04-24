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
  # The.option.resultname = '/Users/WeiFu/Google Drive/myresult'+ strftime("%Y-%m-%d %H:%M:%S")+objective
  The.option.resultname = '/Users/WeiFu/Google Drive/myresult'+ strftime("%Y-%m-%d %H:%M:%S")+objective
  f = open(The.option.resultname,'w').close()

def writefile(s):
	f = open(The.option.resultname, 'a')
	f.write(s+'\n')
	f.close()


def start(path="./data"):
  def saveSat(score,dataname):
    class1 = dataname +": N-Def"
    class2 = dataname +": Y-Def"
    name = [pd,pf,prec,F,g]
    for i, s in enumerate(name):
      # s[class1]= s.get(class1,[])+[float(score[0][i]/100)]
      s[class2]= s.get(class2,[])+[float(score[1][i]/100)]

  def printresult(dataset):
    print "\n" + "+" * 20 + "\n DataSet: "+dataset + "\n" + "+" * 20
    for i, k in enumerate(["pd", "pf","prec","f","g"]):
        # pdb.set_trace()
        express = "\n"+"*"*10+k+"*"*10
        print express
        writefile(express)
        rdivDemo(myrdiv(lst[i]))
    writefile("End time :" +strftime("%Y-%m-%d %H:%M:%S"))
    writefile("\n"*2)
    print "\n"

  def predicttest(predict, testname):
    for i in xrange(1):
      The.data.predict = predict
      score = main()
      saveSat(score, testname)
  
  def cart_predicttest(predict, testname):
    for i in xrange(1):
      The.data.predict = predict
      score = cart()
      writefile(str(score[1]))
      # saveSat(score, testname)
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
    cart_ex()
    # The.option.tuning = False
    # cart_predicttest(predict,"Tuned_Cart")
    # The.classifier.carttuned = False


  def cart_basetest(predict):
    The.classifier.cart = True
    The.cart.criterion = "entropy"
    The.cart.max_features = None
    The.cart.max_depth = None
    The.cart.min_samples_split = 2
    The.cart.min_samples_leaf = 1
    # The.cart.max_leaf_nodes = None
    The.cart.threshold = 0.5
    The.cart.random_state = 0
    cart_predicttest(predict, "Naive_Cart")
    The.classifier.cart = False

  def rf_tunetest(predict):
    The.classifier.rftuned = True
    rf_ex()
    The.option.tuning = False
    cart_predicttest(predict,"Tuned_RFst")
    The.classifier.rftuned = False

  def rndfsttest(predict):
    The.classifier.rf = True
    The.rf.threshold = 0.5
    The.rf.max_features = "auto",
    The.rf.min_samples_split = 2,
    The.rf.min_samples_leaf = 1,
    The.rf.max_leaf_nodes = None,
    The.rf.n_estimators = 100,
    cart_predicttest(predict, "Naive_RFst")
    The.classifier.rf = False
  def cart_ex():
    count=1
    for a in [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]:
      for b in range(1,50,3):
        for c in range(2,20,2):
          for d in range(1,20,2):
            for e in [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]:
              The.classifier.carttuned = True
              global The
              The.cart.max_features = a
              The.cart.max_depth = b
              The.cart.min_samples_split = c
              The.cart.min_samples_leaf = d
              The.option.threshold = e # use the.option.threshold
              writefile("a: "+str(a)+"b:"+str(b)+"c: "+str(c)+"d: "+str(d)+"e: "+str(e))
              count +=1
              print str(count)+" ",
              The.option.tuning = False
              cart_predicttest(predict,"Tuned_Cart")
              The.classifier.carttuned = False


  random.seed(10)
  global The
  The.option.tunedobjective = 0 # 0->pd, 1->pf,2->prec, 3->f, 4->g
  objectives = {0:"pd", 1:"pf", 2:"prec", 3:"f", 4:"g"}
  createfile(objectives[The.option.tunedobjective])
  folders = [f for f in listdir(path) if not isfile(join(path, f))]
  for one in folders[4:]:
    nextpath = join(path, one)
    data = [join(nextpath, f)
            for f in listdir(nextpath) if isfile(join(nextpath, f))]
    for i in range(len(data)):
      pd, pf, prec,F, g = {},{},{},{},{}
      lst = [pd,pf,prec,F,g]
      dataname = one +"V"+str(i)
      try:
        predict = data[i+2]
        tune_predict = data[i+1]
        train = [data[i]]
      except IndexError, e:
        print one+" done!"
        break
      # print train, tune_predict, predict, dataname
      # predict = data.pop(-1)
      # tune_predict = data.pop(-1)
      # train = [data.pop(-1)]
      The.data.predict = tune_predict
      The.data.train = train
      The.option.baseLine = False
      writefile(objectives[The.option.tunedobjective]+ " as the objective\n"+"Begin time :" + strftime("%Y-%m-%d %H:%M:%S"))
      writefile("Dataset: "+dataname)
    ## WHERE
      # timeout = time.time()
      # tunetest(predict)
      # writefile("Tuned_Where Running Time: " + str(time.time()-timeout))
      # timeout = time.time()
      # basetest(predict)
      # writefile("Naive_Where Running Time: " + str(time.time()-timeout))
    #CART
      timeout = time.time()
      print "Tuned_cart"
      The.data.predict = tune_predict # chage the tune predict set for cart tuning
      cart_tunetest(predict)
      writefile("Tuned_Cart Running Time: " + str(time.time()-timeout))
      # timeout = time.time()
      # print "Naive_cart"
      # cart_basetest(predict)
      # writefile("Naive_Cart Running Time: " + str(time.time()-timeout))
      # timeout = time.time()
      The.data.predict = tune_predict
      print "Tuned_rf"
      rf_tunetest(predict)
      writefile("Tuned_RFst Running Time: " + str(time.time()-timeout))
      # timeout = time.time()
      # print "Naive_rf"
      # rndfsttest(predict)
      # writefile("Naive_RFst Running Time: " + str(time.time()-timeout))
      printresult(dataname)



if __name__ =="__main__":
	eval(cmd()) 