M111: Big Data Management
Key Value Database/Store
Winter Semester 2024–2025
Panagiota Gyftou - 7115112400025
------------------------------------------------

-- Compile & Run --

Compile and run the program:

- DataCreation

    python3 createData.py -k keyFile.txt -n <num-lines> -d <max-nesting> -l <max-keys> -m <max-str-length>

    - num-lines: Number of lines (data records) to generate.
    - max-nesting: Maximum nesting level for key-value sets.
    - max-keys: Maximum number of keys within each value.
    - max-str-length: Maximum string length for string-type values.
    - keyFile.txt: File with space-separated key names and their data types.

- KeyValueStore

    -- Broker
        
        python3 kvBroker.py -s serverFile.txt -idataToIndex.txt -k <replication-factor>

        - replication-factor: Replication factor, servers storing replicated data.

    -- Server

        python3  kvServer.py -a <ip_address> -p <port>


Run Examples:


- DataCreation Algorithm

    Data Generation `createData`:

        data = {}
        
        for each line i 
        {
            1. Create a top-level key key{i}.
            2. Generate data using `generateRandomlyData`.
            3. Add the key and its generated data to data.
        }
        
        return data.

    Generate data for key{i} `generateRandomlyData`:
        
        if the maximum depth d is reached or no keys are selected
        {
            return an empty structure -->> {}
        }
        else
        {
            1. Select a random max number of keys between 0 and m
            2. Choose random keys from the available dictionary keyType
            for each selected key
            {
                if the maximum nesting depth is not reached
                    generate nested data by recursively calling `generateRandomlyData`
                else
                    generate a value using `generate_value_by_type` based on the key's data type    
            }
        }

        return the generated dictionary


- Key Value Store Algorithm


    1. Broker initiates the connection with all the servers -->> `connectionToAllServers`:
        
        for each (ip, port) in servers
        {
            1. Create socket connection to (ip, port)
            2. Append connection to active connections list
        }
    

    2. Sending Data from Broker to Servers -->> `sendDataToServers`:

        for each record in data{
            selected_servers <<-- select k unique servers from active connections

            for each (connection, ip, port) in selected_servers
            {   
                1. Send "PUT <record>" to the server
                2. Receive response from the server
            }
        }


    3. Broker handles commands from user -->> `getDataFromServers`:

        do{

            command <<-- User Input
            if command == "EXIT"
            {
                close all active connections `closeConnections`
                break
            }

       
            for each (connection, ip, port) in active connections
            {
                1. Send command to server
                2. Receive response from server
                
                3. Print message
                if response == "Not Found!"
                    Print not found message
                else
                    Print server response
            }

        }while(1)
    

    4. Server processes broker requests -->> `receiveDataFromBroker`:
    
        do{
            Accept incoming connection
            
            do{

                1. Receive request from broker
                2. Determine request type (PUT, GET, DELETE, QUERY, Hello, Exit)
                3. Process request by type `processRequestByType`
                4. Send response back to broker

            }while(connection is active)

        }while(1)


        Command   |           Description           |  	Server Action
        ==========+=================================+=================================
        PUT	      |  Add key-value pair             |  Store data, respond with OK
        ----------+---------------------------------+---------------------------------
        GET	      |  Retrieve value for a key       |  Return value or Not Found!
        ----------+---------------------------------+---------------------------------
        DELETE    |  Remove a key-value pair        |  Delete key, respond with OK
        ----------+---------------------------------+---------------------------------
        QUERY	  |  Retrieve nested key-value pair |  Return nested data
        ----------+---------------------------------+----------------------------------

    Trie Structure:
    
        The structure includes `Nodes`, `Items`, and relationships between them.

        class Item:
            """
            Represents an individual key-value component in the Trie.
            """
            def __init__(self, value, is_leaf=False):
                self.value = value      # The key part (e.g., a character or word)
                self.is_leaf = is_leaf  # Indicates if this item is the end of a key
                self.children = None    # Points to a Node (subtree)

        class Node:
            """
            Represents a level in the Trie, containing multiple Items.
            """
            def __init__(self):
                self.items = []         # List of Item objects at this level

        class Trie:
            """
            The main Trie structure containing the root Node.
            """
            def __init__(self):
                self.root = Node()      # Root node of the Trie


    Trie Operations:

    1. Insert (PUT) -->> `insert`:
        1. Traverse or create nodes for each character of the key.
        2. At the leaf node, insert the associated value (payload).
        3. For nested structures, recursively insert child keys and values.
    
    2. Top-level key retrieval (GET) -->> `getKey`:
        1. Traverse nodes corresponding to the key characters.
        2. If the key exists, return the subtree; otherwise, return "Not Found!"

    3. Delete operation (DELETE) -->> `delete`:
        1. Traverse to the last character node of the key.
        2. Recursively delete the subtree from this node.
        3. Remove the key node from its parent.
    
    4. Query operation (QUERY) -->> `getValueByKey`:
        1. Split the key into top-level and subkeys.
        2. Traverse to the top-level key node, then recursively traverse subkeys.
        3. Return the associated value or subtree.