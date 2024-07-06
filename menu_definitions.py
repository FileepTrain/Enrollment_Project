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
    Option("Select existing instance", "select()"),
    Option("Update existing instance", "update()"),
    Option("Exit", "pass")
])

# options for adding a new instance
add_select = Menu('add select', 'Which type of object do you want to add?:', [
    Option("Student", "add_student()"),
    Option("Department", "add_department()"),
    Option("Major", "add_major()"),
    Option("Course", "add_course()"),
    Option("Exit", "pass")
])

# options for deleting an existing instance
delete_select = Menu('delete select', 'Which type of object do you want to delete?:', [
    Option("Student", "delete_student()"),
    Option("Department", "delete_department()"),
    Option("Major", "delete_major()"),
    Option("Course", "delete_course()"),
    Option("Exit", "pass")
])

# options for listing the existing instances
list_select = Menu('list select', 'Which type of object do you want to list?:', [
    Option("Student", "list_student()"),
    Option("Department", "list_department()"),
    Option("Major", "list_major()"),
    Option("Course", "list_course()"),
    Option("Exit", "pass")
])

# options for testing the select functions
select_select = Menu('select select', 'Which type of object do you want to select:', [
    Option("Student", "select_student()"),
    Option("Department", "select_department()"),
    Option("Major", "select_major()"),
    Option("Course", "select_course()"),
    Option("Exit", "pass")
])

# options for testing the update functions
update_select = Menu("update select", 'Which type of object do you want to update:', [
    Option("Order", "update_order()"),
    Option("Order Items", "update_order_item()"),
    Option("Products", "update_product()"),
    Option("Exit", "pass")
])
