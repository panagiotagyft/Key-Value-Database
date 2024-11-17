import random
import string

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
      
        max_keys = random.randint(0, self.m)
        selected_keys = set()

        if max_keys == 0: return dict()
      
        while len(selected_keys) < max_keys:
            selected_keys.add(random.choice(list(self.keyType.keys())))
        
        record = dict()
        for key in selected_keys:
            
            value_is_nested = random.randint(0,1)
            if depth < self.d and value_is_nested == 1:
                value = self.generateRandomlyData(depth+1)
            else:
                type=self.keyType[key]
                
                if type == 'string':
                    value = ''.join(random.choice(string.ascii_letters) for _ in range(self.l))
                elif type == 'int':
                    value = random.randint(0, 100)
                elif type == 'float':
                    value = random.random()
            
            record[key] = value
        
        return record
                   