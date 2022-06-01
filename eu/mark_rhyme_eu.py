import sys
import unidecode
import collections
import os
from subprocess import Popen
sys.path.append('/ikerlariak/aormazabal024/PhD/Poetry-Generation/Rhyme')
from errimaes import get_class

vowels = 'aeiou'
def fromVowel(component):
    lastVowel = len(component)-1
    for i in range(len(component)):
        if component[i] in vowels:
            lastVowel = i
    if lastVowel>0 and component[lastVowel-1] in vowels:
        lastVowel -=1
    return component[lastVowel:]
ignore_chars = '_-?"!,:()[]{}\'`;»«><'


carry=""
with open(sys.argv[1], 'r', encoding='utf-8') as inf, open(sys.argv[2], 'r', encoding='utf-8') as rhmf, open(sys.argv[3], 'r', encoding='utf-8') as origf, open(sys.argv[4], 'w', encoding='utf-8') as outf:
    for line,rhm,  orig in zip(inf,rhmf, origf):
        try: 
            line = line.strip()
            if orig.strip().isspace() or orig.strip()=='':
                outf.write('\n')
                continue


            line_clean = line.translate(str.maketrans('','',ignore_chars))
            if line_clean.isspace() or line_clean=='':
                carry+=orig[:-1]
                continue

            line = line_clean

            line = line.translate(str.maketrans('','',ignore_chars))
            words = line.lower().split()
            num_slb = sum([len(w.split('.')) for w in words])
            #rhyme_word = words[-1]
            rhyme_word = rhm.strip()
            components = rhyme_word.split('.')

            components = components[-2:]
            components[0] = fromVowel(components[0])
            cls = 'CLS_'+'.'.join(components)
            cls = unidecode.unidecode(cls)


            result = '\t'.join((carry+orig[:-1],  cls, str(num_slb)))+ '\n'
            carry=""
            outf.write(result)
        except Exception as e:
            print('Failure', str(e),line)

