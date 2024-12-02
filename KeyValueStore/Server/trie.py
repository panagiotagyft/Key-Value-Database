import json

class Node:
    def __init__(self):
        self.items = []

    def getItems(self) -> list:
        return self.items

    def getItem(self, index: int):
        return self.items[index]
    
    def addItem(self, entry: str, is_leaf=False):
        item = Item(entry, is_leaf)
        self.items.append(item)
        return item
    
    def elementExists(self, entry: str):
        for index in range(len(self.items)):
            item = self.getItem(index)
            if item.getValue() == entry:  # Σύγκριση απευθείας με το `getValue`
                return item
        return -1
    
    def getChildren(self, item):
        return item.getChildren()
    
    def removeItem(self, element):
        for index in range(len(self.items)):
            item = self.getItem(index)
            if item.getValue() == element:
                del self.items[index]    
                
    def removeItems(self):
        while self.items:
            del self.items[0]


class Item:
    def __init__(self, value='', is_leaf=False):
        self.value = value
        self.children = Node()
        self.is_leaf = is_leaf
    
    def getValue(self) -> str:
        return self.value
    
    def getIsLeaf(self) -> bool:
        return self.is_leaf
    
    def getChildren(self) -> Node:
        return self.children   

    def valueExists(self, entry: str) -> bool:
        if entry == self.value: return True
        return False 
  
    

class Trie:

    payload = ""

    def __init__(self):
        self.root = Node()


    def insert(self, entry: str) -> bool:
       
        current_node = self.root

        # Add the top-level key to the root (top_level_key:=entry[0]).
        # Διασπά τα κλειδιά σε γράμματα
        print(entry)
        top_level_key = entry[0]
        key_parts = list(top_level_key)  # ['k', 'e', 'y', '0']
        # key_parts.pop(0)
        # key_parts.pop(len(key_parts)-1)
        print(key_parts)
        for char in key_parts:
           
            if ( existing_item := current_node.elementExists(char)) == -1:
                item = current_node.addItem(char)
                current_node = item.getChildren()
            else:
                item = existing_item
                current_node = existing_item.getChildren()

        payload = (payload:=entry[1]).replace(";", ",")
        payload = json.loads(payload)

        self.recursive_insertion( item.getChildren(), payload )

        return True
            
    
    def recursive_insertion(self, node, payload) -> bool:
        
        # If the payload is not a dictionary, it means we have reached a value, i.e., we have reached a leaf.
        if not isinstance(payload, dict):
            node.addItem(payload, True)
            return True 
        
        for key in payload.keys():
            item = node.addItem(key)
            self.recursive_insertion( item.getChildren(), payload[key] )

    
    def getKey(self, top_level_key):

        current_node = self.root

        for char in top_level_key:

            if (existing_item := current_node.elementExists(char)) == -1:
                return (False, "Not Found!")
            
            current_node = existing_item.getChildren()


        # print(self.traverse(current_node))
        return (True, self.traverse(current_node))

    def traverse(self, current_node=None):
        
        if current_node is None: current_node = self.root
        print("-----------------------")
        flag = False; result = "{"
        
        for i, item in enumerate(items:=current_node.getItems()):
            print(item.getValue())

            if item.getIsLeaf():  # Αν είναι φύλλο, εμφανίζει την τιμή του
                result = f'"{item.getValue()}"'
                flag = True
                
            else:  # Διαφορετικά, συνεχίζει αναδρομικά
                
                result += f'"{item.getValue()}": {self.traverse(item.getChildren())}'

            if i < len(items) - 1:  # Προσθήκη ';' αν δεν είναι το τελευταίο στοιχείο
                result += "; "
        
        if flag is False: result += "}"
        
        return result

    def get(self, subkey):

        current_node = self.root

        subkey = subkey.split(".")
        top_level_key = subkey[0]; subkeys = subkey[1:]

        for char in top_level_key:

            if (existing_item := current_node.elementExists(char)) == -1:
                return (False, "Not Found!")
            
            current_node = existing_item.getChildren()
        
        for subkey in subkeys: 

            if (existing_item := current_node.elementExists(subkey)) == -1:
                return (False, "Not Found!")
            
            current_node = existing_item.getChildren()
        
        return (True, self.traverse(current_node))        


    def display(self, node=None, level=0, prefix=""):
        if node is None:
            node = self.root

        for item in node.getItems():
            # Δημιουργία εσοχής για ευκρίνεια
            indent = ' ' * (level * 2)
            # Εκτύπωση του τρέχοντος κόμβου
            print(f"{indent}{prefix}{item.getValue()}")

            # Επανάληψη για τα παιδιά του κόμβου
            self.display(item.getChildren(), level + 1, prefix="|-- ")

    def delete(self, top_level_key):
        
        current_node = self.root
        for char in top_level_key:

            if (existing_item := current_node.elementExists(char)) == -1:
                return (False, "Not Found!")
            previous_node = current_node
            current_node = existing_item.getChildren() 
        
        self.recursive_delete(current_node)

        previous_node.removeItem(existing_item.getValue())


    def recursive_delete(self, current_node):
              
        for item in current_node.getItems():
            self.recursive_delete(item.getChildren())

        current_node.removeItems()
        del current_node

# Δημιουργία του Trie
trie = Trie()

# Εισαγωγή δεδομένων
trie.insert(["key0", '{"name": "John", "age": 22}'])
trie.insert(["key1", '{"street": {"height": 73.65, "street": {"height": 64.41, "name": "oAZC", "age": {"street": "xjWY"}, "level": 31}, "name": {"name": {"height": 5.91, "age": 25}, "age": {"height": 86.01, "street": "sMdr", "name": "IelD", "age": 46, "level": 80}, "level": {"street": "FqwV", "age": 18, "level": 51}}, "level": 51}, "name": {"height": 25.09, "name": {"height": 83.96, "street": "zIvS", "name": "jlag", "age": 76, "level": 65}, "age": 40}, "age": 86}'])
trie.display()
# Λήψη string για το "key1"
result = trie.getKey("key1")
print(result)

result = trie.get("key1.street.name.name")
print(f"key1.street.age: {result}\n==========\n")

trie.display()
print("--------------")
trie.delete("key1")
print("--------------")
trie.display()

        

        
