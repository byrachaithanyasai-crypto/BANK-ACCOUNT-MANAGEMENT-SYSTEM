import mysql.connector

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="bankx"
    )
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT user_id, username, role, employee_id, is_active, password_hash FROM USER_ACCOUNT WHERE username = 'admin'")
    admin = cursor.fetchone()
    print("CURRENT ADMIN:", admin)
    
    if admin:
        new_hash = b'.76HMGleOkKSAWW.OuCl4GpkPOaZzJJW/4yaZrwFTPZ1JN.'.decode('utf-8')
        cursor.execute("UPDATE USER_ACCOUNT SET password_hash = %s, is_active = 1 WHERE username = 'admin'", (new_hash,))
        conn.commit()
        print("Updated admin password successfully")
        
except Exception as e:
    print(f"Error: {e}")
