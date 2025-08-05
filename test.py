import unittest
from song import Song
from structures import (
    SongMap,
    DoublyLinkedList,
    Stack,
    Queue,
    BinarySearchTree,
    heap_sort,
)
from playlist import Playlist
from playback import Playback
from dashboard import Dashboard

class TestSong(unittest.TestCase):
    """Tests for the Song class."""

    def test_creation_and_getters(self):
        """Test song creation and that all getters work correctly."""
        song = Song(1, "Test Song", ["Artist 1", "Artist 2"], 200)
        self.assertEqual(song.get_id(), 1)
        self.assertEqual(song.get_name(), "Test Song")
        self.assertEqual(song.get_artists(), ["Artist 1", "Artist 2"])
        self.assertEqual(song.get_duration(), 200)

    def test_setters(self):
        """Test that all setters correctly update the song's attributes."""
        song = Song(1, "Old Name", [], 100)
        song.set_id(99)
        song.set_name("New Name")
        song.set_artists(["New Artist"])
        song.set_duration(300)
        self.assertEqual(song.get_id(), 99)
        self.assertEqual(song.get_name(), "New Name")
        self.assertEqual(song.get_artists(), ["New Artist"])
        self.assertEqual(song.get_duration(), 300)

    def test_str_representation(self):
        """Test the string representation of a Song."""
        song = Song(1, "Test Song", ["Artist 1"], 200)
        expected_str = "ID: 1\nName: Test Song\nArtists: Artist 1\nDuration: 200 seconds"
        self.assertEqual(str(song), expected_str)
        song_no_artists = Song(2, "No Artist Song", [], 150)
        expected_str_no_artists = "ID: 2\nName: No Artist Song\nArtists: \nDuration: 150 seconds"
        self.assertEqual(str(song_no_artists), expected_str_no_artists)


class TestHeapSort(unittest.TestCase):
    """Tests for the heap_sort utility function."""

    def test_sort_normal_case(self):
        """Test heap_sort with a typical list of numbers."""
        arr = [3, 1, 4, 1, 5, 9, 2, 6]
        heap_sort(arr, key=lambda x: x)
        self.assertEqual(arr, [1, 1, 2, 3, 4, 5, 6, 9])

    def test_sort_reverse(self):
        """Test heap_sort in descending order."""
        arr = [3, 1, 4, 1, 5, 9, 2, 6]
        heap_sort(arr, key=lambda x: x, reverse=True)
        self.assertEqual(arr, [9, 6, 5, 4, 3, 2, 1, 1])

    def test_sort_edge_cases(self):
        """Test heap_sort with edge cases like empty and single-element lists."""
        empty_arr = []
        heap_sort(empty_arr, key=lambda x: x)
        self.assertEqual(empty_arr, [])

        single_arr = [42]
        heap_sort(single_arr, key=lambda x: x)
        self.assertEqual(single_arr, [42])

        pre_sorted = [1, 2, 3, 4, 5]
        heap_sort(pre_sorted, key=lambda x: x)
        self.assertEqual(pre_sorted, [1, 2, 3, 4, 5])


class TestSongMap(unittest.TestCase):
    """Tests for the SongMap class."""

    def setUp(self):
        self.song1 = Song(1, "Song A", ["Artist A"], 180)
        self.song2 = Song(2, "Song B", ["Artist B"], 300)
        self.song3 = Song(3, "Song C", ["Artist C"], 240)
        self.song_map = SongMap()
        self.song_map.add_song(self.song1)
        self.song_map.add_song(self.song2)
        self.song_map.add_song(self.song3)

    def test_add_and_search_song(self):
        """Test adding and searching for songs."""
        self.assertEqual(self.song_map.search_song(1), self.song1)
        self.assertIsNone(self.song_map.search_song(99))
        with self.assertRaises(ValueError):
            self.song_map.add_song(Song(1, "Duplicate", [], 100))
        with self.assertRaises(TypeError):
            self.song_map.add_song("not a song")

    def test_remove_song(self):
        """Test removing songs."""
        self.song_map.remove_song(self.song1)
        self.assertIsNone(self.song_map.search_song(1))
        with self.assertRaises(ValueError):
            self.song_map.remove_song(self.song1)
        with self.assertRaises(TypeError):
            self.song_map.remove_song("not a song")
            
    def test_get_longest_songs(self):
        """Test retrieving the longest songs."""
        longest = self.song_map.get_longest_songs(2)
        self.assertEqual(len(longest), 2)
        self.assertEqual(longest[0].get_id(), 2) # Song B, 300s
        self.assertEqual(longest[1].get_id(), 3) # Song C, 240s

        # Test getting more songs than exist
        all_songs = self.song_map.get_longest_songs(5)
        self.assertEqual(len(all_songs), 3)
        self.assertEqual(all_songs[0].get_id(), 2)

        # Test with an empty map
        empty_map = SongMap()
        self.assertEqual(empty_map.get_longest_songs(), [])
        
        with self.assertRaises(ValueError):
            self.song_map.get_longest_songs(0)
            
    def test_str_representation(self):
        """Test the string representation of the song map."""
        map_str = str(self.song_map)
        self.assertIn("ID: 1", map_str)
        self.assertIn("Song A", map_str)
        self.assertIn("ID: 2", map_str)
        self.assertIn("Song B", map_str)

class TestDataStructures(unittest.TestCase):
    """Tests for Stack, Queue, and BinarySearchTree."""

    def test_stack(self):
        """Test the Stack data structure."""
        s = Stack()
        self.assertTrue(s.is_empty())
        self.assertEqual(str(s), "Stack is empty")
        s.push(1)
        s.push(2)
        self.assertIn("1\n2", str(s))
        self.assertEqual(s.get_size(), 2)
        self.assertEqual(s.peek(), [2])
        self.assertEqual(s.pop(), 2)
        self.assertEqual(s.pop(), 1)
        self.assertTrue(s.is_empty())
        with self.assertRaises(IndexError):
            s.pop()

    def test_queue(self):
        """Test the Queue data structure."""
        q = Queue()
        self.assertTrue(q.is_empty())
        self.assertEqual(str(q), "Queue is empty")
        q.enqueue(1)
        q.enqueue(2)
        self.assertIn("1\n2", str(q))
        self.assertEqual(q.get_size(), 2)
        self.assertEqual(q.peek(), 1)
        self.assertEqual(q.dequeue(), 1)
        self.assertEqual(q.dequeue(), 2)
        self.assertTrue(q.is_empty())
        with self.assertRaises(IndexError):
            q.dequeue()
        
    def test_binary_search_tree(self):
        """Test the BinarySearchTree for song ratings."""
        bst = BinarySearchTree()
        bst.insert(4.5, 1) # Song 1, Rating 4.5
        bst.insert(3.2, 2) # Song 2, Rating 3.2
        bst.insert(4.9, 3) # Song 3, Rating 4.9
        bst.insert(0.5, 4) # Song 4, Rating 0.5
        
        self.assertEqual(bst.get_num_by_rating(4, 6), 2)
        self.assertEqual(bst.get_num_by_rating(0, 1), 1)
        self.assertEqual(len(bst.search(3, 5)), 3)
        with self.assertRaises(ValueError):
            bst.insert(6.0, 5) # Invalid rating
        with self.assertRaises(ValueError):
            bst.search(5, 4) # Invalid range

class TestDoublyLinkedList(unittest.TestCase):
    """Tests for the DoublyLinkedList class."""

    def setUp(self):
        self.song_map = SongMap()
        for i in range(1, 6):
            self.song_map.add_song(Song(i, chr(64+i), [f"Artist {i}"], 180 + i*10))
        self.dll = DoublyLinkedList(self.song_map)
        self.dll.append(1)
        self.dll.append(2)
        self.dll.append(3)

    def test_append_and_get_node(self):
        """Test appending items and retrieving them."""
        self.assertEqual(self.dll.get_size(), 3)
        self.assertEqual(self.dll.head.song, 1)
        self.assertEqual(self.dll.tail.song, 3)
        self.assertEqual(self.dll.get_node(1).song, 2)
        with self.assertRaises(IndexError):
            self.dll.get_node(99)
            
    def test_insert(self):
        """Test inserting elements at various positions."""
        self.dll.insert(0, 4)
        self.assertEqual(self.dll.head.song, 4)
        self.assertEqual([s for s in self.dll], [4, 1, 2, 3])
        self.dll.insert(2, 5)
        self.assertEqual([s for s in self.dll], [4, 1, 5, 2, 3])
        self.dll.insert(self.dll.get_size(), 6)
        self.assertEqual(self.dll.tail.song, 6)
        with self.assertRaises(IndexError):
            self.dll.insert(99, 99)

    def test_remove(self):
        """Test removing items from various positions and error handling."""
        self.dll.remove(1) # Remove song '2'
        self.assertEqual([s for s in self.dll], [1, 3])
        with self.assertRaises(IndexError):
            self.dll.remove(99) # Index out of bounds

    def test_move(self):
        """Test moving an element within the list."""
        self.dll.move(0, 2)
        self.assertEqual([s for s in self.dll], [2, 3, 1])
        self.dll.move(2, 0)
        self.assertEqual([s for s in self.dll], [1, 2, 3])

    def test_reverse(self):
        """Test reversing the list."""
        self.dll.reverse()
        self.assertEqual([s for s in self.dll], [3, 2, 1])
        self.assertEqual(self.dll.head.song, 3)
        self.assertEqual(self.dll.tail.song, 1)

    def test_sort_list(self):
        """Test sorting the list by various criteria."""
        self.dll.sort_list("duration")
        self.assertEqual([s for s in self.dll], [1, 2, 3])
        self.dll.sort_list("name", reverse=True)
        self.assertEqual([s for s in self.dll], [3, 2, 1])

    def test_sort_with_new_song(self):
        new_song = Song(6, "D", [], 180) # Shortest song
        self.song_map.add_song(new_song)
        self.dll.append(6) # List is [1, 2, 3, 6]

        self.dll.sort_list("duration")
        self.assertEqual([s for s in self.dll], [6, 1, 2, 3])
        
    def test_shuffle(self):
        """Test shuffling the list and artist constraint."""
        song7 = Song(7, "A", ["Artist A"], 100)
        song8 = Song(8, "A", ["Artist A"], 100)
        song9 = Song(9, "A", ["Artist A"], 100)
        song10 = Song(10, "A", ["Artist A"], 100)
        self.song_map.add_song(song7)
        self.song_map.add_song(song8)
        self.song_map.add_song(song9)
        self.song_map.add_song(song10)

        dll_shuffle = DoublyLinkedList(self.song_map)
        dll_shuffle.append(2) # Artist 2
        dll_shuffle.append(7) # Artist A
        dll_shuffle.append(8) # Artist A
        dll_shuffle.append(9) # Artist A
        dll_shuffle.append(10) # Artist A

        with self.assertRaises(ValueError):
            dll_shuffle.shuffle()

class TestPlaylist(unittest.TestCase):
    """Tests for the Playlist class, including its undo functionality."""

    def setUp(self):
        self.song_map = SongMap()
        self.song1 = Song(1, "A", ["Artist A"], 180)
        self.song2 = Song(2, "B", ["Artist B"], 240)
        self.song3 = Song(3, "C", ["Artist C"], 200)
        self.song_map.add_song(self.song1)
        self.song_map.add_song(self.song2)
        self.song_map.add_song(self.song3)
        self.playlist = Playlist("My Test Playlist", self.song_map)

    def test_operations_and_undo(self):
        """Test each playlist operation and its corresponding undo action."""
        self.playlist.add_song(1)
        self.playlist.add_song(2) # State: [1, 2]
        
        self.playlist.remove_song(0) # State: [2]
        self.playlist.undo_changes() # Undo remove -> State: [1, 2]
        
        self.playlist.move_song(0, 1) # State: [2, 1]
        self.playlist.undo_changes() # Undo move -> State: [1, 2]
        
        self.assertEqual([self.playlist.get_song(i) for i in range(self.playlist.get_size())], [1, 2])

    def test_undo_multiple_changes(self):
        """Test undoing multiple changes at once."""
        self.playlist.add_song(1)
        self.playlist.add_song(2)
        self.playlist.add_song(3)
        self.playlist.remove_song(0)
        
        self.playlist.undo_changes(num=2)
        self.assertEqual([self.playlist.get_song(i) for i in range(self.playlist.get_size())], [1, 2])

    def test_operation_errors(self):
        """Test error handling for playlist operations."""
        with self.assertRaises(IndexError):
            self.playlist.remove_song(0)
        self.playlist.add_song(1)
        with self.assertRaises(IndexError):
            self.playlist.move_song(0, 1)

class TestPlayback(unittest.TestCase):
    """Tests for the Playback class."""

    def setUp(self):
        self.song_map = SongMap()
        self.song1 = Song(1, "A", [], 180)
        self.song2 = Song(2, "B", [], 240)
        self.song_map.add_song(self.song1)
        self.song_map.add_song(self.song2)
        self.playback = Playback(self.song_map)

    def test_queue_and_history(self):
        """Test playing songs and moving them between queue and history."""
        self.playback.add_song_to_queue(1)
        self.playback.add_song_to_queue(2)

        self.assertEqual(self.playback.get_current_song(), self.song1)
        self.playback.play_next()
        self.assertEqual(self.playback.get_current_song(), self.song2)
        self.assertEqual(self.playback.get_history().peek(), [1])
        
    def test_add_playlist_to_queue(self):
        """Test adding an entire playlist to the queue."""
        playlist = Playlist("Test", self.song_map)
        playlist.add_song(1)
        playlist.add_song(2)
        self.playback.add_playlist_to_queue(playlist)
        self.assertEqual(self.playback.get_play_queue().get_size(), 2)
        self.assertEqual(self.playback.get_play_queue().dequeue(), 1)
        self.assertEqual(self.playback.get_play_queue().dequeue(), 2)

    def test_error_cases(self):
        """Test error conditions for playback operations."""
        with self.assertRaises(IndexError):
            self.playback.get_current_song()
        with self.assertRaises(IndexError):
            self.playback.play_next()
        self.playback.add_song_to_queue(1)
        with self.assertRaises(IndexError):
            self.playback.play_next()
        with self.assertRaises(IndexError):
            self.playback.undo_last_play()

class TestDashboard(unittest.TestCase):
    """Integration tests for the Dashboard facade class."""

    def setUp(self):
        self.songs = SongMap()
        self.song1 = Song(1, "Song A", ["Artist A"], 180)
        self.song2 = Song(2, "Song B", ["Artist B"], 240)
        self.songs.add_song(self.song1)
        self.songs.add_song(self.song2)
        self.playlist = Playlist("My Favorites", self.songs)
        self.playback = Playback(self.songs)
        self.bst = BinarySearchTree()
        self.dashboard = Dashboard(self.playlist, self.playback, self.bst, self.songs)

    def test_playlist_facade(self):
        """Test methods that interact with the playlist."""
        self.dashboard.add_song_to_playlist(1)
        self.dashboard.add_song_to_playlist(2)
        self.dashboard.sort_playlist("duration", reverse=True)
        playlist_str = self.dashboard.get_playlist()
        self.assertTrue(playlist_str.find("Song B") < playlist_str.find("Song A"))
        with self.assertRaises(ValueError):
            self.dashboard.sort_playlist("invalid_type")

    def test_playback_and_rating_facade(self):
        """Test methods for playback, rating, and searching."""
        self.dashboard.add_song_to_playlist(1)
        self.dashboard.add_playlist_to_queue()
        
        self.assertIn("Song A", self.dashboard.get_current_song())
        self.dashboard.add_song_to_queue(2)
        self.dashboard.play_next_song()
        self.assertIn("Song B", self.dashboard.get_current_song())
        
        self.dashboard.rate_song(1, 4.5)
        counts = self.dashboard.get_num_songs_by_rating()
        self.assertIn("Songs with rating 4-5: 1", counts)
        
    def test_snapshot_and_search(self):
        """Test the get_snapshot method and song searching."""
        self.dashboard.add_song_to_playlist(1)
        self.dashboard.rate_song(1, 4.8)
        self.dashboard.add_playlist_to_queue()

        snapshot = self.dashboard.get_snapshot()
        self.assertIn("Songs by Ratings:", snapshot)
        self.assertIn("Longest Songs:", snapshot)
        self.assertIn("Playlist:", snapshot)
        
        self.assertIn("Song A", self.dashboard.search_song(1))
        self.assertEqual(self.dashboard.search_song(99), "Song not found")


if __name__ == "__main__":
    unittest.main(argv=['first-arg-is-ignored'], exit=False)