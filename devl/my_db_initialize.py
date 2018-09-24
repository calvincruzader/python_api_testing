import sqlite3
from devl import test_data

conn = sqlite3.connect('my_users.db')
c = conn.cursor()

for user in test_data.users:
    print(user["name"])
    sql_command = """INSERT INTO users (name, age, occupation) VALUES ("{name}", {age}, "{occupation}")"""

    sql_command = sql_command.format(name=user["name"], age=user["age"], occupation=user["occupation"])
    c.execute(sql_command)

conn.commit()