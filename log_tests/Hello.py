import logging

# DEBUG: DETAILED information, typically of interest only when diagnosing problems

# INFO: Confirmation that things are working as expected

# WARNING: An indication that something unexpected happened, or indicative of some problem in near future
# (e.g. 'disk space low'). The software is still working as expected

# ERROR: Due to a more serious problem, the software has not been able to perform some function

# CRITICAL: A serious error, indicating that the program itself may be unable to continue running.

logging.basicConfig(filename='test.log', level=logging.DEBUG, 
format='%(asctime)s:%(levelname)s:%(message)s')

def add(x, y):
    return x + y

def subtract(x, y):
    return x - y

def multiply(x, y):
    return x * y

def divide(x, y):
    return x/y

x = 20
y = 10

add_result = add(x, y)
logging.debug(add_result)

subtract_result = subtract(x, y)
logging.debug(subtract_result)

multiply_result = multiply(x, y)
logging.debug(multiply_result)

divide_result = divide(x, y)
logging.debug(divide_result)
