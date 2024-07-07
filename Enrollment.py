import mongoengine
from mongoengine import *
from Student import Student
from Section import Section
from EnumValues import GradingType, MinimumSatisfactoryGrade, Semester
from datetime import datetime

class Enrollment(Document):
    departmentAbbreviation = StringField(db_field='department_abbreviation', max_length=6, required=True)
    courseNumber = IntField(db_field='course_number', required=True)
    sectionNumber = IntField(db_field='section_number', required=True)
    sectionYear = IntField(db_field='section_year', required=True)
    sectionSemester = EnumField(Semester, db_field='semester', required=True)
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
        self.student = student
        if isinstance(student, Student):
            self.studentFirstName = student.firstName
            self.studentLastName = student.lastName
        self.section = section
        if isinstance(section, Section):
            self.departmentAbbreviation = section.departmentAbbreviation
            self.courseNumber = section.courseNumber
            self.sectionNumber = section.sectionNumber
            self.sectionYear = section.sectionYear
            self.sectionSemester = section.semester

    def __str__(self):
        return f'{self.studentFirstName} {self.studentLastName} is enrolled in {self.departmentAbbreviation} {self.courseNumber} Section {self.sectionNumber} {self.sectionYear} {self.sectionSemester}'
    
    def equals(self, other) -> bool:
         if (self.departmentAbbreviation == other.departmentAbbreviation and
             self.courseNumber == other.courseNumber and
             self.sectionNumber == other.sectionNumber and
             self.sectionYear == other.sectionYear and
             self.sectionSemester == other.sectionSemester and
             self.studentFirstName == other.studentFirstName and
             self.studentLastName == other.studentLastName):
              return True
         return False


class Graded(Enrollment):
    minimum_satisfactory = EnumField(MinimumSatisfactoryGrade, db_field='minimum_satisfactory_grade', required=True)

    def __init__(self, minimumSatisfactory, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.minimumSatisfactory = minimumSatisfactory

    def __str__(self):
        return f'{super().__str__()} with a graded course and needs a minimum satisfactory grade of {self.minimumSatisfactory}'

class PassFail(Enrollment):
    application_date = DateTimeField(db_field='application_date', required=True)

    def __init__(self, application_date, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.application_date = application_date

    def __str__(self):
        return f'{super().__str__()} with a Pass/Fail grading system and an application date of {self.application_date}'



