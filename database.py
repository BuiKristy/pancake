from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///playlists.db', echo=True)
Base = declarative_base()

class Playlist(Base):
    __tablename__ = 'playlists'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    def __repr__(self):
        return "<Playlist(id='%s', name='%s')>" % (self.id, self.name)

class Content(Base):
    __tablename__ = 'contents'

    playlist_id = Column(Integer, ForeignKey('playlists.id'), primary_key=True)
    song_name = Column(String, nullable=False)
    order = Column(Integer, primary_key=True)

    def __repr__(self):
        return "<Content(playlist_id='%s', song_name='%s', order='%s')>" % (self.playlist_id, self.song_name, self.order)

# TODO get_playlists()
    # returns a map of playlist ids to playlist name 

# TODO get_songs_from_playlist(playlist_id)
    # returns a list of song names

# TODO create_playlist(playlist_name)
    # returns id of the playlist created

# TODO delete_playlist(playlist_id)

# TODO update_playlist_name(playlist_id, name)

# TODO add_song_to_playlist(playlist_id, song_name)

# TODO delete_song_from_playlist(index)

# TODO reorder_songs_in_playlist(playlist_id, old_index, new_index)
    # moves song at old index to the new index and shifts the rest of the songs down