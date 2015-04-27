from __future__ import division
import random, pdb 
from main import *
from base import *
import collections 
# from file import *
from start import *

class DeBase(object):
  def __init__(i):
    global The
    i.np = Settings.de.np 
    i.fa = Settings.de.f
    i.cr = Settings.de.cr
    i.repeats = Settings.de.repeats
    i.life = Settings.de.life
    # i.obj = The.option.tunedobjective
    i.obj = -1 ### need to change this to the above line after done!
    i.evaluation = 0
    i.candidates = []
    i.scores = {}
    i.frontier = [i.generate() for _ in xrange(i.np)]
    i.evaluate()
    i.bestconf, i.bestscore=i.best()
  def generate(i):
    raise NotImplementedError(" error")
  def evalute(i):
    raise NotImplementedError(" error")
  def assign(i, tobetuned, tunedvalue):
    keys = tobetuned.keys()
    for key,val in zip(keys, tunedvalue):
      exec(key +"= "+str(val))
      tobetuned[key] =val 
  def best(i):
    sortlst = [], [], None
    if i.obj == 1: # this is for pf
      sortlst= sorted(i.scores.items(), key=lambda x: x[1][i.obj], reverse = True)  # alist of turple
    else:
      sortlst = sorted(i.scores.items(), key=lambda x: x[1][i.obj])  # alist of turple
    bestconf = i.frontier[sortlst[-1][0]] #[(0, [100, 73, 9, 42]), (1, [75, 41, 12, 66])]
    bestscore = sortlst[-1][-1][i.obj]
    # pdb.set_trace()
    return bestconf, bestscore
  def allModel(i): raise NotImplementedError(" error")
  def gen3(i, n, f):
    seen = [n]
    def gen1(seen):
      while 1:
        k = random.randint(0, i.np - 1)
        if k not in seen:
          seen += [k]
          break
      return i.frontier[k]
    a = gen1(seen)
    b = gen1(seen)
    c = gen1(seen)
    return a, b, c
  def update(i, n, old):
    newf = []
    a, b, c = i.gen3(n, old)
    for k in xrange(len(old)):
      if isinstance(old[k], bool):
        newf.append(old[k] if i.cr < random.random() else not old[k])
      else:
        newf.append(old[k] if i.cr < random.random() else i.trim(k,(a[k] + i.fa * (b[k] - c[k]))))
    return i.treat(newf)
    # def trim(i, x): return max(Settings.de.rfLimit_Min[i], min(int(x),Settings.de.rfLimit_Max[i]))
  def DE(i):
    changed = False 
    def isBetter(new, old): return new < old if i.obj == 1 else new >old
    for k in xrange(i.repeats):
      if i.life <= 0:
        break
      nextgeneration = []
      for n, f in enumerate(i.frontier):
        new = i.update(n,f)
        i.assign(i.tobetuned,new)
        newscore = i.callModel()
        i.evaluation +=1
        if isBetter(newscore[i.obj], i.scores[n][i.obj]):
          nextgeneration.append(new)
          i.scores[n] = newscore[:]
          changed = True
        else:
          nextgeneration.append(f)
      i.frontier = nextgeneration[:]
      newbestconf, newbestscore = i.best()
      if isBetter(newbestscore, i.bestscore):
        print "newbestscore %s:" % str(newbestscore)
        print "bestconf %s :" % str(newbestconf)
        i.bestscore = newbestscore
        i.bestconf = newbestconf[:]
      if not changed:
      	i.life -=1
      changed = False
    i.assign(i.tobetuned,i.bestconf)
    print "DONE !!!!"
    
class Where(DeBase):
  def __init__(i):
    i.tobetuned = collections.OrderedDict((
                  ("The.tree.infoPrune" ,The.tree.infoPrune),
                  ("The.tree.min",The.tree.min),
                  ("The.option.threshold",The.option.threshold),
                  ("The.where.wriggle",The.where.wriggle),
                  ("The.where.depthMax",The.where.depthMax),
                  ("The.where.depthMin",The.where.depthMin),
                  ("The.option.minSize",The.option.minSize),
                  ("The.tree.prune",The.tree.prune),
                  ("The.where.prune",The.where.prune)))
    i.limit = Settings.de.limit
    super(Where,i).__init__()
  def genFloat(i,l): return round(random.uniform(0.01,l) ,2) 
  def genInt(i,l): return int(random.uniform(1,l))
  def genBool(i): return random.random() <= 0.5 
  def generate(i):
    i.candidates = [i.genFloat(l) if k not in [1,4,5] else\
                   i.genInt(l) for k,l in enumerate(i.limit)]
    i.candidates.extend([i.genBool() for _ in range(2)]) # 1: treePrune, 2:whereprune
    return i.treat(i.candidates)
  def treat(i, lst):
    if lst[-1] and lst[4] <= lst[5]:
      lst[4] = i.genInt(4)
      lst[5] = i.genInt(5)
      lst = i.treat(lst)
    return lst
  def callModel(i): return main()[-1]
  def evaluate(i):
    The.data.train =["./data/ivy/ivy-1.1.csv"]
    The.data.predict ="./data/ivy/ivy-1.4.csv"
    for n, arglst in enumerate(i.frontier):
      i.assign(i.tobetuned,arglst)
      i.scores[n] = i.callModel() # main return [[pd,pf,prec,f,g],[pd,pf,prec,f,g]], which are N-defective,Y-defecitve
    print i.scores
  def trim(i, n,x):
    if n in [1,4,5]:
      return max(1, min(int(x),i.limit[n]))
    else:
      return max(0.01, min(round(x,2), i.limit[n]))


#test

Where().DE()



