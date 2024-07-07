import mongoengine
from mongoengine import *
from Course import Course
from EnumValues import Semester, Schedule, Building, StartTime

class Section(Document):
    # the course that this section is in (reference from Course)
    course = ReferenceField(Course, db_field='course', required=True, reverse_delete_rule=mongoengine.DENY)
    # department abbreviation (from Course)
    departmentAbbreviation = StringField(db_field='department_abbreviation', max_length=6, required=True)
    # course number (from Course)
    courseNumber = IntField(db_field='course_number', min_value=100, max_value=700, required=True)
    # section number
    sectionNumber = IntField(db_field='section_number', required=True)
    # semester (enum from Semester.py)
    semester = EnumField(Semester, db_field='semester', required=True)
    # section year
    sectionYear = IntField(db_field='section_year', required=True)
    # building (enum from Building.py)
    building = EnumField(Building, db_field='building', required=True)
    # room
    room = IntField(db_field='room', min_value=1, max_value=999, required=True)
    # schedule (enum from Schedule.py)
    schedule = EnumField(Schedule, db_field='schedule', required=True)
    # start time
    startTime = EnumField(StartTime, db_field='start_time', required=True)
    # instructor
    instructor = StringField(db_field='instructor', required=True)
    # list of enrollments
    enrollments = ListField(ReferenceField('Enrollment'))

    # uniqueness constraints
    meta = {'collection': 'sections',
            'indexes': [
                {'unique': True, 'fields': ['departmentAbbreviation', 'courseNumber', 'sectionNumber', 'semester', 'sectionYear'],
                 'name': 'section_uk_01'},
                {'unique': True, 'fields': ['semester', 'sectionYear', 'building', 'room', 'schedule', 'startTime'],
                 'name': 'section_uk_02'},
                {'unique': True, 'fields': ['semester', 'sectionYear', 'schedule', 'startTime', 'instructor'],
                 'name': 'section_uk_03'}
            ]}

    # constructor
    def __init__(self, course: Course, sectionNumber: int, semester, sectionYear: int,
                 building, room: int, schedule, startTime, instructor: str, *args, **values):
        super().__init__(*args, **values)
        self.course = course
        if isinstance(course, Course):
            self.departmentAbbreviation = course.departmentAbbreviation
            self.courseNumber = course.courseNumber
        self.sectionNumber = sectionNumber
        self.semester = semester
        self.sectionYear = sectionYear
        self.building = building
        self.room = room
        self.schedule = schedule
        self.startTime = startTime
        self.instructor = instructor

    # returns a string representation of section
    def __str__(self):
        return f"Course: {self.departmentAbbreviation} {self.courseNumber}, Section Number: {self.sectionNumber}, Year: {self.sectionYear}, Semester: {self.semester}, Location: {self.building} {self.room}, Instructor: {self.instructor}"


