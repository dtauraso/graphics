# https://www.cs.upc.edu/~ps/downloads/tst/tst.html
# if the same item has been already added, make a new char in the terenary search part
# // hash table trie

hash_table_trie = {}

# we don't need a copy of the methods for each vector used in the trie tree
class Vector():
    def __init__(self):
        self.container = []
        self.end = 0
    def __len__(self):
        return len(self.container)
    def last(self):
        return self.container[-1]
    def __getitem__(self, key):
        return self.container[key]
    def __setitem_(self, key, value):
        self.container[key] = value
    def append(self, value):
        self.container.append(value)
    def drop(self, n):
        return self.container[n:]
    def get_in_range(self, a, b):
        return self.container[a:b]

def appendItem(vector, item):
    if len(vector) == 0:
        vector.append(item)
        vector.end = 1
        return vector
    else:
        # last item has data
        if len(vector.last()) > 0:
            # double size of array
            size = len(vector)
            for i in range(size):
                vector.append({})

        vector[end] = item
        vector.end += 1

        return vector

def deleteItem(vector, i):
    if len(vector) == 0:
        return vector
    else:
        new_array = []
        if i == 0:
            new_array = vector.drop(i + 1)
        else:
            new_array = vector.get_in_range(0, i) + vector.drop(i + 1)
        vector.container = new_array
        vector.end -= 1


def findLastParent(trie):
    # last parent whose children haven't been filled up yet
    # it needs to return the parent reference
    print(trie)
    edges = trie['children']
    parent = trie
    while len(edges) >= 93:
        # fails in this loop
        parent = edges
        edges = trie[len(parent) - 1]['children']
    
    children = edges
    
    if len(children) == 0:
        # print({'parent': parent, 'next_child': '!'})
        return {'parent': parent, 'next_child': '!'}
    else:
        next_edge = chr(ord(list(children)[-1]) + 1) 

        # print({'parent': parent, 'next_child': next_edge})
        return {'parent': parent, 'next_child': next_edge}
    
# use hash table for now
# replace with vector
def insert(trie, string):

    trie_tracker = trie
    new_nodes_made = 0
    for i, char in enumerate(string):
        print(char)
        if char not in trie_tracker:
            trie_tracker[char] = {  'children': {},
                                    'end_of_word': False,
                                    'state': 0}
            new_nodes_made += 1
            if i == len(string) - 1:
                trie_tracker[char]['end_of_word'] = True
        else:
            if i == len(string) - 1:
                if not new_nodes_made:
                    print('same item twice', trie_tracker)
                    # locate last parent whose children haven't been filled up yet
                    last_parent_and_child = findLastParent(trie_tracker[char])
                    print(last_parent_and_child)
                    parent = last_parent_and_child['parent']
                    child = last_parent_and_child['next_child']
                    print('pair', child, parent)
                    parent['children'][child] = { 'children': {},
                                                                'end_of_word': True,
                                                                'state': 0}

        trie_tracker = trie_tracker[char]['children']
    
def printTrie(trie, stack):
    # dft
    for char in trie.keys():

        if trie[char]['end_of_word']:
            stack.append(char)

            print(stack)
            del stack[len(stack) - 1]

            printTrie(trie[char]['children'], stack)


        else:
            stack.append(char)
            printTrie(trie[char]['children'], stack)
            del stack[len(stack) - 1]

insert(hash_table_trie, 'testgg')
insert(hash_table_trie, 'test2')
insert(hash_table_trie, 'rap')
insert(hash_table_trie, 'rap')


print(hash_table_trie)
print('printing trie')
printTrie(hash_table_trie, [])