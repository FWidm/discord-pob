from sqlalchemy import Integer, Column, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm.collections import attribute_mapped_collection

from bot.db.setup import Base


class BuildStatistics(Base):
    __tablename__ = 'build_statistics'
    id = Column(Integer, primary_key=True)
    author = Column(String(20))
    role = Column(String(20))
    character = Column(String(20))
    ascendency = Column(String(20))
    main_skill = Column(String(20))
    level = Column(Integer)
    paste_key = Column(String(20))
    stats = relationship("Stat",
                         collection_class=attribute_mapped_collection('stat_key'),
                         backref="item",
                         cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return "{}".format(self.__dict__)


class Stat(Base):
    __tablename__ = 'stat'
    id = Column(Integer, primary_key=True)
    build_statistics_id = Column(Integer, ForeignKey('build_statistics.id'), nullable=False)
    keyword = Column(String)
    text = Column(String)

    def __init__(self, keyword, text):
        self.keyword = keyword
        self.text = text

    @property
    def stat_key(self):
        return (self.keyword, self.text[0:10])
