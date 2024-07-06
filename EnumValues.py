from enum import Enum


class Building(Enum):
    ANAC = 'ANAC'
    CDC = 'CDC'
    DC = 'DC'
    ECS = 'ECS'
    EN2 = 'EN2'
    EN3 = 'EN3'
    EN4 = 'EN4'
    EN5 = 'EN5'
    ET = 'ET'
    HSCI = 'HSCI'
    NUR = 'NUR'
    VEC = 'VEC'


class GradingType(Enum):
    PASS_FAIL = 'Pass/Fail'
    LETTER_GRADE = 'Letter Grade'


class MinimumSatisfactoryGrade(Enum):
    A = 'A'
    B = 'B'
    C = 'C'
    D = 'D'
    F = 'F'
