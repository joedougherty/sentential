# -*- coding: utf-8 -*-

import operator

ENV =  {'and': operator.and_,
        'or' : operator.or_,
        'not': operator.not_,
        '->' : lambda p, q: (not p) or q,
        'iff': lambda p, q: ((p or (not q)) and ((not p) or q))}

# Some delightful little aliases
ENV['&'] = ENV['and']
ENV['v'] = ENV['or']
ENV['¬'] = ENV['not']
ENV['~'] = ENV['not']
ENV['!'] = ENV['not']
ENV['='] = ENV['iff']
