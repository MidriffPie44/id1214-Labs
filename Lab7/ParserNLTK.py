# -*- coding: utf-8 -*-
"""
Created on Wed Dec  9 13:04:57 2020

@author: Rahul Kothuri, Isak Nyberg
"""
import nltk
from nltk import Nonterminal,nonterminals,Production,CFG
w1 = Nonterminal("NP")
w2 = Nonterminal("VP")
S,NP,VP = nonterminals('S,NP,VP')
NLN,LN,V,LNP,DT,VBP,Adj,VBZ,RB= nonterminals('NLN,LN,V,LNP, DT, VBP, Adj,VBZ,RB')
prod1 = Production(S, [NP, VP])
prod2 = Production(NP, [DT, NP])
grammar = CFG.fromstring("""
        S ->  NP VP 
        NP -> Det LN | Det NLN | Det LNP
        VP -> V NP | VBP Adj | VBZ Adj | V RB | V | LN VBZ NP
        Det -> 'The'
        Det -> 'A'
        Det -> 'the'
        Det -> 'that'
        LN -> 'girl' | 'boy' | 'dog' 
        LNP -> 'boys'
        NLN -> 'house' | 'crackers'
        V -> 'eats'
        V -> 'run' | 'runs'
        VBP -> 'are'
        VBZ -> 'is'
        VBZ -> 'likes'
        RB -> 'fast'
        Adj ->'good'
        Adj -> 'happy'
        Adj -> 'big'
    """)
sentence = ['The girl likes the dog.',
            'A boy likes that house.',
            'The crackers are good.',
            'The girl eats.',
            'The dog runs.',
            'Those boys run fast.',
            'The house is big.',
           'The dog is happy.']
parser = nltk.ChartParser(grammar)
n = int(input("Enter the number of sentences you want to parse:- "))
for i in range(n):
    sentence[i] = input().split()
    for t in parser.parse(sentence[i]):
         print(t)
        

 
    

       
