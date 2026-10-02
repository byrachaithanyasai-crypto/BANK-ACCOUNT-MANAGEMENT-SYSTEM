import mysql.connector

passwords = ["root123", "root", "password", "admin", "admin123", ""]
success = False
for p in passwords:
    try:
        conn = mysql.connector.connect(host="localhost", user="root", password=p, database="bankx")
        print(f"SUCCESS_PASSWORD={p}")
        success = True
        break
    except Exception as e:
        pass

if not success:
    print("ALL_FAILED")
