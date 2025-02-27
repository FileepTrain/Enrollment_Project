from Menu import Menu
import logging
from Option import Option

menu_logging = Menu('debug', 'Please select the logging level from the following:', [
    Option("Debugging", "logging.DEBUG"),
    Option("Informational", "logging.INFO"),
    Option("Error", "logging.ERROR")
])

menu_main = Menu('main', 'Please select one of the following options:', [
    Option("Add new instance", "add()"),
    Option("Delete existing instance", "delete()"),
    Option("List existing instances", "list_members()"),
    Option("Update existing instance", "update()"),
    Option("Exit", "pass")
])

# options for adding a new instance
add_select = Menu('add select', 'Which type of object do you want to add?:', [
    Option("Student", "add_student()"),
    Option("Department", "add_department()"),
    Option("Major", "add_major()"),
    Option("Course", "add_course()"),
    Option("Section", "add_section()"),
    Option("Student Major", "add_student_major()"),
    Option("Enrollment", "add_enrollment()"),
    Option("Exit", "pass")
])

# options for deleting an existing instance
delete_select = Menu('delete select', 'Which type of object do you want to delete?:', [
    Option("Student", "delete_student()"),
    Option("Department", "delete_department()"),
    Option("Major", "delete_major()"),
    Option("Course", "delete_course()"),
    Option("Section", "delete_section()"),
    Option("Student Major", "delete_student_major()"),
    Option("Enrollment", "delete_enrollment()"),
    Option("Exit", "pass")
])

# options for listing the existing instances
list_select = Menu('list select', 'Which type of object do you want to list?:', [
    Option("Student", "list_student()"),
    Option("Department", "list_department()"),
    Option("Major", "list_major()"),
    Option("Course", "list_course()"),
    Option("Section", "list_section()"),
    Option("Students in Section", "list_students_in_section()"),
    Option("Sections of Student", "list_sections_of_student()"),
    Option("Instructors in a Course", "list_instructors_in_course()"),
    Option("Exit", "pass")
])

# options for testing the update functions
update_select = Menu("Update Select", 'Which type of object do you want to update:', [
    Option("Department Abbreviation", "update_department_abbreviation()"),
    Option("Course Name", "update_course_name()"),
    Option("Student Name", "update_student_name()"),
    Option("Exit", "pass")
])
