def tp = 0
def fp = 0
def fn = 0

new File('./annotations_fixed.tsv').splitEachLine('\t') {
  def algorithmTag = it[3].indexOf('negated') != -1
  def groundTruth = it[4].indexOf('negated') != -1

  if(algorithmTag) {
    if(groundTruth) {
      tp++
    } else {
      fp++
      println 'fp'
      println it[6]
      println it[2]
      println ''
    }
  } 

  if(groundTruth && !algorithmTag) {
    fn++
  }
}

def precision = tp / (tp + fp)
def recall = tp / (tp + fn)

println "precision: $precision"
println "recall: $recall"
