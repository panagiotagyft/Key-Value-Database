import socket
from Trie.Trie import Trie
import sys

class KVServerManager:

    def __init__(self, ip_address: str, port: int, sck=None):

        self.ip_address = ip_address
        self.port = port
        self.trie = Trie()
        self.socket = sck

    def receiveDataFromBroker(self):
        """
        Listens for incoming connections from the broker, processes requests, and sends responses.
        """
        try:
            # create a socket using IPv4 addressing and TCP protocol
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sck:
                
                # Keep the connection alive.
                sck.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  
                
                # bind the socket to the specified IP address and port
                sck.bind((self.ip_address, self.port))
                    
                # start listening for incoming connections
                sck.listen()
                print(f"Server is listening on {self.ip_address}:{self.port}")
                print(f"Server is up and running. Waiting for incoming connections...")
                
                connection, address = sck.accept()

                self.socket = sck  # for closing the socket when the user types EXIT.
                
                while True:
    
                    try:
                        print(f"Connected by {address}")
                        data = connection.recv(4098)

                        if not data:
                            continue
                                
                        request = data.decode('utf-8')
                                
                        print(f"Received request: {request}")
                            
                        response = self.processBrokerRequest(request)
                        print(response)
                        connection.sendall(response.encode('utf-8'))
                        
                    except socket.error as e:
                        print(f"Error! Failed to communicate with  {address}: {e}")
                        if connection: connection.close()
                        sys.exit(1)
                        
                    except Exception as e:
                        print(f"Unexpected error: {e}")
                        if connection: connection.close()
                        sys.exit(0)
                                    
        except KeyboardInterrupt:
            print("\nShutting down server...")
        except Exception as e:
            print(f"Unexpected error: {e}")
        finally:
            if sck:
                print("Closing server socket.")
                sck.close()
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
            "QUERY": lambda: self.QUERY(data),
            "Hello": lambda: "World",
            "Exit": lambda: self.Exit()
        }
        
        return request_type_handlers.get(request_type, lambda: None)()
    
    def PUT(self, data: str) -> str:
        topLevelKey_payload = data.split(": ", 1)
        status = self.trie.insert(topLevelKey_payload)
        if status == True: return "OK"
        
        return "Error!"
    
    def GET(self, data: str) -> str:
        mess = self.trie.getKey(data)
        return mess
        
    def DELETE(self, data: str) -> str:
        mess = self.trie.delete(data)
        return mess

    def QUERY(self, data: str) -> str:
        mess = self.trie.getValueByKey(data)
        return mess
    
    def Exit(self):
        print("Exiting...")
        if self.socket:
            self.socket.close()
        sys.exit(0)
        