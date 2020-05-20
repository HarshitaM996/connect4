#!/usr/bin/env python

#-------------------------------------------------------------------------------
# Name:        logical_expression
# Purpose:     Contains logical_expression class, inference engine,
#              and assorted functions
#
# Created:     09/25/2011
# Last Edited: 07/22/2013  
# Notes:       *This contains code ported by Christopher Conly from C++ code
#               provided by Dr. Vassilis Athitsos
#              *Several integer and string variables are put into lists. This is
#               to make them mutable so each recursive call to a function can
#               alter the same variable instead of a copy. Python won't let us
#               pass the address of the variables, so put it in a list which is
#               passed by reference. We can also now pass just one variable in
#               the class and the function will modify the class instead of a
#               copy of that variable. So, be sure to pass the entire list to a
#               function (i.e. if we have an instance of logical_expression
#               called le, we'd call foo(le.symbol,...). If foo needs to modify
#               le.symbol, it will need to index it (i.e. le.symbol[0]) so that
#               the change will persist.
#              *Written to be Python 2.4 compliant for omega.uta.edu
#-------------------------------------------------------------------------------

import sys
from copy import copy


class logical_expression:
    """A logical statement/sentence/expression class"""
    # All types need to be mutable, so we don't have to pass in the whole class.
    # We can just pass, for example, the symbol variable to a function, and the
    # function's changes will actually alter the class variable. Thus, lists.
    def __init__(self):
        self.symbol = ['']
        self.connective = ['']
        self.subexpressions = []


def eval_expression(expr, sample):
    if expr.symbol[0]:
        return sample[expr.symbol[0]]
    
    else:
        if expr.connective[0] == 'not':
            return not eval_expression(expr.subexpressions[0], sample)
        
        elif expr.connective[0] == 'and':
            for subexpr in expr.subexpressions:
                if eval_expression(subexpr, sample) == False:
                    return False
            return True
        
        elif expr.connective[0] == 'or':
            for subexpr in expr.subexpressions:
                if eval_expression(subexpr, sample) == True:
                    return True
            return False

        elif expr.connective[0] == 'if':
            if eval_expression(expr.subexpressions[1], sample) == True:
                return True
            elif eval_expression(expr.subexpressions[0], sample) == False:
                return True
            else:
                return False
        
        elif expr.connective[0] == 'iff':
            if eval_expression(expr.subexpressions[1], sample) == eval_expression(expr.subexpressions[0], sample):
                return True
            else:
                return False

        elif expr.connective[0] == 'xor':
            values = []
            for subexpr in expr.subexpressions:
                values.append(eval_expression(subexpr, sample))
            if values.count(True) % 2 == 0:
                return False
            else:
                return True
         
            
def find_symbols(logical_expression, statement):

    def add_symbol(expr):
        if expr.symbol[0]: # If it is a base case (symbol)
            if expr.symbol[0] not in symbols: # checking for unique symbol
                symbols.append(expr.symbol[0])

        else: # Otherwise it is a subexpression
            for subexpr in expr.subexpressions:
                add_symbol(subexpr)

    symbols = []
    add_symbol(logical_expression)
    add_symbol(statement)
    return symbols


def print_expression(expr, separator):
    """Prints the given expression using the given separator"""
    if expr == 0 or expr == None or expr == '':
        print '\nINVALID\n'

    elif expr.symbol[0]: # If it is a base case (symbol)
        sys.stdout.write('%s' % expr.symbol[0])

    else: # Otherwise it is a subexpression
        sys.stdout.write('(%s' % expr.connective[0])
        for subexpr in expr.subexpressions:
            sys.stdout.write(' ')
            print_expression(subexpr, '')
            sys.stdout.write('%s' % separator)
        sys.stdout.write(')')


def read_expression(input_string, counter=[0]):
    """Reads the next logical expression in input_string"""
    # Note: counter is a list because it needs to be a mutable object so the
    # recursive calls can change it, since we can't pass the address in Python.
    result = logical_expression()
    length = len(input_string)
    while True:
        if counter[0] >= length:
            break

        if input_string[counter[0]] == ' ':    # Skip whitespace
            counter[0] += 1
            continue

        elif input_string[counter[0]] == '(':  # It's the beginning of a connective
            counter[0] += 1
            read_word(input_string, counter, result.connective)
            read_subexpressions(input_string, counter, result.subexpressions)
            break

        else:  # It is a word
            read_word(input_string, counter, result.symbol)
            break
    return result


def read_subexpressions(input_string, counter, subexpressions):
    """Reads a subexpression from input_string"""
    length = len(input_string)
    while True:
        if counter[0] >= length:
            print '\nUnexpected end of input.\n'
            return 0

        if input_string[counter[0]] == ' ':     # Skip whitespace
            counter[0] += 1
            continue

        if input_string[counter[0]] == ')':     # We are done
            counter[0] += 1
            return 1

        else:
            expr = read_expression(input_string, counter)
            subexpressions.append(expr)


def read_word(input_string, counter, target):
    """Reads the next word of an input string and stores it in target"""
    while True:
        if counter[0] >= len(input_string):
            break

        if input_string[counter[0]].isalnum() or input_string[counter[0]] == '_':
            target[0] += input_string[counter[0]]
            counter[0] += 1

        elif input_string[counter[0]] == ')' or input_string[counter[0]] == ' ':
            break

        else:
            print('Unexpected character %s.' % input_string[counter[0]])
            sys.exit(1)


def valid_expression(expr):
    """Determines if the given expression is valid according to our rules"""
    if expr.symbol[0]:
        return valid_symbol(expr.symbol[0])

    if expr.connective[0].lower() == 'if' or expr.connective[0].lower() == 'iff':
        if len(expr.subexpressions) != 2:
            print('Error: connective "%s" with %d arguments.' %
                        (expr.connective[0], len(expr.subexpressions)))
            return 0

    elif expr.connective[0].lower() == 'not':
        if len(expr.subexpressions) != 1:
            print('Error: connective "%s" with %d arguments.' %
                        (expr.connective[0], len(expr.subexpressions)))
            return 0

    elif expr.connective[0].lower() != 'and' and \
         expr.connective[0].lower() != 'or' and \
         expr.connective[0].lower() != 'xor':
        print('Error: unknown connective %s.' % expr.connective[0])
        return 0

    for subexpr in expr.subexpressions:
        if not valid_expression(subexpr):
            return 0
    return 1


def valid_symbol(symbol):
    """Returns whether the given symbol is valid according to our rules."""
    if not symbol:
        return 0

    for s in symbol:
        if not s.isalnum() and s != '_':
            return 0
    return 1

# End of ported code
#-------------------------------------------------------------------------------

# Add all your functions here