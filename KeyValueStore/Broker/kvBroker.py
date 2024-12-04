from KVBrokerManager import KVBrokerManager
import Config as Config
import sys


def main():

    # 1. parse configuration parameters from command-line arguments
    servers, data, k = Config.ConfigParser(sys.argv)

    # 2. initialize the KVBrokerManager with the parsed configuration
    kvBrokerManager = KVBrokerManager(servers, data, k)

    # 3. send the data to the servers
    kvBrokerManager.sendDataToServers()

    print("Indexing completed!")

    # 5. execute queries to retrieve or remove data from the servers
    kvBrokerManager.getDataFromServers()


if __name__ == "__main__":
    main()