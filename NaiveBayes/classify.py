from collections import defaultdict
from csv import DictReader, DictWriter

import nltk
from nltk.corpus import wordnet as wn
from nltk.tokenize import RegexpTokenizer


def morphy_stem(word):
    """
    Simple stemmer
    """
    # Morphy returns the base form of a word, ie, dogs -> dog 
    # unknown 'stem' returns word.lower()
    stem = wn.morphy(word)
    if stem:
        return stem.lower()
    else:
        return '0'
        # return word.lower()

class FeatureExtractor:
    def __init__(self):
        """
        You may want to add code here
        """
        self._common = None
    
    def features(self, text):
        d = defaultdict(int)
        
        # Better tokenizer, focuses only on words, not punctuation, for reduced feature set
        tokenizer = RegexpTokenizer(r'\w+')

        # Removed : kTOKENIZER.tokenizer() - Loop through list of tokenized words, ie, ['They', "'ll", 'save', 'and', 'invest', 'more', '.']
        for ii in tokenizer.tokenize(text):
            # Create key += 1, for dict value morphy_stem(ii), which is the base word of the tokenized word
            d[morphy_stem(ii)] += 1
        return d

    def commonFeatures(self, text):

        d = defaultdict(int)

        tokenizer = RegexpTokenizer(r'\w+')

        for ii in tokenizer.tokenize(text):
            for kk in self._common:
                morp_stem = morphy_stem(ii)
                if morp_stem == kk:
                    d[morp_stem] += 1
                else:
                    d['0']

        return d

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--subsample', type=float, default=1.0,
                        help='subsample this amount')
    args = parser.parse_args()
    
    # Init and create feature extractor (you may want to modify this)
    fe = FeatureExtractor()
    
    # Read in training data
    train = DictReader(open("train.csv", 'r'))
    
    # Split off dev section
    dev_train = []
    dev_test = []
    full_train = []

    # Train 
    for ii in train:
        if args.subsample < 1.0 and int(ii['id']) % 100 > 100 * args.subsample:
            continue
        feat = fe.features(ii['text'])
        if int(ii['id']) % 5 == 0:
            # Appends feature stem and category key
            dev_test.append((feat, ii['cat']))
        else:
            # Appends feature stem and category key
            dev_train.append((feat, ii['cat']))
        full_train.append((feat, ii['cat']))

    # Train a classifier
    print("Training classifier ...")
    classifier = nltk.classify.NaiveBayesClassifier.train(dev_train)
    # classifier = nltk.classify.Maxentclassifier.train(dev_train, 'IIS', trace=3, max_iter=2)

    # fe.commonFeatures()
    fe._common = classifier.most_informative_features(500)
    print("OK, common complete")
    
    dev_train = []
    dev_test = []
    full_train = []

    train = DictReader(open("train.csv", 'r'))

    for ii in train:
        if args.subsample < 1.0 and int(ii['id']) % 100 > 100 * args.subsample:
            continue
        feat = fe.commonFeatures(ii['text'])
        # print ii['text']
        if int(ii['id']) % 5 == 0:
            # Appends feature stem and category key
            dev_test.append((feat, ii['cat']))
        else:
            # Appends feature stem and category key
            dev_train.append((feat, ii['cat']))
        full_train.append((feat, ii['cat']))

    # Train a classifier
    print("(Again) Training classifier ...")
    classifier = nltk.classify.NaiveBayesClassifier.train(dev_train)

    # Test the classfier 
    right = 0
    total = len(dev_test)
    for ii in dev_test:
        prediction = classifier.classify(ii[0])
        if prediction == ii[1]:
            right += 1
    print("Accuracy on dev: %f" % (float(right) / float(total)))

    # Retrain on all data
    classifier = nltk.classify.NaiveBayesClassifier.train(dev_train + dev_test)
    
    # Read in test section
    test = {}
    for ii in DictReader(open("test.csv")):
        test[ii['id']] = classifier.classify(fe.features(ii['text']))

    # Write predictions
    o = DictWriter(open('pred.csv', 'w'), ['id', 'pred'])
    o.writeheader()
    for ii in sorted(test):
        o.writerow({'id': ii, 'pred': test[ii]})
