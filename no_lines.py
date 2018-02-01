#!/usr/bin/env python3
import sys
import random


def main():
    # Usage information
    if len(sys.argv) < 5:
        print('Usage: {} <depth> <min length> <outputs> <input files>'.format(sys.argv[0]))
        exit(1)

    DEPTH = int(sys.argv[1])
    LENGTH = int(sys.argv[2])
    OUTPUTS = int(sys.argv[3])

    print('Reading files', end='', flush=True)
    print('\r' + ' '*20 + '\r', end='')

    input_files = sys.argv[4:]
    lines = []
    for input_file in input_files:
        with open(input_file) as f:
            lines += list(f)


    print('Parsing files', end='', flush=True)
    print('\r' + ' '*20 + '\r', end='')

    # Extract starting words
    starts = []
    for line in lines:
        try:
            word = line.split()[0]
            if len(word) > 0:
                starts.append(word)
        except IndexError:
            continue

    # Create chain
    corpus = " ".join(lines).split()
    markov = {}
    for d in range(1, DEPTH + 1):
        for i in range(len(corpus) - d):
            key = tuple(corpus[i:i+d])

            if key not in markov:
                markov[key] = []

            markov[key].append(corpus[i+d])

    # Generate outputs from chain
    for _ in range(OUTPUTS):
        key = random.choice(starts)
        out_string = key + ' '
        key = (key,)

        for d in range(2, DEPTH):
            out_string += random.choice(markov[key]) + ' '
            key = tuple(out_string.split()[-d:])

        while True:
            new_word = random.choice(markov[key])

            if len(out_string.split()) >= LENGTH:
                if out_string[-2] in '.?!)”"':
                    break

            if len(out_string.split()) >= (2 * LENGTH):
                break

            out_string += new_word + ' '
            key = tuple(out_string.split()[-DEPTH:])


        print(out_string)



if __name__ == '__main__':
    main()
