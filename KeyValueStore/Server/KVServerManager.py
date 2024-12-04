import socket
from Trie.Trie import Trie

class KVServerManager:

    def __init__(self, ip_address: str, port: int):

        self.ip_address = ip_address
        self.port = port
        self.trie = Trie()

    def receiveDataFromBroker(self):
        """
        Listens for incoming connections from the broker, processes requests, and sends responses.
        """
        try:
            # create a socket using IPv4 addressing and TCP protocol
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sck:
                    
                # bind the socket to the specified IP address and port
                sck.bind((self.ip_address, self.port))
                
                # start listening for incoming connections
                sck.listen()
                print(f"Server is listening on {self.ip_address}:{self.port}")
                print(f"Server is up and running. Waiting for incoming connections...")
                    
                while True:
                        connection, address = sck.accept()
                        try:
                            print(f"Connected by {address}")
                            data = connection.recv(1024)
                            if not data:
                                continue
                            
                            request = data.decode('utf-8')
                            
                            print(f"Received request: {request}")
                            
                            response = self.processBrokerRequest(request)
                            connection.sendall(response.encode('utf-8'))
                        
                        except socket.error as e:
                            print(f"Error! Failed to communicate with {address}: {e}")
                        except Exception as e:
                            print(f"Error! handling request from {address}: {e}")
                        finally:
                            connection.close()
                        
        except KeyboardInterrupt:
            print("Shutting down server...")
        except Exception as e:
            print(f"Unexpected error: {e}")
        finally:
            print("Server terminated.")


                    

    def processBrokerRequest(self, request: str) -> str:
        
        # extract the request type 
        request_type = request.split(" ")[0]
        space_index = request.find(" ")
        data = request[space_index+1:]

        # delegate the processing based on the request type and return the result
        return self.processRequestByType(request_type, data)
        

    def processRequestByType(self, request_type: str, data: str) -> str:
        
        request_type_handlers = {
            "PUT": lambda: self.PUT(data),
            "GET": lambda: self.GET(data),
            "DELETE": lambda: self.DELETE(data),
            "QUERY": lambda: self.QUERY(data)
        }
        
        return request_type_handlers.get(request_type, lambda: None)()
    
    def PUT(self, data: str) -> str:
        topLevelKey_payload = data.split(": ", 1)
        status = self.trie.insert(topLevelKey_payload)
        if status == True: return "OK"
        
        return "Error!!!"
    
    def GET(self, data: str) -> str:
        mess = self.trie.getKey(data)
        return mess
        
    def DELETE(self, data: str) -> str:
        mess = self.trie.delete(data)
        return mess

    def QUERY(self, data: str) -> str:
        mess = self.trie.getValueByKey(data)
        return mess

        