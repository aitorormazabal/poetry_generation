import sys


if __name__ == "__main__":
    with open(sys.argv[1], 'r', encoding='utf-8') as cls_vocab, open(sys.argv[2],'w', encoding='utf-8') as outf_vocab:
        classes = []
        for line in cls_vocab:
            freq, cls = line.strip().split()
            classes.append((int(freq), cls))
        num_cls = int(sys.argv[3])
        num_len = int(sys.argv[4])

        vocab = []
        vocab_freqs = []


