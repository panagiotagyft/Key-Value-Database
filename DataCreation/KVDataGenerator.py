import random
import string
import numpy as np


class KVDataGenerator:
  
    def __init__(self, keyType: dict, n: int, d: int, l:int, m:int):
        
        self.keyType=keyType
        self.n=n
        self.d=d
        self.l=l
        self.m=m

    def createData(self)->dict:
        """
        Creates top level keys and random data for them.
        """

        data = dict()
   
        for index in range(0, self.n):  
            recordKey = 'key' + str(index)   
            data[recordKey] = self.generateRandomlyData(0)   # generate data randomly

        return data
    
    def generateRandomlyData(self, depth: int) -> dict:
        """
        Generates a random dictionary with nested structures based on specified depth and key types.
        """
        
        # select a random number of keys between 0 and m
        max_keys = random.randint(0, self.m)
        selected_keys = set() # set to ensure unique keys

        # if no keys are selected, return an empty dictionary
        if max_keys == 0: return dict()
        
        # randomly choose keys from the available key types
        while len(selected_keys) < max_keys:
            selected_keys.add(random.choice(list(self.keyType.keys())))

        # generate the dictionary
        record = {
            key: (
                # recursively generate data if the maximum depth is not reached
                self.generateRandomlyData(depth+1)
                if depth < self.d and (np.random.choice([True, False])) # randomly decide if it should be nested
                else self.generate_value_by_type((self.keyType[key])) # otherwise, generate a value based on the key type
            )
            for key in selected_keys
        }
              
        return record
    
    
    def generate_value_by_type(self, key_type: str):
        """
        Generates a value based on the specified key type.
        """
        
        # Define a dictionary mapping key types to functions that generate corresponding values
        type_handlers = {
            "string": lambda: ''.join(np.random.choice(list(string.ascii_letters), self.l)),  # Generate a random string of length 'l'
            "int": lambda: np.random.randint(0, 101),  # Generate a random integer between 0 and 100
            "float": lambda: round(np.random.uniform(0, 100), 2),  # Generate a random float between 0 and 100, rounded to 2 decimal places
        }
        
        # Use the appropriate handler for the given key type or return None if the type is unknown
        return type_handlers.get(key_type, lambda: None)()

    
