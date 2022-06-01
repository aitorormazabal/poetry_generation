#!/bin/bash

input=$1
output=${2}.tag
output_pref=${2}.pref


num_rhm=8000
rhmfst=./FOMA/rhyme_eu.fst
slbfst=./FOMA/syllable_eu.fst
flookup=/ixadata/soft/rhel8/bin/flookup 
mark_rhyme=mark_rhyme_eu.py

perl -0777 -pe 's/\n\n/PARABR/g' $input > ${input}.paragraphs #Turn document delimiter from single break into double break to disambiguate from splits with separators at end of paragraph
perl -0777 -i -pe 's/\n/LINEBR/g' ${input}.paragraphs #Turn document delimiter from single break into double break to disambiguate from splits with separators at end of paragraph
sed -e 's/\([][_?"!,{}»\x3A«;\x27.`-]\)/\1\n/g' -e 's/\t/ /g' < ${input}.paragraphs > ${input}.split.orig
perl -0777  -pe 's/\n*LINEBR/\n\n/g' ${input}.split.orig > ${input}.split
perl -0777 -i -pe 's/\n*PARABR/\n\n\n/g' ${input}.split
sed 's/\([][_?"!,{}»\x3A)(«;\x27.`-]\)//g' < ${input}.split  > ${input}.split.clean
cat ${input}.split.clean | stdbuf -o0 awk '{print tolower($0)}' | stdbuf -o0 $flookup -ibx ${slbfst} | awk 'NR%2==1' > ${input}.slb
cat ${input}.slb | awk '{print $NF}' | stdbuf -o0 $flookup -ibx ${rhmfst} | awk 'NR%2==1'  > ${input}.rhm

echo "python3 $mark_rhyme  ${input}.slb ${input}.rhm ${input}.split ${output}"
python3 $mark_rhyme  ${input}.slb ${input}.rhm ${input}.split ${output}

cut -f2 ${output} | sort | awk 'NF > 0' | uniq -c | sort -nr > ${output}.rhm_freqs

head -n ${num_rhm} ${output}.rhm_freqs | sed 's/^ *//;s/ *$//' | cut -d' ' -f2 | sed 's/$/>/' | sed 's/^/</' > ${output}.rhm_vocab

awk 'BEGIN {for (i=1; i<= 500; i++) printf "<LEN_%s>\n",i; }' > vocab.lens
printf "<BRK>\n<PREF>\n</PREF>\n<SEP>\n<CLS_UNK>\n" > vocab.control

cat vocab.control vocab.lens ${output}.rhm_vocab   > ${output}.special_vocab
cat  ${output}.special_vocab |  sed 's/^/▁/' > ${output}.special_vocab.spaces

python3 /ikerlariak/aormazabal024/PhD/Poetry-Generation/create_tagged_corpus_vocab.py ${output} ${output_pref} ${output}.special_vocab

rm ${output}.rhm_vocab
rm vocab.lens
rm vocab.control

rm ${input}.slb
rm ${input}.split
rm ${input}.split.clean
rm ${input}.paragraphs
rm ${input}.split.orig
