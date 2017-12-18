import unittest

from make_tests import read_input_test, \
                       create_test_versions, \
                       create_version_code_str

class Test_Make_Tests(unittest.TestCase):

    def setUp(self):
        self.input_test_filename = "test_in.txt"

    def run_versions_test(self, num_test_versions):
        input_test_questions = read_input_test(self.input_test_filename)
        test_versions = create_test_versions(input_test_questions, num_test_versions)

        for test_version_indx, test_version in enumerate(test_versions):
            # do we have the expected number of questions in the versions?
            num_questions_input_test_questions = len(input_test_questions)
            num_questions_test_version = len(test_version)
            self.assertEqual(num_questions_input_test_questions,
                             num_questions_test_version,
                             "test input has " + str(num_questions_input_test_questions) +
                             " questions.\n" +
                             "test version has " +
                             str(num_questions_test_version) +
                             " questions"
                             )

            # do we have the correct answers marked in the test version?
            for question_indx in range(num_questions_input_test_questions):
                test_question = input_test_questions[question_indx]
                test_version_question = test_version[question_indx]
                version_correct_answer_indices = [ord(ltr) - ord('A') for ltr in
                                                  test_version_question["correct_answer_letters"]]
                version_correct_answers = [test_version_question["answers_shuffled"][indx]
                                           for indx in version_correct_answer_indices]
                self.assertItemsEqual(version_correct_answers,
                                      test_question["correct_answers"],
                                      "question " + str(question_indx) + '\n' +
                                      test_question["question"] + '\n' +
                                      " correct answers don't match\n" +
                                      str(version_correct_answers) + "\n" +
                                      str(test_question["correct_answers"]) + '\n' +
                                      "input_test_question: " + str(test_question) + '\n' +
                                      "test_version_question: " + str(test_version_question) + '\n' +
                                      "in test_version_indx: " + str(test_version_indx))

            # for single answer questions, do we have different answers
            # in the different versions
            if num_test_versions > 1:
                for test_question_indx in range(len(input_test_questions)):
                    input_test_question = input_test_questions[test_question_indx]
                    if len(input_test_question["correct_answers"]) == 1:
                        correct_answer_letters = set()
                        for test_version in test_versions:
                            question_version_correct_answer_letter = test_version[test_question_indx]["correct_answer_letters"][0]
                            if question_version_correct_answer_letter not in correct_answer_letters:
                                correct_answer_letters.add(question_version_correct_answer_letter)
                            else:
                                err_msg = "found same answer letter for two versions :(" + \
                                          str(input_test_question) + '\n' + \
                                          "correct_answer_letters: " + str(correct_answer_letters) + '\n' + \
                                          "question_version_correct_answer_letter: " + question_version_correct_answer_letter
                                self.assertTrue(False, err_msg)


    def test_one_version(self):
        num_test_versions = 1
        self.run_versions_test(num_test_versions)

    def test_two_versions(self):
        num_test_versions = 2
        self.run_versions_test(num_test_versions)

class Test_Make_Version_Codes(unittest.TestCase):
    def setUp(self):
        input_test_filename = "test_in.txt"
        input_test_questions = read_input_test(input_test_filename)
        num_test_versions = 2
        self.test_versions = create_test_versions(input_test_questions, num_test_versions)

    def test_two_version_codes(self):
        CHAR_OFFSET_FROM_END = 6

        for version_indx, version in enumerate(self.test_versions):
            code_str= create_version_code_str(version_indx)
            expected_version_char = chr(ord('A') + version_indx)
            found_version_char = code_str[len(code_str) - CHAR_OFFSET_FROM_END]
            self.assertEqual(expected_version_char, found_version_char,
                             "did not find expected version char: " + expected_version_char + '\n' +
                             "found version char: " + found_version_char + '\n' +
                             "in version string: " + code_str)




if __name__ == '__main__':
    unittest.main()