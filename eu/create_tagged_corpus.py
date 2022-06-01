import sys
import random
import time
import numpy as np

import collections

no_cls_percentage=0.15

lens_dict = collections.defaultdict(int)
vocab = set()
with open(sys.argv[3], 'r', encoding='utf-8') as vocabf:
    for line in vocabf:
        vocab.add(line.strip())
def process_paragraph(paragraph):
    elems = [1,2,3]
    probs = [0.8, 0.15, 0.05]
    paragraph_merged = []
    i = 0
    while i< len(paragraph):
        if paragraph[i].isspace() or paragraph[i]=='':
            paragraph_merged.append(paragraph[i])
            i+=1
            continue
        num = np.random.choice(elems,p=probs)
        for j in range(0,num):
            if (i+j)<len(paragraph) and (paragraph[i+j].isspace() or paragraph[i+j]==''):
                assert(j>0)
                num = j
                break
        tags = [sent.strip().split('\t') for sent in paragraph[i:i+num]]
        sentences = ['\t'.join(elems[:-2]) for elems  in tags]
        lens = [int(elems[-1]) for elems in tags]
        clss = [elems[-2] for elems in tags]
        sentence = ''.join(sentences)
        cls = clss[-1]
        ln = str(sum(lens))
        lens_dict[ln]+=1
        paragraph_merged.append('\t'.join((sentence, cls, ln)))
        i+=num
    paragraph = paragraph_merged

    last_ind = 0
    result = ''
    while last_ind<len(paragraph):
        size = random.randint(3,10)
        size = min(size, len(paragraph)-last_ind)
        prefix = '<PREF> '
        text = ''
        for ind in range(last_ind, last_ind + size):
            if paragraph[ind].isspace() or paragraph[ind]=='':
                text += '\n'
                prefix += '<SEP> '
                continue
            try:
                elems = paragraph[ind].strip().split('\t')
                assert(len(elems)>2)
                cls = elems[-2]
                ln = elems[-1]
                line = '\t'.join(elems[:-2])
                cls = '<'+cls+'>'
                ln_tok = '<LEN_'+ln+'>'
                if cls in vocab and random.random()>no_cls_percentage:
                    prefix += ln_tok+' '+cls+' '
                else:
                    prefix += ln_tok+' <CLS_UNK> '
                text += line + ' <BRK> '
            except Exception as e:
                print(e)
                print('ERR', paragraph[ind], paragraph[ind].split('\t'))
        prefix += '</PREF> '
        result = result + prefix + text
        last_ind = last_ind + size

    return result
if __name__ == "__main__":
    with open(sys.argv[1], 'r', encoding='utf-8') as tagf, open(sys.argv[2], 'w', encoding='utf-8') as outf, open(sys.argv[2]+'.lens_dist', 'w') as lensf:
        corpus = tagf.read()
        paragraphs = corpus.split('\n\n\n')
        for paragraph in paragraphs:
            paragraph = paragraph.split('\n')
            outf.write(process_paragraph(paragraph)+'\n\n')
        for k,v in sorted(lens_dict.items(), key=lambda x: -x[1]):
            lensf.write('{} {}\n'.format(k,v))
