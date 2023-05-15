"""
MinHeap class for storing key-value items
-----------------------------------------
Operations on Min(Max) Heap
---------------------------
1) getMin():
    It returns the root element of Min Heap.
    Time Complexity is O(1).

2) extractMin():
    Removes the minimum element from MinHeap.
    Time Complexity is O(logn)
    this operation needs to maintain the heap property
    by calling heapify() after removing root.

3) decreaseKey():
    Decreases value of key.
    The time complexity is O(logn).
    [5]
        \
        [10]    -> e.g 9 or 1
        /   \
      [11]  [12]
    If the decreased key value of a node
        is greater than the parent of the node,
        then we don’t need to do anything.
    Else we need to traverse up
        to fix the violated heap property.

4) increaseKey():
    Increases value of key.
    The time complexity is O(logn).
    [5]
        \
        [10]    -> e.g 12 or 20
        /   \
      [15]  [16]
    If the increased key value of a node
        is less than the children of the node,
        then we don’t need to do anything.
    Else we need to traverse down
        to fix the violated heap property.

5) changeKey():
    Decreases or Increases value of key.

6) insert():
    Inserting a new key takes O(logn) time.
    We add a new key at the end of the tree.
    If new key is greater than its parent,
        then we don’t need to do anything.
    Else we need to traverse up
        to fix the violated heap property.

7) delete():
    Deleting a key takes O(logn) time.
    We replace the key to be deleted with
        minimum infinite by calling decreaseKey().
    then as the minus infinite is root,
        we call extractMin() to remove the key.

8) isInMinHeap(v)
    check if exists an item with key = v
    Time complexity is O(1)
"""


class MinHeap:
    def __init__(self, array=[]):
        self.array = []  # tuple (key, value)
        self.pos = {}  # position of key in array
        self.size = len(array)  # number of elements in min heap

        for i, item in enumerate(array):
            self.array.append((item[0], item[1]))
            self.pos[item[0]] = i

        for i in range(self.size // 2, -1, -1):
            self.heapify(i)

    # display items of heap
    def display(self):
        print('array =', end=' ')
        for i in range(self.size):
            print(f'({self.array[i][0]} : {self.array[i][1]})', end=' ')
        print()

    # is heap empty ?
    def isEmpty(self):
        return self.size == 0

    # i is an array index
    # modify array so that i roots a heap, down-heap
    def heapify(self, i):

        min_pos = i  # initialize position of min_item as root

        le = 2 * i + 1  # left  = 2*i + 1
        ri = 2 * i + 2  # right = 2*i + 2

        if le < self.size and self.array[le][1] < self.array[min_pos][1]:
            min_pos = le
        if ri < self.size and self.array[ri][1] < self.array[min_pos][1]:
            min_pos = ri

        if min_pos != i:
            # update pos
            self.pos[self.array[min_pos][0]] = i
            self.pos[self.array[i][0]] = min_pos

            # swap
            self.array[min_pos], self.array[i] = \
                self.array[i], self.array[min_pos]

            self.heapify(min_pos)

    # return the min element of the heap
    def getMin(self):
        if self.size == 0:
            return None

        return self.array[0]

    # return and remove the min element of the heap
    def extractMin(self):
        if self.size == 0:
            return None

        root = self.array[0]
        lastNode = self.array[self.size - 1]

        # new root is last node
        self.array[0] = lastNode

        # update pos
        self.pos[lastNode[0]] = 0

        # delete from dict
        del self.pos[root[0]]

        # update size
        self.size -= 1

        # heapify the new root
        self.heapify(0)

        return root

    # item (key, value) to insert
    # modify array to include item
    def insert(self, item):
        # insert an item at the end with big value
        if self.size < len(self.array):
            self.array[self.size] = (item[0], float('inf'))
        else:
            self.array.append((item[0], float('inf')))

        # insert into dict
        self.pos[item[0]] = self.size

        # increase size
        self.size += 1

        # set value to item (up-heap)
        self.decreaseKey(item)

    # decrease value of item (key, value)
    # with value smaller than current
    def decreaseKey(self, item):
        i = self.pos[item[0]]
        val = item[1]

        # new value must be smaller than current
        if self.array[i][1] <= val:
            return

        self.array[i] = item

        # check if is smaller than parent
        p = (i - 1) // 2
        while i > 0 and self.array[i][1] < self.array[p][1]:
            # update pos
            self.pos[self.array[i][0]] = p
            self.pos[self.array[p][0]] = i

            # swap
            self.array[p], self.array[i] = self.array[i], self.array[p]

            i = p
            p = (i - 1) // 2

    # increase value of item (key, value),
    # with value greater than current
    def increaseKey(self, item):
        i = self.pos[item[0]]
        val = item[1]

        # new value must be greater than current
        if self.array[i][1] >= val:
            return None

        # update array
        self.array[i] = item

        # check children
        self.heapify(i)

    # change value of item (key, value),
    # decreaseKey or increaseKey, Running Time: O(log n)
    def changeKey(self, item):
        i = self.pos[item[0]]
        new_val = item[1]

        if new_val < self.array[i][1]:
            self.decreaseKey(item)

        if new_val > self.array[i][1]:
            self.increaseKey(item)

    # check if exists an item with key = key
    def isInMinHeap(self, key):
        if self.pos.get(key) == None:
            return False
        if self.pos[key] < self.size:
            return True
        return False

    # get the value of item with key = key
    def getValueMinHeap(self, key):
        if self.pos.get(key) == None:
            return None
        if self.pos[key] < self.size:
            return self.array[self.pos[key]][1]
        return None

    # This function deletes key in item. It first reduces
    # value to minus infinite and then calls extractMin() 
    def deleteKey(self, item):
        self.decreaseKey((item[0], float('-inf')))
        self.extractMin()

    # test


if __name__ == '__main__':
    arr = [('a', 50), ('b', 30), ('c', 10), ('d', 20), ('e', 40), ('f', 80)]

    h = MinHeap(arr)
    h.display()

    # h.decreaseKey(('b', 2))
    h.changeKey(('b', 2))
    h.display()
    # h.increaseKey(('b', 30))
    h.changeKey(('b', 30))
    h.display()

    h.extractMin()
    h.display()
    print('a', h.extractMin())
    h.display()

    h.insert(('x', 5))
    h.display()

    print('min=', h.getMin())

    h.deleteKey(('e', 0))
    h.display()

    print(h.isInMinHeap('a'))
    print(h.isInMinHeap('c'))
