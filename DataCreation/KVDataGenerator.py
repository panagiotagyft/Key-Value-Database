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

        data = dict()
   
        for index in range(0, self.n):  
            recordKey = 'key' + str(index)  
            data[recordKey] = self.generateRandomlyData(0)    
        
        return data
    
    def generateRandomlyData(self, depth: int) -> dict:
        """
        Generates a random dictionary with nested structures based on specified depth and key types.
        """

        max_keys = random.randint(0, self.m)
        selected_keys = set()

        if max_keys == 0: return dict()
      
        while len(selected_keys) < max_keys:
            selected_keys.add(random.choice(list(self.keyType.keys())))
        
        record = {
            key: (
                self.generateRandomlyData(depth+1)
                if depth < self.d and (value_is_nested:=np.random.choice([True, False]))
                else self.generate_value_by_type((type:=self.keyType[key]))
            )
            for key in selected_keys
        }
              
        return record
    
    
    def generate_value_by_type(self, key_type: str):
        
        type_handlers = {
            "string": lambda: ''.join(np.random.choice(list(string.ascii_letters), self.l)),
            "int": lambda: np.random.randint(0, 101),
            "float": lambda: round(np.random.uniform(0, 100), 2),
        }
        
        return type_handlers.get(key_type, lambda: None)()
    
