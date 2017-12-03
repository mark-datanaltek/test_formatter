import unittest

from make_tests import  read_input_test, \
                        create_test_version

class Test_Make_Tests(unittest.TestCase):

    def setUp(self):
        self.input_test_filename = "test_in.txt"

    def test_version(self):
        test_questions = read_input_test(self.input_test_filename)
        test_version = create_test_version(test_questions)

        # do we have the expected number of questions in the version?
        num_questions_test_questions = len(test_questions)
        num_questions_test_version = len(test_version)
        self.assertEqual(num_questions_test_questions,
                         num_questions_test_version,
                         "test version has " +
                         str(num_questions_test_version) +
                         " questions and\n" +
                         "test input questions has " +
                         str(num_questions_test_questions) +
                         " questions.")

        # do we have the correct answers marked in the test version?
        for question_indx in range(num_questions_test_questions):
            test_question = test_questions[question_indx]
            test_version_question = test_version[question_indx]
            version_correct_answer_indices = [ord(ltr) - ord('A') for ltr in
                                       test_version_question["correct_answer_letters"]]
            version_correct_answers = [test_version_question["answers_shuffled"][indx]
                               for indx in version_correct_answer_indices]
            self.assertItemsEqual(version_correct_answers,
                                  test_question["correct_answers"],
                                  "question " + str(question_indx) +
                                  " correct answers don't match\n" +
                                  str(version_correct_answers) + "\n" +
                                  str(test_question["correct_answers"]))

if __name__ == '__main__':
    unittest.main()