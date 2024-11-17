import socket
import random

class KVBrokerManager:

    def __init__(self, servers: dict, data: list, k: int):

        self.servers = servers
        self.data = data
        self.k = k
    
    def sendDataToServers(self) -> bool:
        
        selected_servers = set()
      
        while len(selected_servers) < self.k:
            selected_servers.add(random.choice(list(self.servers.items())))
        print(f"{len(selected_servers)} < {self.k}")
        print(f"{selected_servers}")
        # for ip, port in self.servers:

        #     sck = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        #     sck.bind((ip, port))
        #     sck.listen()
        #     print(f"Server listening on {host}:{port}")
        #     while True:
        #         try:
        #             connection, address = sck.accept()
        #         except socket.error:
        #             print(f'Error! Failed to communicate with {ip} {port}.')
