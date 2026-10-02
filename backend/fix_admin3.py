import mysql.connector

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="bankx"
    )
    print("Connected with root:root")
except Exception as e:
    print(f"Error root:root : {e}")

