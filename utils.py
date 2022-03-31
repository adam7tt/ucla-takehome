import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter

def get_change(current, previous):
    if current == previous:
        return 100.0
    try:
        if previous > current:
            return -(abs(current - previous) / previous) * 100.0
        else:
            return (abs(current - previous) / previous) * 100.0
    except ZeroDivisionError:
        return 0

def prime_factorization(n):
    holder = ""
    c = 2
    while(n > 1):
 
        if(n % c == 0):
            holder+=(str(c) + ";")
            n = n / c
        else:
            c = c + 1
    return holder
    
def back_to_int(string):
    return int(string.split("(")[0])

def back_to_float(string):
    return float(string.split("(")[0])

