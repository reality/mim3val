@Grab('com.xlson.groovycsv:groovycsv:1.3')
@Grab(group='org.apache.commons', module='commons-lang3', version='3.4')
@Grab(group='edu.stanford.nlp', module='stanford-corenlp', version='3.7.0')
@Grab(group='edu.stanford.nlp', module='stanford-corenlp', version='3.7.0', classifier='models')
@Grab(group='edu.stanford.nlp', module='stanford-parser', version='3.7.0')

import static com.xlson.groovycsv.CsvParser.parseCsv
import edu.stanford.nlp.pipeline.*
import edu.stanford.nlp.ling.*
import edu.stanford.nlp.semgraph.*
import org.apache.commons.lang3.RandomUtils

println "Loading file... "

def entries = []
def file = new RandomAccessFile('./NOTEEVENTS.csv', 'r')

println "File loaded. Beginning selection sequence..."

while(entries.size() < 1000) {
  def rPos = RandomUtils.nextLong(new Long(0), file.length())

  file.seek(rPos)

  def foundNewRecord
  def newText
  
  while(!foundNewRecord) {
    newText = file.readLine()
    if(newText.indexOf('",') != -1) {
      foundNewRecord = true
    }
  }

  foundNewRecord = false
  def textRecord = ''

  while(!foundNewRecord) {
    newText = file.readLine() 
    if(newText.indexOf('",') != -1) {
      foundNewRecord = true
    } else {
      textRecord += newText
    }
  }

  if(textRecord.indexOf('     ') == -1) {
    entries << textRecord.replaceAll('\n', '').replaceAll('\\s+', ' ').replaceAll('\\.', '. ')
  }
  // @500
  // cont: p: 0.463 r: 0.95
  // koment: p: 0.77 r: 0.9 
  // neg-det: p: 0.6 r: 0.56

  println entries.size()
}

println "Selecting sentences...."

def props = new Properties()
props.put("annotators", "tokenize, ssplit")
coreNLP = new StanfordCoreNLP(props)
pipeline = new AnnotationPipeline()
pipeline.addAnnotator(coreNLP)

def i = 0
def sentences = entries.collect { entry ->
  def aDocument = new Annotation(entry.toLowerCase())

  pipeline.annotate(aDocument)

  println "${++i}"

  def s = aDocument.get(CoreAnnotations.SentencesAnnotation.class).collect { it.toString() }
  //s = s.findAll { it.indexOf('\t') == -1 && it.indexOf('---') == -1 && it.tokenize(' ').size() < 30 }
  //def rPos = RandomUtils.nextInt(0, s.size())
  //s[rPos]*/
  s
}.flatten()
sentences.removeAll([null])

new File('sentences_healtac.txt').text = sentences.join('\n')
