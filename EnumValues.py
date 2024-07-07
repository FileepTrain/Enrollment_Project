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

class Schedule(Enum):
    MW = 'MW'
    TuTh = 'TuTh'
    MWF = 'MWF'
    F = 'F'
    S = 'S'


class Semester(Enum):
    Fall = 'Fall'
    Spring = 'Spring'
    SummerI = 'Summer I'
    SummerII = 'Summer II'
    SummerIII = 'Summer III'
    Winter = 'Winter'

from enum import Enum

class StartTime(Enum):
    t_0800 = '08:00'
    t_0830 = '08:30'
    t_0900 = '09:00'
    t_0930 = '09:30'
    t_1000 = '10:00'
    t_1030 = '10:30'
    t_1100 = '11:00'
    t_1130 = '11:30'
    t_1200 = '12:00'
    t_1230 = '12:30'
    t_1300 = '13:00'
    t_1330 = '13:30'
    t_1400 = '14:00'
    t_1430 = '14:30'
    t_1500 = '15:00'
    t_1530 = '15:30'
    t_1600 = '16:00'
    t_1630 = '16:30'
    t_1700 = '17:00'
    t_1730 = '17:30'
    t_1800 = '18:00'
    t_1900 = '19:00'
    t_1930 = '19:30'
