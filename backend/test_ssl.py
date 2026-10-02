import pymysql
import ssl
try:
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    conn = pymysql.connect(host='localhost', user='bankx', password='password', database='bankx', ssl={'ssl': ctx})
    print("Connected via SSL with bankx:password!")
except Exception as e:
    print(f"Error: {e}")
