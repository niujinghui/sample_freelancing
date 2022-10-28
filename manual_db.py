import os
import database

DATABASE_PATH = os.path.abspath("database")
database.setDAL(path=DATABASE_PATH, filename="tjmarket.db")


sess = database.dal.Session()