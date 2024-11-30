import json

class Node:
    def __init__(self):
        self.items = []

    def getItems(self) -> list:
        return self.items

    def getItem(self, index: int):
        return self.items[index]
    
    def addItem(self, entry: str):
        item = Item(entry)
        self.items.append(item)
        return item
    
    def elementExists(self, entry: str):
        for index in range(len(self.items)):
            item = self.getItem(index)
            if item.getParent() == entry:  # Σύγκριση απευθείας με το `getParent`
                return item
        return -1

    
    def getChildren(self, item):
        return item.getChildren()

class Item:
    def __init__(self, parent=''):
        self.parent = parent
        self.children = Node()
    
    def getParent(self) -> str:
        return self.parent
    
    def getChildren(self) -> Node:
        return self.children   

    def parentExists(self, entry: str) -> bool:
        if entry == self.parent: return True
        return False    
    

class Trie:

    def __init__(self):
        self.root = Node()


    def insert(self, entry: str) -> bool:
       
        current_node = self.root

        # Add the top-level key to the root (top_level_key:=entry[0]).
        # Διασπά τα κλειδιά σε γράμματα
        top_level_key = entry[0]
        key_parts = list(top_level_key)  # ['k', 'e', 'y', '0']
        key_parts.pop(0)
        key_parts.pop(len(key_parts)-1)
        print(key_parts)
        for char in key_parts:
           
            if ( existing_item := current_node.elementExists(char)) == -1:
                item = current_node.addItem(char)
                current_node = item.getChildren()
            else:
                current_node = existing_item.getChildren()

        payload = (payload:=entry[1]).replace(";", ",")
        payload = json.loads(payload)

        return self.recursive_insertion( item.getChildren(), payload )
            
    
    def recursive_insertion(self, node, payload) -> bool:
        
        # If the payload is not a dictionary, it means we have reached a value, i.e., we have reached a leaf.
        if not isinstance(payload, dict):
            node.addItem(payload)
            return True 
        
        for key in payload.keys():
            item = node.addItem(key)
            self.recursive_insertion( item.getChildren(), payload[key] )


    def display(self, node=None, level=0, prefix=""):
        if node is None:
            node = self.root

        for item in node.getItems():
            # Δημιουργία εσοχής για ευκρίνεια
            indent = ' ' * (level * 2)
            # Εκτύπωση του τρέχοντος κόμβου
            print(f"{indent}{prefix}{item.getParent()}")

            # Επανάληψη για τα παιδιά του κόμβου
            self.display(item.getChildren(), level + 1, prefix="|-- ")


        

        
