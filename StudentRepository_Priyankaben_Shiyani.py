"""
Author: Priyankaben Shiyani
Project Description: Implementing Student, Instructor, Major,  Repository
"""
import sqlite3
from typing import DefaultDict, Dict, Iterator, Tuple
from prettytable import PrettyTable
from collections import defaultdict
import os

class Student:
    student_fields = ['CWID', 'Name', 'Major', 'Completed Courses', 'Remaining Required',
                      'Remaining Electives', 'GPA']

    def __init__(self, cwid: str, name: str, major: str, major_information: str) -> None:
        """Initiliaze student id, name, major and a container of courses and grades, major_information that is an
        instance of class Major"""
        self._cwid: str = cwid
        self._name: str = name
        self._major: str = major
        self.major_information = major_information
        self._courses_taken:Dict[str, str] = dict()  # key: course, value: grade

    def add_course(self, course: str, grade: str) -> None:
        """Allows other classes to add a course and grade to the container of courses and grades"""
        self._courses_taken[course]: Dict[str, str] = grade

    def student_info(self) -> Iterator[Tuple[str, str, str, str, str, str]]:
        """Returns the summary data about a single student needed in the pretty table"""
        completed_courses, remaining_required, remaining_electives, GPA = self.major_information.remaining_information(self._courses_taken)
        return [self._cwid, self._name, self._major, sorted(completed_courses), sorted(remaining_required), sorted(remaining_electives), GPA]

class Instructor:
    """store everything about a single Instructor """
    instructor_fields = ['CWId', 'Name', 'Dept', 'Course', 'Students']

    def __init__(self, cwid: str, name: str, dept: str) -> None:
        """Initiliaze instructor id, name, department and a container of courses courses taught"""
        self._cwid: str = cwid
        self._name: str = name
        self._dept: str = dept
        self._courses_taught: DefaultDict[str, int] = defaultdict(int)  # key: course[course_name] value: number of students

    def add_course(self, course: str) -> None:
        """Allows other classes to specify a course, and updates the container of courses taught to increment the number
         of students by 1"""
        self._courses_taught[course] += 1

    def instructor_info(self) -> Iterator[Tuple[str, str, str, str, int]]:
        """Returns information needed by the Instructor prettytable"""
        for course, nr_course in self._courses_taught.items():
            yield self._cwid, self._name, self._dept, course, nr_course

class Major:
    """ Class that contains required courses and elective data for majors """
    major_fields = ['Major', 'Required Courses', 'Electives']

    def __init__(self, dept: str):
        """Initiliaze major department, container of required courses and container of elective courses"""
        self._dept: str = dept
        self._electives = set()
        self._required = set()

    def add_course(self, flag: str, course: str):
        if flag.lower() == 'r':
            self._required.add(course)
        elif flag.lower() == 'e':
            self._electives.add(course)
        else:
            print(f"Unexpected flag {flag} encountered in majors.txt")

    def remaining_information(self, courses):
        """Calculate required, elective courses and GPA"""

        PASSING_GRADES =['A', 'A-', 'B+', 'B', 'B-', 'C+', 'C']
        passing_gpa = {'A':4.0, 'A-':3.75 , 'B+':3.25, 'B':3.0, 'B-':2.75, 'C+':2.25, 'C': 2.0 , 'C-':0 , 'D+':0 , 'D': 0 , 'D-' : 0 , 'F': 0}
        GPA:float = 0.0
        gpa:float = 0.0
        completed_courses = set()
  
        for course , grade in courses.items():
            if grade in PASSING_GRADES:
                completed_courses.add(course)
        
        remaining_required = self._required - completed_courses
        if completed_courses.intersection(self._electives):
            remaining_electives = []
        else :
            remaining_electives = self._electives
        for grade in courses.values():
            for gr , pas in passing_gpa.items():
                if grade == gr:
                    gpa += pas
            if len(completed_courses)== 0:
                print(f"student had low score (0.0 GPA)")
            else:
                GPA: float = round(gpa /len(completed_courses) , 2) 
        return completed_courses ,remaining_required , remaining_electives ,GPA


    def major_info(self):
        """ return the summary data about a single major in the pretty table"""
        return [self._dept, sorted(self._required), sorted(self._electives)]

class Repository:
    def __init__(self, path: str, print_table: bool=True) -> None:
        """store all students, instructor and read student.txt, grades.txt, instructor.txt, major.txt and print prettytable"""
        self._path: str = path
        self._students: Dict[str, Student] = dict()  # key: student_id value: Instance of class Student
        self._instructors: Dict[str, Instructor] = dict()  # key: instructor_id value: Instance of class Instructor
        self._majors = dict()
        # read the student file and create instance of class student
        # read the instructor file and creates instances of class Instructor
        # read the grades file and process each grades
        # read the major file and creates instances of class Major
        try:
            self._read_majors()
            self._read_student()
            self._read_instructor()
            self._read_grades()
        except ValueError and FileNotFoundError as e:
            print(e)
        
        if print_table:
            print('\nMajor Summary')
            print(self.major_pretty_table())
            print('\nStudent Summary')
            print(self.student_pretty_table())
            print('\nInstructor Summary')
            print(self.instructor_pretty_table())
            print('\nStudent Grade Summary')
            print(self.student_table_db(os.path.join(self._path, '810sql')))
           

    def _read_student(self) -> None:  
        """Read each line from student.txt and create an instance of class student for each line in file 
        and add new student to repository """  
        try:
            for cwid, name, major_n in file_reader(os.path.join(self._path, "students.txt"), 3, sep= '\t', header= True):
                if cwid in self._students:
                    raise ValueError(f"Student id: {cwid} is already in file")
                else:
                    if major_n in self._majors:
                        self._students[cwid] = Student(cwid, name, major_n, self._majors[major_n])
                    else:
                        raise ValueError(f"Student with associated id: {cwid} and name: {name} has major with "
                                         f"name: {major_n} which is an unknown major.")
        except FileNotFoundError:
            raise FileNotFoundError(f"{os.path.join(self._path, 'students.txt')} cannot open.")

    def _read_instructor(self) -> None:
        """Read each line from instructiors.txt file and create an instance of class Instructor for each line in the file, and
           add the new Instructor to the repository"""
        try:
            for cwid, name, dept in file_reader(os.path.join(self._path, "instructors.txt"), 3, sep= '\t', header= True):
                if cwid in self._instructors:
                    raise ValueError(f"{cwid} already in file")
                else:
                    self._instructors[cwid] = Instructor(cwid, name, dept)
        except FileNotFoundError:
            raise FileNotFoundError(f"{os.path.join(self._path, 'Students.txt')} cannot open.")

    def _read_grades(self) -> None:
        """Read student_cwid, course, grade, instructor_cwid"""
        try:
            for cwid_st, course, grade, cwid_in in file_reader(os.path.join(self._path, "grades.txt"), 4, sep= '\t',
                                                                    header= True):
                if cwid_st not in self._students:
                    raise ValueError(f"Student with id: {cwid_st} not exist")
                elif cwid_in not in self._instructors:
                    raise ValueError(f"Instructor with id: {cwid_in} not exist")
                else:
                    s: student =  self._students[cwid_st]
                    s.add_course(course, grade)
                    inst: instructors = self._instructors[cwid_in]
                    inst.add_course(course)
        except FileNotFoundError:
            raise FileNotFoundError(f"{os.path.join(self._path, 'grades.txt')} cannot open.")

    def _read_majors(self) -> None:
        """Read the majors.txt file, creating a new instance of class Major for each line in the file, and
        add the new Major to the repository"""
        try:
            for major, flag, course in file_reader(os.path.join(self._path, "majors.txt"), 3, sep='\t', header= True):
                if major not in self._majors:
                    self._majors[major] = Major(major)
                self._majors[major].add_course(flag, course)
        except FileNotFoundError:
            raise FileNotFoundError(f"{os.path.join(self._path, 'majors.txt')} cannot open.")

    def student_pretty_table(self) -> PrettyTable:
        """print a prettytable with the student inforamation"""
        pt = PrettyTable(field_names=Student.student_fields)
        for student in self._students.values():
            pt.add_row(student.student_info())
        return pt
      
        
    def instructor_pretty_table(self) -> PrettyTable:
        """print a prettytable with the instructor information"""
        
        pt = PrettyTable(field_names=Instructor.instructor_fields)
        for instructor in self._instructors.values():
            for row in instructor.instructor_info():
                pt.add_row(row)
        return pt
       
    def major_pretty_table(self) -> PrettyTable:
        """print a prettytable with the Major Information"""
        pt = PrettyTable(field_names=Major.major_fields)
        for major in self._majors.values():
            pt.add_row(major.major_info())
        return pt

    def student_table_db(self, db_path: str) -> PrettyTable:
        """print a prettytable with the Major Information"""
        try:
            db = sqlite3.connect(db_path)
        except sqlite3.OperationalError:
            print(f"Error: Unable to open database at {db_path}")
        else:
            with db:
                query = """select s.Name as [Name], s.CWID, g.Course, g.Grade, i.Name as [Instructor]
                from students s join grades g on s.CWID=g.StudentCWID join instructors i on g.InstructorCWID=i.CWID
                order by s.Name asc;"""
                pt = PrettyTable(field_names=['Name', 'CWID', 'Course', 'Grade', 'Instructor'])
                for row in db.execute(query):
                    pt.add_row(row)
                return pt
        


def file_reader(path: str, num_fields: int, sep: str=',', header: bool=True) -> Iterator[Tuple[str, ...]]:
    """ Function for file reading """
    try:
        fp: IO = open(path, "r", encoding="utf-8")
    except FileNotFoundError:
        raise FileNotFoundError(f"Can't open '{path}'for reading")

    else:
        with fp:
            for counter, line in enumerate(fp, 1):
                fields: List[str] = line.rstrip('\n').split(sep)
                if len(fields)!= num_fields:
                    raise ValueError(f"'{path}' line: {counter}: read {len(fields)} fields but expected {num_fields}")
                elif counter == 1 and header:
                    continue       # skip the header after checking for correct number of fields
                else:
                    yield tuple(fields)

def main():
    """ define repository for stevens"""
    stevens = Repository(r'/Users/priyankashiyani/Documents/class810/HW_11')
    
if __name__ == '__main__':
    main()