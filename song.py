class Song:
    """Represents a song with its details."""
    
    def __init__(self, id: int, name: str, artists: list[str], duration: int):
        """
        Initializes a Song object.

        Args:
            id (int): The unique identifier for the song.
            name (str): The name of the song.
            artists (list[str]): A list of artists who performed the song.
            duration (int): The duration of the song in seconds.
        
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        self.__id = id
        self.__name = name
        self.__artists = artists
        self.__duration = duration

    def get_id(self) -> int:
        """
        Returns the ID of the song.

        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        return self.__id
    
    def set_id(self, id: int) -> None:
        """
        Sets the ID of the song.

        Args:
            id (int): The new ID for the song.

        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        self.__id = id

    def get_name(self) -> str:
        """
        Returns the name of the song.

        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        return self.__name

    def get_artists(self) -> list[str]:
        """
        Returns the list of artists for the song.

        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        return self.__artists

    def get_duration(self) -> int:
        """
        Returns the duration of the song in seconds.

        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        return self.__duration
    
    def set_name(self, name: str) -> None:
        """
        Sets the name of the song.

        Args:
            name (str): The new name for the song.

        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        self.__name = name

    def set_artists(self, artists: list[str]) -> None:
        """
        Sets the list of artists for the song.

        Args:
            artists (list[str]): The new list of artists.

        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        self.__artists = artists
    
    def set_duration(self, duration: int) -> None:
        """
        Sets the duration of the song.

        Args:
            duration (int): The new duration in seconds.

        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        self.__duration = duration
    
    def __str__(self) -> str:
        """
        Returns a string representation of the Song object.

        Time Complexity: O(N) where N is the number of characters in the artists' names.
        Space Complexity: O(M) where M is the number of characters in the resulting string.
        """
        return f"ID: {self.__id}\nName: {self.__name}\nArtists: {', '.join(self.__artists)}\nDuration: {self.__duration} seconds"