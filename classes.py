class order(object):
    def __init__(self, _size = 0):
        self.size = _size
        self.filled = 0 # number of current items in chutes
        self.filled_t = [] # time each item is recieved in chutes
        self.emptying_start_t = -1
        self.emptying_end_t = -1
        self.emptying_processed = -1


class containor(object):
    def __init__(self, _right_items = 0, _id=0):
        self.right_items = _right_items
        self.id = _id
        self.operator = -1
        self.start_time = -1
        self.end_time = -1

class operator(object):
    def __init__(self,_operator_id):
        self.id = _operator_id
        self.next_available_time=-1
        self.containor=-1
        self.remaining_items_in_containor=-1

class emptying_operator(object):
    def __init__(self,_operator_id):
        self.id = _operator_id
        self.next_available_time=-1
        self.order=-1

class Node:
    def __init__(self, _time, _operator_id=0, _containor_id=0 ,_type='put_on_conveyor'):
        self.time = _time 
        self.next = None
        self.operator_id = _operator_id
        self.containor_id = _containor_id
        self.type = _type

class LinkedList:
    def __init__(self):
        self.head = None

    def printList(self):
        temp = self.head
        if not temp:
            print('List is empty.')
            return
        else:
            print('Start:', end=' ')
        while temp:
            print(temp.time, end=' -> ')
            temp = temp.next
        print('end.')

    def insert(self, _time, _operator_id=0, _containor_id=0, _type='put_on_conveyor'):
        new_node = Node(_time,_operator_id,_containor_id,_type)

        # If the linked list is empty
        if self.head is None:
            self.head = new_node

        # If the _time is smaller than the head
        elif self.head.time >= new_node.time:
            new_node.next = self.head
            self.head = new_node

        else:
            # Locate the node before the insertion point
            current = self.head
            while current.next and new_node.time > current.next.time:
                current = current.next

            # Insertion
            new_node.next = current.next
            current.next = new_node

    def delete(self):
        # If the list is empty
        if self.head is None:
            print('Deletion Error: The list is empty.')
            return 

        # Delete head
        self.head = self.head.next
        return


