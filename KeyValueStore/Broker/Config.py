
import sys

def is_integer(argument: str) -> int:
    try:
        value = int(argument)
        return value
    except ValueError:
        print(f"Error! The argument {argument} is not a valid integer.")

def ConfigParser(arguments):

    if len(arguments) < 7:
        print("Arguments are missing, there must be a total of 6!")
        sys.exit(1) 
    if len(arguments) > 7:
        print("Many arguments, there must be a total of 6!")
        sys.exit(1) 
     
    if arguments[1] != '-s':
        print(f"Error! The 1st argument must be '-s', not {arguments[1]}")
        sys.exit(1) 
    if (serverFile := arguments[2]) != 'serverFile.txt':
        print(f"Error! The 2nd argument must be 'serverFile.txt', not {arguments[2]}")
        sys.exit(1) 
    if arguments[3] != '-i':
        print(f"Error! The 3rd argument must be '-i', not {arguments[3]}")
        sys.exit(1) 
    if (dataFile := arguments[4]) != 'dataToIndex.txt':
        print(f"Error! The 4th argument must be 'dataToIndex.txt', not {arguments[4]}")
        sys.exit(1)
    if arguments[5] != '-k':
        print(f"Error! The 5th argument must be '-k', not {arguments[5]}")
        sys.exit(1)

    File = open(serverFile, "r")

    servers = dict()
    for line in File:
        auxiliaryList = line.split()      
        servers[auxiliaryList[0]] = int(auxiliaryList[1])
       
    k = is_integer(arguments[6])       
    if k < 1 or k>len(servers):
        print('''Error! The value of the 6th argument must be greater than or equal to 1 or 
                less than or equal to the number of servers''')
        sys.exit(1)
   
    File = open(dataFile, "r")
    data = [line for line in File]

    return servers, data, k
