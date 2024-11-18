
import sys

def is_integer(argument: str) -> int:
    try:
        value = int(argument)
        return value
    except ValueError:
        print(f"Error! The argument {argument} is not a valid integer.")

def ConfigParser(arguments):

    if len(arguments) < 5:
        print("Arguments are missing, there must be a total of 4!")
        sys.exit(1) 
    if len(arguments) > 5:
        print("Many arguments, there must be a total of 4!")
        sys.exit(1) 
     
    if arguments[1] != '-a':
        print(f"Error! The 1st argument must be '-a', not {arguments[1]}")
        sys.exit(1) 
    if '.' not in (ip_address := arguments[2]):
        print(f"Error! The 2nd argument must be a valid numerical IP address, such as 123.123.12.12, not {arguments[2]}")
        sys.exit(1)
    if arguments[3] != '-p':
        print(f"Error! The 3rd argument must be '-p', not {arguments[3]}")
        sys.exit(1) 
    if (port := is_integer(arguments[4])) < 1:
        print(f"Error! The value of the 4th argument must be greater than or equal to 1.")
        sys.exit(1) 


    return ip_address, port
