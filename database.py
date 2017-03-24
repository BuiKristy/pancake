from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///:memory:', echo=True)
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