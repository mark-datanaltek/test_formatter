#!/usr/bin/env python

import argparse
from random import shuffle

def read_input_test(input_test_filename):
    """
    param: input_test_filename: a tsv input test file
                                with the following columns
                                col1: test_question
                                col2: correct_answer
                                col3-colN: dummy_answers
    returns: test_questions: [question1, question2, ... ] where
             questionN = {question: "what?",
                          correct_answer: "yes",
                          incorrect_answers: ["no", "maybe", "never", ...]

    """
    print "DEBUG: read_input_test"

    LINE_NUM_FIELDS_MIN = 3

    with open(input_test_filename, 'r') as fobj_test_in:
        questions = []
        for line in fobj_test_in:
            fields = line.split('\t')
            if len(fields) < LINE_NUM_FIELDS_MIN:
                err_msg = "line:\n" + line + " has less than " + str(LINE_NUM_FIELDS_MIN) + " fields"
                err_msg += "\nfields found are: " + str(fields)
                raise(err_msg)
            else:
                question = fields[0]
                correct_answer = fields[1]
                dummy_answers = fields[2:]
                question = {"question": test_question, "correct_answer": correct_answer,
                            "dummy_answers": dummy_answers}

            questions.append(question)
    return questions

def create_output_test(test_questions, test_version_label):
    """
    param: test_questions object (see above)
    param: test_version_label: version label string
    returns: formatted_test_str: a formatted test with randomized answer
                                 sequences.
    """
    print "DEBUG: create_output_test"

    formatted_test_str = test_version_label + '\n\n'

    for test_question in test_questions:
        formatted_test_str += test_question["question"] + '\n'
        answers = test_question["correct_answer"] + test_question["dummy_answers"]

    return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_test_filename")
    parser.add_argument("--num_output_test_versions", default=2)
    args = parser.parse_args()

    test_questions = read_input_test(args.input_test_filename)

    for test_num in range(1, args.num_output_test_versions):
        test_version_label = "Test Version " + str(test_num)
        print test_version_label " of " + str(args.num_output_test_versions) + '\n'
        formatted_test_str = create_output_test(test_questions, test_version_label)
        print formatted_test_str
