import mysql.connector

passwords = ["", "root", "password", "Admin123", "Admin123!", "123456", "admin", "mysql", "root1234", "qwerty"]
for p in passwords:
    try:
        conn = mysql.connector.connect(host="localhost", user="root", password=p)
        print(f"SUCCESS with password: '{p}'")
        break
    except Exception as e:
        print(f"Failed with '{p}'")
