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
    lines = ""
    starts = []
    for input_file in input_files:
        with open(input_file) as f:
            for line in list(f):
                lines += line
                starts += line[0].replace('\n', '')

    print('Parsing files', end='', flush=True)
    print('\r' + ' '*20 + '\r', end='')

    lines = lines.replace('\n', ' ')

    # Create chain
    markov = {}
    for d in range(1, DEPTH + 1):
        for i in range(len(lines) - d):
            key = tuple(lines[i:i+d])

            if key not in markov:
                markov[key] = []

            markov[key].append(lines[i+d])

    # Generate outputs from chain
    keys = list(markov.keys())
    for _ in range(OUTPUTS):
        key = random.choice(starts)
        out_string = key
        key = (key,)

        for d in range(2, DEPTH):
            out_string += random.choice(markov[key])
            key = tuple(out_string[-d:])

        while True:
            new_word = random.choice(markov[key])

            if len(out_string) >= LENGTH:
                if out_string[-1] in '.?!)"':
                    break

            if len(out_string) >= (1.5 * LENGTH):
                if out_string[-1] == ' ':
                    break

            if len(out_string) >= (2 * LENGTH):
                break

            out_string += new_word
            key = tuple(out_string[-DEPTH:])

        print(out_string, flush=True)



if __name__ == '__main__':
    main()
