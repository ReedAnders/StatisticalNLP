# Author: Reed Anderson
# Date: 9/12/2014

# Use word_tokenize to split raw text into words
from string import punctuation

import nltk, re
from nltk.tokenize import*

class LimerickDetector:

    def __init__(self):
        """
        Initializes the object to have a pronunciation dictionary available
        """
        self._pronunciations = nltk.corpus.cmudict.dict()

    def num_syllables(self, word):
        """
        Returns the number of syllables in a word.  If there's more than one
        pronunciation, take the shorter one.  If there is no entry in the
        dictionary, return 1.
        """

        pronouncation = 0
        firstProno = 0
        count = 0

        x = word
        t = self._pronunciations

        for i in (x,):
            try:
                pronouncation = t[i]
                firstProno = pronouncation[0]
            except KeyError:
                return 1

        if len(pronouncation) > 1:
            if len(pronouncation[0]) <= len(pronouncation[1]):
                firstProno = pronouncation[0]
            else:
                firstProno = pronouncation[1]

        for i in firstProno:
            syll = re.search(r'[AEIOU]', i)
            if syll != None:
                count += 1

        return count

    def rhymes(self, a, b):
        """
        Returns True if two words (represented as lower-case strings) rhyme,
        False otherwise.
        """

        a = a.lower()
        b = b.lower()

        t = self._pronunciations

        doubleA, doubleB, doubleAB = False, False, False
        rhymes = False
        count = 0

        pattern = re.compile(r'[AEIOU]')

        # Convert value to array
        for i in (a,):
            try:
                a = t[i]
            except KeyError:
                return False

        for i in (b,):
            try:
                b = t[i]
            except KeyError:
                return False

        # Get rid of 2d madness
        if len(a) is 1:
            a = a[0]
        else:
            doubleA = True
            a2 = a[1]
            a = a[0]

        if len(b) is 1:
            b = b[0]
        else:
            doubleB = True
            b2 = b[1]
            b = b[0]

        if doubleA and doubleB:
            doubleAB = True

        # **Cut and Compare**
        # Only TWO syllables
        if len(a) <= 2 or len(b) <= 2:
            del(a[:len(a)-1])
            del(b[:len(b)-1])

            if a == b:
                rhymes = True
                return rhymes

            for i in a[::-1]:
                for j in b[::-1]:
                    vowel_a = re.match(pattern, i)
                    vowel_b = re.match(pattern, j)
                    if vowel_a != None:
                        i = i[:1]
                    if vowel_b != None:
                        j = j[:1]

                    if i == j:
                        return True
                    else:
                        pass


        # Only THREE syllables
        if len(a) <= 3 or len(b) <= 3:
            del(a[:len(a)-2])
            del(b[:len(b)-2])

            if a == b:
                rhymes = True
                return rhymes

            for i in a[::-1]:
                for j in b[::-1]:
                    vowel_a = re.match(pattern, i)
                    vowel_b = re.match(pattern, j)
                    if vowel_a != None:
                        i = i[:1]
                    if vowel_b != None:
                        j = j[:1]

                    if i == j:
                        count += 1
                    else:
                        pass

                    if count == 2:
                        return True

        # At least FOUR syllables
        if len(a) > 3 or len(b) > 3:
            del(a[:len(a)-3])
            del(b[:len(b)-3])

            if a == b:
                rhymes = True
                return rhymes

            for i in a[::-1]:
                for j in b[::-1]:
                    vowel_a = re.match(pattern, i)
                    vowel_b = re.match(pattern, j)
                    if vowel_a != None:
                        i = i[:1]
                    if vowel_b != None:
                        j = j[:1]

                    if i == j:
                        count += 1
                    else:
                        pass

                    if count == 3:
                        return True

        # Check for alt pronos --- A2 & B2 
        if doubleAB:
            # **Cut and Compare --- **
            # Only TWO syllables
            if len(a2) <= 2 or len(b2) <= 2:
                del(a2[:len(a2)-1])
                del(b2[:len(b2)-1])

                if a2 == b2:
                    rhymes = True
                    return rhymes

                for i in a2[::-1]:
                    for j in b2[::-1]:
                        vowel_a2 = re.match(pattern, i)
                        vowel_b2 = re.match(pattern, j)
                        if vowel_a2 != None:
                            i = i[:1]
                        if vowel_b2 != None:
                            j = j[:1]

                        if i == j:
                            return True
                        else:
                            pass


            # Only THREE syllables
            if len(a2) <= 3 or len(b2) <= 3:
                del(a2[:len(a2)-2])
                del(b2[:len(b2)-2])

                if a2 == b2:
                    rhymes = True
                    return rhymes

                for i in a2[::-1]:
                    for j in b2[::-1]:
                        vowel_a2 = re.match(pattern, i)
                        vowel_b2 = re.match(pattern, j)
                        if vowel_a2 != None:
                            i = i[:1]
                        if vowel_b2 != None:
                            j = j[:1]

                        if i == j:
                            count += 1
                        else:
                            pass

                        if count == 2:
                            return True

            # At least FOUR syllables
            if len(a2) > 3 or len(b2) > 3:
                del(a2[:len(a2)-3])
                del(b2[:len(b2)-3])

                if a2 == b2:
                    rhymes = True
                    return rhymes

                for i in a2[::-1]:
                    for j in b2[::-1]:
                        vowel_a2 = re.match(pattern, i)
                        vowel_b2 = re.match(pattern, j)
                        if vowel_a2 != None:
                            i = i[:1]
                        if vowel_b2 != None:
                            j = j[:1]

                        if i == j:
                            count += 1
                        else:
                            pass

                        if count == 3:
                            return True 

        # Check for alt pronos --- A2 
        if doubleA:
            # **Cut and Compare --- **
            # Only TWO syllables
            if len(a2) <= 2 or len(b) <= 2:
                del(a2[:len(a2)-1])
                del(b[:len(b)-1])

                if a2 == b:
                    rhymes = True
                    return rhymes

                for i in a2[::-1]:
                    for j in b[::-1]:
                        vowel_a2 = re.match(pattern, i)
                        vowel_b = re.match(pattern, j)
                        if vowel_a2 != None:
                            i = i[:1]
                        if vowel_b != None:
                            j = j[:1]

                        if i == j:
                            return True
                        else:
                            pass


            # Only THREE syllables
            if len(a2) <= 3 or len(b) <= 3:
                del(a2[:len(a2)-2])
                del(b[:len(b)-2])

                if a2 == b:
                    rhymes = True
                    return rhymes

                for i in a2[::-1]:
                    for j in b[::-1]:
                        vowel_a2 = re.match(pattern, i)
                        vowel_b = re.match(pattern, j)
                        if vowel_a2 != None:
                            i = i[:1]
                        if vowel_b != None:
                            j = j[:1]

                        if i == j:
                            count += 1
                        else:
                            pass

                        if count == 2:
                            return True

            # At least FOUR syllables
            if len(a2) > 3 or len(b) > 3:
                del(a2[:len(a2)-3])
                del(b[:len(b)-3])

                if a2 == b:
                    rhymes = True
                    return rhymes

                for i in a2[::-1]:
                    for j in b[::-1]:
                        vowel_a2 = re.match(pattern, i)
                        vowel_b = re.match(pattern, j)
                        if vowel_a2 != None:
                            i = i[:1]
                        if vowel_b != None:
                            j = j[:1]

                        if i == j:
                            count += 1
                        else:
                            pass

                        if count == 3:
                            return True

        # Check for alt pronos --- B2 
        if doubleB:
            # **Cut and Compare --- **
            # Only TWO syllables
            if len(a) <= 2 or len(b2) <= 2:
                del(a[:len(a)-1])
                del(b2[:len(b2)-1])

                if a == b2:
                    rhymes = True
                    return rhymes

                for i in a[::-1]:
                    for j in b2[::-1]:
                        vowel_a = re.match(pattern, i)
                        vowel_b2 = re.match(pattern, j)
                        if vowel_a != None:
                            i = i[:1]
                        if vowel_b2 != None:
                            j = j[:1]

                        if i == j:
                            return True
                        else:
                            pass


            # Only THREE syllables
            if len(a) <= 3 or len(b2) <= 3:
                del(a[:len(a)-2])
                del(b2[:len(b2)-2])

                if a == b2:
                    rhymes = True
                    return rhymes

                for i in a[::-1]:
                    for j in b2[::-1]:
                        vowel_a = re.match(pattern, i)
                        vowel_b2 = re.match(pattern, j)
                        if vowel_a != None:
                            i = i[:1]
                        if vowel_b2 != None:
                            j = j[:1]

                        if i == j:
                            count += 1
                        else:
                            pass

                        if count == 2:
                            return True

            # At least FOUR syllables
            if len(a) > 3 or len(b2) > 3:
                del(a[:len(a)-3])
                del(b2[:len(b2)-3])

                if a == b2:
                    rhymes = True
                    return rhymes

                for i in a[::-1]:
                    for j in b2[::-1]:
                        vowel_a = re.match(pattern, i)
                        vowel_b2 = re.match(pattern, j)
                        if vowel_a != None:
                            i = i[:1]
                        if vowel_b2 != None:
                            j = j[:1]

                        if i == j:
                            count += 1
                        else:
                            pass

                        if count == 3:
                            return True        

        return rhymes

    def is_limerick(self, text):
        """
        Takes text where lines are separated by newline characters.  Returns
        True if the text is a limerick, False otherwise.

        A limerick is defined as a poem with the form AABBA, where the A lines
        rhyme with each other, the B lines rhyme with each other (and not the A
        lines).

        (English professors may disagree with this definition, but that's what
        we're using here.)
        """
        array = []
        ending = []
        bobo = line_tokenize(text)
        pattern = re.compile(r'[a-z]')

        lim = False

        # Return last word in sentence
        for i in bobo:
            array.append(word_tokenize(i))

        for i in array:
            tempLen = len(i)
            abcs = re.match(pattern, i[tempLen-1])
            if abcs != None:
                ending.append(i[tempLen-1])
            else:
                ending.append(i[tempLen-2])

        if len(ending) != 5:
            lim = False
            return lim

        # Still working on Python loops, this somehow was buggy otherwise
        for c in punctuation:
            ending[0] = ending[0].replace(c,"")
            ending[1] = ending[1].replace(c,"")
            ending[2] = ending[2].replace(c,"")
            ending[3] = ending[3].replace(c,"")
            ending[4] = ending[4].replace(c,"")

        # AABBA
        if self.rhymes(ending[0],ending[1]) == True:
            if self.rhymes(ending[2],ending[3]) == True:
                if self.rhymes(ending[4],ending[0]) == True:
                    if self.rhymes(ending[0],ending[2]) != True:
                        lim = True

        return lim

if __name__ == "__main__":
    buffer = ""
    inline = " "
    while inline != "":
        buffer += "%s\n" % inline
        inline = raw_input()

    ld = LimerickDetector()
    print("%s\n-----------\n%s" % (buffer.strip(), ld.is_limerick(buffer)))