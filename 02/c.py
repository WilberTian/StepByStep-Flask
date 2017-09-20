from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    fullname = Column(String(50))
    password = Column(String(12))

    def __repr__(self):
        return "User %s" % self.name


SQLALCHEMY_DATABASE_URI = "postgresql://{DB_USER}:{DB_PASS}@{DB_ADDR}/{DB_NAME}".format(DB_USER="root", DB_PASS="root", DB_ADDR="127.0.0.1", DB_NAME="w_db")
engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)

Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

session = Session(engine)

wilber = User(name='wilber', fullname='Wilber Tian', password='wt_password')
session.add(wilber)

session.commit()

for row in session.query(User, User.name).all():
    print(row.User, row.name)