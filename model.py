from sqlite3 import Timestamp
from pandas import DatetimeTZDtype
from sqlalchemy import create_engine, Column,Integer,String,DateTime,Float,Text

Base = declarative_base()

class Coins(Base):
    __tablename__ = 'tb_coins'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    symbol = Column(String)
    data_added = Column(Text)
    last_updated = Column(Text)
    price = Column(Float)
    volume_24 = Column(Float)
    circulatin_suply = Column(Float)
    total_suply = Column(Float)
    max_supply = Column(Float)
    volume_24 = Column(Float)
    percent_change_1h = Column(Float)
    percent_change_24 = Column(Float)
    percent_change_17 = Column(Float)

    def start():
        db_string = ""
        engine = create_engine(db_string)
        Session = sessionmaker(bind=engine)
        session = Session()
        Base.metadata.create_all(engine)
        return session, engine
