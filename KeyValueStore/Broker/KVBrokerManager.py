import socket
import random

class KVBrokerManager:

    def __init__(self, servers: list, data: list, k: int, selected_servers=set()):

        self.servers = servers
        self.data = data
        self.k = k
        self.selected_servers = selected_servers

  
    def sendDataToServers(self) -> bool:
        
         
        while len(self.selected_servers) < self.k:
            self.selected_servers.add(random.choice(list(self.servers)))
        print(self.selected_servers)


        for ip, port in self.selected_servers:
             for record in self.data:
                try:
                    # socket(): sets up a communication channel	
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sck:
                
                        sck.connect((ip, port))
                        print(f"Socket connected successfully to {ip}:{port}!")

                        sck.sendall(('PUT ' + record).encode('utf-8'))
                        print("Data sent.")
                        
                        data = sck.recv(1024)
                        print(f"Received from {ip}:{port}:", data.decode('utf-8'))
 
                
                except socket.error as e:
                    print(f"Error! Socket operation failed. Check network connection or server status: {e}")

                except Exception as e:
                    print(f"Error! An unexpected error occurred: {e}")


    def getDataFromServers(self):

        print("Indexing completed!! Enter one of the following commands:")
        print("GET <key> - Retrieve the value for a specific key")
        print("EXIT - Terminate the broker")

        while True:

            try:
                command = input("Enter command: ").strip()

                if not command: continue

                if command == "Exit": break

                for ip, port in self.selected_servers:
                    for record in self.data:
                        try:
                            # socket(): sets up a communication channel	
                            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sck:
                        
                                sck.connect((ip, port))
                                print(f"Socket connected successfully to {ip}:{port}!")

                                sck.sendall((command).encode('utf-8'))
                                print("Data sent.")
                                
                                data = sck.recv(1024)
                                print(f"Received from {ip}:{port}:", data.decode('utf-8'))
        
                        
                        except socket.error as e:
                            print(f"Error! Socket operation failed. Check network connection or server status: {e}")

                        except Exception as e:
                            print(f"Error! An unexpected error occurred: {e}")

            except KeyboardInterrupt:
                print("\nTerminating broker...")
                break