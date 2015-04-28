from __future__ import division, print_function
from main import *
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.cross_validation import cross_val_score

def csv2py(f):
  sym2num = {}
  # sym2num hold all the characters with assinged numbers that never seen

  def str2num(t, p=0):
    def bigt():
      if isinstance(tbl, list):
        t = tbl[0]
        for i in range(1, len(tbl)):
          t._rows += tbl[i]._rows
      else:
        t = tbl
      return t
    t = bigt()
    for r, row in enumerate(t._rows):
      for c, cell in enumerate(row.cells):
        if isinstance(cell, str) and c < t.depen[0].col and isinstance(t.headers[c], Sym):
          if sym2num.get(cell, 0) == 0:
            sym2num[cell] = p
            p += 1
          t._rows[r].cells[c] = sym2num[cell]  # update cell with num
    return t
  if isinstance(f, list):
    tbl = [table(src) for src in f]  # tbl is a list of tables
  else:
    tbl = table(f)
  tbl_num = str2num(tbl)
  return tbl_num

def _Abcd(predicted, actual):
  predicted_txt = []
  abcd = Abcd(db='Traing', rx='Testing')
  if The.option.actualpredicted != "":
    f = open("/Users/WeiFu/Google Drive/"+The.option.actualpredicted,'w').close()
    f = open("/Users/WeiFu/Google Drive/"+The.option.actualpredicted, 'a')
  global The
  def isDef(x):
    return "Defective" if x >= The.option.threshold else "Non-Defective" # use the.option.threshold for cart, rf and where!!
  for data in predicted:
    predicted_txt +=[isDef(data)]
  for act, pre in zip(actual, predicted_txt):
    abcd.tell(act, pre)
    real = "1" if act == "Defective" else "0"
    pred = "1" if pre == "Defective" else "0"
    if The.option.actualpredicted != "":
      f.write(real+","+pred+"\n")
  abcd.header()
  score = abcd.ask()
  # pdb.set_trace()
  return score

def conv(x):
  return [ float(i) for i in x]

def cart():
  clf = None
  # print (The.classifier.carttuned, The.classifier.cart, The.classifier.rf, The.classifier.rftuned)
  # if The.classifier.carttuned:
    # classifier = DecisionTreeClassifier
    # clf = classifier(criterion = The.cart.criterion, random_state = 0)
  clf = DecisionTreeRegressor(
        max_features = The.cart.max_features, max_depth = The.cart.max_depth,
        min_samples_split = The.cart.min_samples_split, min_samples_leaf = The.cart.min_samples_leaf, random_state = 1)
  # elif The.classifier.cart :
  #   clf = DecisionTreeRegressor(random_state = 1)
  # elif The.classifier.rf:
  #   clf = RandomForestRegressor(n_estimators =100, random_state = 1)
  # elif The.classifier.rftuned:
  #   clf = RandomForestRegressor(n_estimators =The.rf.n_estimators,max_features = The.rf.max_features,
  #                           min_samples_split = The.rf.min_samples_split, min_samples_leaf = The.rf.min_samples_leaf,
  #                           max_leaf_nodes = The.rf.max_leaf_nodes,random_state = 1)

  # The.data.train =["./data/ant/ant-1.4.csv"]
  # The.data.predict ="./data/ant/ant-1.5.csv"
  testdata, actual = buildtestdata1(The.data.predict)
  traintable= csv2py(The.data.train)
  traindata_X = [ conv(row.cells[:-1])for row in traintable._rows]
  traindata_Y = [ (row.cells[-1])for row in traintable._rows]
  # pdb.set_trace()
  predictdata_X =[ conv(row.cells[:-1])for row in testdata]
  predictdata_Y =[ (row.cells[-1]) for row in testdata]
  clf = clf.fit(traindata_X, traindata_Y)
  array = clf.predict(predictdata_X)
  # pdb.set_trace()
  predictresult = [i for i in array]
  # print(predictresult)
  # print(predictdata_Y)
  scores = _Abcd(predictresult,actual)
  return scores

# def make():
#   testdata, actual = buildtestdata1(The.data.predict)
#   traintable= csv2py(The.data.train)
#   traindata_X = [ conv(row.cells[:-1])for row in traintable._rows]
#   traindata_Y = [ (row.cells[-1])for row in traintable._rows]
#   # pdb.set_trace()
#   predictdata_X =[ conv(row.cells[:-1])for row in testdata]
#   return [traindata_X, traindata_Y, predictdata_X, actual]
# def cart():
#   pdb.set_trace()
#   clf = DecisionTreeRegressor(
#         max_features = The.cart.max_features, max_depth = The.cart.max_depth,
#         min_samples_split = The.cart.min_samples_split, min_samples_leaf = The.cart.min_samples_leaf, random_state = 1)
#   datasets = make()
#   clf = clf.fit(datasets[0], datasets[1])
#   array = clf.predict(datasets[2])
#   predictresult = [i for i in array]
#   scores = _Abcd(predictresult, datasets[-1])
#   return scores
# def rf():
#   clf = RandomForestRegressor(n_estimators =The.rf.n_estimators,max_features = The.rf.max_features,
#                             min_samples_split = The.rf.min_samples_split, min_samples_leaf = The.rf.min_samples_leaf,
#                             max_leaf_nodes = The.rf.max_leaf_nodes,random_state = 1)
#   datasets = make()
#   clf = clf.fit(datasets[0], datasets[1])
#   array = clf.predict(datasets[2])
#   predictresult = [i for i in array]
#   scores = _Abcd(predictresult, datasets[-1])
#   return scores






# def main():
# 	return cart()

if __name__ == "__main__":
  eval(cmd())
