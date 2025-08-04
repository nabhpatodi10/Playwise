from structures import Stack, Queue, SongMap
from playlist import Playlist
from song import Song

class Playback:
    """
    Manages the playback of songs, including a play queue and a history of played songs.
    """
    def __init__(self, song_map: SongMap) -> None:
        """
        Initializes the Playback manager.

        Args:
            song_map (SongMap): A reference to a SongMap to retrieve song details.
        
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        self.__play_queue = Queue()
        self.__history = Stack()
        self.__songMap = song_map

    def add_song_to_queue(self, song: int) -> None:
        """
        Adds a single song to the end of the play queue.

        Args:
            song (int): The ID of the song to add.
        
        Time Complexity: O(1) amortized, due to Queue.enqueue.
        Space Complexity: O(1)
        """
        self.__play_queue.enqueue(song)

    def add_playlist_to_queue(self, playlist: Playlist) -> None:
        """
        Adds all songs from a playlist to the end of the play queue.

        Args:
            playlist (Playlist): The playlist to add.
        
        Time Complexity: O(n) where n is the number of songs in the playlist,
                         as we iterate through the playlist once.
        Space Complexity: O(1)
        """
        for song_id in playlist.get_songs_iterable():
            self.__play_queue.enqueue(song_id)

    def play_next(self) -> None:
        """
        Simulates playing the next song. Moves the current song from the queue to the history.

        Raises:
            IndexError: If the play queue is empty or has only one song.
        
        Time Complexity: O(n) where n is the number of songs in the queue, due to Queue.dequeue.
        Space Complexity: O(1)
        """
        if self.__play_queue.is_empty():
            raise IndexError("No songs in the queue")
        if self.__play_queue.get_size() == 1:
            raise IndexError("No songs to play next")
        song = self.__play_queue.dequeue()
        self.__history.push(song)
    
    def undo_last_play(self) -> None:
        """
        Undoes the last play action, moving the most recently played song from history back to the queue.

        Raises:
            IndexError: If the history is empty.
        
        Time Complexity: O(1) amortized, due to Stack.pop and Queue.enqueue.
        Space Complexity: O(1)
        """
        if self.__history.is_empty():
            raise IndexError("No history to undo")
        song = self.__history.pop()
        self.__play_queue.enqueue(song)
    
    def get_current_song(self) -> Song:
        """
        Retrieves the currently playing song object from the front of the queue.

        Returns:
            Song: The current song object.

        Raises:
            IndexError: If the play queue is empty.
        
        Time Complexity: O(1) on average, due to Queue.peek and SongMap.search_song.
        Space Complexity: O(1)
        """
        if self.__play_queue.is_empty():
            raise IndexError("No song currently playing")
        return self.__songMap.search_song(self.__play_queue.peek())
    
    def get_play_queue(self) -> Queue:
        """
        Returns the current play queue.

        Returns:
            Queue: The play queue.
        
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        return self.__play_queue
    
    def get_history(self, num: int = -1) -> Stack:
        """
        Returns the history of played songs.

        Args:
            num (int, optional): The number of recent history items to return. 
                                 Defaults to -1, which returns the entire history.

        Returns:
            Stack: A stack containing the requested history.
        
        Time Complexity: O(k) where k is `num` if specified, otherwise O(1) to return the reference.
        Space Complexity: O(k) where k is `num` if specified, otherwise O(1).
        """
        if num == -1 or num > self.__history.get_size():
            return self.__history
        else:
            return Stack(self.__history.peek(num))
        
    def __str__(self) -> str:
        """
        Returns a string representation of the current playback state.

        Returns:
            str: A formatted string showing the queue and history.
        
        Time Complexity: O(n + m) where n is the size of the queue and m is the size of the history.
        Space Complexity: O(n + m) to build the string representations of the queue and history.
        """
        return f"Playback\nQueue:\n{str(self.__play_queue)}\n\nHistory:\n{str(self.__history)}"