from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, func, update, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import Engine

engine = create_engine('sqlite:///playlists.db')
Base = declarative_base()

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

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
        """ Returns a map of playlist ids to playlist name """
        session = self.Session()
        result = dict()

        for playlist in session.query(Playlist):
            result[playlist.id] = playlist.name

        session.close()
        return result

    def get_songs_from_playlist(self, playlist_id):
        """ Returns a list of song names in the playlist with the given playlist id """
        session = self.Session()
        result = session.query(Content).filter_by(playlist_id=playlist_id).\
            order_by(Content.order).all()
        session.close()
        return [row.song_name for row in result]

    def create_playlist(self, playlist_name):
        """ Creates and returns the id of the playlist using the given playlist name """
        session = self.Session()
        new_playlist = Playlist(name=playlist_name)
        session.add(new_playlist)
        session.commit()
        playlist_id = new_playlist.id
        session.close()

        return playlist_id

    def delete_playlist(self, playlist_id):
        """ Deletes the playlist matching the given playlist id """
        session = self.Session()
        session.delete(session.query(Playlist).filter(Playlist.id == playlist_id).one())
        session.commit()
        session.close()

    def update_playlist_name(self, playlist_id, new_name):
        """ Updates the playlist name given the playlist id and the new name """
        session = self.Session()
        session.query(Playlist).filter(Playlist.id == playlist_id).update({"name": new_name})
        
        session.commit()
        session.close()

    def add_song_to_playlist(self, playlist_id, song_name):
        """ Adds the given song name to the playlist matching the playlist id """
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

    def delete_song_from_playlist(self, playlist_id, index):
        """ Deletes the song at the given index from the playlist matching the given playlist id """
        session = self.Session()
        try:
            session.delete(session.query(Content).filter(Content.playlist_id == playlist_id, \
                Content.order == index).one())
            session.query(Content).filter(Content.order > index, Content.playlist_id == playlist_id).\
                update({"order": (Content.order - 1)})
            session.commit()
        except:
            session.rollback()
        finally:
            session.close()

    def reorder_songs_in_playlist(self, playlist_id, old_index, new_index):
        """ Moves the song at the given old index to the new index in the playlist given the playlist id """
        if old_index == new_index:
            return

        session = self.Session()
        song_count = session.query(func.count(Content.order)).filter(Content.playlist_id == playlist_id).scalar()
        
        if old_index >= song_count or new_index >= song_count or old_index < 0 or new_index < 0:
            session.rollback()
            session.close()
            return

        session.execute(update(Content).where((Content.order == old_index) & (Content.playlist_id == playlist_id)).\
            values(order = -(new_index) - 1))

        if old_index > new_index:
            session.execute(update(Content).where((Content.playlist_id == playlist_id) & \
                (new_index <= Content.order) & (Content.order < old_index)).values(order = -(Content.order + 1) - 1))
        elif old_index < new_index:
            session.execute(update(Content).where((Content.playlist_id == playlist_id) & \
                (old_index < Content.order) & (Content.order <= new_index)).values(order = -(Content.order - 1) - 1))

        session.execute(update(Content).where((Content.order < 0) & (Content.playlist_id == playlist_id)).\
            values(order = -(Content.order + 1)))

        session.commit()
        session.close()

DB_connection = PlaylistDB(engine)