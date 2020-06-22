""" A generic B+ tree """
from BPlusTree import constants as const
from bisect import bisect_left


class Node:
    def __init__(self, previous_node, next_node, is_leaf, parent=None, branching_factor=16):
        self.previous = previous_node
        self.next = next_node
        self.parent = parent
        self.branching_factor = branching_factor
        self.keys = []  # NOTE: must keep keys sorted
        self.children = []  # NOTE: children must correspond to parents.
        self.is_leaf = is_leaf

    def set_children(self, keys, children):
        self.keys = keys
        self.children = children
        if not self.is_leaf:
            for child in children:
                child.parent = self

    def split(self):
        is_leaf = False
        if self.is_leaf:
            new_node_keys = self.keys[(len(self.keys) // 2):]
            new_node_children = self.children[(len(self.children) // 2):]
            self.keys = self.keys[:(len(self.keys) // 2)]
            self.children = self.children[:(len(self.children) // 2)]
            is_leaf = True
            k = new_node_keys[0]
        else:
            new_node_keys = self.keys[((len(self.keys) + 1) // 2) - 1:]
            new_node_children = self.children[(len(self.children) // 2):]
            self.keys = self.keys[:((len(self.keys) + 1) // 2) - 1]
            self.children = self.children[:(len(self.children) // 2)]
            k = new_node_keys.pop(0)
        new_node = Node(self, self.next, is_leaf, self.parent, self.branching_factor)
        new_node.set_children(new_node_keys, new_node_children)
        self.next = new_node

        return new_node, k


class BPlusTree:
    def __init__(self, branching_factor=16):
        self.branching_factor = branching_factor
        self.root = Node(None, None, True, branching_factor=branching_factor)
        self.root.set_children([1], [-1])
        open(const.DATABASE_NAME, 'wb+').close()
        self.put(1, [0 for _ in range(const.FIELD_NUM)])

    def __search_tree(self, key):
        current_node = self.root
        while not current_node.is_leaf:
            idx = bisect_left(current_node.keys, key)
            if idx < len(current_node.keys) and current_node.keys[idx] == key:
                idx += 1
            current_node = current_node.children[idx]
        return current_node

    def look_up(self, key):
        node = self.__search_tree(key)
        i = self.__binary_search_list(node.keys, key)
        loc = node.children[max(i, 0)]
        # read the values in the loc of file
        val = self.__parse_fields(const.DATABASE_NAME, loc)
        if int(val[0]) == key:
            return val
        else:
            print("Data with key %d does not exist in the database" % key)
            return "Data with key %d does not exist in the database" % key

    def put(self, key_value, fields):
        # Database update - write the end of the file and get location
        loc = self.__write_fields(key_value, fields, const.DATABASE_NAME)
        # Index update
        leaf = self.__search_tree(key_value)
        self.__insert_key(key_value, loc, leaf)

    def __insert_key(self, key, loc, leaf):
        i = bisect_left(leaf.keys, key)
        leaf.keys.insert(i, key)
        leaf.children.insert(i, loc)
        node = leaf
        while len(node.children) >= self.branching_factor:
            new_child, k = node.split()  # node, new_child
            if node.parent is None:
                # create a parent node and break
                new_root = Node(None, None, False, None, self.branching_factor)
                new_root.set_children([k], [node, new_child])
                self.root = new_root
                break
            else:
                node = node.parent
                # add new node to parent
                i = bisect_left(node.keys, k)
                node.keys.insert(i, k)
                node.children.insert(i + 1, new_child)

    @staticmethod
    def __binary_search_list(list_name, key):
        i = bisect_left(list_name, key) - 1
        if i + 1 < len(list_name) and list_name[i + 1] == key:
            i += 1
        return max(i, 0)

    @staticmethod
    def __write_fields(key, fields, file):
        with open(file, 'ab') as f:
            f.write(BPlusTree.__encode_field(key, const.KEY_SIZE))
            for field in fields:
                f.write(BPlusTree.__encode_field(field, const.FIELD_SIZE))
            location = f.tell() - const.RECORD_SIZE
        return location

    @staticmethod
    def __parse_fields(file, pos):
        # pos is the start of the record
        fields = []
        with open(file, 'rb') as f:
            f.seek(pos, 0)
            key = BPlusTree.__decode_field(f.read(const.KEY_SIZE), 'int')
            for i in range(const.FIELD_NUM):
                fields.append(BPlusTree.__decode_field(f.read(const.FIELD_SIZE), const.FIELD_TYPE))
        return key, fields

    @staticmethod
    def __encode_field(number, size):
        if isinstance(number, int):
            return number.to_bytes(size, byteorder='big', signed=True)
        else:
            if isinstance(number, float) and number == int(number):
                number = int(number)
            if size - len(str(number)) < 0:
                print('Data doesn\'t fit in the provided field size: %s\nAborting...' % str(number))
                exit()
            return bytes(str(number).strip(), 'utf-8') + b" " * (size - len(str(number)))


    @staticmethod
    def __decode_field(number, decode_type):
        if decode_type == 'int':
            return int.from_bytes(number, byteorder='big')
        else:
            return str(number.decode('utf-8').strip())

