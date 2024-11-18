from KeyValueStore.Broker.KVBrokerManager import KVBrokerManager
import KeyValueStore.Broker.Config as Config
import sys


def main():

    servers, data, k = Config.ConfigParser(sys.argv)

    kvBrokerManager = KVBrokerManager(servers, data, k)

    kvBrokerManager.sendDataToServers()


if __name__ == "__main__":
    main()