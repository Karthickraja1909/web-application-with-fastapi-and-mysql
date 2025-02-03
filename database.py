from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

sql_database_url="mysql+pymysql://root:root%40123@localhost:3306/first_db"

engine=create_engine(sql_database_url)

sessionLocal=sessionmaker(autocommit=False, autoflush=False, bind=engine)

base=declarative_base()