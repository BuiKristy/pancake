from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, func, update
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///playlists.db')
Base = declarative_base()

class Playlist(Base):
    __tablename__ = 'playlists'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    def __repr__(self):
        return "<Playlist(id='%s', name='%s')>" % (self.id, self.name)

class Content(Base):
    __tablename__ = 'contents'

    playlist_id = Column(Integer, ForeignKey('playlists.id', ondelete='CASCADE'), primary_key=True)
    song_name = Column(String, nullable=False)
    order = Column(Integer, primary_key=True)

    def __repr__(self):
        return "<Content(playlist_id='%s', song_name='%s', order='%s')>" % (self.playlist_id, self.song_name, self.order)

class PlaylistDB:
    def __init__(self, engine):
        self.engine = engine
        self.Session = sessionmaker(bind=engine)
        Base.metadata.create_all(self.engine)

    def get_playlists(self):
        # returns a map of playlist ids to playlist name
        session = self.Session()
        result = dict()

        for playlist in session.query(Playlist):
            result[playlist.id] = playlist.name

        session.close()
        return result

    def get_songs_from_playlist(self, playlist_id):
        # returns a list of song names
        session = self.Session()
        result = session.query(Content).filter_by(playlist_id=playlist_id).\
            order_by(Content.order).all()
        session.close()
        return [row.song_name for row in result]

    def create_playlist(self, playlist_name):
        # returns id of the playlist created
        session = self.Session()
        new_playlist = Playlist(name=playlist_name)
        session.add(new_playlist)
        session.commit()
        playlist_id = new_playlist.id
        session.close()

        return playlist_id

    # TODO delete_playlist(playlist_id)

    def update_playlist_name(self, playlist_id, new_name):
        session = self.Session()
        session.query(Playlist).filter(Playlist.id==playlist_id).update({"name": new_name})
        
        session.commit()
        session.close()

    def add_song_to_playlist(self, playlist_id, song_name):
        session = self.Session()
        max_order = session.query(func.max(Content.order + 1)).filter_by(playlist_id=playlist_id).scalar()
        
        if max_order is None:
            max_order = 0

        song_to_add = Content(playlist_id=playlist_id, song_name=song_name, order=max_order)
        session.add(song_to_add)

        try:
            session.commit()
        except:
            session.rollback()
        finally:
            session.close()

    # TODO delete_song_from_playlist(index)

    # TODO reorder_songs_in_playlist(playlist_id, old_index, new_index)
        # moves song at old index to the new index and shifts the rest of the songs down