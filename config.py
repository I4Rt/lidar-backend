from flask import Flask
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base, declared_attr

Base = declarative_base()

e = create_engine("postgresql://postgres:qwerty@localhost:5432/lidar_db", echo=False)

