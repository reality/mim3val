import csv
import pyConTextNLP.pyConText as pyConText
from pyConTextNLP.itemData import contextItem
import pyConTextNLP.itemData as itemData
import networkx as nx

def modifies(g,n,modifiers): 
  """g: directed graph representing the ConText markup n: a node in g modifiers: a list of categories e.g. ["definite_negated_existence","probable_existence"] modifies() tests whether n is modified by an objects with category in categories"""
  pred = g.predecessors(n) 
  if( not pred ): 
    return False 
  for n in pred:
    for c in n.getCategory():
      if(c in modifiers):
        return True
  return False

tp = 0.0
fp = 0.0
fn = 0.0
tn = 0.0

iris = []
truths = []
sentences = []
with open('./annotations_fixed.tsv') as sentfile:
  reader = csv.reader(sentfile, delimiter='\t')
  for row in reader:
    print(row)
    truth = "negated" in row[4]
    truths.append(truth)

    iris.append(row[1])
    sentences.append(row[6])

modifiers = itemData.get_items(
    "https://raw.githubusercontent.com/chapmanbe/pyConTextNLP/20c752d6bd5191833f21ab81fc7f41877dca1db6/KB/pneumonia_modifiers.yml")

for i in range(len(sentences)):

  # omg
  targets = []
  with open('./hpo_labels.txt') as labelfile:
    reader = csv.reader(labelfile, delimiter='\t')
    for row in reader:
      if(row[1] == iris[i]): 
        targets.append(contextItem((row[0], row[1], '', '')))


  s = sentences[i]

  markup = pyConText.ConTextMarkup()
  markup.setRawText(s.lower())
  markup.cleanText()

  markup.markItems(modifiers, mode = "modifier")
  markup.markItems(targets, mode = "target")

  markup.applyModifiers()
  markup.pruneMarks()
  markup.pruneSelfModifyingRelationships()
  markup.dropInactiveModifiers()

  foundTargets = [n[0] for n in markup.nodes(data = True) if n[1].get("category","") == 'target']

  status = False

  for edge in markup.edges(data=True):
    c = edge[0].getCategory()[0]
    if c == 'definite_negated_existence' or c == 'probable_negated_existence':
      if edge[1].getCategory()[0] == iris[i].lower():
        status = True
    print(edge[2])
    

  #for t in foundTargets:
  #  if str(t.getCategory()[0]) == iris[i].lower():
  #    if modifies(markup, t, ['definite_negated_existence', 'probable_negated_existence']):
  #      status = True
      #print(t)
      #for p in markup.predecessors(t):
      #  print(p)
      #  if 'definite_negated_existence' in p.getCategory() or 'probable_negated_existence' in p.getCategory():
      #    status = True


  print(status)
  print(truths[i])
  if status == True:
    if truths[i]:
      tp += 1
    else:
      fp += 1
      print('fp: ' + s + ' ' + iris[i])
  else:
    if truths[i]:
      fn += 1
    else:
      tn += 1
      print('woo')

  print(i)
  print(' ')

print(tp)
print(fp)
print(fn)
print(tn)

precision = tp / (tp + fp)
recall = tp / (tp + fn)

print("precision: " + str(precision))
print("recall: " + str(recall))
