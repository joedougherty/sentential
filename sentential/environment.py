# -*- coding: utf-8 -*-

import operator


def conditional(p, q):
    return (not p) or q


def biconditional(p, q):
    return ((p or (not q)) and ((not p) or q))


ENV =  {'and': operator.and_,
        'or' : operator.or_,
        'not': operator.not_,
        '->' : conditional,
        'iff': biconditional}

# Some delightful little aliases
ENV['&'] = ENV['and']
ENV['v'] = ENV['or']
ENV['¬'] = ENV['not']
ENV['~'] = ENV['not']
ENV['!'] = ENV['not']
ENV['='] = ENV['iff']
ENV['<->'] = ENV['iff']
