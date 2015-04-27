from __future__ import division
import random, pdb 
# from main import *
from base import *
from start import *
from rf_cart_prediction import *

# global The

def r(low,high, prec = 2):
  return round(random.uniform(low,high) ,prec)

def ig(low, high):
  return int(random.uniform(low,high))

# def treat(lst):
#   if lst[4]<=lst[5] and lst[-1]: # where prune is true, lst[4] should > lst[5]
#     lst[4] = ig(Settings.de.limit[4])
#     lst[5] = ig(Settings.de.limit[5])
#     lst =treat(lst)
#   return lst

def assign(i):
  global The
  The.cart.max_features = i[0]
  The.cart.max_depth = i[1]
  The.cart.min_samples_split = i[2]
  The.cart.min_samples_leaf = i[3]
  # The.cart.max_leaf_nodes = i[4]
  The.option.threshold = i[4] # use the.option.threshold
  The.cart.random_state = i[5]



def generate():
  candidates = [r(l,h) if isinstance(l, float) else ig(l,h)for l,h in zip(Settings.de.cartLimit_Min, Settings.de.cartLimit_Max)]
  # candidates = treat(candidates)
  return candidates

def trim(i, x):
  return max(Settings.de.cartLimit_Min[i], min(int(x),Settings.de.cartLimit_Max[i]))
def gen3(n, f, frontier):
  np = Settings.de.np
  seen = [n]
  def gen1(seen):
    while 1:
      k = random.randint(0, np - 1)
      if k not in seen:
        seen += [k]
        break
    return frontier[k]
  a = gen1(seen)
  b = gen1(seen)
  c = gen1(seen)
  return a, b, c

def update(n, old, frontier):
  fa = Settings.de.f
  cr = Settings.de.cr
  newf = []
  a, b, c = gen3(n, old, frontier)
  for i in xrange(len(old)):
    # con = a[i]== None or b[i]==None or c[i]==None
    # if i in [4] and con: # the last one is max_leaf_nodes, can be None
    #     newf.append(old[i] if cr<random.random() else None)
    # else:
    newf.append(old[i] if cr < random.random() else trim(i,(a[i] + fa * (b[i] - c[i]))))
  return newf

def writefile(s):
  global The
  f = open(The.option.resultname, 'a')
  f.write(s+'\n')
  f.close()
  
def writeResults(bestscore, evaluation):
  # pdb.set_trace()
  name = ['threshold','bestscore','evaluation','max_features', 'min_samples_split', 
             'min_samples_leaf','max_depth']
  # val =[str(The.option.threshold), str(bestscore), str(evaluation), str(The.cart.criterion), str(The.cart.splitter),
  #         str(The.cart.max_features), str(The.cart.max_depth), str(The.cart.min_samples_split),
  #         str(The.cart.min_samples_leaf)] 
  val =[str(The.option.threshold), str(bestscore), str(evaluation),
          str(The.cart.max_features), str(The.cart.min_samples_split),
          str(The.cart.min_samples_leaf),str(The.cart.max_depth)] 
  for k, v in zip(name, val):
    # pdb.set_trace()
    writefile(k +" : "+v)
    # print k+" : "+v

def cart_de():
  def evaluate(frontier):
    for n, i in enumerate(frontier):
      assign(i)
      scores[n] = cart()[-1] # score[i]= [pd,pf,prec, g], the second objecit in returned value
      # scores[n] = cart()[0] # pd
    # print scores
    return scores

  def best(scores):
    ordered = []
    if The.option.tunedobjective ==1 : # pf
      ordered = sorted(scores.items(), key=lambda x: x[1][The.option.tunedobjective], reverse = True)  # alist of turple
    else:
      ordered = sorted(scores.items(), key=lambda x: x[1][The.option.tunedobjective])  # alist of turple
    # pdb.set_trace()
    bestconf = frontier[ordered[-1][0]] #[(0, [100, 73, 9, 42]), (1, [75, 41, 12, 66])]
    # bestscore = ordered[-1][-1][-1]
    bestscore = ordered[-1][-1][The.option.tunedobjective]
    return bestconf, bestscore

  def isBetter(new, old): return new < old if The.option.tunedobjective == 1 else new >old
  # def isBest(val) : return val == 0 if The.option.tunedobjective ==1 else val == 100
  def isBest(val): return False

  scores = {}
  global The  
  The.option.tuning = True
  np = Settings.de.np
  repeats = Settings.de.repeats
  life = Settings.de.life
  changed = False
  evaluation = 0
  frontier = [generate() for _ in xrange(np)]
  scores = evaluate(frontier)
  bestconf, bestscore = best(scores)
  for k in xrange(repeats):
    if life <= 0 or isBest(bestscore):
      break
    nextgeneration = []
    for n, f in enumerate(frontier):
      new = update(n, f, frontier)
      assign(new)
      newscore = cart()[-1] # Y-Def
      evaluation +=1
      # if newscore[The.option.tunedobjective] > scores[n][The.option.tunedobjective] : # g value
      # if newscore[0] > scores[n][0]: # pd value
      # if newscore[-2] > scores[n][-2]: # f value
      if isBetter(newscore[The.option.tunedobjective], scores[n][The.option.tunedobjective]):
        nextgeneration.append(new)
        scores[n] = newscore[:]
        # changed = True
      else:
        nextgeneration.append(f)
    frontier = nextgeneration[:]
    # pdb.set_trace()
    newbestconf, newbestscore = best(scores)
    # if newbestscore > bestscore:
    if isBetter(newbestscore, bestscore):
      # print "newbestscore %s:" % str(newbestscore)
      # print "bestconf %s :" % str(newbestconf)
      bestscore = newbestscore
      bestconf = newbestconf[:]
      changed = True
    if not changed: # the pareto frontier changed or not
      life -= 1
    changed = False
  assign(bestconf)
  writeResults(bestscore, evaluation)

if __name__ == "__main__":
  eval(cmd())
