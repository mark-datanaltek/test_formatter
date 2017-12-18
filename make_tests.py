#!/usr/bin/env python

import argparse
from random import choice as random_choice
from random import randint as random_randint
from random import shuffle as random_shuffle


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
                err_msg += "skipping this line ..."
                print err_msg
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


def get_test_question_shuffled(test_question):
    """
    randomly shuffles the answers for a test question
    :param test_question:
    :return: test_question_shuffled where
             question = {question: "what?",
                          correct_answer_letters: ['A', ...] # may be only one
                          answers_shuffled: ["no", "maybe", "never", ...]

    """
    answers = test_question["correct_answers"] + test_question["dummy_answers"]
    answer_indices = range(len(answers))

    # shuffle the indices to the answers
    random_shuffle(answer_indices)

    # make the randomized list of answers
    answers_shuffled = [answers[indx] for indx in answer_indices]

    # get the answer_letter for the correct answers
    correct_answer_letters = [chr(ord('A') + answer_indices.index(letter_num))
                              for letter_num in range(len(test_question["correct_answers"]))]

    test_question_shuffled = {"question": test_question["question"],
                              "correct_answer_letters": correct_answer_letters,
                              "answers_shuffled": answers_shuffled}

    return test_question_shuffled


def create_test_versions(test_questions, num_test_versions):
    """
    creates test_versions and ensures that correct_answer_letters for any question
    are different between test_versions (for single answer questions).
    :param test_questions: object (see above)
    :param num_test_versions:
    :return: [test_version1, test_version2, ...] where each test_version is a list of questions
             [question1, question2, ... ] where
             questionN = {question: "what?",
                          correct_answer_letters: ['A', ...] # may be only one
                          answers_shuffled: ["no", "maybe", "never", ...]
    """

    # approach is to loop over questions and create versions of each question in the
    # question loop.  This allows the version answers to be aware of each other.
    test_versions = [[] for i in range(num_test_versions)]
    for test_question in test_questions:
        # if there is only one correct answer we will make sure each
        # version has a different correct answer letter.  If there are
        # more than one correct answer, then we simply shuffle them for
        # each version.
        if len(test_question["correct_answers"]) < 1:
            err_msg = "less than one correct answer in question:\n" + str(test_question)
            raise Exception(err_msg)

        elif len(test_question["correct_answers"]) == 1:
            # for first version simply shuffle to get random order
            test_question_shuffled_v1 = get_test_question_shuffled(test_question)
            test_versions[0].append(test_question_shuffled_v1)

            # for the remaining versions set the correct answer letter to be
            # something other than what it is in the previous versions
            correct_answer_indx_v1 = ord(test_question_shuffled_v1["correct_answer_letters"][0]) - \
                                  ord('A')
            correct_answer_indices = range(len(test_question_shuffled_v1["answers_shuffled"]))

            correct_answer_indices_remaining = list(correct_answer_indices)
            correct_answer_indices_remaining.remove(correct_answer_indx_v1)

            for test_version_indx in range(1, num_test_versions):
                # get a new random correct answer index from those that have not been used
                correct_answer_indx = random_choice(correct_answer_indices_remaining)

                # remove the latest correct answer indx from the remaining list
                if len(correct_answer_indices_remaining) < 1:
                    err_msg = "trying to remove a correct answer indx from an empty list :("
                    raise Exception(err_msg)
                correct_answer_indices_remaining.remove(correct_answer_indx)

                # now create the test_version question object by swapping the positions
                # of the new and original correct answers
                correct_answer_letter = chr(ord('A') + correct_answer_indx)
                answers_shuffled = list(test_question_shuffled_v1["answers_shuffled"])
                answers_shuffled[correct_answer_indx], answers_shuffled[correct_answer_indx_v1] = \
                    answers_shuffled[correct_answer_indx_v1], answers_shuffled[correct_answer_indx]
                test_question_shuffled = {"question": test_question_shuffled_v1["question"],
                                          "correct_answer_letters": [correct_answer_letter],
                                          "answers_shuffled": answers_shuffled}
                test_versions[test_version_indx].append(test_question_shuffled)

        else: # >1 correct answer to this test question
            # so we just shuffle
            for test_version_indx in range(num_test_versions):
                test_question_shuffled = get_test_question_shuffled(test_question)
                test_versions[test_version_indx].append(test_question_shuffled)

    return test_versions


def create_version_code_str(test_version_indx):
    LEN_VERSION_CODE_STR = 20
    CHAR_OFFSET_FROM_END = 6
    version_char_list = [chr(random_randint(ord('!'), ord('`'))) for i in range(LEN_VERSION_CODE_STR)]

    # make sure there are no 'a', 'b', 'A', 'B' chars in version_char_list
    # if there are, replace them with a random char in the range [C, Z]
    for indx in range(len(version_char_list)):
        if version_char_list[indx] in ['a', 'b', 'A', 'B']:
            version_char_list[indx] = chr(random_randint(ord('C'), ord('Z')))

    version_char = chr(ord('A') + test_version_indx)
    version_char_list[LEN_VERSION_CODE_STR - CHAR_OFFSET_FROM_END] = version_char
    version_code_str = ''.join(version_char_list)

    return version_code_str


def get_test_version_str(test_version, test_version_indx, hdr_line1_str):
    """
    creates test version that is ready to be printed with an embedded version string.
    :param test_version:
    :param test_version_indx:
    :return: test_version_str
    """
    version_code_str = create_version_code_str(test_version_indx)
    QUESTION_NUM_FOR_CODE = len(test_version)

    test_version_hdr_str = \
"""Name (please write clearly, Last, First): ___________________________________
   Please fill in the bubble corresponding to the best answer and mark only one answer for each question,
   unless noted "select all that apply". Only the Scantron (answer) sheet will be graded.
   
"""
    test_version_str = hdr_line1_str + '\n' + test_version_hdr_str
    for (question_indx, test_question) in enumerate(test_version):
        question_num = question_indx + 1
        test_version_str += str(question_num) + ". " + test_question["question"] + '\n'
        for (answer_num, answer) in enumerate(test_question["answers_shuffled"]):
            test_version_str += '\t' + chr(ord('A') + answer_num) + ".  " + answer + '\n'

        if question_num == QUESTION_NUM_FOR_CODE:
            test_version_str += version_code_str + '\n'

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
    parser.add_argument("--num_output_test_versions", default=2, type=int)
    parser.add_argument("--hdr_line1_str", default="NU220")
    args = parser.parse_args()

    test_questions = read_input_test(args.input_test_filename)

    test_versions = create_test_versions(test_questions, args.num_output_test_versions)

    for test_version_indx in range(len(test_versions)):
        test_num = test_version_indx + 1
        test_version_label = "Test Version " + str(test_num)
        print test_version_label + " of " + str(args.num_output_test_versions) + '\n'
        test_version = test_versions[test_version_indx]

        with open("version" + str(test_num) + "_" + args.input_test_filename, 'w') as test_version_fobj:
            test_version_str = get_test_version_str(test_version,
                                                    test_version_indx,
                                                    args.hdr_line1_str)
            test_version_fobj.write(test_version_str)

        with open("key_version" + str(test_num) + "_" + args.input_test_filename, 'w') as test_version_key_fobj:
            test_version_key_str = get_test_version_key_str(test_version)
            test_version_key_fobj.write(test_version_key_str)
