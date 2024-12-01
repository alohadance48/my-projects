import time
from time import strftime


def time_show():
    current_day = strftime("%a",time.localtime())
    return current_day

one = 'Mon'
two = 'Tue'
three = 'Wed'
four = 'Thu'
five = 'Fri'
six = 'Sat'
seven = 'Sun'



def schedule(day):
    if day == one:
        return '1'
    if day == two:
        return '2'
    if day == three:
        return '3'
    if day == four:
        return '4'
    if day == five:
        return '5'
    if day == six:
        return '6'
    if day == seven:
        return '7'