from typing import Literal
from playback import Playback
from playlist import Playlist
from structures import BinarySearchTree, SongMap

class Dashboard:
    """
    A facade class that provides a simplified interface to manage and interact
    with the playlist, playback, and song rating systems.
    """
    def __init__(self, playlist: Playlist, playback: Playback, rating_tree: BinarySearchTree, songMap: SongMap) -> None:
        """
        Initializes the Dashboard with references to core components.

        Args:
            playlist (Playlist): The playlist object to manage.
            playback (Playback): The playback control object.
            rating_tree (BinarySearchTree): The BST for song ratings.
            songMap (SongMap): The hash map of all songs.
        
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        self.__playlist = playlist
        self.__playback = playback
        self.__rating_tree = rating_tree
        self.__songMap = songMap

    def get_playlist(self) -> str:
        """
        Returns a string representation of the current playlist.

        Returns:
            str: The formatted string of the playlist.
        
        Time Complexity: O(n) where n is the number of songs in the playlist.
        Space Complexity: O(n) to build the string representation.
        """
        return str(self.__playlist)
    
    def change_playlist_name(self, name: str) -> None:
        """
        Changes the name of the playlist.

        Args:
            name (str): The new name for the playlist.
        
        Time Complexity: O(1) amortized, due to stack push operation.
        Space Complexity: O(1)
        """
        self.__playlist.set_name(name)

    def add_song_to_playlist(self, song: int) -> None:
        """
        Adds a song to the current playlist.

        Args:
            song (int): The ID of the song to add.
        
        Time Complexity: O(1) amortized, due to list append and stack push.
        Space Complexity: O(1)
        """
        self.__playlist.add_song(song)

    def remove_song_from_playlist(self, index: int) -> None:
        """
        Removes a song from the playlist by its index.

        Args:
            index (int): The index of the song to remove.
        
        Time Complexity: O(n) where n is the number of songs in the playlist, due to finding the node by index.
        Space Complexity: O(1)
        """
        self.__playlist.remove_song(index)

    def move_song_in_playlist(self, from_index: int, to_index: int) -> None:
        """
        Moves a song from one position to another in the playlist.

        Args:
            from_index (int): The current index of the song.
            to_index (int): The target index for the song.
        
        Time Complexity: O(n) where n is the number of songs in the playlist, due to finding nodes by index.
        Space Complexity: O(1)
        """
        self.__playlist.move_song(from_index, to_index)

    def reverse_playlist(self) -> None:
        """
        Reverses the order of the songs in the playlist.
        
        Time Complexity: O(n) where n is the number of songs in the playlist.
        Space Complexity: O(1)
        """
        self.__playlist.reverse_playlist()

    def sort_playlist(self, sort_type: Literal["add_time", "name", "duration"], reverse: bool = False) -> None:
        """
        Sorts the playlist based on a given criterion.

        Args:
            sort_type (Literal["add_time", "name", "duration"]): The attribute to sort by.
            reverse (bool, optional): Whether to sort in descending order. Defaults to False.
        
        Time Complexity: O(n log n) where n is the number of songs in the playlist.
        Space Complexity: O(n) to store a copy of the list for sorting and undo.
        """
        if sort_type not in ["add_time", "name", "duration"]:
            raise ValueError("Invalid sort type")
        self.__playlist.sort_playlist(sort_type, reverse)

    def shuffle_playlist(self) -> None:
        """
        Shuffles the playlist.
        
        Time Complexity: O(n log k) where n is the number of songs and k is the number of unique artists.
        Space Complexity: O(n) to store nodes and artist groupings.
        """
        self.__playlist.shuffle_playlist()

    def get_playlist_changes(self) -> str:
        """
        Returns a string representation of the edit history for the playlist.

        Returns:
            str: The formatted string of playlist changes.
        
        Time Complexity: O(c) where c is the number of changes in the edit history.
        Space Complexity: O(c) to build the string representation.
        """
        changes = self.__playlist.get_changes()
        if changes.is_empty():
            return "No changes made to the playlist"
        return str(changes)
    
    def undo_playlist_changes(self, num: int = 1) -> None:
        """
        Undoes a specified number of changes to the playlist.

        Args:
            num (int, optional): The number of changes to undo. Defaults to 1.
        
        Time Complexity: O(num * n) where n is the number of songs in the playlist, as some undo operations are O(n).
        Space Complexity: O(1)
        """
        if num < 1:
            raise ValueError("Number of undos must be at least 1")
        self.__playlist.undo_changes(num)

    def get_playback(self) -> str:
        """
        Returns a string representation of the current playback state (queue and history).

        Returns:
            str: The formatted string of the playback state.
        
        Time Complexity: O(q + h) where q is the size of the queue and h is the size of the history.
        Space Complexity: O(q + h) to build the string representation.
        """
        return str(self.__playback)

    def play_next_song(self) -> None:
        """
        Plays the next song in the queue, moving the current song to history.
        
        Time Complexity: O(q) where q is the number of songs in the queue, due to list-based queue dequeue.
        Space Complexity: O(1)
        """
        self.__playback.play_next()

    def undo_last_play(self) -> None:
        """
        Moves the last played song from history back to the queue.
        
        Time Complexity: O(1) amortized, due to stack pop and queue enqueue.
        Space Complexity: O(1)
        """
        self.__playback.undo_last_play()

    def get_current_song(self) -> str:
        """
        Returns a string representation of the currently playing song.

        Returns:
            str: The formatted string of the current song, or a message if none is playing.
        
        Time Complexity: O(1) on average.
        Space Complexity: O(1)
        """
        try:
            song = self.__playback.get_current_song()
            return str(song)
        except IndexError:
            return "No song currently playing"
        
    def get_play_queue(self) -> str:
        """
        Returns a string representation of the play queue.

        Returns:
            str: The formatted string of the queue.
        
        Time Complexity: O(q) where q is the size of the queue.
        Space Complexity: O(q) to build the string representation.
        """
        return str(self.__playback.get_play_queue())
    
    def get_history(self, num: int = -1) -> str:
        """
        Returns a string representation of the play history.

        Args:
            num (int, optional): The number of recent history items to get. Defaults to -1 (all history).

        Returns:
            str: The formatted string of the history.
        
        Time Complexity: O(h) where h is the number of songs in the history.
        Space Complexity: O(h) to build the string representation.
        """
        return str(self.__playback.get_history(num))
    
    def add_playlist_to_queue(self) -> None:
        """
        Adds all songs from the current playlist to the playback queue.
        
        Time Complexity: O(n^2) where n is the number of songs in the playlist, due to repeated O(n) lookups in the linked list.
        Space Complexity: O(1)
        """
        self.__playback.add_playlist_to_queue(self.__playlist)

    def add_song_to_queue(self, song: int) -> None:
        """
        Adds a single song to the playback queue.

        Args:
            song (int): The ID of the song to add.
        
        Time Complexity: O(1) amortized.
        Space Complexity: O(1)
        """
        self.__playback.add_song_to_queue(song)

    def get_recently_played_songs(self, num: int = 5) -> str:
        """
        Gets a string representation of the last few played songs.

        Args:
            num (int, optional): The number of recent songs to retrieve. Defaults to 5.

        Returns:
            str: A formatted string of the recently played songs.
        
        Time Complexity: O(num) to retrieve and represent the songs.
        Space Complexity: O(num) to store and represent the songs.
        """
        return str(self.__playback.get_history(num))
    
    def search_song(self, song_id: int) -> str:
        """
        Searches for a song by its ID in the main song map.

        Args:
            song_id (int): The ID of the song to search for.

        Returns:
            str: The string representation of the song if found, otherwise a "not found" message.
        
        Time Complexity: O(1) on average, due to hash map lookup.
        Space Complexity: O(1)
        """
        song = self.__songMap.search_song(song_id)
        if song:
            return str(song)
        else:
            return "Song not found"
        
    def rate_song(self, song_id: int, rating: float) -> None:
        """
        Rates a song and stores it in the rating tree.

        Args:
            song_id (int): The ID of the song to rate.
            rating (float): The rating to assign (0-5).
        
        Time Complexity: O(log k) where k is the number of rating buckets (a constant).
        Space Complexity: O(log k) for the recursion stack.
        """
        if not (0 <= rating <= 5):
            return "Rating must be between 0 and 5"
        self.__rating_tree.insert(rating, song_id)
        
    def search_songs_by_rating(self, start: int, end: int) -> str:
        """
        Searches for songs within a specified rating range.

        Args:
            start (int): The inclusive start of the rating range.
            end (int): The exclusive end of the rating range.

        Returns:
            str: A newline-separated string of songs in the range, or a "not found" message.
        
        Time Complexity: O(log k + m) where k is the number of buckets and m is the number of songs in the matching range.
        Space Complexity: O(log k + m) for the recursion stack and result dictionary.
        """
        songs = self.__rating_tree.search(start, end)
        if not songs:
            return "No songs found in the specified rating range"
        return "\n".join(str(song) + " : " + str(songs[song]) for song in songs)
    
    def get_num_songs_by_rating(self) -> str:
        """
        Gets a summary of the number of songs in predefined rating buckets.

        Returns:
            str: A formatted string showing song counts per rating range.
        
        Time Complexity: O(log k + m) for each call to get_num_by_rating, where k is the number of buckets and m is the number of songs in the range. Since this is done a constant number of times, it's dominated by the largest range.
        Space Complexity: O(log k + m) for each call, dominated by the largest range.
        """
        return f"Songs with rating 0-1: {self.__rating_tree.get_num_by_rating(0, 1)}\n\
            Songs with rating 1-2: {self.__rating_tree.get_num_by_rating(1, 2)}\n\
            Songs with rating 2-3: {self.__rating_tree.get_num_by_rating(2, 3)}\n\
            Songs with rating 3-4: {self.__rating_tree.get_num_by_rating(3, 4)}\n\
            Songs with rating 4-5: {self.__rating_tree.get_num_by_rating(4, 6)}"
    
    def get_longest_songs(self, num: int = 5) -> str:
        """
        Gets the longest songs from the entire song collection.

        Args:
            num (int, optional): The number of longest songs to return. Defaults to 5.

        Returns:
            str: A newline-separated string of the longest songs.
        
        Time Complexity: O(N log N) where N is the total number of songs in the SongMap.
        Space Complexity: O(N) to create a list of all songs for sorting.
        """
        longest_songs = self.__songMap.get_longest_songs(num)
        if not longest_songs:
            return "No songs available"
        return "\n".join(str(song) for song in longest_songs)
    
    def get_snapshot(self) -> str:
        """
        Provides a full snapshot of the current state, including ratings,
        longest songs, recent plays, playlist, and playback queue.

        Returns:
            str: A comprehensive formatted string of the application's state.
        
        Time Complexity: O(N log k + n + q + h) where N is total songs, n is playlist size, q is queue size, and h is history size. Dominated by O(N log k) from get_longest_songs.
        Space Complexity: O(k + n + q + h) to build the various string representations. Dominated by O(N) from get_longest_songs.
        """
        return f"Songs by Ratings:\n{self.get_num_songs_by_rating()}\n\nLongest Songs:\n{self.get_longest_songs()}\n\nRecently Played:\n{self.get_recently_played_songs()}\n\nPlaylist:\n{self.get_playlist()}\n\nPlayback:\n{self.get_playback()}"