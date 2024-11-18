import socket
import random

class KVServerManager:

    def __init__(self, ip_address: str, port: int):

        self.ip_address = ip_address
        self.port = port

    def receiveDataFromClients(self):
        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sck:

            sck.bind((self.ip_address, self.port))
            sck.listen()
            print(f"Server is listening on {self.ip_address}:{self.port}")
            print(f"Server is up and running. Waiting for incoming connections...")
            
            while True:
                try:
                    connection, address = sck.accept()
                    
                    data = connection.recv(1024)
                
                    if not data: continue 
                    
                    request = data.decode(('utf-8'))
                    print(f"Received a request from client {self.ip_address}:{self.port} -> {request}")

                    self.processClientRequest(request)
                
                except socket.error:
                    print(f'Error! Failed to communicate with {self.ip_address}:{self.port}.')
                    

    def processClientRequest(self, request: str) -> str:

        request_type = request.split(" ")[0]
        space_index = request.find(" ")
        data = request[space_index+1:]
        return self.processRequestByType(request_type, data)


    def processRequestByType(self, request_type: str, data: str):
        
        request_type_handlers = {
            "PUT": lambda: self.PUT(data)
            # "GET": lambda:
            # "DELETE": lambda: 
            # "QUERY": lambda:
        }
        
        return request_type_handlers.get(request_type, lambda: None)()
    
    def PUT(self, data: str) -> str:

        