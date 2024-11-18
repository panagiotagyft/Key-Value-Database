from KVDataGenerator import KVDataGenerator
import Config
import json
import sys


def main():

    keyType, n, d, l, m = Config.ConfigParser(sys.argv)

    kv_data_gen = KVDataGenerator(keyType, n, d, l, m)

    data = kv_data_gen.createData()
    
    data = '\n'.join(f'"{x}": {json.dumps(y).replace(",", ";")}' for x, y in data.items())
    
    with open("../Broker/KeyValueStore/dataToIndex.txt", "w") as file:
        sys.stdout = file
        print(data)
       
if __name__ == "__main__":
    main()