from database.connection import engine
import pandas as pd

df = pd.read_sql('SELECT user_id, username, role, is_active, password_hash FROM USER_ACCOUNT', con=engine)
print(df)
