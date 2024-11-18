from KeyValueStore.Server.trie import Node

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

class Node:
    def __init__(self):
        self.items = []

    def getItems(self) -> list:
        return self.items

    def getItem(self, index: int) -> Item:
        return self.items[index]
    
    def addItem(self, entry: str) -> Node:
        item = Item(entry)
        self.items.append(item)
        return item.getChildren()
    
    def substringExists(self, entry: str) -> Item:
        for index in range(len(self.items)):
            if (item:=self.getItem(index)).getParent(entry) == True: return item
        return -1
    
    def getChildren(self, item: Item) -> Node:
        return item.getChildren()

class Trie:
    def __init__(self):
        self.root = Node()

    def insert(self, entry: str):
       
        current_node = self.root

        for substring in entry:
            
            if not (items:=current_node.getItems()) or  (item:=current_node.substringExists(substring)) == False:
                current_node = current_node.addItem(substring)
                continue
            
            current_node = current_node.getChildren(item)
