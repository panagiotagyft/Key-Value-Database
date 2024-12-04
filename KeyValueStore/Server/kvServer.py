from KVServerManager import KVServerManager
import Config
import sys


def main():

    # 1. parse configuration parameters from command-line arguments
    ip_address, port = Config.ConfigParser(sys.argv)

    # 2. initialize the KVServerManager with the parsed configuration
    kvServerManager = KVServerManager(ip_address, port)

    # 3. receive  data from the broker
    kvServerManager.receiveDataFromBroker()


if __name__ == "__main__":
    main()