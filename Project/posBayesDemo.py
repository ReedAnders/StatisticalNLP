from nltk.classify import PositiveNaiveBayesClassifier

# Some sentences about sports:
sports_sentences = [ 'cathage team dominated the game', 
                      'They lost the ball',
                      'The game was intense',
                      'The goalkeeper catched the ball',
                      'The other team controlled the ball' ]

# Mixed topics, including sports:
various_sentences = [ 'The President did not comment',
                       'I lost the keys',
                       'The team won the game',
                       'Sara has two kids',
                       'The ball went off the court',
                       'They had the ball for the whole game',
                       'The show is over' ]

# The features of a sentence are simply the words it contains:
def features(sentence):
    words = sentence.lower().split()
    # return dict(('contains(%s)' % w, True) for w in words)
    return dict((w, True) for w in words)


# We use the sports sentences as positive examples, the mixed ones ad unlabeled examples:  
# map() is apply features() function to pos_sentences iterable, return list

# positive_featuresets - A list of featuresets that are known as positive examples (i.e., their label is True).  
positive_featuresets = map(features, sports_sentences)

print '\n ''positive_featuresets'' full list: \n', positive_featuresets
print '\n positive_featuresets:'
for ii in positive_featuresets:
    print 'answer:', ii

# unlabeled_featuresets - A list of featuresets whose label is unknownself.
unlabeled_featuresets = map(features, various_sentences)

print '\n unlabeled_featuresets:'
for ii in unlabeled_featuresets:
    print 'answer:', ii

# To train, pass in a list of 'true' dictionaries for POS and for NEG
classifier = PositiveNaiveBayesClassifier.train(positive_featuresets, unlabeled_featuresets)


# Is the following sentence about sports?
print '\n','The cat is on the table --', classifier.classify(features('The cat is on the table'))

# What about this one?
print 'My team lost the game --', classifier.classify(features('My team lost the game'))

# Output

#  positive_featuresets full list: 
# [{'the': True, 'dominated': True, 'game': True, 'team': True}, {'the': True, 'ball': True, 'lost': True, 'they': True}, {'the': True, 'was': True, 'game': True, 'intense': True}, {'the': True, 'ball': True, 'goalkeeper': True, 'catched': True}, {'the': True, 'other': True, 'controlled': True, 'ball': True, 'team': True}]

#  positive_featuresets:
# sentence: {'the': True, 'dominated': True, 'game': True, 'team': True}
# sentence: {'the': True, 'ball': True, 'lost': True, 'they': True}
# sentence: {'the': True, 'was': True, 'game': True, 'intense': True}
# sentence: {'the': True, 'ball': True, 'goalkeeper': True, 'catched': True}
# sentence: {'the': True, 'other': True, 'controlled': True, 'ball': True, 'team': True}

#  unlabeled_featuresets:
# sentence: {'did': True, 'president': True, 'the': True, 'not': True, 'comment': True}
# sentence: {'i': True, 'keys': True, 'the': True, 'lost': True}
# sentence: {'the': True, 'won': True, 'game': True, 'team': True}
# sentence: {'has': True, 'sara': True, 'two': True, 'kids': True}
# sentence: {'court': True, 'the': True, 'ball': True, 'off': True, 'went': True}
# sentence: {'ball': True, 'for': True, 'had': True, 'game': True, 'they': True, 'the': True, 'whole': True}
# sentence: {'the': True, 'over': True, 'is': True, 'show': True}

# The cat is on the table -- False
# My team lost the game -- True
