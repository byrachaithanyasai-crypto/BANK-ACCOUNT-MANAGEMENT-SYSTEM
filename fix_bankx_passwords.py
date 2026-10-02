import os
import sys
from dotenv import load_dotenv

sys.path.append(os.path.join(os.getcwd(), 'backend'))
load_dotenv(os.path.join('backend', '.env'))

from backend.database.connection import engine
from sqlalchemy import text
from backend.auth.security import get_password_hash

def main():
    print("=============================================")
    print("BANKX - Updating Account Passwords & Status")
    print("=============================================")
    
    accounts_to_update = {
        'admin': 'admin123',
        'manager2': 'manager123',
        'teller2': 'teller123'
    }
    
    try:
        with engine.begin() as conn:
            for username, plain_pass in accounts_to_update.items():
                # Check if user exists
                check_query = text("SELECT user_id, username FROM USER_ACCOUNT WHERE username = :username")
                result = conn.execute(check_query, {"username": username}).fetchone()
                
                if result:
                    valid_hash = get_password_hash(plain_pass)
                    update_query = text("UPDATE USER_ACCOUNT SET password_hash = :hash, is_active = 1 WHERE username = :username")
                    conn.execute(update_query, {"hash": valid_hash, "username": username})
                    print(f"[+] Updated '{username}' with a valid bcrypt hash and set is_active = 1.")
                else:
                    print(f"[-] User '{username}' not found in the database. Skipping.")
            
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
