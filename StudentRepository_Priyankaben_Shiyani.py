"""
Author: Priyankaben Shiyani
Project Description: Implementing Student, Instructor, Repository
"""
from typing import DefaultDict, Dict, Iterator, Tuple
from prettytable import PrettyTable
from collections import defaultdict
import os

class Student:
    """store everything about a single student """
    student_fields = ['Student Id', 'Student Name', 'Student Major', 'Courses']

    def __init__(self, cwid: str, name: str, major: str) -> None:
        """Initiliaze student id, name, major and a container of courses and grades"""
        self._cwid: str = cwid
        self._name: str = name
        self._major: str = major
        self._courses_taken: Dict[str, str] = dict()  # key: courses[course_name], value: grade

    def add_course(self, course: str, grade: str) -> None:
        """Allows other classes to add a course and grade to the container of courses and grades"""
        self._courses_taken[course] = grade

    def student_info(self) -> Iterator[Tuple[str, str, str, str]]:
        """Returns the summary data about a single student needed for the pretty table"""
        return [self._cwid, self._name, self._major, sorted(self._courses_taken.keys())]

class Instructor:
    """store everything about a single Instructor """
    instructor_fields = ['Instructor Id', ' Instructor Name', 'Department', 'Course', 'Number of Students']

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

class Repository:
    """ store all students, instructor for a university and pretty tables """
    def __init__(self, path: str, print_table: bool=True) -> None:
        """store all students, instructor and read student.txt, grades.txt, instructor.txt and print prettytable"""
        self._path: str = path
        self._students: Dict[str, Student] = dict()  # key: students[cwid] value: student()
        self._instructors: Dict[str, Instructor] = dict()  # key: instructor[cwid] value: Instructor()

        # read the student file and create instance of class student
        # read the instructor file and creates instances of class Instructor
        # read the grades file and process each grades
        self.read_student()
        self.read_instructor()
        self.read_grades()

        if print_table:
            print('\nStudent Summary')
            print(self.student_pretty_table())
            print('\nInstructor Summary')
            print(self.instructor_pretty_table())

    def read_student(self)-> None:  
        """Read each line from student.txt and create an instance of class student for each line in file 
        and add new student to repository """  
        try:
            for cwid, name, major in file_reader(os.path.join(self._path, "students.txt"), 3, sep= '\t', header= False):
                if cwid in self._students:
                    raise ValueError(f"Student id: {cwid} is already in file")
                else:
                    self._students[cwid] = Student(cwid, name, major)
        except FileNotFoundError:
            raise FileNotFoundError(f"{os.path.join(self._path, 'students.txt')} cannot open.")

    def read_instructor(self)-> None:
        """Read each line from instructiors.txt file and create an instance of class Instructor for each line in the file, and
           add the new Instructor to the repository"""
        try:
            for cwid, name, dept in file_reader(os.path.join(self._path, "instructors.txt"), 3, sep= '\t', header= False):
                if cwid in self._instructors:
                    raise ValueError(f"{cwid} already in file")
                else:
                    self._instructors[cwid] = Instructor(cwid, name, dept)
        except FileNotFoundError:
            raise FileNotFoundError(f"{os.path.join(self._path, 'instructors.txt')} cannot open.")

    def read_grades(self) -> None:
        """Read student_cwid, course, grade, instructor_cwid"""
        try:
            for cwid_st, course, grade, cwid_in in file_reader(os.path.join(self._path, "grades.txt"), 4, sep= '\t',
                                                                    header= False):
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
       

    
def file_reader(path: str, num_fields: int, sep: str=',', header: bool=False) -> Iterator[Tuple[str, ...]]:
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
    stevens = Repository(r'/Users/priyankashiyani/Documents/class810/HW_09')
    
if __name__ == '__main__':
    main()