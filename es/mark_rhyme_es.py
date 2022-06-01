import sys
import unidecode
import collections
import os
from subprocess import Popen
from FOMA.rhyme_es import get_class
import subprocess

if __name__ == "__main__":
    ignore_chars = '_-?"!,:()+[]{}\'`;»«><'



    carry=""
    with open(sys.argv[1], 'r', encoding='utf-8') as inf, open(sys.argv[2], 'r', encoding='utf-8') as origf, open(sys.argv[3], 'w', encoding='utf-8') as outf:
        for line, orig in zip(inf,origf):
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
                
                words = line.lower().split()
                num_slb = sum([len(w.split('.')) for w in words])
                rhyme_word = words[-1]
                    
                cls = 'CLS_'+get_class(rhyme_word)
                cls = unidecode.unidecode(cls)


                result = '\t'.join((carry+orig[:-1],  cls, str(num_slb)))+ '\n'
                carry=''
                outf.write(result)
            except Exception as e:
                print('Failure', str(e),line)

