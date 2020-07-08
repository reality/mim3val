#!/usr/bin/env groovy
@Grab(group='commons-cli', module='commons-cli', version='1.4')
@Grab(group='org.apache.commons', module='commons-lang3', version='3.4')
@Grab(group='edu.stanford.nlp', module='stanford-corenlp', version='3.7.0')
@Grab(group='edu.stanford.nlp', module='stanford-corenlp', version='3.7.0', classifier='models')
@Grab(group='edu.stanford.nlp', module='stanford-parser', version='3.7.0')
@Grab(group='org.codehaus.groovy.modules.http-builder', module='http-builder', version='0.7.1')

import edu.stanford.nlp.pipeline.*
import edu.stanford.nlp.ling.*
import edu.stanford.nlp.semgraph.*

def REP_TOKEN = 'biscuit'
    def props = new Properties()
    props.put("annotators", "tokenize, ssplit, pos, lemma, ner, depparse")
    props.put("parse.maxtime", "20000")
    props.put("regexner.ignorecase", "true")
    props.put("depparse.nthreads", 8)
    props.put("ner.nthreads", 8)
    props.put("parse.nthreads", 8)
def    advancedCoreNLP = new StanfordCoreNLP(props)


def concepts = [:]
new File('../hpo_labels.txt').splitEachLine('\t') {
  if(!concepts.containsKey(it[1])) {
    concepts[it[1]] = []
  }
  concepts[it[1]] << it[0]
}

def tp=0
def fp=0
def fn=0

new File('./mimic_will_fix.tsv').splitEachLine('\t') {

  def iri = it[1]
  def sentence = it[5]
  def negated = it[3].indexOf('n') != -1

    def klSentence = new Sentence(sentence.toString(), it[2])
    klSentence.genTypeDeps(advancedCoreNLP, concepts[iri], REP_TOKEN) 

    if(klSentence.isNegated([REP_TOKEN])) {
      if(negated) {
        tp++
      } else {
        fp++
        println "fp (${it[2]}) sentence: $sentence"
      }
    } else {
      if(negated) {
        fn++
        println "fn (${it[2]}) sentence: $sentence"
      }
    }
}

def precision = tp / (tp + fp)
def recall = tp / (tp + fn)

println tp
println fp
println fn

println 'tp: ' + precision
println 'recall: ' + recall
