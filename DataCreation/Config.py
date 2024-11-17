
import sys

def is_integer(argument: str) -> int:
    try:
        value = int(argument)
        return value
    except ValueError:
        print(f"Error! The argument {argument} is not a valid integer.")

def ConfigParser(arguments):

    if len(arguments) < 12:
        print("Arguments are missing, there must be a total of 11!")
        sys.exit(1) 
    if len(arguments) > 12:
        print("Many arguments, there must be a total of 11!")
        sys.exit(1) 
    
    if arguments[1] != 'createData':
        print(f"Error! The 1st argument must be 'createData', not {arguments[1]}")
        sys.exit(1) 
    if arguments[2] != '-k':
        print(f"Error! The 2nd argument must be '-k', not {arguments[2]}")
        sys.exit(1) 
    if (keyFile := arguments[3]) != 'keyFile.txt':
        print(f"Error! The 3rd argument must be 'keyFile.txt', not {arguments[3]}")
        sys.exit(1) 
    if arguments[4] != '-n':
        print(f"Error! The 4th argument must be '-n', not {arguments[4]}")
        sys.exit(1) 
    if (n := is_integer(arguments[5])) < 1:
        print(f"Error! The value of the 5th argument must be greater than or equal to 1.")
        sys.exit(1)
    if arguments[6] != '-d':
        print(f"Error! The 6th argument must be '-d', not {arguments[6]}")
        sys.exit(1)        
    if (d := is_integer(arguments[7])) < 0:
        print(f"Error! The value of the 7th argument must be greater than or equal to 0.")
        sys.exit(1)
    if arguments[8] != '-l':
        print(f"Error! The 8th argument must be '-l', not {arguments[8]}")
        sys.exit(1)        
    if (l := is_integer(arguments[9])) < 1:
        print(f"Error! The value of the 9th argument must be greater than or equal to 1.")
        sys.exit(1)
    if arguments[10] != '-m':
        print(f"Error! The 10th argument must be '-m', not {arguments[10]}")
        sys.exit(1)        
    if (m := is_integer(arguments[11])) < 0:
        print(f"Error! The value of the 11th argument must be greater than or equal to 0.")
        sys.exit(1)

    File = open(keyFile, "r")

    keyType = dict()
    for line in File:
        auxiliaryList = line.split()
        keyType[auxiliaryList[0]] = auxiliaryList[1]
       
    return keyType, n, d, l, m
