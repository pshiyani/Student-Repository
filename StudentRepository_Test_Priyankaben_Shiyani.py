"""
Author: Priyankaben Shiyani
Project Description: Testing Student, Instructor, Repository, Major
"""
import unittest
from HW10_Priyankaben_Shiyani import Student, Instructor, Repository, Major


class TestContainer(unittest.TestCase):
    def setUp(self):
        self.test_path = r'/Users/priyankashiyani/Documents/class810/HW_10'
        self.repo = Repository(self.test_path, True)

    def test_instructor_prettytable(self) -> None:
        """ Unit Testing for instructor_prettytable"""
        expected1 = []
        for instructor in self.repo._instructors.values():
            for row in instructor.instructor_info():
                expected1.append(row)

        actual1 = [('98765', 'Einstein, A', 'SFEN', 'SSW 567', 4),
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

        self.assertEqual(expected1, actual1)

    def test_student_prettytable(self) ->None:
        """ Unit Testing for student_prettytable"""
        expect = [student.student_info() for student in self.repo._students.values()]
        actual = [['10103', 'Baldwin, C', 'SFEN', ['CS 501', 'SSW 564', 'SSW 567', 'SSW 687'], ['SSW 540', 'SSW 555'],
                   [],3.44],
                    ['10115', 'Wyatt, X', 'SFEN', ['CS 545', 'SSW 564', 'SSW 567', 'SSW 687' ],
                    ['SSW 540', 'SSW 555'], [], 3.81], 
                    ['10172', 'Forbes, I', 'SFEN', ['SSW 555', 'SSW 567'], ['SSW 540', 'SSW 564'], 
                    ['CS 501', 'CS 513', 'CS 545'], 3.88],
                    ['10175', 'Erickson, D', 'SFEN', ['SSW 564', 'SSW 567', 'SSW 687'], ['SSW 540', 'SSW 555'], 
                    ['CS 501', 'CS 513', 'CS 545'], 3.58],
                    ['10183', 'Chapman, O', 'SFEN', ['SSW 689'], ['SSW 540', 'SSW 555', 'SSW 564', 'SSW 567'],
                    ['CS 501', 'CS 513', 'CS 545'], 4.0], 
                    ['11399', 'Cordova, I', 'SYEN', ['SSW 540'], ['SYS 612', 'SYS 671',  'SYS 800'], [], 3.0],
                    ['11461', 'Wright, U', 'SYEN', ['SYS 611', 'SYS 750', 'SYS 800'], ['SYS 612', 'SYS 671'], 
                    [ 'SSW 540', 'SSW 565', 'SSW 810'], 3.92],
                    ['11658', 'Kelly, P', 'SYEN', [], ['SYS 612', 'SYS 671', 'SYS 800'],
                    [ 'SSW 540', 'SSW 565', 'SSW 810'], 0.0], 
                    ['11714', 'Morton, A', 'SYEN', ['SYS 611', 'SYS 645'], ['SYS 612', 'SYS 671', 'SYS 800'],
                    [ 'SSW 540', 'SSW 565', 'SSW 810'],3.0],
                    ['11788', 'Fuller, E', 'SYEN', ['SSW 540'], ['SYS 612', 'SYS 671', 'SYS 800'], [], 4.0]]
        self.assertEqual(expect, actual)

    def test_major_prettytable(self) -> None:
        """ Unit Testing for major_prettytable"""
        expected2 = [major.major_info() for major in self.repo._majors.values()]
        actual2 = [['SFEN', ['SSW 540', 'SSW 555', 'SSW 564', 'SSW 567'], ['CS 501', 'CS 513', 'CS 545']],
                  ['SYEN', ['SYS 612', 'SYS 671', 'SYS 800'], ['SSW 540', 'SSW 565', 'SSW 810']]]
        self.assertEqual(expected2, actual2)


if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)