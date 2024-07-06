import mongoengine
from mongoengine import *
from Student import Student
from Section import Section


class Enrollment(Document):
    departmentAbbreviation = StringField(db_field='department_abbreviation', max_length=6, required=True)
    courseNumber = IntField(db_field='course_number', required=True)
    sectionNumber = IntField(db_field='section_number', required=True)
    sectionYear = IntField(db_field='section_year', required=True)
    # section_semester = EnumField(choices=['Fall', 'Spring', 'Summer', 'Winter'], required=True)
    studentFirstName = StringField(db_field='student_first_name', max_length=50, required=True)
    studentLastName = StringField(db_field='last_name', max_length=50, required=True)
    student = ReferenceField(Student, required=True, reverse_delete_rule=mongoengine.DENY)
    section = ReferenceField(Section, required=True, reverse_delete_rule=mongoengine.DENY)

    meta = {'allow_inheritance': True,
            'collection': 'enrollments',
            'indexes': [
                {'unique': True, 'fields': ['student', 'section']}
            ]}

    def __init__(self, student: Student, section: Section, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if student:
            self.student = student
            self.studentFirstName = student.firstName
            self.studentLastName = student.lastName

        if section:
            self.departmentAbbreviation = section.departmentAbbreviation
            self.courseNumber = section.courseNumber
            self.sectionNumber = section.sectionNumber
            self.sectionYear = section.sectionYear
            # self.section_semester = section.semester

    def __str__(self):
        return f'{self.studentFirstName} {self.studentLastName} is enrolled in {self.courseNumber} Section {self.sectionNumber}'


class CourseType(Enrollment):
    type = EnumField(required=True, choices=['Pass/Fail', 'Letter Grade'])
    minimum_satisfactory = EnumField(choices=['A', 'B', 'C', 'D', 'F'], db_field='min_satisfactory')

    def __init__(self, type, minimum_satisfactory, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.type = type
            if type == 'Letter Grade':
                self.minimum_satisfactory = minimum_satisfactory

    def __str__(self):
        if self.type == 'Letter Grade':
            return f'{super().__str__()} with a {self.type} grading system and a minimum satisfactory grade of {self.minimum_satisfactory}'
        return f'{super().__str__()} with a {self.type} grading system

