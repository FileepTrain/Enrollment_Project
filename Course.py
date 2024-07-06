import mongoengine
from mongoengine import *
from Department import Department

class Course(Document):
    # the department that this course is in (reference from Department)
    department = ReferenceField(Department, db_field='department', required=True, reverse_delete_rule=mongoengine.DENY)
    # department abbreviation
    departmentAbbreviation = StringField(db_field='department_abbreviation', max_length=6, required=True)
    # course number
    courseNumber = IntField(db_field='course_number', min_value=100, max_value=700, required=True)
    # course name
    courseName = StringField(db_field='course_name', max_length=50, required=True)
    # course description
    description = StringField(db_field='description', max_length=500, required=True)
    # number of units 
    units = IntField(db_field='units', min_value=1, max_value=5, required=True)

    # unique index
    meta = {'collection': 'courses',
            'indexes': [
                {'unique': True, 'fields': ['departmentAbbreviation', 'courseNumber'], 'name': 'course_uk_01'},
                {'unique': True, 'fields': ['departmentAbbreviation', 'courseName'], 'name': 'course_uk_02'}
            ]}
    
    # initialization:
    def __init__(self, department: Department, courseNumber: int, courseName: str, description: str, units: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.department = department
        self.departmentAbbreviation = department.abbreviation
        self.courseNumber = courseNumber
        self.courseName = courseName
        self.description = description
        self.units = units

    
    # returns a string representation of course
    def __str__(self):
        return (f"Department Abbreviation: {self.departmentAbbreviation}, Course Number: {self.courseNumber}, Course Name: {self.courseName}, Description: {self.description}, Units: {self.units}")
    # fucnction to check if 2 courses is the same
    def equals(self, other) -> bool:
        if self.departmentAbbreviation == other.departmentAbbreviation and self.courseNumber == other.courseNumber:
            return True
        return False

