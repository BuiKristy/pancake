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

    def test_update_playlist(self):
        test_playlist1 = self.test_playlistDB.create_playlist("test1")
        self.test_playlistDB.update_playlist_name(test_playlist1, "new name")
        all_playlists = self.test_playlistDB.get_playlists()

        self.assertEqual(all_playlists[test_playlist1], "new name", "name is not updated")

    def test_update_multiple_playlists(self):
        test_playlist1 = self.test_playlistDB.create_playlist("test1")
        test_playlist2 = self.test_playlistDB.create_playlist("test2")
        test_playlist3 = self.test_playlistDB.create_playlist("test1")

        self.test_playlistDB.update_playlist_name(test_playlist1, "new test1")
        all_playlists = self.test_playlistDB.get_playlists()

        self.assertEqual(all_playlists, {test_playlist1: "new test1", test_playlist2: "test2", \
            test_playlist3: "test1"}, "playlist mappings don't match")
    
    def test_delete_playlist(self):
        test_playlist1 = self.test_playlistDB.create_playlist("test1")
        test_playlist2 = self.test_playlistDB.create_playlist("test2")
        test_playlist3 = self.test_playlistDB.create_playlist("test1")

        self.test_playlistDB.delete_playlist(test_playlist1)
        all_playlists = self.test_playlistDB.get_playlists()
        all_songs = self.test_playlistDB.get_songs_from_playlist(test_playlist1)

        self.assertEqual(all_playlists, {test_playlist2: "test2", test_playlist3: "test1"}, \
            "playlist deletion is wrong")
        self.assertEqual(all_songs, [], "songs still exist in deleted playlist")

    def test_check_song_in_invalid_playlist(self):
        self.test_playlistDB.add_song_to_playlist(2, "song2")
        self.assertEqual(self.test_playlistDB.get_songs_from_playlist(2), [], \
            "song should not exist at this playlist")

    def test_check_deleted_songs(self):
        test_playlist1 = self.test_playlistDB.create_playlist("test1")
        test_playlist2 = self.test_playlistDB.create_playlist("test2")
        test_playlist3 = self.test_playlistDB.create_playlist("test1")

        self.test_playlistDB.add_song_to_playlist(test_playlist1, "song1")
        self.test_playlistDB.delete_playlist(test_playlist1)
        all_songs = self.test_playlistDB.get_songs_from_playlist(test_playlist1)

        self.assertEqual(all_songs, [], "songs still exist in deleted playlist")

    def test_check_other_playlist_songs(self):
        test_playlist1 = self.test_playlistDB.create_playlist("test1")
        test_playlist2 = self.test_playlistDB.create_playlist("test2")
        test_playlist3 = self.test_playlistDB.create_playlist("test1")

        self.test_playlistDB.add_song_to_playlist(test_playlist1, "song1")
        self.test_playlistDB.add_song_to_playlist(test_playlist2, "song2")
        self.test_playlistDB.add_song_to_playlist(test_playlist3, "song3")
        self.test_playlistDB.delete_playlist(test_playlist1)
        all_playlists = self.test_playlistDB.get_playlists()
        all_songs = self.test_playlistDB.get_songs_from_playlist(test_playlist3)

        self.assertEqual(all_songs, ["song3"], "songs don't exist in existing playlist")

    def setUp(self):
        engine = create_engine('sqlite:///:memory:')
        self.test_playlistDB = PlaylistDB(engine)

if __name__ == '__main__':
    unittest.main()