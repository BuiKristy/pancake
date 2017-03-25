from sqlalchemy import create_engine
import unittest
from database import PlaylistDB

class TestDatabase(unittest.TestCase):

    def test_create_playlist(self):
        test_playlist1 = self.test_playlistDB.create_playlist("test1")
        all_playlists = self.test_playlistDB.get_playlists()
        self.assertEqual(all_playlists[test_playlist1], "test1", "playlist names are not the same")

    def test_get_songs(self):
        test_playlist1 = self.test_playlistDB.create_playlist("test1")
        self.test_playlistDB.add_song_to_playlist(test_playlist1, "song1")
        self.test_playlistDB.add_song_to_playlist(test_playlist1, "song2")
        self.test_playlistDB.add_song_to_playlist(test_playlist1, "song3")
        all_songs = self.test_playlistDB.get_songs_from_playlist(test_playlist1)
        self.assertEqual(all_songs, ["song1", "song2", "song3"], "song lists are not the same")

    def setUp(self):
        engine = create_engine('sqlite:///:memory:')
        self.test_playlistDB = PlaylistDB(engine)

if __name__ == '__main__':
    unittest.main()