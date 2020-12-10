# -*- coding: utf-8 -*-
"""
Created on Thu Dec 10 13:51:10 2020

@author: Rahul Kothuri, Isak Nyberg
"""
from nltk import Nonterminal,nonterminals,Production,CFG
from nltk.parse.generate import generate

grammar = CFG.fromstring("""
        S ->  NP VP 
        NP -> Det 
        VP -> NLNP VBP Adj |LN PV RB |LN PV | LN VBZ NP | LNP V RB | NLN VBZ Adj 
        VP -> LN LVBZ 'the' LN | LN LVBZ 'the' NLN |LN LVBZ 'the' NLNP
        Det -> 'Those'
        Det -> 'A'
        Det -> 'the'
        Det -> 'that'
        Det -> 'The'
        LN -> 'girl' | 'boy' | 'dog' 
        LNP -> 'boys'
        NLN -> 'house'
        NLNP -> 'crackers'
        V -> 'run' 
        PV -> 'runs'| 'eats'
        VBP -> 'are'
        VBZ -> 'is'
        LVBZ -> 'likes'
        RB -> 'fast'
        Adj ->'good'
        EAdj -> 'happy'
        Adj -> 'big'
    """)
for sentence in generate(grammar,depth=4):
    print(' '.join(sentence))
