# https://www.cs.upc.edu/~ps/downloads/tst/tst.html
# if the same item has been already added, make a new char in the terenary search part
# // hash table trie

hash_table_trie = {}


# use hash table for now
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