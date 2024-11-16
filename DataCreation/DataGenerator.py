import KVDataGenerator
import Config
import sys

def main():
    
    keyType,n,d,l,m = Config.ConfigParser(sys.argv)

    kv_data_gen = KVDataGenerator(keyType,n,d,l,m)

    kv_data_gen.createData()
       
if __name__ == "__main__":
    main()
