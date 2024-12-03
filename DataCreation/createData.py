from KVDataGenerator import KVDataGenerator
import Config
import json
import sys


def main():

    # 1. parse configuration parameters from command-line arguments
    keyType, n, d, l, m = Config.ConfigParser(sys.argv)

    # 2. initialize the KVDataGenerator with the parsed configuration
    kv_data_gen = KVDataGenerator(keyType, n, d, l, m)

    # 3. generate the data 
    data = kv_data_gen.createData()
    
    # convert the data to a string format with custom formatting:
    # replace ',' with ';' in the JSON representation of the values
    data = '\n'.join(f'"{x}": {json.dumps(y).replace(",", ";")}' for x, y in data.items())
    
    # write the formatted data to a file
    with open("../Broker/KeyValueStore/dataToIndex.txt", "w") as file:
        sys.stdout = file
        print(data)
       
if __name__ == "__main__":
    main()