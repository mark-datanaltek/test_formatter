#!/usr/bin/env python

NUM_QUESTIONS = 50

from random import randint
for question_num in range(1, NUM_QUESTIONS+1):
    random_letter = chr(ord('A') + randint(0,3))
    print '\t'.join([str(question_num), random_letter])
