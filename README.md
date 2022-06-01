Code for the paper "PoeLM: A Meter- and Rhyme-Controllable Language Model for
Unsupervised Poetry Generation"

## Creating the augmented corpus

To create the augmented corpus given a regular text corpus, simply use the corresponding pipeline_{lan}.sh command. For example, for Spanish: 

```
./pipeline_es.sh corpus augmented_corpus
```

This will create various files, and the augmented corpus will be saved to `agumented_corpus.pref`. The special control codes are saved to `augmented_corpus.tag.special_vocab` and `augmented_corpus.tag.special_vocab.spaces`. We can then train a sentencepiece model using these files:

```
% spm_train  --user_defined_symbols=augmented_corpus.tag.special_vocab.spaces --input=augmented_corpus.pref --model_prefix=spm --vocab_size=50000
```

Finally, we can encode the text using this sentencepiece model and train a regular language model with it.

## Generation and filtering 

Coming soon

## Perplexity evaluation

Coming soon

##Publication

If you use this code for academic research, please cite the PoeLM paper:

```
@misc{https://doi.org/10.48550/arxiv.2205.12206,
  doi = {10.48550/ARXIV.2205.12206},
  
  url = {https://arxiv.org/abs/2205.12206},
  
  author = {Ormazabal, Aitor and Artetxe, Mikel and Agirrezabal, Manex and Soroa, Aitor and Agirre, Eneko},
  
  keywords = {Computation and Language (cs.CL), Artificial Intelligence (cs.AI), FOS: Computer and information sciences, FOS: Computer and information sciences},
  
  title = {PoeLM: A Meter- and Rhyme-Controllable Language Model for Unsupervised Poetry Generation},
  
  publisher = {arXiv},
  
  year = {2022},
  
  copyright = {Creative Commons Attribution 4.0 International}
}
```
