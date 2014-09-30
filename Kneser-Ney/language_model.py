# Reed Anderson

from __future__ import division
from math import log, exp
from collections import defaultdict
from string import lower
import argparse

from numpy import mean

import nltk
from nltk import FreqDist
from nltk.util import bigrams
from nltk.tokenize import TreebankWordTokenizer, RegexpTokenizer

kLM_ORDER = 2
kUNK_CUTOFF = 3
kNEG_INF = -1e6

kSTART = "<s>"
kEND = "</s>"

def lg(x):
    return log(x) / log(2.0)

class BigramLanguageModel:

    def __init__(self, unk_cutoff, jm_lambda=0.6, dirichlet_alpha=0.1,
                 katz_cutoff=5, kn_discount=0.1, kn_concentration=1.0,
                 tokenize_function=TreebankWordTokenizer().tokenize,
                 normalize_function=lower):
        self._unk_cutoff = unk_cutoff
        self._jm_lambda = jm_lambda
        self._dirichlet_alpha = dirichlet_alpha
        self._katz_cutoff = katz_cutoff
        self._kn_concentration = kn_concentration
        self._kn_discount = kn_discount
        self._vocab_final = False

        self._tokenizer = tokenize_function
        self._normalizer = normalize_function
        
        # Add your code here!
        self._vocab_freq = FreqDist()
        self._gram_freq = FreqDist()
        self._context_freq = FreqDist()

        self._vocab_freq[kSTART] += kUNK_CUTOFF + 1
        self._vocab_freq[kEND] += kUNK_CUTOFF + 1


    def train_seen(self, word, count=1):
        """
        Tells the language model that a word has been seen @count times.  This
        will be used to build the final vocabulary.
        """
        assert not self._vocab_final, \
            "Trying to add new words to finalized vocab"

        self._vocab_freq.inc(word, count)

        return self._vocab_freq[word] 

    def tokenize(self, sent):
        """
        Returns a generator over tokens in the sentence.  

        No modify
        """
        for ii in self._tokenizer(sent):
            yield ii
        
    def vocab_lookup(self, word):
        """
        Given a word, provides a vocabulary representation.  Words under the
        cutoff threshold shold have the same value.  All words with counts
        greater than or equal to the cutoff should be unique and consistent.
        """

        assert self._vocab_final, \
            "Vocab must be finalized before looking up words"

        freqCount = self._vocab_freq[word]

        if freqCount > self._unk_cutoff:
            return word
        else:
            return "<UNK>"

    def finalize(self):
        """
        Fixes the vocabulary as static, prevents keeping additional vocab from
        being added

        No modify
        """
        self._vocab_final = True

    def tokenize_and_censor(self, sentence):
        """
        Given a sentence, yields a sentence suitable for training or
        testing.  Prefix the sentence with <s>, replace words not in
        the vocabulary with <UNK>, and end the sentence with </s>.

        No modify
        """
        yield self.vocab_lookup(kSTART)
        for ii in self._tokenizer(sentence):
            yield self.vocab_lookup(self._normalizer(ii))
        yield self.vocab_lookup(kEND)


    def normalize(self, word):
        """
        Normalize a word

        No modify
        """
        return self._normalizer(word)


    def mle(self, context, word):
        """
        Return the log MLE estimate of a word given a context.  If the
        MLE would be negative infinity, use kNEG_INF
        """
        prob = 0.0
        bgram = (context, word)

        numer = self._gram_freq[bgram]
        denom = self._context_freq[context]

        if denom == 0:
            return kNEG_INF

        if self._gram_freq[bgram] != 0:
            prob = numer / denom

        if prob == 0.0:
            return kNEG_INF
        else:
            return lg(prob)

    def laplace(self, context, word):
        """
        Return the log MLE estimate of a word given a context.
        """
        bgram = (context, word)

        numer = self._gram_freq[bgram] + 1
        denom = len(self._vocab_freq.keys()) + self._context_freq[context]

        prob = numer / denom

        return lg(prob)

    def good_turing(self, context, word):
        """
        Return the Good Turing probability of a word given a context
        """
        return 0.0

    def jelinek_mercer(self, context, word):
        """
        Return the Jelinek-Mercer log probability estimate of a word
        given a context; interpolates context probability with the
        overall corpus probability.
        """

        bigram = (context, word)
        bigram_prob = 0

        unigram_prob = (1 - self._jm_lambda) * (1 / len(self._vocab_freq))
    
        for i in self._gram_freq:
            if i == bigram:
                bigram_count = 1
                bigram_prob = (self._jm_lambda+unigram_prob) * bigram_count

        result = unigram_prob + bigram_prob
        return lg(result)

    def kneser_ney(self, context, word):
        """
        Return the log probability of a word given a context given
        Kneser Ney backoff
        """
        
        bgram = (context, word)
        unigram_freq = FreqDist()

        theta = self._kn_concentration
        vocabulary = 1 / len(self._vocab_freq.keys())
        discount_delta = self._kn_discount
        unigram_T = len(self._context_freq.keys())
        bigram_T = self._context_freq[context]

        for i in self._gram_freq:
            unigram_freq.inc(i[1])

        # Unigram Restaurant
        # C_0,x
        count_unirest_wordTable = unigram_freq[word]
        # C_0,.
        count_unirest_allTable = unigram_freq.N()

        # u_Bigram Restaurant
        # C_u,x
        count_birest_wordTable = self._gram_freq[bgram]

        # C_u,.
        count_birest_allTable = self._context_freq[context]

        existingTable_numer = count_birest_wordTable - discount_delta
        existingTable_denom = theta + count_birest_allTable 
        existingTable = existingTable_numer / existingTable_denom

        if existingTable < 0:
            existingTable = 0

        newTable_numer = theta + (bigram_T*discount_delta)
        newTable_denom = theta + count_birest_allTable 
        newTable = newTable_numer / newTable_denom

        back_a_numer = count_unirest_wordTable - discount_delta
        back_a_denom = count_unirest_allTable + theta
        back_a = back_a_numer / back_a_denom
        if back_a < 0:
            back_a = 0

        back_b_numer = theta + (unigram_T * discount_delta)
        back_b_denom = count_unirest_allTable + theta
        back_b = back_b_numer / back_b_denom
        back_b = back_b * vocabulary

        result = existingTable + (newTable*(back_a+back_b))
        return lg(result)



    def dirichlet(self, context, word):
        """
        Additive smoothing, assuming independent Dirichlets with fixed
        hyperparameter.
        """

        prob = 0.0
        bgram = (context, word)

        numer = self._gram_freq[bgram] + self._dirichlet_alpha
        denom = self._context_freq[context] + (self._dirichlet_alpha * len(self._vocab_freq.keys()))

        prob = numer / denom

        return lg(prob)


    def add_train(self, sentence):
        """
        Add the counts associated with a sentence.
        """

        # You'll need to complete this function, but here's a line of code that
        # will hopefully get you started.

        # Add new vocab counts
        nopunc_tokenize = RegexpTokenizer(r'\w+')
        nopunc_list = nopunc_tokenize.tokenize(sentence)
        for i in nopunc_list:
            self._vocab_freq[i] += 1

        # Count occurances of bigrams
        for context, word in bigrams(self.tokenize_and_censor(sentence)):
            x = (context, word)
            self._gram_freq.inc(x)
            self._context_freq.inc(context)


    def perplexity(self, sentence, method):
        """
        Compute the perplexity of a sentence given a estimation method

        No modify
        """
        return 2.0 ** (-1.0 * mean([method(context, word) for context, word in \
                                    bigrams(self.tokenize_and_censor(sentence))]))

    def sample(self, samples=25):
        """
        Sample words from the language model.
        
        @arg samples The number of samples to return.
        """
        yield ""
        return

if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--jm_lambda", help="Parameter that controls " + \
                           "interpolation between unigram and bigram",
                           type=float, default=0.6, required=False)
    argparser.add_argument("--dir_alpha", help="Dirichlet parameter " + \
                           "for pseudocounts",
                           type=float, default=0.1, required=False)
    argparser.add_argument("--unk_cutoff", help="How many times must a word " + \
                           "be seen before it enters the vocabulary",
                           type=int, default=2, required=False)    
    argparser.add_argument("--katz_cutoff", help="Cutoff when to use Katz " + \
                           "backoff",
                           type=float, default=0.0, required=False)
    argparser.add_argument("--lm_type", help="Which smoothing technique to use",
                           type=str, default='mle', required=False)
    argparser.add_argument("--brown_limit", help="How many sentences to add " + \
                           "from Brown",
                           type=int, default=-1, required=False)
    argparser.add_argument("--kn_discount", help="Kneser-Ney discount parameter",
                           type=float, default=0.1, required=False)
    argparser.add_argument("--kn_concentration", help="Kneser-Ney concentration parameter",
                           type=float, default=1.0, required=False)
    argparser.add_argument("--method", help="Which LM method we use",
                           type=str, default='laplace', required=False)
    
    args = argparser.parse_args()    
    lm = BigramLanguageModel(kUNK_CUTOFF, jm_lambda=args.jm_lambda,
                             dirichlet_alpha=args.dir_alpha,
                             katz_cutoff=args.katz_cutoff,
                             kn_concentration=args.kn_concentration,
                             kn_discount=args.kn_discount)

    for ii in nltk.corpus.brown.sents():
        for jj in lm.tokenize(" ".join(ii)):
            lm.train_seen(lm._normalizer(jj))

    print("Done looking at all the words, finalizing vocabulary")
    lm.finalize()

    sentence_count = 0
    for ii in nltk.corpus.brown.sents():
        sentence_count += 1
        lm.add_train(" ".join(ii))

        if args.brown_limit > 0 and sentence_count >= args.brown_limit:
            break

    print("Trained language model with %i sentences from Brown corpus." % sentence_count)
    assert args.method in ['kneser_ney', 'mle', 'dirichlet', 'jelinek_mercer', 'good_turing', 'laplace'], \
      "Invalid estimation method"

    sent = raw_input()
    while sent:
        print("#".join(str(x) for x in lm.tokenize_and_censor(sent)))
        print(lm.perplexity(sent, getattr(lm, args.method)))
        sent = raw_input()
