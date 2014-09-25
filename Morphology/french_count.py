import sys, re
from fst import FST
from fsmutils import composewords, trace

kFRENCH_TRANS = {0: "zero", 1: "un", 2: "deux", 3: "trois", 4:
                 "quatre", 5: "cinq", 6: "six", 7: "sept", 8: "huit",
                 9: "neuf", 10: "dix", 11: "onze", 12: "douze", 13:
                 "treize", 14: "quatorze", 15: "quinze", 16: "seize",
                 20: "vingt", 30: "trente", 40: "quarante", 50:
                 "cinquante", 60: "soixante", 100: "cent"}

kFRENCH_AND = 'et'

def prepare_input(integer):
    assert isinstance(integer, int) and integer < 1000 and integer >= 0, \
      "Integer out of bounds"
    return list("%03i" % integer)

def french_count():
    f = FST('french')

    f.add_state('0')
    f.add_state('1')
    f.add_state('2')
    f.add_state('3')
    f.add_state('4')
    f.add_state('5')
    f.add_state('6')
    f.add_state('7')
    f.add_state('8')
    f.add_state('9')
    f.add_state('10')
    f.add_state('11')
    f.add_state('12')
    f.add_state('13')
    f.add_state('14')
    f.add_state('15')
    f.add_state('16')
    f.add_state('17')
    f.add_state('18')
    f.add_state('19')
    f.add_state('20')
    f.add_state('21')
    f.add_state('22')
    f.add_state('23')
    f.add_state('24')
    f.add_state('25')

    f.initial_state = '0'

    f.set_final('1')
    f.set_final('3')
    f.set_final('6')
    f.set_final('7')
    f.set_final('8')
    f.set_final('9')
    f.set_final('11')
    f.set_final('13')
    f.set_final('14')
    f.set_final('18')
    f.set_final('20')

    zero = [0]
    one = [1]
    two_to_six = [2,3,4,5,6]
    one_to_six = [1,2,3,4,5,6]
    seven = [7]
    seven_eight_nine = [7,8,9]
    eight = [8]
    nine = [9]
    singles_all = [1,2,3,4,5,6,7,8,9]
    singles = [2,3,4,5,6,7,8,9]
    tens = [20,30,40,50]

    # Edge from initial to final, if preceding zero in input
    for i in zero:
        # f.add_arc('0','9', str(i), [kFRENCH_TRANS[i]])
        f.add_arc('0','0', str(i), ())
        f.add_arc('4','6', str(i), ())
        f.add_arc('5','8', str(i), ())
        f.add_arc('0','9', str(i), [kFRENCH_TRANS[i]])
        f.add_arc('10','11', str(i), [kFRENCH_TRANS[i+10]])
        f.add_arc('12','13', str(i), [kFRENCH_TRANS[20]])
        f.add_arc('16','18', str(i), [kFRENCH_TRANS[20],kFRENCH_TRANS[10]])
        f.add_arc('17','19', str(i), ())
        f.add_arc('19','9', str(i), ())

    for i in one:
        f.add_arc('0','2', str(i), ())
        f.add_arc('17','2', str(i), ())
        f.add_arc('0','17', str(i), [kFRENCH_TRANS[100]])
        f.add_arc('0','5', str(i), [kFRENCH_TRANS[i*10]])
        f.add_arc('17','5', str(i), [kFRENCH_TRANS[i*10]])
        f.add_arc('4','7', str(i), [kFRENCH_AND, kFRENCH_TRANS[i]])
        f.add_arc('10','11', str(i), [kFRENCH_AND, kFRENCH_TRANS[i+10]])
        f.add_arc('12','14', str(i), [kFRENCH_TRANS[20], kFRENCH_AND, kFRENCH_TRANS[i]])
        f.add_arc('16','20', str(i), [kFRENCH_TRANS[20], kFRENCH_AND, kFRENCH_TRANS[i+10]])

    for i in one_to_six:
        f.add_arc('2','3', str(i), [kFRENCH_TRANS[i+10]])

    for i in two_to_six:
        f.add_arc('0','4', str(i), [kFRENCH_TRANS[i*10]])
        f.add_arc('17','4', str(i), [kFRENCH_TRANS[i*10]])
        f.add_arc('10','11', str(i), [kFRENCH_TRANS[i+10]])
        f.add_arc('16','20', str(i), [kFRENCH_TRANS[20],kFRENCH_TRANS[i+10]])

    for i in singles:
        f.add_arc('4','7', str(i), [kFRENCH_TRANS[i]])
        f.add_arc('0','17', str(i), [kFRENCH_TRANS[i],kFRENCH_TRANS[100]])
        f.add_arc('12','14', str(i), [kFRENCH_TRANS[20], kFRENCH_TRANS[i]])

    for i in singles_all:
        f.add_arc('0','1', str(i), [kFRENCH_TRANS[i]])
        f.add_arc('19','1', str(i), [kFRENCH_TRANS[i]])

    for i in seven_eight_nine:
        f.add_arc('5','8', str(i), [kFRENCH_TRANS[i]])
        f.add_arc('10','11', str(i), [kFRENCH_TRANS[10], kFRENCH_TRANS[i]])
        f.add_arc('16','20', str(i), [kFRENCH_TRANS[20], kFRENCH_TRANS[10], kFRENCH_TRANS[i]])

    for i in seven:
        f.add_arc('0','10',str(i), [kFRENCH_TRANS[60]])
        f.add_arc('17','10',str(i), [kFRENCH_TRANS[60]])

    for i in eight:
        f.add_arc('0','12',str(i), [kFRENCH_TRANS[4]])
        f.add_arc('17','12',str(i), [kFRENCH_TRANS[4]])

    for i in nine:
        f.add_arc('0','16',str(i), [kFRENCH_TRANS[4]])
        f.add_arc('17','16',str(i), [kFRENCH_TRANS[4]])

    return f

if __name__ == '__main__':
    user_input = int(raw_input())
    f = french_count()
    if user_input:
        print user_input, '-->',
        print " ".join(f.transduce(prepare_input(user_input)))