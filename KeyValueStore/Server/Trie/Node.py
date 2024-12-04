class Node:
    """
    Represents a node in the Trie. Each node contains a list of items, 
    where each item can either be a child node or a value (leaf).
    """

    def __init__(self):
        self.items = []

    def getItems(self) -> list:
        """
        Retrieves all items stored in this node.
        """
        return self.items

    def getItem(self, index: int):
        """
        Retrieves an item by its index.
        """
        return self.items[index]

    def addItem(self, entry: str, is_leaf=False):
        """
        Adds a new item to the node.
        """
        item = Item(entry, is_leaf)
        self.items.append(item)
        return item

    def elementExists(self, entry: str):
        """
        Checks if an item with the specified value exists in the node.
        """
        for index in range(len(self.items)):
            item = self.getItem(index)
            if item.getValue() == entry:
                return item
        return -1

    def getChildren(self, item):
        """
        Retrieves the children of the specified item.
        """
        return item.getChildren()

    def removeItem(self, element):
        """
        Removes an item with the specified value from the node.
        """
        for index in range(len(self.items)):
            item = self.getItem(index)
            if item.getValue() == element:
                del self.items[index]
                return

    def removeItems(self):
        """
        Removes all items from the node.
        """
        while self.items:
            del self.items[0]


class Item:
    """
    Represents an item in a Trie node. Each item has a value, 
    an indicator of whether it is a leaf, and a set of children (if applicable).
    """

    def __init__(self, value='', is_leaf=False):
        self.value = value   
        self.children = Node()
        self.is_leaf = is_leaf

    def getValue(self) -> str:
        """
        Retrieves the value of the item.
        """
        return self.value

    def getIsLeaf(self) -> bool:
        """
        Checks if the item is a leaf.
        """
        return self.is_leaf

    def getChildren(self) -> Node:
        """
        Retrieves the children of the item.
        """
        return self.children
