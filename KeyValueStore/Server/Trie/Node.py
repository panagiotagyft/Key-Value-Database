
class Node:
    def __init__(self):
        self.items = []

    def getItems(self) -> list:
        return self.items

    def getItem(self, index: int):
        print(index)
        return self.items[index]
    
    def addItem(self, entry: str, is_leaf=False):
        item = Item(entry, is_leaf)
        self.items.append(item)
        return item
    
    def elementExists(self, entry: str):
        for index in range(len(self.items)):
            item = self.getItem(index)
            if item.getValue() == entry:  
                return item
        return -1
    
    def getChildren(self, item):
        return item.getChildren()
    
    def removeItem(self, element):
        
       for index in range(len(self.items)):
            item = self.getItem(index) 
            if item.getValue() == element:
                del self.items[index] 
                return
             
                
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