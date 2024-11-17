
import sys

def is_integer(argument: str) -> int:
    try:
        value = int(argument)
        return value
    except ValueError:
        print(f"Error! The argument {argument} is not a valid integer.")

def ConfigParser(arguments):

    if len(arguments) < 11:
        print("Arguments are missing, there must be a total of 10!")
        sys.exit(1) 
    if len(arguments) > 11:
        print("Many arguments, there must be a total of 10!")
        sys.exit(1) 
     
    if arguments[1] != '-k':
        print(f"Error! The 1st argument must be '-k', not {arguments[1]}")
        sys.exit(1) 
    if (keyFile := arguments[2]) != 'keyFile.txt':
        print(f"Error! The 2nd argument must be 'keyFile.txt', not {arguments[2]}")
        sys.exit(1) 
    if arguments[3] != '-n':
        print(f"Error! The 3rd argument must be '-n', not {arguments[3]}")
        sys.exit(1) 
    if (n := is_integer(arguments[4])) < 1:
        print(f"Error! The value of the 4th argument must be greater than or equal to 1.")
        sys.exit(1)
    if arguments[5] != '-d':
        print(f"Error! The 5th argument must be '-d', not {arguments[5]}")
        sys.exit(1)        
    if (d := is_integer(arguments[6])) < 0:
        print(f"Error! The value of the 6th argument must be greater than or equal to 0.")
        sys.exit(1)
    if arguments[7] != '-l':
        print(f"Error! The 7th argument must be '-l', not {arguments[7]}")
        sys.exit(1)        
    if (l := is_integer(arguments[8])) < 1:
        print(f"Error! The value of the 8th argument must be greater than or equal to 1.")
        sys.exit(1)
    if arguments[9] != '-m':
        print(f"Error! The 9th argument must be '-m', not {arguments[9]}")
        sys.exit(1)        
    if (m := is_integer(arguments[10])) < 0:
        print(f"Error! The value of the 10th argument must be greater than or equal to 0.")
        sys.exit(1)

    File = open(keyFile, "r")

    keyType = dict()
    for line in File:
        auxiliaryList = line.split()
        keyType[auxiliaryList[0]] = auxiliaryList[1]
       
    return keyType, n, d, l, m
