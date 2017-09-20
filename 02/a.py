from sqlalchemy import create_engine, select
from sqlalchemy import Table, MetaData, Column, Integer, String, ForeignKey

SQLALCHEMY_DATABASE_URI = "postgresql://{DB_USER}:{DB_PASS}@{DB_ADDR}/{DB_NAME}".format(DB_USER="root", DB_PASS="root", DB_ADDR="127.0.0.1", DB_NAME="w_db")
db = create_engine(SQLALCHEMY_DATABASE_URI, echo=True, client_encoding='utf8')

metadata = MetaData()
user_table = Table('user', metadata,
            Column('id', Integer, primary_key=True),
            Column('name', String(50)),
            Column('fullname', String(50)),
            Column('password', String(12))
        )

metadata.drop_all(db) 
metadata.create_all(db) 

conn = db.connect()


wilber = { 'name': 'wilber', 'fullname': 'Wilber Tian', 'password': 'wt_password'}
conn.execute(user_table.insert(), wilber)

sql = select([user_table, ])
res =conn.execute(sql)
print res.fetchall()


conn.close()

