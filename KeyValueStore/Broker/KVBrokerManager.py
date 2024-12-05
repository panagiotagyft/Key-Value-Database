import socket
import random
import sys

class KVBrokerManager:

    def __init__(self, servers: list, data: list, k: int):

        self.servers = servers
        self.data = data
        self.k = k

        self.connections = list()

    def connectionToAllServers(self):
        """
        Initiates the connection with all the servers and stores the connection between them.
        """

        for ip, port in self.servers:
            try:
                # socket(): sets up a communication channel	
                sck = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sck.connect((ip, port))
                print(f"Socket connected successfully to {ip}:{port}!")
                self.connections.append((sck, ip, port))
            
            except Exception as e:
                print(f"Error! Socket operation failed. Check network connection or server status: {e}")
    

    def closeConnections(self):
        """
        Closes all active connections.
        """
        for sck, ip, port in self.connections:
            try:
                sck.sendall("Exit".encode('utf-8'))
                sck.close()
                print(f"Closed connection to {ip}:{port}")
            except Exception as e:
                print(f"Error closing connection to {ip}:{port}: {e}")
        self.connections = []


    def sendDataToServers(self) -> bool:
        """ 
        Selects -k- unique servers and inserts the replicated data into them. 
        """
        
        try:
            for record in self.data:

                # 1. randomly select -k- unique servers for replication
                selected_servers = set()
                while len(selected_servers) < self.k:
                    selected_servers.add(random.choice(list(self.connections)))
                    
                # 2. send data to selected server
                for connection, ip, port in selected_servers:
                    
                        try:
                            connection.sendall(('PUT ' + record).encode('utf-8'))
                            # print("Data sent.")
                                    
                            data = connection.recv(1024)
                            # print(f"Received from {ip}:{port}:", data.decode('utf-8'))
            
                        except Exception as e:
                            print(f"Unexpected error with {ip}:{port}. Closing connection: {e}")
                            connection.close()
                            self.connections.remove((connection, ip, port))  
                            break 
                        

        except KeyboardInterrupt:
            self.closeConnectionst()
            sys.exit(0) 

        return True
        

    def checkActiveServers(self, type) -> bool:
        """
        Checks the availability of active servers and ensures sufficient resources
        are available to process the given request type.

        Parameters:
        -----------
        type : str
            The type of request to check for. Supported types are:
            - "GET": Ensures at least `k` servers are operational.
            - "DELETE": Requires all servers to be operational.
            - "QUERY": Ensures at least `k` servers are operational.
            - "CHECK": Requires all servers to be operational.

        Returns:
        --------
        bool
            - True if the required number of servers are active for the request type.
            - False if the required conditions are not met, accompanied by an appropriate warning.        
        """
        for connection, ip, port in self.connections:
            try:
                connection.sendall("Hello".encode('utf-8'))
                # Ρυθμίζουμε ένα μικρό timeout για την απάντηση
                connection.settimeout(2)
                response = connection.recv(1024)

                if response.decode('utf-8') != "World":
                    raise Exception("Invalid response")
                
            except Exception as e:
                self.connections.remove((connection, ip, port))  # Remove it from active connections
        
        active_servers = len(self.connections)

       
        def handle_get_query():
            if active_servers < self.k:
                print(f"Warning: {self.k} or more servers are down, so we cannot guarantee accurate results.")
                return False

        def handle_delete():
            if active_servers != 3:
                print("Warning: The deletion cannot be performed because the servers are unable to support this process as not all of them are operational.")
                return False

        def handle_check():
            if active_servers == 0:
                print("Warning: All servers are down; we will be forced to terminate the program.")
                return False

        request_type_handlers = {
            "GET": handle_get_query,
            "DELETE": handle_delete,
            "QUERY": handle_get_query,
            "CHECK": handle_check
        }

        # Get and execute the handler for the given type
        return request_type_handlers.get(type, lambda: True)()


    def getDataFromServers(self):
        """
        Requests data from the servers based on user commands.

        Supported commands: GET, DELETE, QUERY, EXIT
        """

        try:
            print("Enter one of the following commands:")
            print("GET <key> - Retrieve the value for a specific top-level-key")
            print("DELETE <key> - Delete a specific top-level-key")
            print("QUERY <keypath> - Retrieve the value for a specific subkey")
            print("EXIT - Terminate the process\n")

            while True:

                # read user input and strip extra spaces
                command = input("Enter command: ").strip()

                if not command: continue
                
                # split command into parts (action and data, if applicable)
                command_parts = command.split(" ", 1)

                # validate command format
                if command_parts[0] not in ["EXIT", "GET", "DELETE", "QUERY"]:
                    print("Invalid command. Please try again.")
                    print("Supported commands: EXIT, GET, DELETE, QUERY")
                    continue

                if command_parts[0] != "EXIT" and len(command_parts) != 2:
                    print("Invalid command. Please try again.")
                    print("Supported commands: EXIT, GET <key>, DELETE <key>, QUERY <keypath>")
                    continue

                if self.checkActiveServers("CHECK") == False:
                    self.closeConnections()
                    break
                
                # check active servers before processing commands
                status = True
                if command_parts[0] == "GET":      status = self.checkActiveServers("GET")
                elif command_parts[0] == "DELETE": status = self.checkActiveServers("DELETE")
                elif command_parts[0] == "QUERY":  status = self.checkActiveServers("QUERY")

                if status == False:
                    self.closeConnections()
                    break

                if command == "EXIT": 
                    self.closeConnections()
                    break
                
                flag = True
                for connection, ip, port in self.connections:
        
                    try:     
                        connection.sendall((command).encode('utf-8'))
                                  
                        data = connection.recv(1024)
                        mess = data.decode('utf-8')

                        if mess == "OK":
                            flag = False
                            continue
                        
                        if mess != "Not Found!":
                            flag = False
                            print(f"{command_parts[1]}:", mess)
                            break
            
                    except Exception as e:
                        print(f"Unexpected error with {ip}:{port}. Closing connection: {e}")
                        connection.close()
                        self.connections.remove((connection, ip, port))  
                        break  
                
                # print Not Found!
                if flag == True:  print(f"{command_parts[1]}:", mess)

        except KeyboardInterrupt:
            self.closeConnections()
            sys.exit(0)
