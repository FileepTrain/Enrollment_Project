from mongoengine import *


class Student(Document):
    lastName = StringField(db_field='last_name', max_length=50, required=True)
    firstName = StringField(db_field='first_name', max_length=50, required=True)
    email = StringField(db_field='email', min_lenth=10, max_length=100, required=True)
    enrollments = ListField(ReferenceField('Enrollment'))
    studentMajors = ListField(ReferenceField('StudentMajor'))

    meta = {
        'collection': 'students',
        'indexes': [
            {'fields': ['lastName', 'firstName'], 'unique': True, 'name': 'student_uk_01'},
            {'fields': ['email'], 'unique': True, 'name': 'student_uk_02'}
        ]
    }

    def add_enrollment(self, enrollment):
        for alreadyEnrolled in self.enrollments:
            if enrollment.equals(alreadyEnrolled):
                return  # Already enrolled, don't add it.
        self.enrollments.append(enrollment)

    def remove_enrollment(self, enrollment):
        for already_enrolled in self.enrollments:
            if enrollment.equals(already_enrolled):
                self.enrollments.remove(enrollment)
                return

    def add_major(self, studentMajor):
        for already_enrolled in self.studentMajors:
            if studentMajor.majorName.equals(already_enrolled.majorName):
                return  # Already enrolled, don't add it.
        self.studentMajors.append(studentMajor)

    def remove_major(self, studentMajor):
        for major in self.studentMajors:
            if studentMajor.equals(major):
                self.studentMajors.remove(major)
                return
    def __init__(self, lastName: str, firstName: str, email: str, *args, **values):
        super().__init__(*args, **values)
        if self.enrollments is None:
            self.enrollments = []  # initialize to no enrollments.
        self.firstName = firstName
        self.lastName = lastName
        self.email = email

    def __str__(self):
        return f'{self.firstName}  {self.lastName} \nEmail: {self.email}'
