from typing import Literal
from structures import DoublyLinkedList, Stack, SongMap

class Change:
    """Represents a single change operation for undo/redo functionality."""
    def __init__(self, change_type: Literal["add", "remove", "move", "reverse", "sort", "rename", "shuffle"], change: dict | list) -> None:
        """
        Initializes a Change object.

        Args:
            change_type: The type of change.
            change: Data associated with the change.
        
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        self.change_type = change_type
        self.change = change

    def __str__(self) -> str:
        """
        Returns a string representation of the change.
        
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        return f"Change Type: {self.change_type}, Change: {self.change}"

class Playlist:
    """
    Represents a playlist of songs, allowing for various operations like
    adding, removing, moving, sorting, and shuffling songs. It also supports
    undoing changes.
    """
    def __init__(self, name: str, song_map: SongMap) -> None:
        """
        Initializes a new Playlist.

        Args:
            name (str): The name of the playlist.
            song_map (SongMap): A reference to a SongMap to retrieve song details.
        
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        self.__name = name
        self.__songs = DoublyLinkedList(song_map)
        self.__edits = Stack()

    def get_name(self) -> str:
        """
        Returns the name of the playlist.

        Returns:
            str: The playlist's name.
        
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        return self.__name
    
    def set_name(self, name: str) -> None:
        """
        Updates the name of the playlist and records the change for undo.

        Args:
            name (str): The new name for the playlist.
        
        Time Complexity: O(1) amortized due to Stack.push.
        Space Complexity: O(1)
        """
        self.__edits.push(Change("rename", {"initial_name": self.__name, "new_name": name}))
        self.__name = name

    def add_song(self, song: int) -> None:
        """
        Adds a song to the end of the playlist.

        Args:
            song (int): The ID of the song to add.

        Raises:
            TypeError: If the provided song is not an integer ID.
        
        Time Complexity: O(1) amortized, as both DoublyLinkedList.append and Stack.push are O(1).
        Space Complexity: O(1)
        """
        if not isinstance(song, int):
            raise TypeError("Expected a Song ID")
        self.__edits.push(Change("add", {"song_added": song}))
        self.__songs.append(song)

    def remove_song(self, index: int) -> None:
        """
        Removes a song from the playlist at a specific index.

        Args:
            index (int): The index of the song to remove.

        Raises:
            IndexError: If the index is out of bounds.
        
        Time Complexity: O(n) where n is the number of songs, due to DoublyLinkedList.remove.
        Space Complexity: O(1)
        """
        if index < 0 or index >= self.get_size():
            raise IndexError("Index out of bounds")
        song = self.__songs.remove(index)
        self.__edits.push(Change("remove", {"song_removed": song, "index": index}))

    def move_song(self, from_index: int, to_index: int) -> None:
        """
        Moves a song from one position to another within the playlist.

        Args:
            from_index (int): The current index of the song.
            to_index (int): The new index for the song.

        Raises:
            IndexError: If either index is out of bounds.
        
        Time Complexity: O(n) where n is the number of songs, due to DoublyLinkedList.move.
        Space Complexity: O(1)
        """
        if from_index < 0 or from_index >= self.get_size() or to_index < 0 or to_index >= self.get_size():
            raise IndexError("Index out of bounds")
        self.__songs.move(from_index, to_index)
        self.__edits.push(Change("move", {"from_index": from_index, "to_index": to_index}))

    def reverse_playlist(self) -> None:
        """
        Reverses the order of songs in the playlist.
        
        Time Complexity: O(n) where n is the number of songs, due to DoublyLinkedList.reverse.
        Space Complexity: O(1)
        """
        self.__songs.reverse()
        self.__edits.push(Change("reverse", {"playlist_reversed": True}))

    def sort_playlist(self, sort_type: Literal["add_time", "name", "duration"], reverse: bool = False) -> None:
        """
        Sorts the playlist based on a specified criterion.

        Args:
            sort_type (Literal["add_time", "name", "duration"]): The attribute to sort by.
            reverse (bool, optional): If True, sorts in descending order. Defaults to False.
        
        Time Complexity: O(n log n) where n is the number of songs, due to DoublyLinkedList.sort_list.
        Space Complexity: O(n) to store the list state for the undo operation.
        """
        self.__edits.push(Change("sort", [{"sort_type": sort_type, "reverse": reverse}, self.__songs]))
        self.__songs.sort_list(sort_type=sort_type, reverse=reverse)

    def shuffle_playlist(self) -> None:
        """
        Shuffles the playlist, ensuring no two songs by the same primary artist play consecutively.
        
        Time Complexity: O(n log k) where n is the number of songs and k is the number of unique artists, due to DoublyLinkedList.shuffle.
        Space Complexity: O(n) to store the list state for the undo operation.
        """
        self.__songs.shuffle()
        self.__edits.push(Change("shuffle", [{"playlist_shuffled": True}, self.__songs]))

    def undo_changes(self, num: int = 1) -> None:
        """
        Undoes the last 'num' changes made to the playlist.

        Args:
            num (int, optional): The number of changes to undo. Defaults to 1.

        Raises:
            ValueError: If num is less than 1 or greater than the number of available edits.
        
        Time Complexity: O(num * n) where n is the number of songs in the playlist. The complexity of each undo operation depends on the change type, with 'move' being O(n).
        Space Complexity: O(1)
        """
        if num < 1:
            raise ValueError("Number of undos must be at least 1")
        if num > self.__edits.get_size():
            raise ValueError("Not enough edits to undo")
        for _ in range(num):
            if not self.__edits.is_empty():
                change = self.__edits.pop()
                if change.change_type == "rename":
                    self.__name = change.change["initial_name"]
                elif change.change_type == "add":
                    self.__songs.remove(self.__songs.get_size() - 1)
                elif change.change_type == "remove":
                    self.__songs.append(change.change["song_removed"])
                elif change.change_type == "move":
                    self.__songs.move(change.change["to_index"], change.change["from_index"])
                elif change.change_type == "reverse":
                    self.__songs.reverse()
                elif change.change_type == "sort":
                    self.__songs = change.change[1]
                elif change.change_type == "shuffle":
                    self.__songs = change.change[1]

    def get_song(self, index: int) -> int:
        """
        Retrieves the song ID at a specific index in the playlist.

        Args:
            index (int): The index of the song to retrieve.

        Returns:
            int: The song ID.

        Raises:
            IndexError: If the index is out of bounds.
        
        Time Complexity: O(n) where n is the number of songs, due to DoublyLinkedList.get_node.
        Space Complexity: O(1)
        """
        if index < 0 or index >= self.get_size():
            raise IndexError("Index out of bounds")
        return self.__songs.get_node(index).song

    def get_size(self) -> int:
        """
        Returns the number of songs in the playlist.

        Returns:
            int: The size of the playlist.
        
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        return self.__songs.size
    
    def get_changes(self) -> Stack:
        """
        Returns the stack of changes made to the playlist.

        Returns:
            Stack: The stack containing all edit operations.
        
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        return self.__edits
    
    def get_songs_iterable(self):
        """
        Returns an iterator for the songs in the playlist.

        Returns:
            iterator: An iterator that yields song IDs.
        
        Time Complexity: O(1) to create the iterator object.
        Space Complexity: O(1)
        """
        return iter(self.__songs)
    
    def __str__(self) -> str:
        """
        Returns a string representation of the playlist.

        Returns:
            str: A formatted string of the playlist name and its songs.
        
        Time Complexity: O(n) where n is the number of songs, due to iterating through the list.
        Space Complexity: O(n) to build the string representation.
        """
        return f"Playlist Name: {self.__name}\nSongs:\n{str(self.__songs)}"