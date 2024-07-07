"""
Created on 04/05/2024
These are utilities that are common between the sample code and the worked homework for the MongoDB One to Many
assignment.
"""
import decimal
from datetime import datetime

from StudentMajor import StudentMajor
from Enrollment import Enrollment, Graded, PassFail
from Department import Department
from Course import Course
from Major import Major
from Student import Student
from Utilities import Utilities
from ConstraintUtilities import select_general, unique_general, prompt_for_date
from Menu import Menu
from Option import Option
from Section import Section
from EnumValues import GradingType, MinimumSatisfactoryGrade


def select_department() -> Department:
    return select_general(Department)


def select_major() -> Major:
    return select_general(Major)


def select_student() -> Student:
    return select_general(Student)


def select_course() -> Course:
    return select_general(Course)


def select_section() -> Section:
    return select_general(Section)

def select_enrollment() -> Enrollment:
    return select_general(Enrollment)


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


def add_student():
    success: bool = False
    new_student = None
    while not success:
        lastName = input('Enter Student Last Name --> ')
        firstName = input('Enter Student First Name --> ')
        email = input('Enter Student Email --> ')
        new_student = Student(lastName, firstName, email)

        violated_constraints = unique_general(new_student)
        if len(violated_constraints) > 0:
            for violated_constraint in violated_constraints:
                print('Your input values violated constraint: ', violated_constraint)
            print('try again')
        else:
            try:
                new_student.save()
                success = True
            except Exception as e:
                print('Errors storing the new student:')
                print(Utilities.print_exception(e))


def delete_student():
    student = select_student()
    if student.enrollments or student.studentMajors:
        print("Error: This department cannot be deleted because it has associated majors or courses.")
        return
    try:
        student.delete()
        print(f"{student.name} has been successfully deleted.")
    except Exception as e:
        print('Errors deleting the student:')
        print(Utilities.print_exception(e))


def list_student():
    all_students = Student.objects().order_by('last_name', 'first_name')
    for student in all_students:
        print(f'{student.last_name}, {student.first_name}')



def add_department():
    success: bool = False
    new_department = None
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


def list_department():
    all_departments = Department.objects().order_by('name')  # Assuming departments have a 'name' field
    for department in all_departments:
        print(f'{department.name}')  # Adjust the field according to your actual Department model


def add_major():
    success: bool = False
    new_major = None
    while not success:
        department = select_department()
        name = input('Enter Major Name --> ')
        description = input('Enter Major Description --> ')
        new_major = Major(department, name, description)
        violated_constraints = unique_general(new_major)
        if len(violated_constraints) > 0:
            for violated_constraint in violated_constraints:
                print('Your input values violated constraint: ', violated_constraint)
            print('try again')
        else:
            try:
                new_major.save()
                department.add_major(new_major)  # Add this Course to the Department's MongoDB list of items.
                department.save()
                success = True
            except Exception as e:
                print('Errors storing the new major:')
                print(Utilities.print_exception(e))


def delete_major():
    major = select_major()
    student_count = Student.objects(major=major).count()
    if student_count > 0:
        print(f"Error: This Major cannot be deleted because it has {student_count} students.")
        return
    try:
        major.delete()
        print(f"Department {major.name} has been successfully deleted.")
    except Exception as e:
        print('Errors deleting the department:')
        print(Utilities.print_exception(e))


def list_major():
    department = select_department()
    if not department:
        print("No department selected.")
        return

    all_majors = sorted(department.majors, key=lambda x: x.name)  # Assuming majors have a 'name' field
    for major in all_majors:
        print(f'{major.name}')  # Adjust the field according to your actual Major model



def add_student_major():
    success: bool = False
    new_student_major: StudentMajor
    student: Student
    major: Major
    while not success:
        print('Select Student')
        student = select_student()
        print('Select Major')
        major = select_major()
        declaration = prompt_for_date('Declaration Date (may not be a future date): ')
        new_student_major = StudentMajor(major, student, declaration)
        violated_constraints = unique_general(new_student_major)
        if len(violated_constraints) > 0:
            for violated_constraint in violated_constraints:
                print('Your input values violated constraint: ', violated_constraint)
            print('try again')
        else:
            try:
                new_student_major.save()
                student.add_major(new_student_major)  # Add this Course to the Department's MongoDB list of items.
                student.save()
                success = True
            except Exception as e:
                print('Errors storing the new student major:')
                print(Utilities.print_exception(e))


def delete_student_major():
    student = select_student()
    all_student_majors = student.studentMajors  # Assuming this is a list of student majors
    menu_student_majors = [Option(studentMajor.__str__(), studentMajor) for studentMajor in all_student_majors]
    studentMajor = Menu('Major Menu', 'Choose which Major to remove', menu_student_majors).menu_prompt()
    try:
        print(type(studentMajor))
        student.remove_major(studentMajor)
        student.save()
        studentMajor.delete()
        print(
            f'{student.firstName} is no longer in the {studentMajor.majorName}. The major has been successfully deleted.')
    except Exception as e:
        print('Errors deleting Student Major:')
        print(Utilities.print_exception(e))


def add_course():
    success: bool = False
    new_course: Course
    department: Department
    while not success:
        department = select_department()  # prompt the user for a department
        course_number = int(input('Enter Course Number (>= 100 and < 700) --> '))
        course_name = input('Enter Course Name --> ')
        description = input('Enter Course Description --> ')
        units = int(
            input('Enter number of units for this course (units must be no less than 1 and no greater than 5) --> '))
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
                department.add_course(new_course)  # Add this Course to the Department's MongoDB list of items.
                department.save()
                success = True
            except Exception as e:
                print('Exception trying to add the new course:')
                print(Utilities.print_exception(e))


# delete a course from a department
def delete_course():
    department = select_department()
    all_courses = department.courses  # the list of courses in this department
    menu_courses: [Option] = []
    for course in all_courses:
        menu_courses.append(Option(course.__str__(), course))
    course = Menu('Course Menu',
                  'Choose which course to remove', menu_courses).menu_prompt()
    try:
        department.remove_course(course)  # delete the course inside department
        department.save()
        course.delete()  # delete the course
        print(f'Course {course.departmentAbbreviation} {course.courseNumber} has been successfully deleted.')
    except Exception as e:
        print('Errors deleting course:')
        print(Utilities.print_exception(e))


def list_courses():
    department = select_department()
    if not department:
        print("No department selected.")
        return

    # Retrieve all courses in the department and sort them alphabetically by course name
    sorted_courses = sorted(department.courses, key=lambda x: x.course_name)

    print(f"Courses for Department {department.department_name}:")
    for course in sorted_courses:
        print(f"Course Name: {course.course_name}, Course Number: {course.course_number}, Description: {course.description}")



def add_section():
    success: bool = False
    new_section: Section
    course: Course
    while not success:
        course = select_course()  # select a course
        section_number = int(input("Enter Section Number --> "))
        semester = prompt_for_enum("Enter Semester (Fall, Spring, Summer I, Summer II, Summer III, Winter) --> ",
                                   Section, 'semester')
        section_year = int(input("Enter Year --> "))
        building = prompt_for_enum("Enter Building (ANAC, CDC, DC, ECS, EN2, EN3, EN4, EN5, ET, HSCI, NUR, VEC) --> ",
                                   Section, 'building')
        room = int(input("Enter Room Number (> 1 and < 1000) --> "))
        schedule = prompt_for_enum("Enter Schedule (MW, TuTh, MWF, F, S) --> ", Section, 'schedule')
        start_time = prompt_for_enum("Enter Section Start Time (HH:MM, 24-hour format, >= 08:00 and <= 19:30) --> ",
                                     Section, 'startTime')
        instructor = input("Enter Instructor Name --> ")
        # create a new section
        new_section = Section(course=course, sectionNumber=section_number, semester=semester,
                              sectionYear=section_year, building=building, room=room, schedule=schedule,
                              startTime=start_time, instructor=instructor)
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
                print('Exception trying to add the new section:')
                print(Utilities.print_exception(e))


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
def list_sections():
    course = select_course()
    if not course:
        print("No course selected.")
        return
    enrollments = Enrollment.objects(course=course)  # get all enrollments within that course
    sections = {enrollment.section for enrollment in enrollments}  # use a set to avoid duplicates
    sorted_sections = sorted(sections, key=lambda x: x.section_number)  # sort sections by section number
    print(f"Sections for Course {course.course_name} (Course Number: {course.course_number}):")
    for section in sorted_sections:
        print(f"Section Number: {section.section_number}")

def list_instructors_in_course():
    success = False
    while not success:
        course = select_course()
        instructors = []
        try:
            sections = Section.objects(course=course)
            for section in sections:
                instructor = section.instructor
                if instructor not in instructors:
                    instructors.add(instructor)
            instructors = sorted(instructors)
            # Print the unique instructors
            for instructor in instructors:
                print(instructor)
            success = True
        except ValueError as ve:
            print('Attempted status change failed because:')
            print(ve)

    # Check and print instructors who were not found in the hashmap
    for instructor in instructors:
        if instructors[instructor] == 0:
            print(f'Instructor not found: {instructor}')
        else:
            print(f'Instructor found: {instructor}, count: {instructors[instructor]}')

def add_enrollment():
    success: bool = False
    newEnrollment: Enrollment
    section: Section
    student: Student
    while not success:
        section = select_section()
        student = select_student()
        gradingType = prompt_for_enum('Select Grading Type --> (Pass/Fail, Letter Grade)', Enrollment, 'type')
        if gradingType == GradingType.LETTER_GRADE:
            minimum_satisfactory_grade = prompt_for_enum('Select Minimum Satisfactory Grade --> (A, B, C)',
                                                         Graded, 'minimum_satisfactory')
            newEnrollment = Graded(
                student=student,
                section=section,
                type=gradingType,
                minimum_satisfactory=minimum_satisfactory_grade
            )
        else:
            application_date = prompt_for_date('Enter the application date (YYYY-MM-DD): ')
            newEnrollment = PassFail(
                student=student,
                section=section,
                type=gradingType,
                application_date=application_date
            )
        # check unique
        violated_constraints = unique_general(newEnrollment)
        if len(violated_constraints) > 0:
            for violated_constraint in violated_constraints:
                print('Your input values violated constraint: ', violated_constraint)
            print('Try again')
        else:
            try:
                newEnrollment.save()  # save new section
                student.add_enrollment(newEnrollment)
                student.save()
                section.add_enrollment(newEnrollment)
                section.save()
                success = True
            except Exception as e:
                print('Exception trying to add the new enrollment:')
                print(Utilities.print_exception(e))


def delete_enrollment():
    enrollment = select_enrollment()
    section = enrollment.section
    student = enrollment.student

    try:
        section.remove_enrollment(enrollment)
        section.save()
        print(f'An enrollment has been successfully deleted from section.')
    except Exception as e:
        print('Errors deleting enrollment from section:')
        print(Utilities.print_exception(e))

    try:
        student.remove_enrollment(enrollment)
        student.save()
        print(f'An enrollment has been successfully deleted from student.')
    except Exception as e:
        print('Errors deleting enrollment from student:')
        print(Utilities.print_exception(e))

    try:
        enrollment.delete()
        enrollment.save()
        print(f'An enrollment has been succesfully deleted.')
        print(
            f'The student {enrollment.studentFirstName} {enrollment.studentLastName} has been unerolled in {enrollment.departmentAbbreviation} {enrollment.courseNumber} Section {enrollment.sectionNumber}')
    except Exception as e:
        print('Errors deleting enrollment from student:')
        print('Error:')
        print(Utilities.print_exception(e))

def list_students_in_section():
    section = select_section()
    if not section:
        print("No section selected.")
        return

    enrollments = section.enrollments.order_by('student.last_name', 'student.first_name')
    for enrollment in enrollments:
        print(f'{enrollment.student.last_name}, {enrollment.student.first_name}')  # Assuming Enrollment model has a student field that references Student

def list_sections_of_student():
    student = select_student()
    if not student:
        print("No student selected.")
        return

    enrollments = student.enrollments.order_by('departmentAbbreviation', 'courseNumber', 'sectionNumber')
    for enrollment in enrollments:
        print(f'{enrollment.departmentAbbreviation} {enrollment.courseNumber} Section {enrollment.sectionNumber} {enrollment.sectionYear} {enrollment.sectionSemester}')


def update_department_abbreviation():
    success: bool = False
    department: Department
    while not success:
        department = select_department()  # Find an order to modify.
        new_abbreviation = input('New Abbreviation: ')
        old_abbreviation = department.abbreviation
        try:
            department.abbreviation = new_abbreviation
            department.save()
            majors = Major.objects(department=department)
            for major in majors:
                major.departmentAbbreviation = new_abbreviation
                major.save()
            courses = Course.objects(department=department)
            for course in courses:
                course.departmentAbbreviation = new_abbreviation
                course.save()
            sections = Section.objects(departmentAbbreviation=old_abbreviation)
            for section in sections:
                enrollments = Enrollment.objects(section=section)
                for enrollment in enrollments:
                    enrollment.departmentAbbreviation = new_abbreviation
                    enrollment.save()
                section.departmentAbbreviation = new_abbreviation
                section.save()
            success = True
        except ValueError as VE:
            print('Attempted status change failed because:')
            print(VE)


def update_course_name():
    success: bool = False
    course: Course
    while not success:
        course = select_course()
        new_name = input('New Name: ')
        try:
            course.courseName = new_name
            course.save()
            success = True
        except ValueError as VE:
            print('Attempted status change failed because:')
            print(VE)


def update_student_name():
    success: bool = False
    student: Student
    while not success:
        student = select_student()
        new_first = input('New First Name: ')
        new_last = input('New Last Name: ')
        try:
            student.firstName = new_first
            student.lastName = new_last
            student.save()
            majors = StudentMajor.objects(student=student)
            for major in majors:
                major.studentFirstName = new_first
                major.studentLastName = new_last
                major.save()
            enrollments = Enrollment.objects(student=student)
            for enrollment in enrollments:
                enrollment.studentFirstName = new_first
                enrollment.studentLastName = new_last
                enrollment.save()
            success = True
        except ValueError as VE:
            print('Attempted status change failed because:')
            print(VE)
