import mongoengine
from mongoengine import *
from Department import Department


class Major(Document):
    department = ReferenceField(Department, db_field='department', required=True, reverse_delete_rule=mongoengine.DENY)
    departmentAbbreviation = StringField(db_field='department_abbreviation', max_length=6, required=True)
    name = StringField(db_field='name', max_length=50, required=True)
    description = StringField(db_field='description', max_length=500, required=True)

    # unique index
    meta = {'collection': 'majors',
            'indexes': [
                {'unique': True, 'fields': ['name'], 'name': 'major_uk_01'},
            ]}

    # initialization:
    def __init__(self, department: Department, name: str, description: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.department = department
        if isinstance(department, Department):
            self.departmentAbbreviation = department.abbreviation
        self.name = name
        self.description = description

    def equals(self, other) -> bool:
         if (self.department == other.department and
             self.departmentAbbreviation == other.departmentAbbreviation and
             self.name == other.name and
             self.description == other.description):
             return True
         return False


    # returns a string representation of course
    def __str__(self):
        return (f"Department Abbreviation: {self.departmentAbbreviation}, Name: {self.name}, Description: {self.description}")


