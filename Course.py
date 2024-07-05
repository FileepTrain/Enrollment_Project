import mongoengine
from mongoengine import *
from Department import Department

class Course(Document):
    # the department that this course is in (reference from Department)
    departmentAbbreviation = ReferenceField(Department, db_field='department_abbreviation', required=True, reverse_delete_rule=mongoengine.DENY)
    # course number
    courseNumber = IntField(db_field='course_number', min_value=0,required=True)
    # course name
    courseName = StringField(db_field='course_name', max_length=50, required=True)
    # course description
    description = StringField(db_field='description', max_length=500, required=True)
    # number of units 
    units = IntField(db_field='units', min_value=0, required=True)

    # unique index
    meta = {'collection': 'courses',
            'indexes': [
                {'unique': True, 'fields': ['department_abbreviation', 'course_number'], 'name': 'course_uk_01'}    
            ]}
    
    # initialization
    def __init__(self, departmentAbbreviation: str, courseNumber: int, courseName: str, 
               description: str, units: int, *args, **values):
        super().__init__(*args, **values)
        self.departmentAbbreviation = departmentAbbreviation
        self.courseNumber = courseNumber
        self.courseName = courseName
        self.description = description
        self.units = units
    
    # returns a string representation of course
    def __str__(self):
        return (f"Department Abbreviation: {self.departmentAbbreviation}, Course Number: {self.courseNumber},
                Course Name: {self.courseName}, Description: {self.description}, Units: {self.units}")
