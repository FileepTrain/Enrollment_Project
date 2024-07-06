"""
Created on 04/05/2024
These are utilities that are common between the sample code and the worked homework for the MongoDB One to Many
assignment.
"""
import decimal

from Department import Department
from Course import Course
from Utilities import Utilities
from ConstraintUtilities import select_general, unique_general, prompt_for_date
from Menu import Menu
from Option import Option
from Section import Section


def select_course() -> Course:
    return select_general(Course)

def select_section() -> Section:
    return select_general(Section)

def select_department() -> Department:
    return select_general(Department)


def prompt_for_enum(prompt: str, cls, attribute_name: str):
    """
    MongoEngine attributes can be regulated with an enum.  If they are, the definition of
    that attribute will carry the list of choices allowed by the enum (as well as the enum
    class itself) that we can use to prompt the user for one of the valid values.  This
    represents the 'don't let bad data happen in the first place' strategy rather than
    wait for an exception from the database.
    :param prompt:          A text string telling the user what they are being prompted for.
    :param cls:             The class (not just the name) of the MongoEngine class that the
                            enumerated attribute belongs to.
    :param attribute_name:  The NAME of the attribute that you want a value for.
    :return:                The enum class member that the user selected.
    """
    attr = getattr(cls, attribute_name)  # Get the enumerated attribute.
    if type(attr).__name__ == 'EnumField':  # Make sure that it is an enumeration.
        enum_values = []
        for choice in attr.choices:  # Build a menu option for each of the enum instances.
            enum_values.append(Option(choice.value, choice))
        # Build an "on the fly" menu and prompt the user for which option they want.
        return Menu('Enum Menu', prompt, enum_values).menu_prompt()
    else:
        raise ValueError(f'This attribute is not an enum: {attribute_name}')


def add_department():
    success: bool = False
    while not success:
        name = input('Enter Department Name --> ')
        abbreviation = input('Enter the Department Abbreviation --> ')
        chair_name = input('Enter Chair Name --> ')
        building = prompt_for_enum('Select building:', Department, 'building')
        office = int(input('Enter Office --> '))
        description = input('Enter Department Description --> ')
        new_department = Department(name,
                                    abbreviation,
                                    chair_name, building, office, description)

        violated_constraints = unique_general(new_department)
        if len(violated_constraints) > 0:
            for violated_constraint in violated_constraints:
                print('Your input values violated constraint: ', violated_constraint)
            print('try again')
        else:
            try:
                new_department.save()
                success = True
            except Exception as e:
                print('Errors storing the new department:')
                print(Utilities.print_exception(e))


def delete_department():
    department = select_department()

    if department.majors or department.courses:
        print("Error: This department cannot be deleted because it has associated majors or courses.")
        return

    try:
        department.delete()
        print(f"Department {department.name} has been successfully deleted.")
    except Exception as e:
        print('Errors deleting the department:')
        print(Utilities.print_exception(e))

# add a course to an existing department
def add_course():
    success: bool = False
    new_course: Course
    department: Department
    while not success:
        department = select_department() # prompt the user for a department
        course_number = int(input('Enter Course Number (>= 100 and < 700) --> '))
        course_name = input('Enter Course Name --> ')
        description = input('Enter Course Description --> ')
        units = int(input('Enter number of units for this course (units must be no less than 1 and no greater than 5) --> '))
        # create a new course
        new_course = Course(department, course_number, course_name, description, units)
        # check unique
        violated_constraints = unique_general(new_course)
        if len(violated_constraints) > 0:
            for violated_constraint in violated_constraints:
                print('Your input values violated constraint: ', violated_constraint)
            print('Try again')
        else:
            try:
                new_course.save()
                department.add_course(new_course) # Add this Course to the Department's MongoDB list of items.
                department.save()
                success = True
            except Exception as e:
                print('Exception trying to add the new course:')
                print(Utilities.print_exception(e))
# delete a course from a department

def delete_course():
    department = select_department()
    all_courses = department.courses    # the list of courses in this department
    menu_courses: [Option] = []
    for course in all_courses:
        menu_courses.append(Option(course.__str__(), course))
    department.remove_course(Menu('Course Menu',
                                  'Choose which course to remove', menu_courses).menu_prompt())
    department.save()

# list all courses form a specific department:
def list_course():
    department = select_department()
    all_courses = department.courses    # all courses in that department
    for course in all_courses:
        print(course)
 

# add a section to a course
def add_section():
    success: bool = False
    new_section: Section
    course: Department
    while not success:
        course = select_course() # select a course 
        section_number = int(input("Enter Section Number --> "))
        semester = prompt_for_enum("Enter Semester (Fall, Spring, Summer I, Summer II, Summer III, Winter) --> ", Section, 'semester')
        section_year = int(input("Enter Year --> "))
        building = prompt_for_enum("Enter Building (ANAC, CDC, DC, ECS, EN2, EN3, EN4, EN5, ET, HSCI, NUR, VEC) --> ", Section, 'building')
        room = int(input("Enter Room Number (> 1 and < 1000) --> "))
        schedule = prompt_for_enum("Enter Schedule (MW, TuTh, MWF, F, S) --> ", Section, 'schedule')
        start_time = prompt_for_enum("Enter Section Start Time (HH:MM, 24-hour format, >= 08:00 and <= 19:30) --> ", Section, 'startTime')
        instructor = input("Enter Instructor Name --> ")
        # create a new section
        new_section = Section(course, section_number, semester, section_year, building, room, schedule, start_time, instructor)
        # check unique
        violated_constraints = unique_general(new_section)
        if len(violated_constraints) > 0:
            for violated_constraint in violated_constraints:
                print('Your input values violated constraint: ', violated_constraint)
            print('Try again')
        else:
            try:
                new_section.save()  # save new section
                success = True
            except Exception as e:
                print('Exception trying to add the new course:')
                print(Utilities.print_exception(e))

# delete a section from a course
def delete_section():
    section = select_section()
    # check for enrollments
    if section.enrollments:
        print("This section cannot be deleted because it has students enrolled in it.")
        return
    # delete the section
    try:
        section.delete()
        print(f'Section {section.sectionNumber} has been successfully deleted.')
    except Exception as e:
        print('Errors deleting section:')
        print(Utilities.print_exception(e))    

# list all sections of a course
def list_section():
    course = select_course()
    all_sections = Section.objects(course=course) # get all section within that course
    for section in all_sections:
        print(section)

