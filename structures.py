from typing import Any, Literal, List, Callable, TypeVar
from song import Song
from datetime import datetime
import random
import heapq

T = TypeVar('T')

def heap_sort(arr: List[T], key: Callable[[T], any], reverse: bool = False) -> None:
    """
    Sorts a list in-place using the heap sort algorithm.

    Args:
        arr (List[T]): The list to be sorted.
        key (Callable[[T], any]): A function to extract a comparison key from an element.
        reverse (bool, optional): If True, sorts in descending order. Defaults to False.
    
    Time Complexity: O(n log n)
    Space Complexity: O(log n) for the recursion stack.
    """
    n = len(arr)

    def heapify(sub_arr: List[T], size: int, root_idx: int, key_func: Callable[[T], any]):
        """
        Helper function to maintain the heap property of a subtree.

        Args:
            sub_arr (List[T]): The array representing the heap.
            size (int): The size of the heap.
            root_idx (int): The root index of the subtree to heapify.
            key_func (Callable[[T], any]): The key function for comparison.
        
        Time Complexity: O(log n)
        Space Complexity: O(log n) for the recursion stack.
        """
        extreme_idx = root_idx
        left_child_idx = 2 * root_idx + 1
        right_child_idx = 2 * root_idx + 2

        if not reverse:
            if left_child_idx < size and key_func(sub_arr[left_child_idx]) > key_func(sub_arr[extreme_idx]):
                extreme_idx = left_child_idx
            if right_child_idx < size and key_func(sub_arr[right_child_idx]) > key_func(sub_arr[extreme_idx]):
                extreme_idx = right_child_idx
        else:
            if left_child_idx < size and key_func(sub_arr[left_child_idx]) < key_func(sub_arr[extreme_idx]):
                extreme_idx = left_child_idx
            if right_child_idx < size and key_func(sub_arr[right_child_idx]) < key_func(sub_arr[extreme_idx]):
                extreme_idx = right_child_idx

        if extreme_idx != root_idx:
            sub_arr[root_idx], sub_arr[extreme_idx] = sub_arr[extreme_idx], sub_arr[root_idx]
            heapify(sub_arr, size, extreme_idx, key_func)

    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i, key)

    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        heapify(arr, i, 0, key)

class SongMap:
    """A hash map to store and manage Song objects using their ID as the key."""
    def __init__(self) -> None:
        """
        Initializes an empty SongMap.
        
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        self.song_map = {}

    def add_song(self, song: Song) -> None:
        """
        Adds a song to the map.

        Args:
            song (Song): The song object to add.

        Raises:
            TypeError: If the provided object is not a Song instance.
            ValueError: If a song with the same ID already exists.
        
        Time Complexity: O(1) on average
        Space Complexity: O(1)
        """
        if not isinstance(song, Song):
            raise TypeError("Expected a Song instance")
        if song.get_id() in self.song_map:
            raise ValueError(f"Song with ID {song.get_id()} already exists")
        self.song_map[song.get_id()] = song

    def search_song(self, song_id: str) -> Song | None:
        """
        Searches for a song by its ID.

        Args:
            song_id (str): The ID of the song to search for.

        Returns:
            Song | None: The Song object if found, otherwise None.
        
        Time Complexity: O(1) on average
        Space Complexity: O(1)
        """
        return self.song_map.get(song_id)

    def remove_song(self, song: Song) -> None:
        """
        Removes a song from the map.

        Args:
            song (Song): The song object to remove.

        Raises:
            TypeError: If the provided object is not a Song instance.
            ValueError: If the song does not exist in the map.
        
        Time Complexity: O(1) on average
        Space Complexity: O(1)
        """
        if not isinstance(song, Song):
            raise TypeError("Expected a Song instance")
        if song.get_id() not in self.song_map:
            raise ValueError(f"Song with ID {song.get_id()} does not exist")
        del self.song_map[song.get_id()]

    def get_longest_songs(self, num: int = 5) -> List[Song]:
        """
        Gets the longest songs from the map.

        Args:
            num (int, optional): The number of longest songs to return. Defaults to 5.

        Returns:
            List[Song]: A list of the longest songs, sorted by duration in descending order.
        
        Time Complexity: O(n log k) where n is the total number of songs and k is num.
        Space Complexity: O(k) to store the heap.
        """
        if num <= 0:
            raise ValueError("Number of songs must be greater than 0")
        min_heap = []
        for song in self.song_map.values():
            if len(min_heap) < num:
                heapq.heappush(min_heap, (song.get_duration(), song.get_id(), song))
            else:
                # If the current song is longer than the shortest in the heap, replace it.
                if song.get_duration() > min_heap[0][0]:
                    heapq.heapreplace(min_heap, (song.get_duration(), song.get_id(), song))
        
        # The heap now contains the 'num' longest songs. Sort them by duration descending.
        longest_songs = [song for _, _, song in min_heap]
        longest_songs.sort(key=lambda s: s.get_duration(), reverse=True)
        return longest_songs

    def __str__(self) -> str:
        """
        Returns a string representation of all songs in the map.
        
        Time Complexity: O(n) where n is the number of songs.
        Space Complexity: O(n) to build the string.
        """
        return "\n".join(str(song) for song in self.song_map.values())

class DoublyLinkedListNode:
    """Node for use in a DoublyLinkedList."""
    def __init__(self, song: int):
        """
        Initializes a DoublyLinkedListNode.

        Args:
            song (int): The ID of the song.
        
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        self.song = song
        self.prev = None
        self.next = None
        self.add_time = datetime.now()

class DoublyLinkedList:
    """A doubly linked list implementation for a playlist."""
    def __init__(self, songMap: SongMap):
        """
        Initializes an empty DoublyLinkedList.

        Args:
            songMap (SongMap): A reference to a SongMap to retrieve song details.
        
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        self.head = None
        self.tail = None
        self.size = 0
        self.__songMap = songMap

    def __sort(self, key: Callable[['DoublyLinkedListNode'], any], reverse: bool = False) -> None:
        """
        Internal helper to sort the linked list.

        Args:
            key (Callable[['DoublyLinkedListNode'], any]): The key function for sorting.
            reverse (bool, optional): Sort in descending order. Defaults to False.
        
        Time Complexity: O(n log n) where n is the size of the list.
        Space Complexity: O(n) to store nodes in a list for sorting.
        """
        if self.size <= 1:
            return
        
        nodes = []
        current = self.head
        while current:
            nodes.append(current)
            current = current.next
        
        heap_sort(nodes, key=key, reverse=reverse)

        if not nodes:
            self.head = None
            self.tail = None
            return

        self.head = nodes[0]
        self.head.prev = None
        self.tail = nodes[-1]
        self.tail.next = None

        for i in range(len(nodes) - 1):
            nodes[i].next = nodes[i + 1]
            nodes[i + 1].prev = nodes[i]

    def append(self, song: int) -> None:
        """
        Appends a new song to the end of the list.

        Args:
            song (int): The ID of the song to append.
        
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        new_node = DoublyLinkedListNode(song)
        if not self.head:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node
        self.size += 1

    def insert(self, index: int, song: int) -> None:
        """
        Inserts a new song at a specific index in the list.

        Args:
            index (int): The index at which to insert the song.
            song (int): The ID of the song to insert.
        
        Time Complexity: O(n)
        Space Complexity: O(1)
        """
        if index < 0 or index > self.size:
            raise IndexError("Index out of bounds")

        if index == self.size:
            self.append(song)
            return

        new_node = DoublyLinkedListNode(song)
        if index == 0:
            new_node.next = self.head
            if self.head:
                self.head.prev = new_node
            self.head = new_node
            if self.tail is None:
                self.tail = new_node
        else:
            current = self.get_node(index)
            new_node.prev = current.prev
            new_node.next = current
            if current.prev:
                current.prev.next = new_node
            current.prev = new_node
        
        self.size += 1

    def remove(self, index: int) -> int:
        """
        Removes a song from the list at a specific index.

        Args:
            index (int): The index of the song to remove.

        Returns:
            int: The ID of the removed song, or None if index is invalid.
        
        Time Complexity: O(n) in the worst case (removing from the end).
        Space Complexity: O(1)
        """
        if not (0 <= index < self.size):
            raise IndexError("Index out of bounds for remove")
        current = self.head
        for _ in range(index):
            if current is None:
                return
            current = current.next
        if current is None:
            return
        if current.prev:
            current.prev.next = current.next
        if current.next:
            current.next.prev = current.prev
        if current == self.head:
            self.head = current.next
        if current == self.tail:
            self.tail = current.prev
        self.size -= 1
        return current.song

    def move(self, old_index: int, new_index: int) -> None:
        """
        Moves a song from an old index to a new index.

        Args:
            old_index (int): The current index of the song.
            new_index (int): The new index for the song.
        
        Time Complexity: O(n) due to finding nodes by index.
        Space Complexity: O(1)
        """
        if old_index < 0 or new_index < 0:
            return
        if old_index >= self.size or new_index >= self.size:
            return
        current = self.head
        for _ in range(old_index):
            if current is None:
                return
            current = current.next
        if current is None:
            return
        song = current.song
        song = self.remove(old_index)
        self.insert(new_index, song)

    def reverse(self) -> None:
        """
        Reverses the order of the linked list in-place.
        
        Time Complexity: O(n)
        Space Complexity: O(1)
        """
        current = self.head
        prev = None
        self.tail = current
        while current:
            next_node = current.next
            current.next = prev
            current.prev = next_node
            prev = current
            current = next_node
        self.head = prev

    def sort_list(self, sort_type: Literal["add_time", "name", "duration"], reverse: bool = False) -> None:
        """
        Sorts the list based on a specified criterion.

        Args:
            sort_type (Literal["add_time", "name", "duration"]): The attribute to sort by.
            reverse (bool, optional): Sort in descending order. Defaults to False.
        
        Time Complexity: O(n log n) due to using heap sort.
        Space Complexity: O(n) to store nodes in a list for sorting.
        """
        if sort_type == "add_time":
            self.__sort(key=lambda node: node.add_time, reverse=reverse)
        else:
            if sort_type == "name":
                self.__sort(key=lambda node: self.__songMap.search_song(node.song).get_name(), reverse=reverse)
            elif sort_type == "duration":
                self.__sort(key=lambda node: self.__songMap.search_song(node.song).get_duration(), reverse=reverse)

    def shuffle(self) -> None:
        """
        Shuffles the playlist, ensuring no two songs by the same primary artist play consecutively.
        Uses a max-heap to distribute songs from the most frequent artists.

        Raises:
            ValueError: If the playlist cannot be shuffled due to a high concentration of songs by a single artist.
        
        Time Complexity: O(n log k) where n is the number of songs and k is the number of unique artists.
        Space Complexity: O(n) to store nodes and artist groupings.
        """
        if self.size <= 1:
            return

        nodes = []
        current = self.head
        while current:
            nodes.append(current)
            current = current.next
    
        random.shuffle(nodes)

        songs_by_artist = {}
        for node in nodes:
            primary_artist = self.__songMap.search_song(node.song).get_artists()[0] if self.__songMap.search_song(node.song).get_artists() else "Unknown"
            if primary_artist not in songs_by_artist:
                songs_by_artist[primary_artist] = []
            songs_by_artist[primary_artist].append(node)

        max_freq = 0
        if songs_by_artist:
            max_freq = max(len(songs) for songs in songs_by_artist.values())
        
        if max_freq > (self.size - max_freq) + 1:
            raise ValueError("Cannot shuffle playlist: too many songs by a single artist to avoid consecutive playback.")

        max_heap = [(-len(songs), artist) for artist, songs in songs_by_artist.items()]
        heapq.heapify(max_heap)

        shuffled_nodes = []

        prev_artist_group = None

        while max_heap:
            count, artist = heapq.heappop(max_heap)

            node = songs_by_artist[artist].pop()
            shuffled_nodes.append(node)

            if prev_artist_group:
                heapq.heappush(max_heap, prev_artist_group)

            if songs_by_artist[artist]:
                prev_artist_group = (count + 1, artist)
            else:
                prev_artist_group = None

        self.head = shuffled_nodes[0]
        self.head.prev = None
        self.tail = shuffled_nodes[-1]
        self.tail.next = None

        for i in range(len(shuffled_nodes) - 1):
            shuffled_nodes[i].next = shuffled_nodes[i+1]
            shuffled_nodes[i+1].prev = shuffled_nodes[i]

    def get_size(self) -> int:
        """
        Returns the number of songs in the list.
        
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        return self.size
    
    def get_node(self, index: int) -> DoublyLinkedListNode:
        """
        Retrieves the node at a specific index.

        Args:
            index (int): The index of the node to retrieve.

        Raises:
            IndexError: If the index is out of bounds.

        Returns:
            DoublyLinkedListNode: The node at the specified index.
        
        Time Complexity: O(n) in the worst case.
        Space Complexity: O(1)
        """
        if index < 0 or index >= self.size:
            raise IndexError("Index out of bounds")
        current = self.head
        for _ in range(index):
            current = current.next
        return current
    
    def __iter__(self):
        """Allows iteration over the linked list's songs."""
        current = self.head
        while current:
            yield current.song
            current = current.next

    def __str__(self) -> str:
        """
        Returns a string representation of the playlist.
        
        Time Complexity: O(n) where n is the number of songs.
        Space Complexity: O(n) to build the string.
        """
        current = self.head
        if not current:
            return "No songs in the playlist."
        songs_str = ""
        while current:
            songs_str += str(self.__songMap.search_song(current.song)) + "\nAdded at: " + str(current.add_time) + "\n\n"
            current = current.next
        return songs_str

class Stack:
    """A standard Stack implementation (LIFO)."""
    def __init__(self, items: List[Any] = None):
        """
        Initializes the stack.

        Args:
            items (List[Any], optional): An initial list of items. Defaults to None.
        
        Time Complexity: O(1) or O(n) if items are provided.
        Space Complexity: O(1) or O(n) if items are provided.
        """
        self.items = [] if items is None else items

    def push(self, item: Any) -> None:
        """
        Pushes an item onto the top of the stack.

        Args:
            item (Any): The item to push.
        
        Time Complexity: O(1) on average.
        Space Complexity: O(1)
        """
        self.items.append(item)

    def pop(self) -> Any:
        """
        Pops an item from the top of the stack.

        Returns:
            Any: The popped item.

        Raises:
            IndexError: If the stack is empty.
        
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        if not self.is_empty():
            return self.items.pop()
        raise IndexError("Pop from empty stack")

    def peek(self, n: int = 1) -> list[Any]:
        """
        Returns the top n items of the stack without removing them.

        Args:
            n (int, optional): The number of items to peek. Defaults to 1.

        Returns:
            list[Any]: A list of the top n items.

        Raises:
            IndexError: If the stack is empty.
        
        Time Complexity: O(n) for slicing.
        Space Complexity: O(n) for the returned slice.
        """
        if not self.is_empty():
            return self.items[-1:-n-1:-1]
        raise IndexError("Peek from empty stack")

    def is_empty(self) -> bool:
        """
        Checks if the stack is empty.
        
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        return len(self.items) == 0

    def get_size(self) -> int:
        """
        Returns the size of the stack.
        
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        return len(self.items)
    
    def __str__(self) -> str:
        """
        Returns a string representation of the stack.
        
        Time Complexity: O(n)
        Space Complexity: O(n)
        """
        return "\n".join(str(item) for item in self.items) if not self.is_empty() else "Stack is empty"
    
class Queue:
    """A standard Queue implementation (FIFO)."""
    def __init__(self, items: List[Any] = None):
        """
        Initializes the queue.

        Args:
            items (List[Any], optional): An initial list of items. Defaults to None.
        
        Time Complexity: O(1) or O(n) if items are provided.
        Space Complexity: O(1) or O(n) if items are provided.
        """
        self.items = [] if items is None else items

    def enqueue(self, item: Any) -> None:
        """
        Adds an item to the end of the queue.

        Args:
            item (Any): The item to add.
        
        Time Complexity: O(1) on average.
        Space Complexity: O(1)
        """
        self.items.append(item)

    def dequeue(self) -> Any:
        """
        Removes an item from the front of the queue.

        Returns:
            Any: The removed item.

        Raises:
            IndexError: If the queue is empty.
        
        Time Complexity: O(n) because list.pop(0) is O(n).
        Space Complexity: O(1)
        """
        if not self.is_empty():
            return self.items.pop(0)
        raise IndexError("Dequeue from empty queue")

    def peek(self) -> Any:
        """
        Returns the item at the front of the queue without removing it.

        Returns:
            Any: The item at the front.

        Raises:
            IndexError: If the queue is empty.
        
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        if not self.is_empty():
            return self.items[0]
        raise IndexError("Peek from empty queue")

    def is_empty(self) -> bool:
        """
        Checks if the queue is empty.
        
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        return len(self.items) == 0

    def get_size(self) -> int:
        """
        Returns the size of the queue.
        
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        return len(self.items)
    
    def __str__(self) -> str:
        """
        Returns a string representation of the queue.
        
        Time Complexity: O(n)
        Space Complexity: O(n)
        """
        return "\n".join(str(item) for item in self.items) if self.items else "Queue is empty"

class BinarySearchTreeBucketNode:
    """An internal node in the BinarySearchTree, representing a range of ratings."""
    def __init__(self, start: int, end: int):
        self.start = start
        self.end = end
        self.left = None
        self.right = None

class BinarySearchTreeLeafNode:
    """A leaf node in the BinarySearchTree, holding songs within a specific rating range."""
    def __init__(self, start: int, end: int, songs: dict = {}):
        self.start = start
        self.end = end
        self.songs = songs

class BinarySearchTree:
    """A custom Binary Search Tree to store songs based on their rating."""
    def __init__(self) -> None:
        """
        Initializes the BST with a predefined structure of buckets for ratings 0-5.
        
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        self.root = BinarySearchTreeBucketNode(0, 6)
        self.root.left = BinarySearchTreeBucketNode(0, 3)
        self.root.right = BinarySearchTreeBucketNode(3, 6)
        self.root.left.left = BinarySearchTreeBucketNode(0, 2)
        self.root.left.right = BinarySearchTreeLeafNode(2, 3)
        self.root.right.left = BinarySearchTreeLeafNode(3, 4)
        self.root.right.right = BinarySearchTreeLeafNode(4, 6)
        self.root.left.left.left = BinarySearchTreeLeafNode(0, 1)
        self.root.left.left.right = BinarySearchTreeLeafNode(1, 2)

    def __insert(self, node: BinarySearchTreeBucketNode | BinarySearchTreeLeafNode, rating: float, song: int) -> None:
        """
        Internal helper to recursively insert a song.
        
        Time Complexity: O(log k) where k is the number of buckets (constant in this implementation).
        Space Complexity: O(log k) for recursion stack.
        """
        if isinstance(node, BinarySearchTreeLeafNode):
            if rating < node.start or rating >= node.end:
                raise ValueError("Rating out of bounds for leaf node")
            node.songs[song] = rating
        else:
            if rating < node.start or rating >= node.end:
                raise ValueError("Rating out of bounds for bucket node")
            if rating < (node.start + node.end) / 2:
                if not node.left:
                    node.left = BinarySearchTreeLeafNode(node.start, (node.start + node.end) / 2)
                self.__insert(node.left, rating, song)
            else:
                if not node.right:
                    node.right = BinarySearchTreeLeafNode((node.start + node.end) / 2, node.end)
                self.__insert(node.right, rating, song)

    def insert(self, rating: float, song: int) -> None:
        """
        Inserts a song into the tree based on its rating.

        Args:
            rating (float): The rating of the song (0-5).
            song (int): The ID of the song.
        
        Time Complexity: O(log k) where k is the number of buckets (constant).
        Space Complexity: O(log k) for recursion stack.
        """
        if rating < 0 or rating > 5:
            raise ValueError("Rating must be between 0 and 5")
        self.__insert(self.root, rating, song)

    def __search(self, node: BinarySearchTreeBucketNode | BinarySearchTreeLeafNode, start: int, end: int) -> dict:
        """
        Internal helper to recursively search for songs in a rating range.
        
        Time Complexity: O(log k + m) where k is the number of buckets and m is the number of songs in the matching range.
        Space Complexity: O(log k + m) for recursion stack and result dictionary.
        """
        if not node:
            return {}
        if isinstance(node, BinarySearchTreeLeafNode):
            if node.start >= end or node.end <= start:
                return {}
            return {k: v for k, v in node.songs.items() if v >= start and v < end}
        # If it's a bucket node, search both sides
        return {**self.__search(node.left, start, end), **self.__search(node.right, start, end)}
    
    def search(self, start: int, end: int) -> dict:
        """
        Searches for songs within a given rating range.

        Args:
            start (int): The start of the rating range (inclusive).
            end (int): The end of the rating range (exclusive).

        Returns:
            dict: A dictionary of songs matching the rating range.
        
        Time Complexity: O(log k + m) where k is the number of buckets and m is the number of songs in the matching range.
        Space Complexity: O(log k + m) for recursion stack and result dictionary.
        """
        if start < 0 or end > 6 or start >= end:
            raise ValueError("Invalid range for search")
        return self.__search(self.root, start, end)
    
    def __delete(self, node: BinarySearchTreeBucketNode | BinarySearchTreeLeafNode, song: int) -> bool:
        """
        Internal helper to recursively delete a song.
        
        Time Complexity: O(k + n) in the worst case, where k is number of buckets and n is number of songs in a leaf, as it may traverse the whole tree.
        Space Complexity: O(log k) for recursion stack.
        """
        if not node:
            return False
        if isinstance(node, BinarySearchTreeLeafNode):
            if song in node.songs.values():
                del node.songs[song]
                return True
            return False
        # If it's a bucket node, try to delete from both sides
        return self.__delete(node.left, song) or self.__delete(node.right, song)

    def delete(self, song: int) -> bool:
        """
        Deletes a song from the tree.

        Args:
            song (int): The ID of the song to delete.

        Returns:
            bool: True if the song was found and deleted, False otherwise.
        
        Time Complexity: O(k + n) in the worst case, where k is number of buckets and n is number of songs in a leaf.
        Space Complexity: O(log k) for recursion stack.
        """
        if not isinstance(song, int):
            raise TypeError("Expected song to be an integer ID")
        return self.__delete(self.root, song)
    
    def get_num_by_rating(self, start: int, end: int) -> int:
        """
        Gets the number of songs within a given rating range.

        Args:
            start (int): The start of the rating range (inclusive).
            end (int): The end of the rating range (exclusive).

        Returns:
            int: The number of songs in the range.
        
        Time Complexity: O(log k + m) where k is the number of buckets and m is the number of songs in the matching range.
        Space Complexity: O(log k + m) for the search result.
        """
        if start < 0 or end > 6 or start >= end:
            raise ValueError("Invalid range for get_num_by_rating")
        return len(self.search(start, end))