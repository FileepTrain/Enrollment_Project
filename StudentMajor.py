import mongoengine
from mongoengine import Document, StringField, DateTimeField, ReferenceField
import datetime

from Major import Major
from Student import Student


class StudentMajor(Document):
    major = ReferenceField(Major, required=True, reverse_delete_rule=mongoengine.DENY)
    student = ReferenceField(Student, required=True, reverse_delete_rule=mongoengine.DENY)
    majorName = StringField(db_field='major_name', max_length=50, required=True)
    studentLastName = StringField(db_field='student_last_name', max_length=50, required=True)
    studentFirstName = StringField(db_field='student_first_name', max_length=50, required=True)
    declaration = DateTimeField(db_field='declaration', required=True)

    # unique index
    meta = {
        'collection': 'student_majors',
        'indexes': [
            {'unique': True, 'fields': ['major', 'student'], 'name': 'student_major_uk_01'},
        ]
    }

    def __init__(self, major: Major, student: Student, declaration: datetime, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.major = major
        if isinstance(major, Major):
            self.majorName = major.name
        self.student = student
        if isinstance(student, Student):
            self.studentLastName = student.lastName
            self.studentFirstName = student.firstName
        self.declaration = declaration

    def clean(self):
        # Ensure declaration date is not in the future
        if self.declaration > datetime.now():
            raise mongoengine.ValidationError('Declaration date cannot be in the future.')
    def __str__(self):
        return (f"Major: {self.majorName}, First: {self.studentFirstName}, Last: {self.studentLastName}, Declaration: {self.declaration}")

    def get_major(self):
        from Major import Major
        return Major.objects(id=self.major).first()

    def get_student(self):
        from Student import Student
        return Student.objects(id=self.student).first()

    def equals(self, other) -> bool:
        if self.majorName == other.majorName and self.studentLastName == other.studentLastName and self.studentFirstName == other.studentFirstName == other.declaration:
            return True
        return False