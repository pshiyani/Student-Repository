"""
Author: Priyankaben Shiyani
Project Description: Implementing Student grade summary
"""
import sqlite3
from flask import Flask, render_template
from typing import Dict

app: Flask = Flask(__name__)

@app.route('/students')
def studnets_grades_summary() -> str:
    """ Function to print student grade summary """
    db_path = r'/Users/priyankashiyani/Documents/class810/HW_12/810sql'
    try:
        db: sqlite3 = sqlite3.connect(db_path)
    except sqlite3.OperationalError:
        print(f"Error: Unable to open database at {db_path}")
    else:
            query: str = """select s.Name as [Name], s.CWID, g.Course, g.Grade, i.Name as [Instructor]
                from students s join grades g on s.CWID=g.StudentCWID join instructors i on g.InstructorCWID=i.CWID
                order by s.Name asc;"""

            data: Dict[str, str] = [{"Name":Name , "CWID":CWID, "Course":Course, "Grade":Grade, "Instructor":Instructor} for
                    Name, CWID, Course, Grade, Instructor in db.execute(query)]
            db.close()
            return render_template('student.html', header='Stevens Repository', table ='Name , Course, Grade, and Instructor' , student = data)
if __name__ == "__main__":
    app.run(debug=True)