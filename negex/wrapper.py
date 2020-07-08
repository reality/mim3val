from negex import *
import csv

tp = 0.0
fp = 0.0
fn = 0.0
tn = 0.0

rfile = open(r'negex_triggers.txt')
irules = sortRules(rfile.readlines())

sentences = []
with open('../komenti/mimic_will_fix.tsv') as f:
  r = csv.reader(f, delimiter='\t')
  for row in r:
    sentences.append({ 'sentence': row[5], 'sid': row[4], 'concept': row[1], 'cname': row[2], 'negated': row[3] })
    print 'sentence: ' + row[5]
    print 'concept: ' + row[2]
    print 'negated: ' + row[3]
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
  tagger = negTagger(sentence = x['sentence'],
                     phrases = ['biscuit'], 
                     rules = irules, 
                     negP=False)
      #report.append(tagger.getNegTaggedSentence())
  if tagger.getNegationFlag() == 'negated':
    if x['negated'] == 'n':
      tp += 1
    else:
      fp += 1
      print(x['sentence'])
  else:
    if x['negated'] == 'n':
      fn += 1
    else: 
      tn += 1
        #report = report + tagger.getScopes()
   
precision = tp / (tp + fp)
recall = tp / (tp + fn)

print("precision: " + str(precision))
print("recall: " + str(recall))

#def main():
#    reports = csv.reader(open(r'Annotations-1-120.txt','rb'), delimiter = '\t')
#    reports.next()
#    reportNum = 0
#    correctNum = 0
#    ofile = open(r'negex_output.txt', 'w')
#    output = []
#    outputfile = csv.writer(ofile, delimiter = '\t')
#    for report in reports:
#        tagger = negTagger(sentence = report[2], phrases = [report[1]], rules = irules, negP=False)
#        report.append(tagger.getNegTaggedSentence())
#        report.append(tagger.getNegationFlag())
#        report = report + tagger.getScopes()
#        reportNum += 1
#        if report[3].lower() == report[5]:
#            correctNum +=1
#        output.append(report)
#    outputfile.writerow(['Percentage correct:', float(correctNum)/float(reportNum)])
#    for row in output:
#        if row:
#            outputfile.writerow(row)
#    ofile.close()
