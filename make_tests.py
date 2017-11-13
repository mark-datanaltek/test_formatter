#!/usr/bin/env python

import argparse
from random import shuffle

def read_input_test(input_test_filename):
    """
    param: input_test_filename: a tsv input test file
                                with the following columns
                                col1: test_question
                                col2: num_correct_answers
                                col3-colN: answers
    returns: test_questions: [question1, question2, ... ] where
             questionN = {question: "favorite colors?",
                          correct_answers: ["blue", "green"]
                          incorrect_answers: ["orange", "yellow", ...]

    """

    LINE_NUM_FIELDS_MIN = 4
    COL_NUM_QUESTION = 0
    COL_NUM_NUM_CORRECT_ANSWERS = 1
    COL_NUM_FIRST_CORRECT_ANSWER = 2

    with open(input_test_filename, 'r') as fobj_test_in:
        questions = []
        for line in fobj_test_in:
            fields = line.rstrip().split('\t')
            if len(fields) < LINE_NUM_FIELDS_MIN:
                err_msg = "line:\n" + line + " has less than " + str(LINE_NUM_FIELDS_MIN) + " fields"
                err_msg += "\nfields found are: " + str(fields)
                raise(err_msg)
            else:
                question = fields[COL_NUM_QUESTION]
                num_correct_answers = int(fields[COL_NUM_NUM_CORRECT_ANSWERS])
                col_num_first_incorrect_answer = COL_NUM_FIRST_CORRECT_ANSWER + num_correct_answers
                correct_answers = fields[COL_NUM_FIRST_CORRECT_ANSWER:COL_NUM_FIRST_CORRECT_ANSWER+num_correct_answers]
                dummy_answers = fields[col_num_first_incorrect_answer:]
                question = {"question": question, "correct_answers": correct_answers,
                            "dummy_answers": dummy_answers}

            questions.append(question)
    return questions

def create_test_version(test_questions):
    """
    param: test_questions object (see above)
    returns: test_questions_suffled: [question1, question2, ... ] where
             questionN = {question: "what?",
                          correct_answer_letter: 'A',
                          answers_shuffled: ["no", "maybe", "never", ...]
    """

    test_questions_shuffled = []
    for test_question in test_questions:

        # put all the correct and incorrect answers into one list
        answers = test_question["correct_answers"] + test_question["dummy_answers"]

        # shuffle the indicies to the answers
        answer_indices = range(len(answers))
        shuffle(answer_indices)

        # get the answer_letter for the correct answers
        correct_answer_letters = [chr(ord('A') + answer_indices.index(letter_num))
                                  for letter_num in range(len(test_question["correct_answers"]))]

        # make the randomized list of answers
        answers_shuffled = [answers[indx] for indx in answer_indices]

        test_question_shuffled = {"question": test_question["question"],
                                  "correct_answer_letters": correct_answer_letters,
                                  "answers_shuffled": answers_shuffled}
        test_questions_shuffled.append(test_question_shuffled)

    return test_questions_shuffled

def get_test_version_str(test_version):
    test_version_str = ""
    for (question_num, test_question) in enumerate(test_version):
        test_version_str += str(question_num+1) + ". " + test_question["question"] + '\n'
        for (answer_num, answer) in enumerate(test_question["answers_shuffled"]):
            test_version_str += '\t' + chr(ord('A') + answer_num) + ".  " + answer + '\n'

        test_version_str += '\n' # end of question and answers separator

    return test_version_str

def get_test_version_key_str(test_version):
    test_version_key_str = ""
    for (question_num, test_question) in enumerate(test_version):
        test_version_key_str += str(question_num+1) + ". " + \
                                " ".join(sorted(test_question["correct_answer_letters"])) + '\n'

    return test_version_key_str

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_test_filename")
    parser.add_argument("--num_output_test_versions", default=2)
    args = parser.parse_args()

    test_questions = read_input_test(args.input_test_filename)

    for test_num in range(1, args.num_output_test_versions+1):
        test_version_label = "Test Version " + str(test_num)
        print test_version_label + " of " + str(args.num_output_test_versions) + '\n'
        test_version = create_test_version(test_questions)

        with open("version" + str(test_num) + "_" + args.input_test_filename, 'w') as test_version_fobj:
            test_version_str = get_test_version_str(test_version)
            test_version_fobj.write(test_version_str)

        with open("key_version" + str(test_num) + "_" + args.input_test_filename, 'w') as test_version_key_fobj:
            test_version_key_str = get_test_version_key_str(test_version)
            test_version_key_fobj.write(test_version_key_str)
