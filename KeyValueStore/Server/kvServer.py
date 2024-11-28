from KVServerManager import KVServerManager
import Config
import sys


def main():

    ip_address, port = Config.ConfigParser(sys.argv)

    kvServerManager = KVServerManager(ip_address, port)

    kvServerManager.receiveDataFromClients()


if __name__ == "__main__":
    main()