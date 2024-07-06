import mongoengine
from mongoengine import *
from Major import Major
from Student import Student
import datetime



class StudentMajor(Document):
    major = ReferenceField(Major, db_field='major', required=True, reverse_delete_rule=mongoengine.DENY)
    student = ReferenceField(Student, db_field='student', required=True, reverse_delete_rule=mongoengine.DENY)
    majorName = StringField(db_field='course_name', max_length=50, required=True)
    studentLastName = StringField(db_field='student_last_name', max_length=50, required=True)
    studentFirstName = StringField(db_field='student_first_name', max_length=50, required=True)
    declaration = DateTimeField(db_field='declaration',  required=True)

    # unique index
    meta = {'collection': 'majors',
            'indexes': [
                {'unique': True, 'fields': ['major', 'student'], 'name': 'course_uk_01'},
            ]}

    # initialization:
    def __init__(self, major: Major, student: Student, declaration: datetime, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.major = major
        self.student = student
        self.majorName = major.name
        self.studentLastName = student.lastName
        self.studentFirstName = student.firstName
        self.declaration = declaration

    # returns a string representation of course
    def __str__(self):
        return (f"Major: {self.majorName}, First: {self.studentFirstName}, Last: {self.studentLastName}, Declaration: {self.declaration}")


