#!/usr/bin/env python

import argparse

def read_input_test(input_test_filename):
    """
    param: input_test_filename: a tsv input test file
                                with the following columns
                                col1: test question
                                col2: correct answer
                                col3-colN: dummy answers
    returns: test_questions: [question1, question2, ... ] where
             questionN = {question: "what?",
                          correct_answer: "yes",
                          incorrect_answers: ["no", "maybe", "never", ...]

    """
    print "DEBUG: read_input_test"

    LINE_LENGTH_MIN = 

    with open(input_test_filename, 'r') as fobj_test_in:
        for line in fobj_test_in:
            line = line.split('\t')
            if len(line) < LINE_LENGTH_MIN:

    return None

def create_output_test(test_questions):
    """
    param: test_questions object (see above)
    returns: formatted_test_str: a formatted test with randomized answer
                                 sequences.
    """
    print "DEBUG: create_output_test"
    return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_test_filename")
    parser.add_argument("--num_output_test_versions", default=2)
    args = parser.parse_args()

    test_questions = read_input_test(args.input_test_filename)

    for test_num in range(1, args.num_output_test_versions):
        print "Test Version " + str(test_num) + " of " + str(args.num_output_test_versions) + '\n'
        formatted_test_str = create_output_test(test_questions)
        print formatted_test_str
