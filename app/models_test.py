from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()

class Board(Base):
    __tablename__ = 'board'
    id = Column(Integer, primary_key=True)
    out0 = Column(Integer)
    out1 = Column(Integer)
    out2 = Column(Integer)
    out3 = Column(Integer)
    out4 = Column(Integer)
    out5 = Column(Integer)
    out6 = Column(Integer)
    di0 = Column(Integer)
    di1 = Column(Integer)
    di2 = Column(Integer)
    di3 = Column(Integer)
    ia0 = Column(Integer)
    ia1 = Column(Integer)
    ia2 = Column(Integer)
    ia3 = Column(Integer)
    ia4 = Column(Integer)
    ia5 = Column(Integer)
    ia6 = Column(Integer)
    ia7 = Column(Integer)
    ia8 = Column(Integer)
    ia9 = Column(Integer)
    ia10 = Column(Integer)
    ia11 = Column(Integer)
    ia12 = Column(Integer)
    ia13 = Column(Integer)
    ia14 = Column(Integer)
    ia15 = Column(Integer)
    ia16 = Column(Integer)
    ia17 = Column(Integer)
    ia18 = Column(Integer)
    ia19 = Column(Integer)
    freq = Column(Integer)
    duty = Column(Integer)
    pwm = Column(Integer),
    sec0 = Column(Integer)
    sec1 = Column(Integer)
    sec2 = Column(Integer)
    sec3 = Column(Integer)
    sec4 = Column(Integer)
    dt = Column(DateTime)


# class User(Base):
#     __tablename__ = 'usertb'
#     id = Column(Integer, primary_key=True)
#     name = Column(String(64))
#     des = Column(String(120))
#
#     def __repr__(self):
#         return '<User %r>' % (self.name)

if __name__ == '__main__':



    class Users(Base):
        __tablename__ = 'users'

        id = Column(Integer, primary_key=True)
        name = Column(String)
        des = Column(String)

        def __init__(self, name, des):
            self.name = name
            self.des = des

        def __repr__(self):
            return "<User('%s','%s')>" % (self.name, self.des)


    # engine = create_engine('sqlite:///home/mateusz/PycharmProjects/lan_kontroler/sqltst/lancontrol.db', echo=True)
    dbpath = '/home/mati/PycharmProjects/lan_kontroler/lancontrol.db'
    engine = create_engine('sqlite:///' + dbpath, echo=True)
    engine = create_engine('sqlite:///' + dbpath)
    # engine = create_engine('sqlite:///lancontrol.db', echo=True)

    Base.metadata.create_all(engine)

    # tworzenie sesji dla danej bazy:
    Session = sessionmaker(bind=engine)
    session = Session()

    ed_user = Users('Ed Jones', 'edspassword')
    session.add(ed_user)
    # wykonywanie operacji
    session.commit()
    print(ed_user.id)

    # sensor = Board.query.filter(Board.ia7, Board.ia8, Board.ia14, Board.ia15, Board.dt).limit(12).all()


