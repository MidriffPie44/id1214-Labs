import nltk
from nltk.tokenize import PunktSentenceTokenizer
from nltk.corpus import inaugural
from nltk.corpus import treebank

train_text = inaugural.raw("1789-Washington.txt")
sample_text = ("Those boys run fast")

custom_sent_tokenizer = PunktSentenceTokenizer(train_text)
tokenized = custom_sent_tokenizer.tokenize(sample_text)

def process_content():
    try:
       for i in tokenized:
           words = nltk.word_tokenize(i)
           tagged = nltk.pos_tag(words)
           print(tagged)
        
    except Exception as e:
        print(str(e))
        
process_content() 

""" To draw a Parse Tree for the treebank corpus reader """

t = treebank.parsed_sents('wsj_0001.mrg')[0]
t.draw()
