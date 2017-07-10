# -*- coding: utf-8 -*-

import operator

ENV =  {'and': operator.and_,
        'or'  : operator.or_,
        'not' : operator.not_}

# Some delightful little aliases
ENV['&'] = ENV['and']
ENV['v'] = ENV['or']
ENV['¬'] = ENV['not']
ENV['~'] = ENV['not']
