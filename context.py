import csv
import pyConTextNLP.pyConText as pyConText
from pyConTextNLP.itemData import contextItem
import pyConTextNLP.itemData as itemData
import networkx as nx

tp = 0.0
fp = 0.0
fn = 0.0

syns = []
targets = []
with open('./hpo_labels.txt') as labelfile:
  reader = csv.reader(labelfile, delimiter='\t')
  for row in reader:
    targets.append(contextItem((row[0], row[1], '', '')))

iris = []
truths = []
sentences = []
with open('./annotations_fixed.tsv') as sentfile:
  reader = csv.reader(sentfile, delimiter='\t')
  for row in reader:
    truth = "negated" in row[4]
    print(row[3] + ' ' + str(truth))
    truths.append(truth)

    iris.append(row[1])
    sentences.append(row[6])

modifiers = itemData.get_items(
    "https://raw.githubusercontent.com/chapmanbe/pyConTextNLP/master/KB/lexical_kb_05042016.yml")

for i in range(len(sentences)):
  s = sentences[i]

  markup = pyConText.ConTextMarkup()
  markup.setRawText(s.lower())
  markup.cleanText()

  markup.markItems(targets, mode = "target")
  markup.markItems(modifiers, mode = "modifier")

  markup.applyModifiers()

  foundTargets = [n[0] for n in markup.nodes(data = True) if n[1].get("category","") == 'target']

  status = False
  for t in foundTargets:
    if str(t.getCategory()[0]) == iris[i].lower():
      for p in markup.predecessors(t):
        print(p.getCategory())
        if 'definite_negated_existence' in p.getCategory() or 'probable_negated_existence' in p.getCategory():
          status = True
    else:
      print('exluded')

  if status:
    if truths[i]:
      tp += 1
    else:
      fp += 1
      print(s)
  else:
    if truths[i]:
      fn += 1
      print('fn')
      print(s)

  print(i)


precision = tp / (tp + fp)
recall = tp / (tp + fn)

print("precision: " + str(precision))
print("recall: " + str(recall))
