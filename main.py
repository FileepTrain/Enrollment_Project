from ConstraintUtilities import select_general, unique_general, prompt_for_date
from StudentMajor import StudentMajor
from Course import Course
from Department import Department
from Major import Major
from Student import Student
from Utilities import Utilities
from CommandLogger import CommandLogger, log
from pymongo import monitoring
from Menu import Menu
from Option import Option
from menu_definitions import menu_main, add_select, list_select, select_select, delete_select, update_select
import CommonUtilities as CU  # Utilities that work for the sample code & the worked HW assignment.

"""
This protects Order from deletions in OrderItem of any of the objects reference by Order
in its order_items list.  We could not include this in Order itself since that would 
make a cyclic delete_rule between Order and OrderItem.  I've commented this out because
it makes it impossible to remove OrderItem instances.  But you get the idea how it works."""


# OrderItem.register_delete_rule(Order, 'orderItems', mongoengine.DENY)

def menu_loop(menu: Menu):
    """Little helper routine to just keep cycling in a menu until the user signals that they
    want to exit.
    :param  menu:   The menu that the user will see."""
    action: str = ''
    while action != menu.last_action():
        action = menu.menu_prompt()
        print('next action: ', action)
        exec(action)


def add():
    menu_loop(add_select)


def list_members():
    menu_loop(list_select)


def select():
    menu_loop(select_select)


def delete():
    menu_loop(delete_select)


def update():
    menu_loop(update_select)

def select_student() -> Student:
    return select_general(Student)
def select_department() -> Department:
    return select_general(Department)
def select_major() -> Major:
    return select_general(Major)

def select_course() -> Course:
    return select_general(Course)

def prompt_for_enum(prompt: str, cls, attribute_name: str):
    return CU.prompt_for_enum(prompt, cls, attribute_name)

def add_department():
    CU.add_department()

def delete_department():
    CU.delete_department()


def add_major():
    CU.add_major()

def delete_major():
    CU.delete_major()

def add_course():
    CU.add_course()

def delete_course():
    CU.delete_course()

def list_course():
    CU.list_course()

if __name__ == '__main__':
    print('Starting in main.')
    monitoring.register(CommandLogger())
    db = Utilities.startup()
    main_action: str = ''
    while main_action != menu_main.last_action():
        main_action = menu_main.menu_prompt()
        print('next action: ', main_action)
        exec(main_action)
    log.info('All done for now.')
