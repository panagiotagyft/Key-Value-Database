from KeyValueStore.Server.KVServerManager import KVServerManager
import KeyValueStore.Server.Config as Config
import sys


def main():

    ip_address, port = Config.ConfigParser(sys.argv)

    kvServerManager = KVServerManager(ip_address, port)

    kvServerManager.receiveDataFromClients()


if __name__ == "__main__":
    main()