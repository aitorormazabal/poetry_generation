import unidecode
import sys
from .spanishstress import setstress



tildes="áéíóú"
v="aeiou"
strong_v='aeo'

def is_vowel(c):
    return c in v or c in tildes

def vowel_rank(c):
    assert(is_vowel(c))
    if c in tildes:
        return 2
    elif c in strong_v:
        return 1
    else:
        return 0

def get_class(word):
    syllables= word.split('.')
    if (len(syllables)==0):
        return 'EMPTY'
    if ('' in syllables):
        return 'HASEMPTY'
    stress = setstress(syllables)
    if '?' in stress:
        return 'MONO'
    else:
        relevant = syllables[stress.index('+'):]
        first = relevant[0]
        for i,c in enumerate(first):
            if is_vowel(c):
                break
        first=first[i:]
        if len(first)>1 and is_vowel(first[1]):
            if vowel_rank(first[0])>vowel_rank(first[1]):
                first = first[0]+first[2:]
            elif vowel_rank(first[0])<vowel_rank(first[1]):
                first = first[1:]
            else:
                first=relevant[0]
        relevant[0]=first

        cls = unidecode.unidecode('.'.join(relevant))
        return  cls
