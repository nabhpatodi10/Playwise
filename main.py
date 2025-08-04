from dashboard import Dashboard
from playlist import Playlist
from playback import Playback
from structures import BinarySearchTree, SongMap
from song import Song

songs = SongMap()
my_playlist = Playlist("My Favorite Songs", songs)
my_playback = Playback(songs)
dashboard = Dashboard(my_playlist, my_playback, BinarySearchTree(), songs)

song1 = Song(1, "Song A", ["Artist A"], 180)
song2 = Song(2, "Song B", ["Artist B"], 240)
song3 = Song(3, "Song C", ["Artist C"], 200)
song4 = Song(4, "Song D", ["Artist D", "Artist B"], 300)

songs.add_song(song1)
songs.add_song(song2)
songs.add_song(song3)
songs.add_song(song4)

dashboard.add_song_to_playlist(1)
dashboard.add_song_to_playlist(2)
dashboard.add_song_to_playlist(3)
dashboard.add_song_to_playlist(4)

print(dashboard.get_playlist())

dashboard.add_playlist_to_queue()
print(dashboard.get_playback())

print()
dashboard.play_next_song()
print(dashboard.get_playback())

print()
dashboard.rate_song(1, 4.5)
print("Snapshot")
print(dashboard.get_snapshot())

print()
dashboard.sort_playlist("duration", True)
print(dashboard.get_playlist())

print()
dashboard.reverse_playlist()
print(dashboard.get_playlist())

print()
dashboard.shuffle_playlist()
print(dashboard.get_playlist())

print()
dashboard.undo_last_play()
print(dashboard.get_playback())

print()
dashboard.change_playlist_name("My Updated Playlist")
print(dashboard.get_playlist())

print()
print(dashboard.search_song(3))

print()
print("Snapshot")
print(dashboard.get_snapshot())

print()
dashboard.undo_playlist_changes()
print(dashboard.get_playlist())