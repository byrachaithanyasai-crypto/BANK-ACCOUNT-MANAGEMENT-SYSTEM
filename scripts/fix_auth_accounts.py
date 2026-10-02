import os
import sys
from dotenv import load_dotenv

sys.path.insert(0, os.path.join(os.getcwd(), 'backend'))
load_dotenv(os.path.join('backend', '.env'))

from database.connection import engine
from sqlalchemy import text
from auth.security import get_password_hash

def main():
    print("--- FIXING AUTH ACCOUNTS ---")
    accounts_to_update = {
        'admin': 'admin123',
        'manager2': 'manager123',
        'teller2': 'teller123'
    }
    
    try:
        with engine.begin() as conn:
            for username, plain_pass in accounts_to_update.items():
                check_query = text("SELECT user_id, username FROM USER_ACCOUNT WHERE username = :username")
                result = conn.execute(check_query, {"username": username}).fetchone()
                
                if result:
                    valid_hash = get_password_hash(plain_pass)
                    update_query = text("UPDATE USER_ACCOUNT SET password_hash = :hash, is_active = 1 WHERE username = :username")
                    conn.execute(update_query, {"hash": valid_hash, "username": username})
                    print(f"[+] Updated '{username}' with a valid bcrypt hash and set is_active = 1.")
                else:
                    print(f"[-] User '{username}' not found.")
            
            print("\n--- VERIFICATION ---")
            for username in accounts_to_update.keys():
                verify_query = text("SELECT username, role, is_active FROM USER_ACCOUNT WHERE username = :username")
                row = conn.execute(verify_query, {"username": username}).fetchone()
                if row:
                    print(f"Username: {row[0]} | Role: {row[1]} | is_active: {row[2]}")
                
    except Exception as e:
        print(f"[-] Error: {e}")

if __name__ == '__main__':
    main()
