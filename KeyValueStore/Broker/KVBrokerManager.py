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

        for record in self.data:

            for ip, port in selected_servers:

                try:
                    # socket(): sets up a communication channel	
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sck:
                
                        sck.connect((ip, port))
                        print(f"Socket {sck} connected successfully to {ip}:{port}!")

                        sck.sendall(('PUT ' + record).encode('utf-8'))
                        print("Data sent.")
                        
                        data = sck.recv(1024)
                        print("Received:", data.decode('utf-8'))
                
                except socket.error as e:
                    print(f"Error! Socket operation failed. Check network connection or server status: {e}")

                except Exception as e:
                    print(f"Error! An unexpected error occurred: {e}")
