

select Name from students where CWID = '10115';

select Major, count(*) as [Number of student ] from students  group by Major;

select Grade, count(Grade) as [GRADE count ]
from grades
where Course='SSW 810' group by Grade
limit 1;


select CWID , Name , count(Course) as Total_Course
from students s join grades g on s.CWID = g.StudentCWID
group by CWID, Name;


select s.Name as [Name], s.CWID, g.Course, g.Grade, i.Name as [Instructor]
from students s join grades g on s.CWID=g.StudentCWID join instructors i on g.InstructorCWID=i.CWID
order by s.Name asc;