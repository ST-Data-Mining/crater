from __future__ import division
import random, pdb 
from main import *
from base import *
from file import *
from start import *
# global The

def r(limit, prec = 2):
  return round(random.uniform(0.01,limit) ,prec)

def ig(limit):
  return int(random.uniform(1,limit))

def treat(lst):
  if lst[4]<=lst[5] and lst[-1]: # where prune is true, lst[4] should > lst[5]
    lst[4] = ig(Settings.de.limit[4])
    lst[5] = ig(Settings.de.limit[5])
    lst =treat(lst)
  return lst

def assign(i):
  global The
  The.tree.infoPrune = i[0]
  The.tree.min = i[1]
  The.option.threshold = i[2]
  The.where.wriggle = i[3]
  The.where.depthMax = i[4]
  The.where.depthMin = i[5]
  The.option.minSize = i[6]
  The.tree.prune = i[7]
  The.where.prune = i[8]

def generate():
  candidates = [r(l) if i not in [1,4,5] else ig(l)for i,l in enumerate(Settings.de.limit)]
  candidates.extend([random.random() <= 0.5 for _ in range(2)]) # 1: treePrune, 2:whereprune
  candidates = treat(candidates)
  return candidates

def trim(i, x):
  if i in [1,4,5]:
    return max(1, min(int(x),Settings.de.limit[i]))
  else:
    return max(0.01, min(round(x,2), Settings.de.limit[i]))

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
    if i >= len(old) - 2: # the last two are true or false
      newf.append(old[i] if cr < random.random() else not old[i])
    else:
      newf.append(old[i] if cr < random.random() else trim(i,(a[i] + fa * (b[i] - c[i]))))
  return treat(newf)

def writeResults(bestscore, evaluation):
  name = ['threshold','bestscore','infoPrune','min_sample_size','min_Size', 'wriggle', 
             'depthMin', 'depthMax' , 'wherePrune', 'treePrune','Evaluations']
  val =[str(The.option.threshold), str(bestscore), str(The.tree.infoPrune), 
          str(The.tree.min), str(The.option.minSize), str(The.where.wriggle),
          str(The.where.depthMin), str(The.where.depthMax), 
          str(The.where.prune),str(The.tree.prune),str(evaluation)] 
  for k, v in zip(name, val):
    # print k +" : "+v
    writefile(k +" : "+v)

def de():
  def evaluate(frontier):
    for n, i in enumerate(frontier):
      assign(i)
      scores[n] = main()[-1] # score[i]= [pd,pf,prec,f, g], the second objecit in returned value
    # print scores
    return scores

  def best(scores):
    ordered = []
    if The.option.tunedobjective ==1 : # pf
      ordered = sorted(scores.items(), key=lambda x: x[1][The.option.tunedobjective], reverse = True)  # alist of turple
    else:
      ordered = sorted(scores.items(), key=lambda x: x[1][The.option.tunedobjective])  # alist of turple
    # pdb.set_trace()
    # print ordered
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
      newscore = main()[-1] # Y-Def
      evaluation +=1
      # pdb.set_trace()
      # if newscore[The.option.tunedobjective] > scores[n][The.option.tunedobjective] : # g value
      #if newscore[0] > scores[n][0] : # pd value
      # if newscore[-2] > scores[n][-2] : # f value
      if isBetter(newscore[The.option.tunedobjective], scores[n][The.option.tunedobjective]):
        nextgeneration.append(new)
        scores[n] = newscore[:]
        # changed = True
      else:
        nextgeneration.append(f)
    frontier = nextgeneration[:]
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
