import sqlite3

connection = sqlite3.connect("./../my_users.db")

cursor = connection.cursor()

cursor.execute("UPDATE users SET age=24, occupation='Software Engineer' where name='Calvin'")

connection.commit()
