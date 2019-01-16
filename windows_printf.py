
#Making windows dll function calls through the use of the ctypes library
from ctypes import *

msvcrt = cdll.msvcrt
message_string = "Hello World!\n"
msvcrt.printf("Testing: %s", message_string)