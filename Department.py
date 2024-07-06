import decimal

from mongoengine import *
from EnumValues import Building


class Department(Document):
    name = StringField(db_field='name', max_length=50, required=True)
    abbreviation = StringField(db_field='abbreviation', max_length=6, required=True)
    chairName = StringField(db_field='chair_name', max_length=80, required=True)
    building = EnumField(Building, db_field='building', required=True)
    office = IntField(db_field='office', min_value=0, required=True)
    description = StringField(db_field='description', max_length=80, required=True)
    majors = ListField(ReferenceField('Major'))
    courses = ListField(ReferenceField('Course'))

    meta = {'collection': 'departments',
            'indexes': [
                {'unique': True, 'fields': ['name'], 'name': 'department_uk_01'},
                {'unique': True, 'fields': ['abbreviation'], 'name': 'department_uk_02'},
                {'unique': True, 'fields': ['chairName'], 'name': 'department_uk_03'},
                {'unique': True, 'fields': ['building', 'office'], 'name': 'department_uk_04'},
                {'unique': True, 'fields': ['description'], 'name': 'department_uk_05'},
            ]}

    def __init__(self, name: str, abbreviation: str, chairName: str, building: Building,
                 office: int, description: str, *args, **values):
        super().__init__(*args, **values)
        if self.majors is None:
            self.majors = []
        if self.courses is None:
            self.courses = []
        self.name = name
        self.abbreviation = abbreviation
        self.chairName = chairName
        self.building = building
        self.office = office
        self.description = description

    def __str__(self):
        """
        Returns a string representation of the Order instance.
        :return: A string representation of the Order instance.
        """
        return (f' Abbreviation: {self.abbreviation}, Name: {self.name}, Location: {self.building} {self.office}, '
                f'Description: {self.description},')

    def add_major(self, major):
        for already_added_major in self.majors:
            if major.equals(already_added_major):
                return # don't add course if it already exists
        self.courses.append(major)
    # remove a course from the department
    def remove_major(self, major):
        for available_major in self.majors:
            if major.equals(available_major):
                self.courses.remove(available_major)
                return
    # added:
    # add a course to the department
    def add_course(self, course):
        for already_added_course in self.courses:
            if course.equals(already_added_course):
                return # don't add course if it already exists
        self.courses.append(course)
    # remove a course from the department
    def remove_course(self, course):
        for available_course in self.courses:
            if course.equals(available_course):
                self.courses.remove(available_course)
                return
