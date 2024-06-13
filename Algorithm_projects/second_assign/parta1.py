import time
import matplotlib.pyplot as plt
from collections import defaultdict


def load_dictionary_naive_list(filename):
    with open(filename, 'r') as file:
        dictionary = file.read().split()
    return dictionary

def spell_check_naive_list(dictionary, word):
    return word in dictionary


class AVLNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1


class AVLTree:
    def insert(self, root, key):
        
        if not root:
            return AVLNode(key)
        elif key < root.key:
            root.left = self.insert(root.left, key)
        else:
            root.right = self.insert(root.right, key)

        
        root.height = 1 + max(self.get_height(root.left),
                              self.get_height(root.right))

        
        balance = self.get_balance(root)

        
       
        if balance > 1 and key < root.left.key:
            return self.right_rotate(root)

        
        if balance < -1 and key > root.right.key:
            return self.left_rotate(root)

     
        if balance > 1 and key > root.left.key:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)

        
        if balance < -1 and key < root.right.key:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root

    def left_rotate(self, z):
        y = z.right
        T2 = y.left

        # Perform rotation
        y.left = z
        z.right = T2

        # Update heights
        z.height = 1 + max(self.get_height(z.left),
                           self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left),
                           self.get_height(y.right))

        # Return the new root
        return y

    def right_rotate(self, z):
        y = z.left
        T3 = y.right

        
        y.right = z
        z.left = T3

        
        z.height = 1 + max(self.get_height(z.left),
                           self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left),
                           self.get_height(y.right))

        
        return y

    def get_height(self, root):
        if not root:
            return 0
        return root.height

    def get_balance(self, root):
        if not root:
            return 0
        return self.get_height(root.left) - self.get_height(root.right)

    def search(self, root, key):
        if root is None or root.key == key:
            return root is not None

        if key < root.key:
            return self.search(root.left, key)
        else:
            return self.search(root.right, key)

def load_dictionary_bbst(filename):
    avl_tree = AVLTree()
    root = None
    with open(filename, 'r') as file:
        for word in file.read().split():
            root = avl_tree.insert(root, word)
    return root

def spell_check_bbst(root, word):
    avl_tree = AVLTree()
    return avl_tree.search(root, word)



class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True

    def search(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end_of_word

def load_dictionary_trie(filename):
    trie = Trie()
    with open(filename, 'r') as file:
        for word in file.read().split():
            trie.insert(word)
    return trie

def spell_check_trie(trie, word):
    return trie.search(word)


class HashMap:
    def __init__(self):
        self.map = {}

    def add(self, key):
        self.map[key] = True

    def contains(self, key):
        return key in self.map

def load_dictionary_hash_map(filename):
    hash_map = HashMap()
    with open(filename, 'r') as file:
        words = file.read().split()
        for word in words:
            hash_map.add(word)
    return hash_map

def spell_check_hash_map(hash_map, word):
    return hash_map.contains(word)


def measure_time(func, *args):
    start_time = time.time()
    result = func(*args)
    end_time = time.time()
    return result, (end_time - start_time) * 1e9  


def run_comparisons(text_file, test_words):
    results = defaultdict(dict)

    
    naive_list_dict, load_time_naive_list = measure_time(load_dictionary_naive_list, text_file)
    check_times_naive_list = []
    total_check_time_naive_list = 0
    for word in test_words:
        _, check_time = measure_time(spell_check_naive_list, naive_list_dict, word)
        check_times_naive_list.append(check_time)
        total_check_time_naive_list += check_time
    results['Naive List']['load_time'] = load_time_naive_list
    results['Naive List']['avg_check_time'] = total_check_time_naive_list / len(test_words)

    
    root_bbst, load_time_bbst = measure_time(load_dictionary_bbst, text_file)

    
    check_times_bbst = []
    total_check_time_bbst = 0

    for word in test_words:
        _, check_time = measure_time(spell_check_bbst, root_bbst, word)
        check_times_bbst.append(check_time)
        total_check_time_bbst += check_time

    
    results['BBST (set)']['load_time'] = load_time_bbst
    results['BBST (set)']['avg_check_time'] = total_check_time_bbst / len(test_words)

    
    trie_dict, load_time_trie = measure_time(load_dictionary_trie, text_file)
    check_times_trie = []
    total_check_time_trie = 0
    for word in test_words:
        _, check_time = measure_time(spell_check_trie, trie_dict, word)
        check_times_trie.append(check_time)
        total_check_time_trie += check_time
    results['Trie']['load_time'] = load_time_trie
    results['Trie']['avg_check_time'] = total_check_time_trie / len(test_words)

    
    hash_map_dict, load_time_hash_map = measure_time(load_dictionary_hash_map, text_file)
    check_times_hash_map = []
    total_check_time_hash_map = 0
    for word in test_words:
        _, check_time = measure_time(spell_check_hash_map, hash_map_dict, word)
        check_times_hash_map.append(check_time)
        total_check_time_hash_map += check_time
    results['Hash Map']['load_time'] = load_time_hash_map
    results['Hash Map']['avg_check_time'] = total_check_time_hash_map / len(test_words)

    for label in ['Naive List', 'BBST (set)', 'Trie', 'Hash Map']:
        print(f"{label}:")
        print(f"  Load time: {results[label]['load_time']} s")
        print(f"  Average spell check time: {results[label]['avg_check_time']} ns")
        print("")

    
    labels = ['Naive List', 'BBST (set)', 'Trie', 'Hash Map']
    load_times = [results[label]['load_time'] for label in labels]
    avg_check_times = [results[label]['avg_check_time'] for label in labels]

    x = range(len(labels))

    plt.figure(figsize=(14, 7))
    
    plt.subplot(1, 2, 1)
    plt.bar(x, load_times, color='skyblue')
    plt.xlabel('Data Structure')
    plt.ylabel('Time (seconds)')
    plt.title('Dictionary Load Time')
    plt.xticks(x, labels, rotation='vertical')

    plt.subplot(1, 2, 2)
    plt.bar(x, avg_check_times, color='salmon')
    plt.xlabel('Data Structure')
    plt.ylabel('Time (nanoseconds)')
    plt.title('Average Spell Check Time')
    plt.xticks(x, labels, rotation='vertical')

    plt.tight_layout()
    plt.show()

test_words = [
    'anticipate', 'brutal', 'checker', 'each', 'enarmous', 'funny', 
    'huge', 'groom', 'final', 'data', 'simple', 'search', 
    'implement', 'destroy', 'update', 'vase', 'too', 'measure', 'time', 
    'code'
] * 10000  
run_comparisons('english_words.txt', test_words)
