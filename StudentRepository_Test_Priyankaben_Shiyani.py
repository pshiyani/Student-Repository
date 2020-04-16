"""
Author: Priyankaben Shiyani
Project Description: Testing Student, Instructor, Repository, Major
"""
import sqlite3
import unittest
from StudentRepository_Priyankaben_Shiyani import Student, Instructor, Repository, Major


class TestContainer(unittest.TestCase):
    def setUp(self):
        self.test_path = r'/Users/priyankashiyani/Documents/class810/HW_11'
        self.repo = Repository(self.test_path, False)

    def test_instructor_prettytable(self) -> None:
        """ Unit Testing for instructor_prettytable"""
        expected1 = []
        for instructor in self.repo._instructors.values():
            for row in instructor.instructor_info():
                expected1.append(row)

        actual1 = [('98764', 'Cohen, R', 'SFEN', 'CS 546', 1),
                   ('98763', 'Rowland, J', 'SFEN', 'SSW 810', 4),
                   ('98763', 'Rowland, J', 'SFEN', 'SSW 555', 1),
                   ('98762', 'Hawking, S', 'CS', 'CS 501', 1),
                   ('98762', 'Hawking, S', 'CS', 'CS 546', 1),
                   ('98762', 'Hawking, S', 'CS', 'CS 570', 1)]

        self.assertEqual(expected1, actual1)

    def test_student_prettytable(self) ->None:
        """ Unit Testing for student_prettytable"""
        expected = [student.student_info() for student in self.repo._students.values()]
        actual = [['10103', 'Jobs, S', 'SFEN', ['CS 501', 'SSW 810'], ['SSW 540', 'SSW 555'], [], 3.38],
                  ['10115', 'Bezos, J', 'SFEN', ['SSW 810'], ['SSW 540', 'SSW 555'], ['CS 501', 'CS 546'], 4.0],
                  ['10183', 'Musk, E', 'SFEN', ['SSW 555', 'SSW 810'], ['SSW 540'], ['CS 501', 'CS 546'], 4.0],
                  ['11714', 'Gates, B', 'CS', ['CS 546', 'CS 570', 'SSW 810'], [], [], 3.5]]

        self.assertEqual(expected, actual)

    def test_major_prettytable(self) -> None:
        """ Unit Testing for major_prettytable"""
        expected2 = [major.major_info() for major in self.repo._majors.values()]
        actual2 = [['SFEN', ['SSW 540', 'SSW 555', 'SSW 810'], ['CS 501', 'CS 546']],
                   ['CS', ['CS 546', 'CS 570'], ['SSW 565', 'SSW 810']]]
        self.assertEqual(expected2, actual2)

    def test_student_grade_table_db(self) -> None:
        """ Unit Testing for student_grade_table_db prettytable"""
        db_path = r'/Users/priyankashiyani/Documents/class810/HW_11/810sql'
        db = sqlite3.connect(db_path)
        expected3 = []
        query = """select s.Name as [Name], s.CWID, g.Course, g.Grade, i.Name as [Instructor]
from students s join grades g on s.CWID=g.StudentCWID join instructors i on g.InstructorCWID=i.CWID
order by s.Name asc;"""
        for row in db.execute(query):
            expected3.append(row)

        actual3 = [('Bezos, J', '10115', 'SSW 810', 'A', 'Rowland, J'),
                    ('Bezos, J', '10115', 'CS 546', 'F', 'Hawking, S'),
                    ('Gates, B', '11714', 'SSW 810', 'B-', 'Rowland, J'), 
                    ('Gates, B', '11714', 'CS 546', 'A', 'Cohen, R'),
                    ('Gates, B', '11714', 'CS 570', 'A-', 'Hawking, S'), 
                    ('Jobs, S', '10103', 'SSW 810', 'A-','Rowland, J'), 
                    ('Jobs, S', '10103', 'CS 501', 'B', 'Hawking, S' ),
                    ('Musk, E', '10183', 'SSW 555', 'A', 'Rowland, J'), 
                    ('Musk, E', '10183', 'SSW 810', 'A', 'Rowland, J' )]

        self.assertEqual(expected3, actual3)

if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)
