from .Node import Node
import json

class Trie:

    payload = ""

    def __init__(self):
        # Initialize the root of the Trie as an instance of the Node class
        self.root = Node()

    def insert(self, entry: str) -> bool:
        """
        Inserts a key-value entry into the Trie.

        Parameters:
        ----------
        entry : str
            The key-value pair to insert into the Trie.

        Returns:
        -------
        bool
            True if the insertion was successful.
        """

        try:
            current_node = self.root

            # parse the top-level key and prepare it for insertion
            top_level_key = entry[0]
            key_parts = list(top_level_key)  
            
            # remove the opening and closing characters -->> ""
            key_parts.pop(0)  
            key_parts.pop(len(key_parts) - 1) 

            # traverse or create the path in the Trie for the key
            for char in key_parts:
                if (existing_item := current_node.elementExists(char)) == -1:
                    item = current_node.addItem(char)
                    current_node = item.getChildren()
                else:
                    item = existing_item
                    current_node = existing_item.getChildren()

            # parse and store the payload
            payload = (payload := entry[1]).replace(";", ",")  # replace separators
            payload = json.loads(payload)  # convert to JSON object

            # recursively insert the payload into the Trie
            self.recursive_insertion(item.getChildren(), payload)

            return True
        
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return False

    def recursive_insertion(self, node, payload):
        """
        Recursively inserts a payload into the Trie.

        Parameters:
        ----------
        node : Node
            The current node where the payload is being inserted.
        payload : dict or value
            The data to insert into the Trie.
        """
        
        # if the payload is a leaf value (not a dictionary), add it directly
        if not isinstance(payload, dict):
            node.addItem(payload, True)
            return 

        # traverse the dictionary and insert each key-value pair recursively
        for key in payload.keys():
            item = node.addItem(key)
            self.recursive_insertion(item.getChildren(), payload[key])

    def getKey(self, top_level_key):
        """
        Retrieves the value associated with a top-level key.

        Parameters:
        ----------
        top_level_key : str
            The key to search for in the Trie.

        Returns:
        -------
        tuple:
            A tuple containing a success flag and the retrieved value or error message.
        """
        current_node = self.root

        # traverse the Trie to find the key
        for char in top_level_key:
            if (existing_item := current_node.elementExists(char)) == -1:
                return "Not Found!"

            current_node = existing_item.getChildren()

        # return the string representation of the node's children
        return self.nodeTraversalToString(current_node)

    def nodeTraversalToString(self, current_node=None):
        """
        Converts the subtree of a node to a string representation.

        Parameters:
        ----------
        current_node : Node, optional
            The starting node for traversal.

        Returns:
        -------
        str
            A string representation of the node and its children.
        """
        if current_node is None:
            current_node = self.root

        print("-----------------------")
        flag = False
        result = "{"

        # iterate through the node's items
        for i, item in enumerate(items := current_node.getItems()):
            
            # if it's a leaf, add its value
            if item.getIsLeaf():  
                result = f'"{item.getValue()}"'
                flag = True
            else:  # otherwise, recurse into its children
                result += f'"{item.getValue()}": {self.nodeTraversalToString(item.getChildren())}'

            # add separators for values
            if i < len(items) - 1:
                result += "; "

        if not flag:
            result += "}"

        return result

    def getValueByKey(self, subkey):
        """
        Retrieves the value associated with a subkey (e.g., `key1.subkey`).

        Parameters:
        ----------
        subkey : str
            The full path of the key, including subkeys.

        Returns:
        -------
        tuple:
            A tuple containing a success flag and the retrieved value or error message.
        """
        current_node = self.root

        # split the subkey into parts for traversal
        subkey = subkey.split(".")
        top_level_key = subkey[0]
        subkeys = subkey[1:]

        # traverse the top-level key
        for char in top_level_key:
            if (existing_item := current_node.elementExists(char)) == -1:
                return "Not Found!"
            current_node = existing_item.getChildren()

        # traverse the subkeys
        for subkey in subkeys:
            if (existing_item := current_node.elementExists(subkey)) == -1:
                return "Not Found!"
            current_node = existing_item.getChildren()

        # return the string representation of the node's children
        return self.nodeTraversalToString(current_node)

    def display(self, node=None, level=0, prefix=""):
        """
        Displays the Trie structure in a readable format.

        Parameters:
        ----------
        node : Node, optional
            The current node to display.
        level : int, optional
            The current depth level for indentation.
        prefix : str, optional
            A prefix for formatting the display.
        """
        if node is None:
            node = self.root

        # Display all items in the node
        for item in node.getItems():
            indent = ' ' * (level * 2)  # Create indentation
            print(f"{indent}{prefix}{item.getValue()}")
            self.display(item.getChildren(), level + 1, prefix="|-- ")

    def delete(self, top_level_key):
        """
        Deletes a top-level key and its associated subtree from the Trie.

        Parameters:
        ----------
        top_level_key : str
            The key to delete.

        Returns:
        -------
        tuple:
            A tuple containing a success flag and a message.
        """
        current_node = self.root

        # traverse to the key
        for char in top_level_key:
            if (existing_item := current_node.elementExists(char)) == -1:
                return "Not Found!"
            previous_node = current_node
            current_node = existing_item.getChildren()

        # recursively delete the key's subtree
        self.recursive_delete(current_node)
        previous_node.removeItem(existing_item.getValue())
        return "OK"

    def recursive_delete(self, current_node):
        """
        Recursively deletes all items in a subtree.

        Parameters:
        ----------
        current_node : Node
            The root of the subtree to delete.
        """
        for item in current_node.getItems():
            self.recursive_delete(item.getChildren())

        current_node.removeItems()
        del current_node
