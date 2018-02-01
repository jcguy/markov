#!/usr/bin/env python3
import sys
import random


DEPTH = 3
LENGTH = 20
OUTPUTS = 10

START_STRING = ''
MIN_DISTANCE = 5


def check_distance(t1, t2):
    distance = 0
    for i in range(len(t1)):
        word_distance = 0
        str1 = t1[i].lower()
        str2 = t2[i].lower()
        len1 = len(str1)
        len2 = len(str2)
        extra = abs(len1 - len2)

        for j in range(min(len1, len2)):
            if str1[j] != str2[j]:
                word_distance += 1

        distance += word_distance + extra

    return distance


def main():
    if len(sys.argv) < 2:
        print('Usage: {} <input files>')
        exit(1)

    lines = []

    print('Reading files', end='', flush=True)

    input_files = sys.argv[1:]
    for input_file in input_files:
        with open(input_file) as f:
            lines += list(f)

    markov = {}

    print('\b'*20, end='')
    print('Parsing files', end='', flush=True)

    for line in lines:
        line_words = line.split()
        for i, word in enumerate(line_words):
            if (i + DEPTH + 1) < len(line_words):
                key = tuple(line_words[i:i+DEPTH])
                if key not in markov:
                    markov[key] = []
                markov[key].append(line_words[i+DEPTH+1])

    print('\b'*20, end='')
    print('Constructing line', end='', flush=True)

    for _ in range(OUTPUTS):
        out_string = ''
        key = random.choice(list(markov.keys()))
        out_string += ' '.join(key) + ' '

        while len(out_string.split()) < LENGTH:
            print('\b'*25, end='')
            print('Loading string: {}%'.format(int(100 * len(out_string.split()) / LENGTH)), end='', flush=True)

            try:
                if out_string == '' and START_STRING != '':
                    raise KeyError
                else:
                    next_word = random.choice(markov[key])
            except KeyError:
                best = (999, ())
                for k in markov.keys():
                    distance = check_distance(key, k)
                    if distance < best[0]:
                        best = (distance, k)
                    if best[0] <= MIN_DISTANCE:
                        break

                if best[0] < 999:
                    next_word = random.choice(markov[best[1]])
                else:
                    break

            out_string += next_word + ' '
            key = tuple(out_string.split()[-DEPTH:])

        print('\b'*20, end='')
        print(out_string)






if __name__ == '__main__':
    main()
