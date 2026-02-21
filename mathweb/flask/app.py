import math
from flask import Flask
import math
from flask import Flask
import math
from flask import Flask

def factorial(n):
    "compute factorial"

    if n == 0:
        return 1
    else:
        return n * factorial(n-1)

def get_factorial(n):
    return str(math.factorial(n))
import math
from flask import Flask

def factorial(n):
    "compute factorial"

    if n == 0:
        return 1
    else:
        return n * factorial(n-1)

def get_factorial(n):
    return str(math.factorial(n))
