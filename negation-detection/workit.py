import negation_detection
import csv

sentences = []
with open('../annotations_fixed.tsv') as f:
  r = csv.reader(f, delimiter='\t')
  for row in r:
    #row[6] = row[6].replace('(', '. ')
    #row[6] = row[6].replace(')', '. ')
    sentences.append({ 'sentence': row[6], 'sid': row[5], 'concept': row[1], 'cname': row[2], 'negated': row[4] })
    print 'sentence: ' + row[6]
    print 'concept: ' + row[2]
    print 'negated: ' + row[4]
    print ''

targets = dict()
with open('../hpo_labels.txt') as labelfile:
  reader = csv.reader(labelfile, delimiter='\t')
  for row in reader:
    if not row[1] in targets:
      targets[row[1]] = []
    targets[row[1]].append(row[0].replace('\\', ''))

tp = 0.0
fp = 0.0
tn = 0.0
fn = 0.0
    
for x in sentences:
  for o in targets[x['concept']]:
    x['sentence'] = x['sentence'].replace(o, 'biscuit')

  result = negation_detection.predict(x['sentence'], 'biscuit')

  if(result == False):
    if(x['negated'] == 'negated'):
      tp += 1
    else:
      fp += 1
      print 'fp: ' + x['sentence'] 
      print '    ' + x['sid'] + ' ' + x['cname']
  else:
    if(x['negated'] == 'negated'):
      fn += 1
      print 'fn: ' + x['sentence']
      print '    ' + x['sid'] + ' ' + x['cname']
    else:
      tn += 1

  print ''

print tp
print fp
print fn

precision = tp/(tp+fp)
recall = tp/(tp+fn)
f = 2 * ((precision * recall) / (precision + recall))

print '\n'

print precision
print recall

print 'precision: ' + str(precision)
print 'recall: ' + str(recall)
print 'f: ' + str(f)


