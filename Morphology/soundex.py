from fst import FST
import string, sys
from fsmutils import composechars, trace

def letters_to_numbers():
    """
    Returns an FST that converts letters to numbers as specified by
    the soundex algorithm
    """

    # Let's define our first FST
    f1 = FST('soundex-generate')
    aeoy = ['a','e','h','i','o','u','w','y']
    one = ['b','f','p','v']
    two = ['c','g','j','k','q','s','x','z']
    three = ['d','t']
    four = ['l'] 
    five = ['m','n']
    six = ['r']

    # Indicate that '1' is the initial state
    f1.add_state('initial')
    f1.add_state('0')
    f1.add_state('1')
    f1.add_state('2')
    f1.add_state('3')
    f1.add_state('4')
    f1.add_state('5')
    f1.add_state('6')
    f1.initial_state = 'initial'

    # Set all the final states
    f1.set_final('0')
    f1.set_final('1')
    f1.set_final('2')
    f1.set_final('3')
    f1.set_final('4')
    f1.set_final('5')
    f1.set_final('6')

    # Add the rest of the arcs
    for letter in string.ascii_letters:
        f1.add_arc('initial','0',(letter),(letter))
        if letter in aeoy:
            f1.add_arc('0','0', (letter), ())
            f1.add_arc('1','0', (letter), ())
            f1.add_arc('2','0', (letter), ())
            f1.add_arc('3','0', (letter), ())
            f1.add_arc('4','0', (letter), ())
            f1.add_arc('5','0', (letter), ())
            f1.add_arc('6','0', (letter), ())
        else:
            if letter in one:
                f1.add_arc('0','1', (letter), '1')
                f1.add_arc('2','1', (letter), '1')
                f1.add_arc('3','1', (letter), '1')
                f1.add_arc('4','1', (letter), '1')
                f1.add_arc('5','1', (letter), '1')
                f1.add_arc('6','1', (letter), '1')
                f1.add_arc('1','0', (letter), ())
            if letter in two:
                f1.add_arc('0','2', (letter), '2')
                f1.add_arc('1','2', (letter), '2')
                f1.add_arc('3','2', (letter), '2')
                f1.add_arc('4','2', (letter), '2')
                f1.add_arc('5','2', (letter), '2')
                f1.add_arc('6','2', (letter), '2')
                f1.add_arc('2','0', (letter), ())
            if letter in three:
                f1.add_arc('0','3', (letter), '3')
                f1.add_arc('1','3', (letter), '3')
                f1.add_arc('2','3', (letter), '3')
                f1.add_arc('4','3', (letter), '3')
                f1.add_arc('5','3', (letter), '3')
                f1.add_arc('6','3', (letter), '3')
                f1.add_arc('3','0', (letter), ())
            if letter in four:
                f1.add_arc('0','4', (letter), '4')
                f1.add_arc('1','4', (letter), '4')
                f1.add_arc('2','4', (letter), '4')
                f1.add_arc('3','4', (letter), '4')
                f1.add_arc('5','4', (letter), '4')
                f1.add_arc('6','4', (letter), '4')
                f1.add_arc('4','0', (letter), ())
            if letter in five:
                f1.add_arc('0','5', (letter), '5')
                f1.add_arc('1','5', (letter), '5')
                f1.add_arc('2','5', (letter), '5')
                f1.add_arc('3','5', (letter), '5')
                f1.add_arc('4','5', (letter), '5')
                f1.add_arc('6','5', (letter), '5')
                f1.add_arc('5','0', (letter), ())
            if letter in six:
                f1.add_arc('0','6', (letter), '6')
                f1.add_arc('1','6', (letter), '6')
                f1.add_arc('2','6', (letter), '6')
                f1.add_arc('3','6', (letter), '6')
                f1.add_arc('4','6', (letter), '6')
                f1.add_arc('5','6', (letter), '6')
                f1.add_arc('6','0', (letter), ())

    return f1

def truncate_to_three_digits():
    """
    Create an FST that will truncate a soundex string to three digits
    """

    # Ok so now let's do the second FST, the one that will truncate
    # the number of digits to 3
    f2 = FST('soundex-truncate')

    # Indicate initial and final states
    f2.add_state('1')
    f2.add_state('2')
    f2.add_state('3')
    f2.add_state('4')
    f2.initial_state = '1'
    f2.set_final('1')
    f2.set_final('2')
    f2.set_final('3')
    f2.set_final('4')

    # Adds letters from input string of 'A###0000'
    for letter in string.letters:
        f2.add_arc('1', '1', (letter), (letter))

    # Adds numbers from first FST of range 0-9
    for n in range(10):
        f2.add_arc('1', '2', str(n), (str(n)))
        f2.add_arc('2', '3', str(n), (str(n)))
        f2.add_arc('3', '4', str(n), (str(n)))
        f2.add_arc('4', '4', str(n), ())


    return f2

def add_zero_padding():
    # Now, the third fst - the zero-padding fst
    f3 = FST('soundex-padzero')

    f3.add_state('1')
    f3.add_state('2')
    f3.add_state('3')
    f3.add_state('4')
    
    f3.initial_state = '1'
    f3.set_final('4')

    for letter in string.letters:
        f3.add_arc('1', '1', letter, letter)
    for number in xrange(10):
        f3.add_arc('1', '2', str(number), str(number))
        f3.add_arc('2', '3', str(number), str(number))
        f3.add_arc('3', '4', str(number), str(number))
    
    for n in range(10):
        f3.add_arc('1', '4', (), '000')
        f3.add_arc('2', '4', (), '00')
        f3.add_arc('3', '4', (), '0')

    return f3

if __name__ == '__main__':
    user_input = raw_input().strip().lower()
    f1 = letters_to_numbers()
    f2 = truncate_to_three_digits()
    f3 = add_zero_padding()

    if user_input:
        print("%s -> %s" % (user_input, composechars(tuple(user_input), f1, f2, f3)))
