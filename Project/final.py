#NLP Final Project

from collections import defaultdict
from csv import DictReader, DictWriter

import re
import nltk
from nltk.corpus import wordnet as wn
from nltk.tokenize import TreebankWordTokenizer
from nltk.classify import PositiveNaiveBayesClassifier
from nltk.util import ngrams

train = DictReader(open("train.csv", 'r'))
#Fields:
#Question, Question Text, QANTA Scores, Answer, Sentence Position, IR_Wiki Scores, category

def features(sentence):
    words = sentence.lower().split()
    return dict(('contains(%s)' % w, True) for w in words)

#Using this counter to look at the first few questions only
i=0;

for ii in train:
	


# 	if i==3:

# 		#Assign positive features for question 1
# 		sentence=[str(ii['Question Text'])]
# 		positive_featuresets=map(features,sentence)
	
# 	if i==7:
# 		#assign negative feature for question 2
# 		sentence=[str(ii['Question Text'])]
# 		unlabeled_featuresets = map(features, sentence)

	#Print first answer,weight
	print re.split(':',re.split(',',ii['IR_Wiki Scores'])[0])[0],re.split(':',re.split(',',ii['IR_Wiki Scores'])[0])[1]

	#6 means first 2 questions
	if i>6:
		break
	i+=1

# print '\n ''positive_featuresets'' full list: \n', positive_featuresets

# classifier = PositiveNaiveBayesClassifier.train(positive_featuresets, unlabeled_featuresets)

# print ''
# print "TESTING ON SENTENCES"
# print ''

# #Should be true
# print "...Should be true..."
# print 'it was founded as kart-hadasht meaning new town and it is now a suburb of a world capital --', classifier.classify(features('it was founded as kart-hadasht meaning new town and it is now a suburb of a world capital'))

# #Should be false
# print '\n',"...The rest should be False..."
# print 'the nations involved in it had allied immediately before it through the treaty of chaumont and one of the figures involved in it continued the reforms of karl vom stein --', classifier.classify(features('the nations involved in it had allied immediately before it through the treaty of chaumont and one of the figures involved in it continued the reforms of karl vom stein'))
# print '\n','this man opponent humorously promised to not exploit his youth and inexperience --', classifier.classify(features('this man opponent humorously promised to not exploit his youth and inexperience'))
# print '\n','his autobiography thirty years view is one of the best of the period and teddy roosevelt wrote a later biography on him --', classifier.classify(features('his autobiography thirty years view is one of the best of the period and teddy roosevelt wrote a later biography on him'))
# print '\n','The cat is on the table --', classifier.classify(features('The cat is on the table'))