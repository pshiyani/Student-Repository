"""
Author: Priyankaben Shiyani
Project Description: Testing Student, Instructor, Repository
"""
import unittest
from HW09_Priyankaben_Shiyani import Student, Instructor, Repository


class TestContainer(unittest.TestCase):

    def test_fileerror(self) -> None:
        """ Unit Testing for test_fileerror"""
        with self.assertRaises(FileNotFoundError):
            Repository("non-existent file directory")

    def test_student_prettytable(self) -> None:
        """ Unit Testing for test_student_prettytable"""
        stevens = Repository(r'/Users/priyankashiyani/Documents/class810/HW_09')

        result = [student.student_info() for student in stevens._students.values()]
        expect = [['10103', 'Baldwin, C', 'SFEN', ['CS 501', 'SSW 564', 'SSW 567', 'SSW 687']],
                  ['10115', 'Wyatt, X', 'SFEN', ['CS 545', 'SSW 564', 'SSW 567', 'SSW 687']],
                  ['10172', 'Forbes, I', 'SFEN', ['SSW 555', 'SSW 567']],
                  ['10175', 'Erickson, D', 'SFEN', ['SSW 564', 'SSW 567', 'SSW 687']],
                  ['10183', 'Chapman, O', 'SFEN', ['SSW 689']],
                  ['11399', 'Cordova, I', 'SYEN', ['SSW 540']],
                  ['11461', 'Wright, U', 'SYEN', ['SYS 611', 'SYS 750', 'SYS 800']],
                  ['11658', 'Kelly, P', 'SYEN', ['SSW 540']],
                  ['11714', 'Morton, A', 'SYEN', ['SYS 611', 'SYS 645']],
                  ['11788', 'Fuller, E', 'SYEN', ['SSW 540']]]
        self.assertEqual(result, expect)

    def test_instructor_prettytable(self)-> None:
        """ Unit Testing for test_instructor_prettytable"""
        stevens = Repository(r'/Users/priyankashiyani/Documents/class810/HW_09')
        result1 = []
        for instructor in stevens._instructors.values():
            for row in instructor.instructor_info():
                result1.append(row)

        expect1 = [('98765', 'Einstein, A', 'SFEN', 'SSW 567', 4),
                   ('98765', 'Einstein, A', 'SFEN', 'SSW 540', 3),
                   ('98764', 'Feynman, R', 'SFEN', 'SSW 564', 3),
                   ('98764', 'Feynman, R', 'SFEN', 'SSW 687', 3),
                   ('98764', 'Feynman, R', 'SFEN', 'CS 501', 1),
                   ('98764', 'Feynman, R', 'SFEN', 'CS 545', 1),
                   ('98763', 'Newton, I', 'SFEN', 'SSW 555', 1),
                   ('98763', 'Newton, I', 'SFEN', 'SSW 689', 1),
                   ('98760', 'Darwin, C', 'SYEN', 'SYS 800', 1),
                   ('98760', 'Darwin, C', 'SYEN', 'SYS 750', 1),
                   ('98760', 'Darwin, C', 'SYEN', 'SYS 611', 2),
                   ('98760', 'Darwin, C', 'SYEN', 'SYS 645', 1)]

        self.assertEqual(result1, expect1)
if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)