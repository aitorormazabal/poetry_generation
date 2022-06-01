import sys
import subprocess
import os
from subprocess import Popen
from FOMA.rhyme_es import get_class
from sacrebleu.metrics import BLEU

vowels = 'aeiou'


def get_bleus(lines):
    for line in lines:
        if line.lower().translate(str.maketrans('', '',ignore_chars)).strip()=='':
            return 0,0
    bleu = BLEU(effective_order=True)
    lines= [line.lower().translate(str.maketrans('', '',ignore_chars)).strip() for line in lines]
    scores = []
    for i in range(len(lines)):
        for j in range(i):
            sc = bleu.sentence_score(lines[i], [lines[j]]).score
            scores.append(sc)
    return max(scores), sum(scores)/len(scores)
                   




def process_pref(pref):
    pref = pref.strip().split()
    pref = [elem for elem in pref if 'SEP' not in elem]
    for i in range(0,len(pref),2):
        pref[i] = int(pref[i][5:-1])
    for i in range(1,len(pref),2):
        pref[i] = pref[i][5:-1]
    assert len(pref) % 2 == 0
    pref = [ (pref[i], pref[i+1]) for i in range(0,len(pref),2)]
    return pref


ignore_chars = '_-?"!,:’‘()[].{}\'`;»«><'
silabafst = 'FOMA/syllable_es.fst'
def process_line(line):
    line = line.lower().translate(str.maketrans('', '',ignore_chars))
    if line.isspace() or line=="":
        return '', 'CLS_EMPTY'
    silabacmd = ['/ixadata/soft/rhel8/bin/flookup', '-ibx' ,silabafst]
    result = subprocess.run(silabacmd, stdout=subprocess.PIPE, input=line.encode('utf-8'))
    syllabified = result.stdout.decode('utf-8').split('\n')[0]
    if len(syllabified.split())==0:
        return 'emp.ty', 'CLS_EMPTY'
    
    rhmword = syllabified.split()[-1]

    rhmword = rhmword.strip()
    components = rhmword.split('.')

    cls = get_class(rhmword)
    return syllabified,cls

    
def analyze_poem(poem,prefix):
    print('Analyzing poem', poem,prefix)
    if len(poem)!=len(prefix):
        size = min(len(poem), len(prefix))
        print('SIZE MISMATCH POEM: {} PREFIX:{}, DISCARDING'.format(len(poem), len(prefix)))
        return -1,-1,-1,-1,-1,-1
        poem = poem[:size]
        prefix = prefix[:size]

    nlines = 0
    lendev = 0
    lenacc = 0
    rhmacc = 0
    print('Analyzing poem:', poem,prefix)
    prev_lastwords = []
    poto = False
    for line, pref in zip(poem,prefix):
        slb, cls = process_line(line.strip())
        if cls=='CLS_EMPTY':
            print('CLS EMPTY POEM: {} PREFIX:{}, DISCARDING'.format(len(poem), len(prefix)))
            #return -1,-1,-1 
        else:
            rhmword = slb.split()[-1]
            if rhmword in prev_lastwords:
                poto = True
            prev_lastwords.append(rhmword)
        ln = sum([len(word.split('.')) for word in slb.split()])
        if (cls!= pref[1] and pref[1]!='UNK'):
            print('PREF MISMATCH in line ',nlines,pref,line)
        else:
            rhmacc += 1
        if (ln!=pref[0]):
            print('LEN MISMATCH in line ',nlines,pref,line, ln)
            lendev += abs(ln- pref[0])
        else:
            lenacc += 1
        nlines +=1
    max_bleu, mean_bleu = get_bleus(poem)
    cls_acc = rhmacc/nlines
    ln_acc = lenacc/nlines
    ln_dev = lendev/nlines
    return cls_acc, ln_acc, ln_dev, max_bleu, mean_bleu, poto

CODE_OK = 0
CODE_PREF = 1
CODE_CLS = 2
CODE_BLEU = 3
CODE_REPEAT = 4
CODE_LEN = 5
BLEU_maxthres=35
BLEU_avgthres=20
def validate_poem(poem_txt, prefix):
    prefix_clss = [cls for cls in prefix.split() if 'CLS_' in cls]
    prefix_lens = [int(ln[5:-1]) for ln in prefix.split() if 'LEN_' in ln]
    assert len(prefix_clss)==len(prefix_lens)
    result_lines = poem_txt.split('<BRK>')[:-1] #Assuming it ends in BRK

    if len(result_lines)!=len(prefix_clss):
        return  CODE_PREF

    prev_rhymes = set()
    for line_len, line_cls ,line in zip(prefix_lens, prefix_clss, result_lines):
        slb, cls = process_line(line)

        rhyme = slb.split()[-1]

        if rhyme in prev_rhymes:
            return CODE_REPEAT

        prev_rhymes.add(rhyme)

        got_len = sum([len(word.split('.')) for word in slb.split()])
        got_class = '<CLS_{}>'.format(cls)
        if got_len!=line_len:
            return CODE_LEN
        if got_class!=line_cls:
            return CODE_CLS

    max_bleu,avg_bleu = get_bleus(result_lines)
    if max_bleu>=BLEU_maxthres or avg_bleu>=BLEU_avgthres:
        return CODE_BLEU

    return CODE_OK
